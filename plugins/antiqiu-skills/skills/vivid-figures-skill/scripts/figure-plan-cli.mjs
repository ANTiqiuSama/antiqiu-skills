import { mkdir } from 'node:fs/promises';
import { resolve, join } from 'node:path';
import { beginFigurePlan, validateFigurePlan } from './figure-plan.ts';
const args = process.argv.slice(2);
const option = (name, fallback) => { const i=args.indexOf(name); return i < 0 ? fallback : args[i+1]; };
const cwd = resolve(option('--workspace', '.'));
if (!['begin', 'validate'].includes(args[0])) throw new Error('Use begin|validate --workspace PATH [--minimum N] [--plan FIGURE_PLAN.json]');
await mkdir(join(cwd, '.vivid'), { recursive: true });
const result = args[0] === 'begin'
  ? await beginFigurePlan(cwd, Number(option('--minimum', '8')))
  : await validateFigurePlan(cwd, option('--plan', 'FIGURE_PLAN.json'));
console.log(JSON.stringify(result, null, 2));
