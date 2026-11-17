return (async()=>{const out={};const errs=[];window.addEventListener('error',e=>errs.push(String(e.message)));
 const one=()=>{const R=tcF9CK.story();return{ok:R.ok,sum:R.sum,bad:R.text.split('\n').filter(l=>/✗/.test(l)),a3:R.text.split('\n').filter(l=>/A3-TRAIN/.test(l))[0]}};
 out.clock0=gameClock().hhmm;out.plain=one();
 const ok=A34PLAY.startMatchNow();const b0=G84_CLOCK.base,M0=JSON.stringify(window.__TC_A3_MATCH);out.forced=ok;out.matchOn=!!A34PLAY.matchNow();
 out.withMatch=one();out.restored=G84_CLOCK.base===b0&&JSON.stringify(window.__TC_A3_MATCH)===M0&&!!A34PLAY.matchNow();
 for(const h of [6,23.5]){try{gameClockSet(Math.floor(h),(h%1)*60);delete window.__TC_A3_MATCH;out['at'+h]=Object.assign({clock:gameClock().hhmm},one())}catch(e){out['at'+h]=String(e)}}
 out.errs=errs;return out})()
