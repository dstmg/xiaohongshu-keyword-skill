function renderAnalysis(entries){
 const cards=document.getElementById('analysisCards'), summary=document.getElementById('analysisSummary'), status=document.getElementById('analysisStatus'), note=document.getElementById('analysisNote');
 if(!cards)return;
 cards.replaceChildren();
 const analyses=entries.map(([root,d])=>({root,a:d.analysis})).filter(v=>v.a);
 const total=analyses.reduce((n,v)=>n+v.a.items.length,0);
 const hasAgent=analyses.some(v=>v.a.interpretation?.length);
 status.textContent=total?(hasAgent?'AI初步解读＋规则分类 · 待业务验证':'规则初步分析 · 待Agent综合解读'):'无有效词条，待采集后分析';
 summary.textContent='依据当前词根及批次的真实词条整理，综合解读与逐词规则分类分别展示。无具体商品资料，不构成已验证卖点、品牌推荐或经营结论。';
 note.textContent=total?'已完成关键词初步分析，进入“运营建议”查看来源词、建议动作及待验证资料。':'本批无有效词条，暂不生成运营建议。';
 for(const {root,a} of analyses){
  for(const insight of a.interpretation||[]){const card=document.createElement('article');card.className='action-card';const h=document.createElement('h3');h.textContent=root+' · '+insight.title;const f=document.createElement('p');f.textContent=insight.finding;const action=document.createElement('p');action.textContent='下一步：'+insight.action;const v=document.createElement('p');v.className='hint';v.textContent='待验证：'+insight.verification;const terms=document.createElement('p');terms.className='hint';terms.textContent='来源词：'+insight.source_terms.join('；');card.append(h,f,action,v,terms);for(const source of insight.sources){if(source.screenshot){const link=document.createElement('a');link.href=source.screenshot;link.textContent=source.query+' · '+source.rank+'位 / 截图 ';link.target='_blank';link.rel='noopener';card.append(link)}}cards.append(card)}
  for(const group of a.groups){const card=document.createElement('article');card.className='action-card';const h=document.createElement('h3');h.textContent=root+' · '+group.category;const count=document.createElement('p');count.className='hint';count.textContent=group.count+'个去重词（不是搜索量）';const examples=document.createElement('p');examples.textContent=group.examples.map(t=>'“'+t+'”').join('、');const sample=a.items.find(i=>i.category===group.category);const task=document.createElement('p');task.textContent='可做：'+sample.action;const verify=document.createElement('p');verify.className='hint';verify.textContent='待验证：'+sample.verification;card.append(h,count,examples,task,verify);cards.append(card)}
 }
 const table=document.createElement('table');const head=document.createElement('tr');['词根 / 原始词','研究方向','建议动作','待验证资料','来源证据'].forEach(t=>cell(head,t));table.append(head);
 for(const {root,a} of analyses)for(const item of a.items){const tr=document.createElement('tr');cell(tr,root+' / '+item.term);cell(tr,item.category);cell(tr,item.action);cell(tr,item.verification);const td=cell(tr,'');for(const source of item.sources){const text=document.createElement('div');text.textContent=source.query+' · 第'+source.rank+'位';td.append(text);if(source.screenshot){const link=document.createElement('a');link.href=source.screenshot;link.textContent='查看截图';link.target='_blank';link.rel='noopener';td.append(link)}}table.append(tr)}
 document.getElementById('analysisTable').replaceChildren(table);
}
