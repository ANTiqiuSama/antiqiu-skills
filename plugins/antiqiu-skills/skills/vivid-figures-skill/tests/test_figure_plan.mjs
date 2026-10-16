import test from 'node:test';
import assert from 'node:assert/strict';
import { figurePlanErrors } from '../scripts/figure-plan.ts';

function plan() {
  const figure = (id, cls, ext, extras={}) => ({ id, class:cls, question:'q1',
    chartType:id, recipe:'custom', reason:'source supports this expression',
    message:'test claim', section:'results', layout:'single', finalWidthMm:136,
    sources:['results.json'], outputs:[`figures/${id}.${ext}`], ...extras });
  return { questions:[{id:'q1',kind:'data',modelCount:1,spatial:false}], figures:[
    ...Array.from({length:8},(_,i)=>figure(`fig_data_${i}`,'DATA','png')),
    figure('fig_roadmap','DRAWIO','pdf',{purpose:'roadmap'}),
    figure('fig_scene','ILLUSTRATION','png'),
    figure('fig_flow','HTML','html'),
    figure('fig_state','MERMAID','mmd'),
    figure('TABLE_summary','TABLE','md')
  ] };
}

test('all supported renderer classes accept their real output formats',()=>{
  assert.deepEqual(figurePlanErrors(plan()),[]);
});
test('renderer output mismatch is rejected',()=>{
  const p=plan();p.figures.find(f=>f.class==='ILLUSTRATION').outputs=['figures/fig_scene.csv'];
  assert.ok(figurePlanErrors(p).some(e=>e.includes('supported artifact')));
});
test('existing data count and roadmap requirements remain',()=>{
  const p=plan();p.figures=p.figures.filter(f=>f.class!=='DRAWIO');p.figures.shift();
  const errors=figurePlanErrors(p);
  assert.ok(errors.some(e=>e.includes('at least 8')));
  assert.ok(errors.some(e=>e.includes('roadmap')));
});
test('consistent comparisons do not require arbitrary chart type variety',()=>{
  const p=plan();p.questions[0].modelCount=4;
  for(const f of p.figures) if(f.class==='DATA') f.chartType='paired forest';
  assert.deepEqual(figurePlanErrors(p),[]);
});
