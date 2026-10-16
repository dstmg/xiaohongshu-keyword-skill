import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
class Element {
 constructor(){this.children=[];this.value='';this.hidden=false;this.dataset={};this.classList={toggle(){},add(){},remove(){}}}
 append(...items){const first=this.children.length===0;this.children.push(...items);if(first&&items[0]?.value!==undefined)this.value=items[0].value}
 replaceChildren(...items){this.children=items;this.value=''}
 get options(){return this.children}
 setAttribute(){}
 getBoundingClientRect(){return {width:900,height:320}}
 getContext(){return new Proxy({createLinearGradient:()=>({addColorStop(){}})}, {get:(o,k)=>o[k]||(()=>{})})}
}
const nodes=new Map(), get=id=>{if(!nodes.has(id))nodes.set(id,new Element());return nodes.get(id)};
const q={query:'词根',depth:0,status:'ok',captured_at:'2026-10-16',screenshots:['evidence/test.png'],suggestions:[{term:'扩展词',rank:1}]};
const item={queries:[q],complete:true,batch:'a'};
get('projectData').textContent=JSON.stringify({roots:{'词根':item,'新增词':{...item,queries:[{...q,query:'新增词'}]}},batches:[{id:'a',date:'2026-10-16',roots:{'词根':item}}]});
const title=new Element();
const context={document:{getElementById:get,createElement:()=>new Element(),querySelector:()=>title,querySelectorAll:()=>[]},requestAnimationFrame:f=>f(),devicePixelRatio:1,ResizeObserver:class{observe(){}}};
vm.createContext(context);
vm.runInContext(fs.readFileSync(new URL('../assets/research.js',import.meta.url),'utf8'),context);
assert.equal(get('rows').children.length,2);
get('root').value='新增词';get('root').onchange();assert.equal(get('rows').children.length,1);
get('search').value='不存在';get('search').oninput();assert.equal(get('rows').children.length,0);
get('reset').onclick();assert.equal(get('rows').children.length,1);
get('root').value='词根';get('root').onchange();get('batch').value='a';get('batch').onchange();assert.equal(get('rows').children.length,1);
get('table').onclick();assert.equal(get('chartBox').hidden,true);get('bars').onclick();assert.equal(get('chartBox').hidden,false);
assert.equal(get('evidenceList').children[0].children[2].href,'evidence/test.png');
console.log('PASS: root/batch switches, filtering, reset, table/chart controls, evidence links (mock DOM; not visual QA)');
