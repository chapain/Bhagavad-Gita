/* ---------------- the drill engine ----------------
   One queue. A miss is not a failure: it goes to the back and comes round
   again, and the run ends only when the queue is genuinely empty. */
var LQ=[], LQi=0, LQmiss=0, LQdone=null, LQlab='', LQpick=[], LQci=0;
/* Where the queue's footer should lead. The learn path is inside a chapter;
   Play is not — it passed ci=0 and so offered "back to chapter", which sent the
   reader to chapter 1 from a game that spans the whole Gītā (owner
   2026-09-01). */
var LQback = null;
function lrRun(ci, items, label, done, back){
  LQci=ci; LQback=back||null; LQ=items.slice(); LQi=0; LQmiss=0; LQlab=label; LQdone=done; lrPaint();
}
function lrPaint(resumeUi){
  if(LQi >= LQ.length) return typeof LQdone === 'function' ? LQdone() : showLearn(LQci);
  const it = LQ[LQi];
  if(!resumeUi) LQpick = [];
  /* A one-item queue (Play) has no progress to show: the bar would sit at 0%
     forever and the counter would read "1 / 1". Show the run's streak instead,
     which is the only number that means anything in an endless game
     (owner 2026-09-01). */
  const single = LQ.length === 1 && LQback;
  const pct = Math.round(LQi/LQ.length*100);
  const head = single
    ? `<div class="lr-progl pl-head">${esc(LQlab)}</div>`
    : `<div class="lr-prog"><i style="width:${pct}%"></i></div>
       <div class="lr-progl">${esc(LQlab)} · ${numL(LQi+1)} / ${numL(LQ.length)}${
         LQmiss?' · '+esc(fmt(L('learn_revisit'),{n:numL(LQmiss)})):''}</div>`;
  /* Re-shuffle options on every fresh paint. Restore paints use the validated
     option/chip order from this tab's snapshot instead. */
  if(it.kind === 'pick' && it._seen && !resumeUi) it.opts = lrShuffle(it.opts);
  it._seen = 1;
  let body;
  if(it.kind === 'pick'){
    body = `<div class="lr-ask">${it.ask}</div>
       <div class="lr-opts">${it.opts.map((o,i)=>`
         <button class="lr-opt" data-lr-opt="${esc(o.oid||'')}" onclick="lrPick(${i})">
           <span class="onum">${numL(i+1)}</span>
           <span class="ol${o.deva?' dv':''}"${o.deva?' lang="sa"':''}>${o.deva?o.label:esc(o.label)}</span>
           ${o.iast?`<span class="giast" lang="sa-Latn">${esc(o.iast)}</span>`:''}
           ${o.sub?`<span class="os">${esc(o.sub)}</span>`:''}
         </button>`).join('')}</div>`;
  }else if(it.kind === 'match'){
    if(!resumeUi) LQpick = {left:null, right:null, done:{}};
    body = `<div class="lr-ask">${it.ask}</div>
      <div class="lr-match">
        <div class="lr-mcol nums">${it.left.map((o,i)=>`
          <button class="lr-mbtn num" data-n="${esc(o.n)}" onclick="lrMpick('left',${i})">${esc(o.lab)}</button>`).join('')}</div>
        <div class="lr-mcol vs">${it.right.map((o,i)=>`
          <button class="lr-mbtn vs" data-n="${esc(o.n)}" onclick="lrMpick('right',${i})">
            <span class="ol dv" lang="sa">${o.lab}</span>
            ${o.iast?`<span class="giast" lang="sa-Latn">${esc(o.iast)}</span>`:''}
          </button>`).join('')}</div>
      </div>`;
  }else{
    let chips = lrShuffle(it.chips);
    if(resumeUi && Array.isArray(resumeUi.chipOrder)){
      const byId = new Map(it.chips.map(c=>[c.id,c]));
      const ordered = resumeUi.chipOrder.map(id=>byId.get(id)).filter(Boolean);
      if(ordered.length === it.chips.length) chips = ordered;
    }
    body = `<div class="lr-ask">${it.ask}</div>
       <div class="lr-slots" id="lrSlots"></div>
       <div class="lr-chips">${chips.map(c=>`
         <button class="lr-chip2${c.deva?' dv':''}" data-lr-chip="${c.id}"${c.deva?' lang="sa"':''} onclick="lrChip(this,${c.id})"><span class="lr-t">${esc(c.label)}</span>${c.iast?`<span class="giast" lang="sa-Latn">${esc(c.iast)}</span>`:''}</button>`).join('')}</div>`;
  }
  view.innerHTML = `<div class="lrn fade-in">${head}
    <div class="lr-qbox">${body}<div class="lr-fb" id="lrFb"></div></div>
    </div>` + (LQback
      ? backFoot(LQback.fn, L(LQback.label))
      : backFoot(`showChapter(${LQci})`, L('back_chapter_one')));
  if(resumeUi) restoreQuizUi(it, resumeUi);
  scrollViewTop();
}
function restoreQuizUi(it, ui){
  const root = document.getElementById('view');
  if(!root || !ui) return;
  if(it.kind === 'pick' && ui.wrong && Array.isArray(it.opts)){
    const wrong = it.opts.findIndex(o=>o.oid === ui.wrong);
    if(wrong >= 0){
      const buttons = root.querySelectorAll('.lr-opt');
      buttons.forEach((b,i)=>{
        b.disabled = true;
        if(it.opts[i].ok) b.classList.add('right');
        else if(i === wrong) b.classList.add('wrong');
      });
      const fb = root.querySelector('#lrFb');
      if(fb) fb.innerHTML = (it.note?`<div class="nt">${it.note}</div>`:'')
        + `<button class="lr-cta" onclick="LQi++;lrPaint()">${esc(L('learn_retry'))}</button>`;
    }
  }else if(it.kind === 'order' && Array.isArray(LQpick)){
    const slots = root.querySelector('#lrSlots');
    LQpick.forEach((id,k)=>{
      const chip = it.chips.find(c=>c.id === id);
      if(!chip || !slots) return;
      const button = root.querySelector(`[data-lr-chip="${id}"]`);
      if(button){ button.disabled = true; button.classList.add('used'); }
      const slot = document.createElement('span');
      slot.className = 'lr-slot' + (chip.deva ? ' dv' : '');
      if(chip.deva) slot.lang = 'sa';
      slot.textContent = numL(k+1) + '. ' + chip.label;
      if(chip.iast){
        const iast = document.createElement('span');
        iast.className = 'giast'; iast.lang = 'sa-Latn'; iast.textContent = chip.iast;
        slot.appendChild(iast);
      }
      slots.appendChild(slot);
    });
    if(ui.bad){
      const fb = root.querySelector('#lrFb'), want = it.answer[LQpick.length];
      const next = it.chips.find(c=>c.id === want);
      if(fb) fb.innerHTML = `<div class="bad">${esc(L('learn_nextis'))} <b>${esc(next?next.label:'')}</b></div>`;
    }
  }else if(it.kind === 'match' && ui.match){
    const left = root.querySelectorAll('.lr-mbtn.num'), right = root.querySelectorAll('.lr-mbtn.vs');
    const done = new Set(Array.isArray(ui.match.done) ? ui.match.done : []);
    root.querySelectorAll('.lr-mbtn').forEach(b=>{
      if(done.has(b.dataset.n)){ b.disabled = true; b.classList.add('right'); }
    });
    if(Number.isInteger(ui.match.left) && left[ui.match.left]) left[ui.match.left].classList.add('on');
    if(Number.isInteger(ui.match.right) && right[ui.match.right]) right[ui.match.right].classList.add('on');
  }
}
function restoreQuizSession(saved){
  if(!saved || !Array.isArray(saved.queue) || !saved.queue.length || saved.queue.length > 500
     || !Array.isArray(LQ) || !LQ.length) return false;
  const base = new Map();
  LQ.forEach(it=>{ if(it && typeof it.qid === 'string') base.set(it.qid,it); });
  if(!base.size || saved.queue.some(id=>typeof id !== 'string' || !base.has(id))) return false;
  const counts = new Map();
  LQ.forEach(it=>counts.set(it.qid,(counts.get(it.qid)||0)+1));
  saved.queue.forEach(id=>counts.set(id,(counts.get(id)||0)-1));
  const diffs = Array.from(counts.values());
  const extra = diffs.reduce((n,x)=>n + Math.max(0,-x),0);
  if(diffs.some(n=>n>0) || saved.queue.length !== LQ.length + extra
     || !Number.isInteger(saved.misses) || saved.misses < extra) return false;
  const queue = saved.queue.map(id=>base.get(id));
  if(queue.length !== saved.queue.length) return false;
  LQ = queue;
  LQi = Number.isInteger(saved.index) ? Math.max(0,Math.min(saved.index,LQ.length)) : 0;
  LQmiss = Number.isInteger(saved.misses) ? Math.max(0,Math.min(saved.misses,1000)) : 0;
  if(LQi >= LQ.length){ LQpick = []; lrPaint(); return true; }
  const it = LQ[LQi], ui = saved.ui && saved.ui.kind === it.kind ? saved.ui : null;
  if(it.kind === 'pick'){
    if(ui && Array.isArray(ui.optionOrder)){
      const remaining = it.opts.slice(), ordered = [];
      ui.optionOrder.forEach(id=>{
        const k = remaining.findIndex(o=>typeof o.oid === 'string' && o.oid === id);
        if(k >= 0) ordered.push(remaining.splice(k,1)[0]);
      });
      it.opts = ordered.concat(remaining);
    }
    LQpick = [];
  }else if(it.kind === 'order'){
    const valid = new Set(it.answer);
    LQpick = ui && Array.isArray(ui.picked)
      ? ui.picked.filter((id,k,a)=>Number.isInteger(id)&&valid.has(id)&&a.indexOf(id)===k).slice(0,it.answer.length) : [];
  }else if(it.kind === 'match'){
    const m = ui && ui.match || {};
    LQpick = {left:Number.isInteger(m.left)&&m.left>=0&&m.left<it.left.length ? m.left : null,
      right:Number.isInteger(m.right)&&m.right>=0&&m.right<it.right.length ? m.right : null, done:{}};
    (Array.isArray(m.done)?m.done:[]).forEach(id=>{
      if(it.left.some(o=>o.n===id)&&it.right.some(o=>o.n===id)) LQpick.done[id]=1;
    });
  }else LQpick = [];
  lrPaint(ui);
  return true;
}
function lrPick(i){
  const it = LQ[LQi], o = it.opts[i];
  document.querySelectorAll('.lr-opt').forEach((b,k)=>{
    b.disabled = true;
    if(it.opts[k].ok) b.classList.add('right');
    else if(k === i) b.classList.add('wrong');
  });
  const fb = document.getElementById('lrFb');
  if(o.ok){
    fb.innerHTML = `<div class="good">${esc(L('learn_yes'))}</div>`;
    LQi++; setTimeout(lrPaint, 620);
  }else{
    LQmiss++; LQ.push(it);
    /* The tick and cross on the options already say right and wrong, so the
       feedback line drops the verdict and keeps only what the reader cannot
       see: the correct verse and its meaning. The button says what pressing it
       DOES — in Play the same question returns, so "select again" is literally
       true; in a multi-question drill the missed item is requeued and comes
       back later, which is the same promise. (owner 2026-09-02) */
    fb.innerHTML = (it.note?`<div class="nt">${it.note}</div>`:'')
      + `<button class="lr-cta" onclick="LQi++;lrPaint()">${esc(L('learn_retry'))}</button>`;
  }
}
function lrMpick(side, i){
  const it = LQ[LQi];
  if(!LQpick || typeof LQpick !== 'object' || Array.isArray(LQpick)) LQpick = {left:null, done:{}};
  const col = side === 'left' ? it.left : it.right;
  const o = col[i];
  if(LQpick.done[o.n]) return;
  const btns = document.querySelectorAll(side==='left' ? '.lr-mbtn.num' : '.lr-mbtn.vs');
  btns.forEach(b=>b.classList.remove('on'));
  LQpick[side] = i;
  if(btns[i]) btns[i].classList.add('on');
  if(LQpick.left==null || LQpick.right==null) return;
  const a = it.left[LQpick.left], b = it.right[LQpick.right];
  const lb = document.querySelectorAll('.lr-mbtn.num')[LQpick.left];
  const rb = document.querySelectorAll('.lr-mbtn.vs')[LQpick.right];
  const fb = document.getElementById('lrFb');
  if(a.n === b.n){
    LQpick.done[a.n] = 1;
    if(lb){ lb.classList.add('right'); lb.disabled = true; lb.classList.remove('on'); }
    if(rb){ rb.classList.add('right'); rb.disabled = true; rb.classList.remove('on'); }
    LQpick.left = LQpick.right = null;
    if(Object.keys(LQpick.done).length >= it.left.length){
      if(fb) fb.innerHTML = `<div class="good">${esc(L('learn_yes'))}</div>`;
      LQi++; setTimeout(lrPaint, 700);
    }
  }else{
    if(lb) lb.classList.add('shake');
    if(rb) rb.classList.add('shake');
    setTimeout(()=>{
      if(lb){ lb.classList.remove('shake','on'); }
      if(rb){ rb.classList.remove('shake','on'); }
    }, 380);
    LQpick.left = LQpick.right = null;
    if(fb) fb.innerHTML = '';
  }
}
function lrChip(el, id){
  const it = LQ[LQi], want = it.answer[LQpick.length];
  const fb = document.getElementById('lrFb');
  if(id === want){
    /* Clear any standing "not there yet" the moment the reader gets it right.
       Without this the correction stays on screen for the rest of the question
       and reads as though the new, correct answer were also wrong
       (owner 2026-09-01). */
    if(fb) fb.innerHTML = '';
    LQpick.push(id); el.disabled = true; el.classList.add('used');
    /* carry the chip's script class through, or a Devanagari pāda drops back
       to the Latin face the moment it is placed */
    const dv = el.classList.contains('dv') ? ' dv' : '';
    const chp = it.chips.find(c=>c.id===id);
    const iast = (chp && chp.iast) ? `<span class="giast" lang="sa-Latn">${esc(chp.iast)}</span>` : '';
    document.getElementById('lrSlots').insertAdjacentHTML('beforeend',
      `<span class="lr-slot${dv}"${dv?' lang="sa"':''}>${numL(LQpick.length)}. ${esc(chp?chp.label:el.textContent.trim())}${iast}</span>`);
    if(LQpick.length === it.answer.length){
      fb.innerHTML = `<div class="good">${esc(L('learn_thread_ok'))}</div>`;
      LQi++; setTimeout(lrPaint, 700);
    }
  }else{
    LQmiss++;
    el.classList.add('shake'); setTimeout(()=>el.classList.remove('shake'), 380);
    const r = it.chips.find(c=>c.id===want);
    fb.innerHTML = `<div class="bad">${esc(L('learn_nextis'))} <b>${esc(r?r.label:'')}</b></div>`;
  }
}

