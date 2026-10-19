/* Learn session boundary: Core stores the returned plain object and never
   reaches into the memorization feature's mutable working state. */
function learnSessionSnapshot(){
  const snap = {at:state.lrAt || null,
    test:typeof lrTest === 'number' ? lrTest : 0,
    open:typeof lrOpen === 'object' && lrOpen ? lrOpen : {},
    level:typeof LV === 'object' && LV ? LV.level : 'full',
    shown:typeof LV === 'object' && LV ? LV.shown : {}};
  const quiz = App.drills.capture();
  if(quiz) snap.quiz = quiz;
  if(state.lrAt && state.lrAt.kind === 'free' && FP && FP.v)
    snap.free = {ci:FP.ci, ti:FP.ti, verse:FP.v.n,
      deal:Array.isArray(FP.deal) ? FP.deal.slice() : [],
      picked:Array.isArray(FP.picked) ? FP.picked.slice() : []};
  return snap;
}
function restoreLearnSession(snap){
  if(!snap || snap.view !== 'learn' || !snap.learn || !snap.learn.at) return;
  const ci = Number.isInteger(snap.chapter) ? snap.chapter : null;
  if(ci == null) return;
  const at = snap.learn.at;
  if(at.kind === 'story'){
    lrTest = snap.learn.test ? 1 : 0;
    lrOpen = snap.learn.open && typeof snap.learn.open === 'object' ? snap.learn.open : {};
    lrStory(ci, Number.isInteger(at.step) ? at.step : 0,
      Number.isInteger(at.seed) ? at.seed : null);
  }else if(at.kind === 'storyDone'){
    lrStoryDone(ci);
  }else if(at.kind === 'theme' && Number.isInteger(at.ti)){
    if(typeof LV === 'object' && LV){
      LV.level = ['full','first','half','blind'].includes(snap.learn.level) ? snap.learn.level : 'full';
      LV.shown = snap.learn.shown && typeof snap.learn.shown === 'object' ? snap.learn.shown : {};
    }
    lrTheme(ci, at.ti, Number.isInteger(at.k) ? at.k : 0);
  }else if(at.kind === 'drill' && Number.isInteger(at.ti)
           && DATA[ci] && DATA[ci].themes[at.ti]){
    lrDrill(ci, at.ti, thVerses(DATA[ci].themes[at.ti]),
      Number.isInteger(snap.learn.quiz && snap.learn.quiz.seed) ? snap.learn.quiz.seed
        : (Number.isInteger(at.seed) ? at.seed : null));
  }else if(at.kind === 'free' && snap.learn.free){
    const f = snap.learn.free, loc = App.library.location(f.verse);
    if(loc && loc.ci === ci){
      FP.ci = ci; FP.ti = Number.isInteger(f.ti) ? f.ti : -1;
      FP.v = App.library.verse(loc); FP.order = (FP.v.flow||[]).filter(x=>x.k==='p');
      const valid = a => Array.isArray(a) && a.length === FP.order.length
        && a.every(Number.isInteger) && new Set(a).size === a.length
        && a.every(i=>i >= 0 && i < FP.order.length);
      FP.deal = valid(f.deal) ? f.deal.slice() : FP.order.map((_,i)=>i);
      FP.picked = Array.isArray(f.picked) ? f.picked.filter(i=>Number.isInteger(i)
        && i >= 0 && i < FP.order.length).slice(0,FP.order.length) : [];
      state.view='learn'; state.chapter=ci; state.theme=FP.ti < 0 ? null : FP.ti;
      state.lrAt = {kind:'free', ti:FP.ti}; lrFreePaint();
    }
  }else showLearn(ci);
  if(snap.learn.quiz) App.drills.restore(snap.learn.quiz);
}
