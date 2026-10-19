/* Data backup (Phase 5.4) — versioned JSON export/import for favs, notes, Learn */
const DATA_SCHEMA_VERSION = 1;
function dataCurrentSnapshot(){
  let favs=[],notes={},learn={};
  try{ favs=JSON.parse(localStorage.getItem('gitaFavs')||'[]'); }catch(e){ favs=[]; }
  try{ notes=JSON.parse(localStorage.getItem('gitaFavNotes')||'{}'); }catch(e){ notes={}; }
  try{ learn=JSON.parse(localStorage.getItem('gitaLearn')||'{}'); }catch(e){ learn={}; }
  if(!Array.isArray(favs)) favs=[];
  if(!notes||typeof notes!=='object'||Array.isArray(notes)) notes={};
  if(!learn||typeof learn!=='object'||Array.isArray(learn)) learn={};
  favs=favs.filter(function(x){ return typeof x==='string'&&/^\d{1,2}\.\d{1,2}$/.test(x); });
  const clean={};
  for(const k in notes) if(typeof notes[k]==='string'&&/^\d{1,2}\.\d{1,2}$/.test(k)) clean[k]=notes[k];
  return {favs:favs,favNotes:clean,learn:learn};
}
function dataStats(snap){
  const favs=snap.favs||[],notes=snap.favNotes||{},learn=snap.learn||{};
  let held=0,chapters=0;
  for(const ch in learn){
    if(!/^\d{1,2}$/.test(ch)) continue;
    chapters++;
    const c=learn[ch];
    if(c&&c.held&&typeof c.held==='object') held+=Object.keys(c.held).length;
  }
  return {favs:favs.length,notes:Object.keys(notes).length,chapters:chapters,held:held};
}
function dataExport(){
  const snap=dataCurrentSnapshot();
  const payload={version:DATA_SCHEMA_VERSION,app:"Bhagavad-Gita",exportedAt:new Date().toISOString(),data:snap};
  const json=JSON.stringify(payload,null,2);
  const blob=new Blob([json],{type:"application/json"});
  const url=URL.createObjectURL(blob);
  const a=document.createElement('a');
  a.href=url;
  a.download="gita-backup-"+new Date().toISOString().slice(0,10)+".json";
  document.body.appendChild(a);
  a.click();
  setTimeout(function(){ document.body.removeChild(a); URL.revokeObjectURL(url); },500);
  dataShowMessage(L('data_exported'),true);
}
function dataValidateImport(obj){
  if(!obj||typeof obj!=='object') return "not an object";
  if(obj.version!==1&&obj.version!==DATA_SCHEMA_VERSION) return "unsupported version";
  if(!obj.data||typeof obj.data!=='object') return "missing data";
  const d=obj.data;
  if(d.favs&&!Array.isArray(d.favs)) return "favs not array";
  if(d.favNotes&&(typeof d.favNotes!=='object'||Array.isArray(d.favNotes))) return "favNotes not object";
  if(d.learn&&(typeof d.learn!=='object'||Array.isArray(d.learn))) return "learn not object";
  if(Array.isArray(d.favs)){
    for(let i=0;i<d.favs.length;i++){
      const v=d.favs[i];
      if(typeof v!=='string'||!/^\d{1,2}\.\d{1,2}$/.test(v)) return "bad fav id: "+v;
    }
  }
  if(d.favNotes&&typeof d.favNotes==='object'){
    for(const k in d.favNotes){
      if(!/^\d{1,2}\.\d{1,2}$/.test(k)) return "bad note key: "+k;
      if(typeof d.favNotes[k]!=='string') return "bad note value for "+k;
    }
  }
  if(d.learn&&typeof d.learn==='object'){
    for(const ch in d.learn){
      if(!/^\d{1,2}$/.test(ch)) return "bad learn chapter: "+ch;
      const c=d.learn[ch];
      if(!c||typeof c!=='object') return "bad learn entry "+ch;
      if(c.themes&&typeof c.themes!=='object') return "bad themes "+ch;
      if(c.held&&typeof c.held!=='object') return "bad held "+ch;
    }
  }
  return null;
}
function dataMergeImport(imported){
  let curFavs=[],curNotes={},curLearn={};
  try{ curFavs=JSON.parse(localStorage.getItem('gitaFavs')||'[]'); }catch(e){ curFavs=[]; }
  try{ curNotes=JSON.parse(localStorage.getItem('gitaFavNotes')||'{}'); }catch(e){ curNotes={}; }
  try{ curLearn=JSON.parse(localStorage.getItem('gitaLearn')||'{}'); }catch(e){ curLearn={}; }
  if(!Array.isArray(curFavs)) curFavs=[];
  if(!curNotes||typeof curNotes!=='object') curNotes={};
  if(!curLearn||typeof curLearn!=='object') curLearn={};
  const imp=imported.data||{};
  const impFavs=Array.isArray(imp.favs)?imp.favs:[];
  const impNotes=imp.favNotes&&typeof imp.favNotes==='object'?imp.favNotes:{};
  const impLearn=imp.learn&&typeof imp.learn==='object'?imp.learn:{};
  const favSet={};
  curFavs.forEach(function(id){ favSet[id]=1; });
  impFavs.forEach(function(id){ favSet[id]=1; });
  const mergedFavs=Object.keys(favSet).sort(function(a,b){
    const ap=a.split('.').map(Number),bp=b.split('.').map(Number);
    if(ap[0]!==bp[0]) return ap[0]-bp[0];
    return ap[1]-bp[1];
  });
  const mergedNotes={};
  for(const k in curNotes) if(typeof curNotes[k]==='string') mergedNotes[k]=curNotes[k];
  for(const k in impNotes) if(typeof impNotes[k]==='string') mergedNotes[k]=impNotes[k];
  const mergedLearn={};
  for(const ch in curLearn) mergedLearn[ch]=JSON.parse(JSON.stringify(curLearn[ch]));
  for(const ch in impLearn){
    const cur=mergedLearn[ch]||{story:0,themes:{},held:{}};
    const im=impLearn[ch];
    const out={};
    out.story=Math.max(cur.story||0,im.story||0)?1:0;
    out.themes={};
    const curThemes=cur.themes||{},impThemes=im.themes||{};
    for(const t in curThemes) if(curThemes[t]===1) out.themes[t]=1;
    for(const t in impThemes) if(impThemes[t]===1) out.themes[t]=1;
    out.held={};
    const curHeld=cur.held||{},impHeld=im.held||{};
    for(const v in curHeld) if(curHeld[v]===1) out.held[v]=1;
    for(const v in impHeld) if(impHeld[v]===1) out.held[v]=1;
    if(Array.isArray(cur.map)) out.map=cur.map.slice();
    else if(Array.isArray(im.map)) out.map=im.map.slice();
    mergedLearn[ch]=out;
  }
  try{
    localStorage.setItem('gitaFavs',JSON.stringify(mergedFavs));
    localStorage.setItem('gitaFavNotes',JSON.stringify(mergedNotes));
    localStorage.setItem('gitaLearn',JSON.stringify(mergedLearn));
  }catch(e){ return {ok:false,error:"storage full"}; }
  try{ FAV=mergedFavs.slice(); }catch(e){}
  try{ FAVNOTE=Object.assign({},mergedNotes); }catch(e){}
  const stats=dataStats({favs:mergedFavs,favNotes:mergedNotes,learn:mergedLearn});
  return {ok:true,stats:stats,imported:{favs:impFavs.length,notes:Object.keys(impNotes).length,chapters:Object.keys(impLearn).length}};
}
function dataHandleImportFile(file){
  if(!file) return;
  const reader=new FileReader();
  reader.onload=function(){
    try{
      const obj=JSON.parse(reader.result);
      const err=dataValidateImport(obj);
      if(err){ dataShowMessage(L('data_import_failed')+" ("+err+")",false); return; }
      const res=dataMergeImport(obj);
      if(!res.ok){ dataShowMessage(L('data_import_failed')+" — "+res.error,false); return; }
      const msg=L('data_imported').replace('{n}',String(res.imported.favs)).replace('{m}',String(res.imported.notes)).replace('{k}',String(res.imported.chapters));
      dataShowMessage(msg,true);
      setTimeout(function(){ showData(); },800);
    }catch(e){ dataShowMessage(L('data_import_failed'),false); }
  };
  reader.readAsText(file);
}
function dataClearAll(){
  if(!confirm(L('data_clear_q'))) return;
  try{
    localStorage.removeItem('gitaFavs');
    localStorage.removeItem('gitaFavNotes');
    localStorage.removeItem('gitaLearn');
  }catch(e){}
  try{ FAV=[]; FAVNOTE={}; }catch(e){}
  dataShowMessage(L('data_cleared'),true);
  setTimeout(function(){ showData(); },600);
}
function dataShowMessage(text,ok){
  const el=document.getElementById('dataMsg');
  if(!el) return;
  el.textContent=text;
  el.className='data-msg '+(ok?'ok':'bad');
  el.style.display='block';
}
function showData(){
  App.session.update({view:'data',chapter:null,theme:null}); App.views.persist(); App.views.renderCrumbs();
  const snap=dataCurrentSnapshot();
  const st=dataStats(snap);
  const hasData=st.favs>0||st.notes>0||st.chapters>0;
  view.innerHTML=`
    <div class="data-wrap fade-in">
      ${App.views.breadcrumbs([[L('sections_title'),'App.views.sections()'], [L('data_title'), null]])}
      <div class="view-title" role="heading" aria-level="2">${esc(L('data_title'))}</div>
      <div class="view-sub">${esc(L('data_sub'))}</div>
      <div class="data-card">
        <h3>${esc(L('data_current'))}</h3>
        <div class="data-stats">
          <span class="data-stat"><b>${st.favs}</b> ${esc(L('favorites'))}</span>
          <span class="data-stat"><b>${st.notes}</b> ${esc(L('data_notes'))}</span>
          <span class="data-stat"><b>${st.chapters}</b> ${esc(L('data_chapters'))} · <b>${st.held}</b> ${esc(L('data_held'))}</span>
        </div>
        <p>${esc(L('data_local_note'))}</p>
      </div>
      <div class="data-card">
        <h3>${esc(L('data_export'))}</h3>
        <p>${esc(L('data_export_desc'))}</p>
        <div class="data-actions"><button class="lr-cta" onclick="App.data.export()">${esc(L('data_export'))}</button></div>
      </div>
      <div class="data-card">
        <h3>${esc(L('data_import'))}</h3>
        <p>${esc(L('data_import_desc'))}</p>
        <div class="data-actions">
          <button class="lr-ghost" onclick="document.getElementById('dataFile').click()">${esc(L('data_import'))}</button>
          <input type="file" id="dataFile" class="data-import" accept=".json,application/json" onchange="if(this.files[0]) App.data.importFile(this.files[0]); this.value='';">
        </div>
        <div id="dataMsg" class="data-msg" style="display:none"></div>
      </div>
      <div class="data-card">
        <h3>${esc(L('data_clear'))}</h3>
        <p>${esc(L('data_clear_desc'))}</p>
        <div class="data-actions"><button class="lr-ghost" ${hasData?'':'disabled'} onclick="App.data.clear()">${esc(L('data_clear'))}</button></div>
      </div>
      <div class="data-foot">${esc(L('data_foot'))}</div>
    </div>`+backFoot('App.views.welcome()',L('home_plain'));
  scrollViewTop();
}
App.data = Object.freeze({
  export:dataExport,
  importFile:dataHandleImportFile,
  clear:dataClearAll,
  show:showData,
  snapshot:dataCurrentSnapshot,
  stats:dataStats,
  validate:dataValidateImport,
  merge:dataMergeImport,
  version:DATA_SCHEMA_VERSION
});
