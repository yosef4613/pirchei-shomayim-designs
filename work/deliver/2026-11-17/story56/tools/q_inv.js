// story56 · המלאי לפני הבנייה (כלל 19): סיפורי האזורים, המקומות, העבודות, הרישיונות, ה-API של הנעילות, הסצנות — מתוך S7F302
return (()=>{const R={};const T=(k,f)=>{try{R[k]=f()}catch(e){R[k]={error:String(e&&e.stack||e).slice(0,300)}}};
T('zs',()=>Object.entries(S9STORY.ST).map(([id,S])=>[id,S.zone,S.name,S.who||'',(S.steps||[]).length,(S.steps||[]).map(s=>(s.title||s.text||'').slice(0,40)+'@'+(s.poi||s.at||'')).join(' | ')]));
T('poi',()=>{const P=navPoiRegistry();return Object.keys(P).map(k=>[k,(P[k].label||'').slice(0,40),P[k].chunk||(()=>{try{return currentChunkId(P[k].x,P[k].y)}catch(e){return ''}})(),Math.round(P[k].x),Math.round(P[k].y)])});
T('jobs',()=>Object.values(MISSION_DEFS).map(d=>[d.id,(d.name||'').slice(0,40),d.type||d.jobKey||'',d.license||'',d.chunk||'',d.pickup||d.start||'',d.dropoff||'',(d.stops||[]).join('/'),d.vehicle?(d.vehicle.asset||'')+':'+(d.vehicle.ref||''):'']));
T('lic',()=>Object.keys(LICENSE_TRIALS).map(k=>[k,(LICENSE_TRIALS[k].name||LICENSE_TRIALS[k].label||'').slice(0,40)]));
T('licAll',()=>{try{return Object.entries(LICENSES||{}).map(([k,v])=>[k,(v.name||v.label||'').slice(0,40)])}catch(e){return String(e)}});
T('tclock',()=>typeof TCLOCK!=='undefined'?Object.keys(TCLOCK):null);
T('cuts',()=>({scenes:Object.keys(TC_CUTS.scenes),on:TC_CUTS.on,tccut:Object.keys(TCCUT)}));
T('flight',()=>{const o={};for(const k of ['TCFLY','TCFLIGHT','HELI','__TC_FLY','__TC_FLIGHT','heliFly','TCHELI','TCPOLICE'])try{o[k]=eval('typeof '+k)}catch(e){};return o});
T('weather',()=>{const o={};for(const k of ['WEATHER','TCWX','weatherNow','WX','__TC_WX','WORLD_WEATHER','W01'])try{o[k]=eval('typeof '+k)}catch(e){};return o});
T('vehAssets',()=>{try{return Object.keys(VEHICLE_ASSETS||{}).filter(k=>/FT|FIRE|POL|TOW|AMB|HELI|BUS|TR|PK/i.test(k)).slice(0,80)}catch(e){return String(e)}});
T('shows',()=>({films:TCSHOW.FILMS.map(f=>f.id+':'+f.name),plays:TCSHOW.PLAYS.map(f=>f.id+':'+f.name)}));
T('apis',()=>Object.keys(window).filter(k=>/^(__TC_|TC[A-Z]|S9|S1[0-9]|MB|MMIS|LN|LIC|SPORT|LEAGUE)/.test(k)).sort());
return JSON.stringify(R)})()
