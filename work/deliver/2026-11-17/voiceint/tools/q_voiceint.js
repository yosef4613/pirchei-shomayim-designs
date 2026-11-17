// q_voiceint.js — הבדיקה של קול 3 בתוך המשחק (17.11, voiceint): שיחה ומשימה עם קול. דרך התור: bash W/tools_pack/bslot.sh node q_voiceint.js <game.html> <out.json>
// (1) הנתונים: TCVSIDE.audit (כל הקלטה — בקול של איש הקשר שלה, המשימות ואנשי הקשר קיימים, בלי שם השחקן); 93 + 63 הישנות לא השתנו (story_vrec).
// (2) שיחה נכנסת ← עונים ← הפתיחה של איש הקשר מתנגנת מההקלטה (AudioBufferSourceNode.start באורך ההקלטה), עם כתובית בשיחה; שיחה שנייה — גם שורה משלו;
//     סוגרים באמצע — הקול נעצר. (3) משימה אמיתית (startMission) ← ההודעה של הנותן מתנגנת ונשמרת בטלפון בקול שלו; missionComplete ← התודה.
// (4) הטלפון: הודעה קולית מאיש קשר ← msg.vv = הקול שלו, g77SpPlay מנגן את ההקלטה. (5) "כבוי" ← לא מתנגן. קול הדפדפן מדומה (כמו q_storyvoice.js).
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
(async () => {
  const [file, out] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--autoplay-policy=no-user-gesture-required'] });
  const ctx = await b.newContext({ viewport: { width: 1280, height: 800 } });
  await ctx.addInitScript(() => {
    const voices = [{ name: 'Microsoft Asaf - Hebrew (Israel)', lang: 'he-IL', localService: true, default: false, voiceURI: 'asaf' }];
    const q = []; let cur = null; window.__fakeSpoken = [];
    const fake = { get speaking() { return !!cur }, get pending() { return q.length > 0 }, paused: false, getVoices: () => voices, addEventListener() {}, removeEventListener() {},
      speak(u) { q.push(u); if (!cur) next() }, cancel() { const a = [cur, ...q].filter(Boolean); q.length = 0; cur = null; a.forEach(u => { try { u.onerror && u.onerror({ error: 'canceled' }) } catch (e) {} }) }, pause() {}, resume() {} };
    function next() { cur = q.shift(); if (!cur) return; const u = cur; window.__fakeSpoken.push([String(u.text).slice(0, 30), u.voice && u.voice.name]);
      setTimeout(() => { if (cur !== u) return; u.onstart && u.onstart(); setTimeout(() => { if (cur !== u) return; cur = null; u.onend && u.onend(); next() }, 1000 * u.text.length / 14 / (u.rate || 1)) }, 5) }
    Object.defineProperty(window, 'speechSynthesis', { value: fake, configurable: true });
    window.SpeechSynthesisUtterance = function (t) { this.text = t; };
    window.__starts = []; const st0 = AudioBufferSourceNode.prototype.start;
    AudioBufferSourceNode.prototype.start = function () { window.__starts.push({ dur: this.buffer ? +this.buffer.duration.toFixed(2) : null, t: performance.now() }); return st0.apply(this, arguments) };
  });
  const p = await ctx.newPage(); const errs = [], cons = [];
  p.on('pageerror', e => errs.push(String(e).slice(0, 240))); p.on('console', m => { if (m.type() === 'error') cons.push(m.text().slice(0, 200)) });
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  await p.waitForTimeout(1500);
  const ev = s => p.evaluate(x => Promise.resolve(window.__TC_DEV.ev(x)).then(v => typeof v === 'string' ? v : JSON.stringify(v)), s).then(r => { try { return JSON.parse(r) } catch (e) { return r } });
  const R = { build: await ev('typeof BUILD!=="undefined"?BUILD:null') };
  R.audio = await ev('(()=>{const a=PlayerProfile.settings.audio;PlayerProfile.settings.audio=1;try{TCSND.ensure()}catch(e){}return a})()');
  R.data = await ev(`(()=>{const a=TCVSIDE.audit();return{audit:a,st:Object.assign({},TCVSIDE.st),stN:TCVREC.st.n,mode:TCVREC.mode,story:TCVREC_ST.audit().ok,
    contacts:Object.keys(TCVSIDE.S.by).length,missions:Object.keys(TCVSIDE.S.mis).length,shimon:TCVREC.D.modes.cast.cast['st-shimon'],ezra:TCVREC.D.modes.cast.cast['zs-b4-ezra']}})()`);
  const W = `const w=ms=>new Promise(r=>setTimeout(r,ms));const waitP=async(p0,ms)=>{let t=0;while(TCVREC.st.played<=p0&&t<ms){await w(100);t+=100}return t};`;
  /* (2) the calls: twice (opening; opening + trait), then a third closed in the middle */
  R.calls = await ev(`(async()=>{${W}const o=[];const who=Object.keys(TCVSIDE.S.by).find(w=>{const K=TCVSIDE.S.by[w];return (K.call||[]).filter(id=>TCVSIDE.hasRec(w,id)).length>=2&&(K.trait||[]).some(id=>TCVSIDE.hasRec(w,id))&&g77S().chars[w]});
    for(let k=0;k<3;k++){const c={k};try{g77DlgClose(true);State.phoneOpen=false;const p0=TCVREC.st.played,s0=window.__starts.length,f0=window.__fakeSpoken.length,c0=TCVSIDE.st.calls;
      g77CallIn(who,'st-demo',{ring:20});await w(300);c.ring=!!g77Sp().ring;c.ans=g77SpAnswer();c.dlg=!!g77S().open;c.t=await waitP(p0,5000);c.played=TCVREC.st.played-p0;c.calls=TCVSIDE.st.calls-c0;
      const L=TCVSIDE.st.last;c.id=L&&L.id;const tx=TCVSIDE.S.ids[c.id]||'',v=TCVREC.voiceFor(who,tx),r=TCVREC.rec(tx,v);c.voice=v;c.recSec=r?r[0]:null;const S=window.__starts.slice(s0);c.bufDur=S.length?S[0].dur:null;
      await w(400);const cp=g77S().el&&g77S().el.querySelector('[data-vsd]');c.caption=cp?cp.textContent.slice(0,40):null;c.tts=window.__fakeSpoken.length-f0;
      if(k<2){const e0=TCVREC.st.ended;let t=0;while(TCVREC.st.ended===e0&&t<(c.recSec||6)*1000+3000){await w(200);t+=200}c.ended=TCVREC.st.ended>e0;await w(800);c.traitsNow=TCVSIDE.st.traits;
        if(TCVSIDE.st.traits>0){const p1=TCVREC.st.played;await waitP(p1-1,1500);const L2=TCVSIDE.st.last;c.trait=L2&&L2.kind==='traits'?L2.id:null;const e1=TCVREC.st.ended;let t2=0;while(TCVREC.st.ended===e1&&t2<12000){await w(200);t2+=200}}
        await w(300);c.capAfter=!!(g77S().el&&g77S().el.querySelector('[data-vsd]'));g77DlgClose(false)}
      else{const st0=TCVSIDE.st.stopped;g77DlgClose(false);await w(300);c.stopped=TCVSIDE.st.stopped-st0;c.curAfter=TCVREC.state().cur}
    }catch(e){c.err=String(e&&e.stack||e).slice(0,300)}o.push(c)}return o})()`);
  /* (3) a real mission: the first in TCVSIDE.S.mis that starts from where the player is now */
  R.mission = await ev(`(async()=>{${W}const o={tried:[]};try{g77DlgClose(true);State.phoneOpen=false;for(const id of Object.keys(TCVSIDE.S.mis)){if(PlayerProfile.activeMission)break;const p0=TCVREC.st.played,m0=TCVSIDE.st.missions;try{startMission(id)}catch(e){}
      if(PlayerProfile.activeMission&&PlayerProfile.activeMission.id===id){o.id=id;o.giver=TCVSIDE.S.mis[id][0];o.t=await waitP(p0,5000);o.played=TCVREC.st.played-p0;o.missions=TCVSIDE.st.missions-m0;
        const M=g77St().msgs[g77St().msgs.length-1];o.msg=M?{who:M.who,vv:M.vv,dur:M.dur,voice:M.voice,read:M.read,text:M.text.slice(0,30)}:null;o.voice=TCVREC.voiceFor(o.giver,TCVSIDE.S.ids[TCVSIDE.S.mis[id][1]]);
        const e0=TCVREC.st.ended;let t=0;while(TCVREC.st.ended===e0&&t<15000){await w(200);t+=200}
        const p1=TCVREC.st.played,th0=TCVSIDE.st.thanks;missionComplete();o.after=!PlayerProfile.activeMission;o.tt=await waitP(p1,6000);o.thanks=TCVSIDE.st.thanks-th0;o.thanksId=TCVSIDE.st.last&&TCVSIDE.st.last.id;
        const M2=g77St().msgs[g77St().msgs.length-1];o.msg2=M2?{who:M2.who,vv:M2.vv,voice:M2.voice}:null;await w(300);break}
      o.tried.push(id)}}catch(e){o.err=String(e&&e.stack||e).slice(0,300)}o.tried=o.tried.length;return o})()`);
  /* (4) the phone: a voice message of a contact (an opening of ezra), played from the phone */
  R.phone = await ev(`(async()=>{${W}const o={};try{try{TCVOICE.stop()}catch(e){}await w(300);const who='zs-b4-ezra',id=(TCVSIDE.S.by[who]||{}).call[0],tx=TCVSIDE.S.ids[id];const m=g77MsgIn(who,tx,{voice:true,silent:true});
    o.vv=m.vv;o.dur=m.dur;const r=TCVREC.rec(tx,m.vv);o.recSec=r?r[0]:null;const p0=TCVREC.st.played;g77SpPlay(m.id);o.t=await waitP(p0,4000);o.played=TCVREC.st.played-p0;await w(500);g77SpStop()}catch(e){o.err=String(e&&e.stack||e).slice(0,300)}return o})()`);
  /* (5) "off": an answered call does not play */
  R.off = await ev(`(async()=>{${W}const o={};try{g77DlgClose(true);TCVREC.setMode('off');const p0=TCVREC.st.played;g77CallIn('st-shimon','st-demo',{ring:20});await w(300);g77SpAnswer();await w(1500);o.played=TCVREC.st.played-p0;g77DlgClose(false);TCVREC.setMode('cast');o.mode=TCVREC.mode}catch(e){o.err=String(e&&e.stack||e).slice(0,300)}return o})()`);
  R.road = await ev(`(()=>{try{const r=roadAudit();const L=r.checks||r.results||[];const c=L.find(x=>x.id==='side_vrec');return c?{ok:c.ok,detail:c.detail}:null}catch(e){return String(e)}})()`);
  R.errs = { page: errs, console: cons, vrec: await ev('TCVREC.st.err'), side: await ev('TCVSIDE.st.err') };
  const C = R.calls, M = R.mission, near = (a, b) => a != null && b != null && Math.abs(a - b) < 0.08;
  R.summary = {
    data: !!(R.data.audit && R.data.audit.ok && R.data.story),
    call_opening: C.slice(0, 2).every(c => c.ans && c.played >= 1 && c.calls === 1 && near(c.bufDur, c.recSec) && c.caption && !c.tts),
    call_trait: !!(C[1] && C[1].trait),
    call_stop: !!(C[2] && C[2].stopped === 1 && !C[2].curAfter),
    mission_start: !!(M.id && M.played >= 1 && M.missions === 1 && M.msg && M.msg.vv === M.voice && M.msg.who === M.giver),
    mission_thanks: !!(M.after && M.thanks === 1 && M.msg2 && M.msg2.who === M.giver && M.msg2.vv),
    phone: !!(R.phone.vv && R.phone.played === 1 && R.phone.dur === Math.max(1, Math.round(R.phone.recSec))),
    off: R.off.played === 0 && R.off.mode === 'cast',
    road: !!(R.road && R.road.ok),
    errors: !errs.length && !R.errs.vrec && !R.errs.side
  };
  R.ok = Object.values(R.summary).every(Boolean);
  fs.writeFileSync(out, JSON.stringify(R, null, 1)); console.log(JSON.stringify(R.summary), 'ok=' + R.ok);
  await b.close(); process.exit(R.ok ? 0 : 1);
})().catch(e => { console.error(e); process.exit(2) });
