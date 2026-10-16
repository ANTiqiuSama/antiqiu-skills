(function(){
  var TOL=6, ATOL=4;
  var fig=document.querySelector('.fig');
  if(!fig) return {error:'no .fig'};
  var F=fig.getBoundingClientRect();
  function directText(el){for(var i=0;i<el.childNodes.length;i++){var n=el.childNodes[i];
    if(n.nodeType===3 && n.textContent.trim().length>0) return true;} return false;}
  // ⛔ KaTeX 每条公式会同时产出「可见 HTML」+「视觉隐藏的 .katex-mathml 副本」(裁到 1px)。
  //    MathML 子孙仍报完整布局盒，若计入会让每个公式字形与其 HTML 版重复→假重叠/假溢出，
  //    使含公式的图永远过不了自检。故跳过 .katex-mathml 整棵子树（它本就不可见，不影响观感）。
  function inHiddenMath(el){for(var p=el;p&&p!==fig;p=p.parentElement){
    if(p.classList&&p.classList.contains('katex-mathml')) return true;} return false;}
  var blocks=[], all=fig.querySelectorAll('*');
  for(var i=0;i<all.length;i++){var el=all[i];
    if(!directText(el)) continue;
    if(inHiddenMath(el)) continue;
    var r=el.getBoundingClientRect();
    if(r.width<1||r.height<1) continue;
    blocks.push({el:el,r:r,txt:el.textContent.trim().replace(/\s+/g,' ').slice(0,20)});
  }
  var overflow=[],clip=[],overlap=[];
  for(var k=0;k<blocks.length;k++){var b=blocks[k],e=b.el;
    if(e.scrollWidth>e.clientWidth+TOL||e.scrollHeight>e.clientHeight+TOL)
      overflow.push({txt:b.txt,sw:e.scrollWidth,cw:e.clientWidth,sh:e.scrollHeight,ch:e.clientHeight});
    var r=b.r;
    var ol=F.left-r.left, ot=F.top-r.top, orr=r.right-F.right, ob=r.bottom-F.bottom;
    if(ol>TOL||ot>TOL||orr>TOL||ob>TOL)
      clip.push({txt:b.txt,left:Math.round(ol),top:Math.round(ot),right:Math.round(orr),bottom:Math.round(ob)});
  }
  for(var i=0;i<blocks.length;i++)for(var j=i+1;j<blocks.length;j++){
    var a=blocks[i],c=blocks[j];
    if(a.el.contains(c.el)||c.el.contains(a.el)) continue;
    var ix=Math.min(a.r.right,c.r.right)-Math.max(a.r.left,c.r.left);
    var iy=Math.min(a.r.bottom,c.r.bottom)-Math.max(a.r.top,c.r.top);
    if(ix>TOL&&iy>TOL) overlap.push({a:a.txt,b:c.txt,area:Math.round(ix*iy)});
  }
  // ④ 声明式对齐检测（geom-check 抓不出「参差不齐」的精细偏差 → 让作图时显式声明对齐意图）：
  //    data-mh-col="k" 的元素应竖直成一列（中轴 x 一致）；data-mh-row="k" 应水平成一行（中轴 y 一致）。
  //    ⛔ 只测被显式标记的元素——没打标记的图这里恒空 → 与旧行为完全一致，零回归。
  //    连线（竖箭头/横挂线的 div，本身无文字不进 blocks）也可打同一 col/row → 直接验证「端点接节点中轴」。
  var misalign=[];
  function checkAlign(attr, axis){
    // axis: 'x' 量中轴横坐标(同列竖直对齐) / 'y' 量中轴纵坐标(同行水平对齐)
    // ⛔ groups 用无原型对象：否则 data-mh-col="__proto__"/"constructor" 等键会命中
    //    Object.prototype 上的属性(取到的不是数组)，push 抛异常 → 整个探针崩(geom_probe_failed)。
    var marked=fig.querySelectorAll('['+attr+']'), groups=Object.create(null);
    for(var i=0;i<marked.length;i++){var el=marked[i];
      if(inHiddenMath(el)) continue;
      var r=el.getBoundingClientRect();
      if(r.width<1||r.height<1) continue;
      var key=el.getAttribute(attr); if(key==null||key==='') continue;
      var center = axis==='x' ? (r.left+r.right)/2 : (r.top+r.bottom)/2;
      var lbl=(el.textContent||'').trim().replace(/\s+/g,' ').slice(0,16) || ('<'+el.tagName.toLowerCase()+'>');
      (groups[key]||(groups[key]=[])).push({c:center,lbl:lbl});
    }
    for(var k in groups){   // groups 无原型(Object.create(null))，for-in 只遍历自身键，无需 hasOwnProperty 防护
      var g=groups[k]; if(g.length<2) continue;   // 单成员无从谈对齐
      var mn=g[0].c, mx=g[0].c;
      for(var m=1;m<g.length;m++){if(g[m].c<mn)mn=g[m].c; if(g[m].c>mx)mx=g[m].c;}
      var spread=mx-mn;
      if(spread>ATOL){
        var names=[]; for(var m=0;m<g.length&&m<4;m++) names.push(g[m].lbl);
        misalign.push({attr:attr,group:k,axis:axis,spread:Math.round(spread),count:g.length,members:names});
      }
    }
  }
  checkAlign('data-mh-col','x');   // 同列 → 中轴横坐标应一致
  checkAlign('data-mh-row','y');   // 同行 → 中轴纵坐标应一致
  return {fig:{w:Math.round(F.width),h:Math.round(F.height)},blocks:blocks.length,
    overflow:overflow,clip:clip,overlap:overlap,misalign:misalign};
})()
