// בדיקה בלי דפדפן: החלק 074zu עם עולם מדומה (מנוע סיפורים מינימלי מתוך stories_dump.json) — check(), ציור על קנבס מדומה, וכפתור הכרטיס
const fs=require('fs');const [part,dump]=process.argv.slice(2);const D=JSON.parse(fs.readFileSync(dump,'utf8'));
const errs=[];const noop=()=>{};
const ctxMock=new Proxy({},{get:(t,k)=>k in t?t[k]:(k==='measureText'?()=>({width:10}):noop),set:(t,k,v)=>{t[k]=v;return true}});
const G={};G.window={addEventListener:(t,f)=>{G._click=f}};G.document={addEventListener:noop};G.performance={now:()=>Date.now()};
G.PlayerProfile={mode:'walk',money:1000,story:{flags:{},msgs:[],journal:[]}};G.PlayerPed={x:100,y:100,heading:0,moving:false};G.PlayerCar={x:300,y:300};G.State={phoneOpen:false,navigation:null};
G.Camera={x:0,y:0,zoom:1.5};G.location={hash:''};G.ctx=ctxMock;G.g77St=()=>G.PlayerProfile.story;G.toast=noop;G.setPhoneOpen=v=>{G.State.phoneOpen=v};G.renderPhone=noop;G.pnote=t=>'<div class="pnote">'+t+'</div>';
const reg={};for(const S of D)for(const s of S.steps)if(s.x!=null)reg[s.poi]={x:s.x,y:s.y};G.navPoiRegistry=()=>reg;
G.ensureEconomySchema=()=>G._eco||(G._eco={transactions:[]});G.ensureActivitySchema=()=>G._act||(G._act={certs:{}});
const ST={};for(const S of D)ST[S.id]={name:S.name,zone:S.zone,steps:S.steps.map(s=>{const o={poi:s.poi,title:s.title,btn:s.btn};for(const k of s.keys)o[k]=k==='drive'?[s.x||0,s.y||0,60]:true;return o})};
const fl=()=>G.PlayerProfile.story.flags;
G.S9STORY={ST,step:id=>+(fl()['s9:'+id]||0),done:id=>!!fl()['s9:'+id+':done'],advance(id){const n=this.step(id),S=ST[id];if(n>=S.steps.length){fl()['s9:'+id+':done']=1;fl()['s9:'+id]=0;G.PlayerProfile.money+=100;G.ensureEconomySchema().transactions.push(1);return true}fl()['s9:'+id]=n+1;G.State.navigation={t:id};return true},
 card(poi){let h='';for(const [id,S] of Object.entries(ST)){const n=this.step(id);if(n<1)continue;const s=S.steps[n-1];if(s.poi!==poi||!s.btn)continue;h+='<section><div class="pnote">t</div><div class="phoneActions"><button class="primary" data-s9-step="'+id+'">'+s.btn+'</button></div></section>'}return h}};
G.P34G={live:true,pl:null,plKey:null,n:{player:0}};G.p34On=()=>true;G.p34M=()=>({});G.p672Pl=()=>({h:1.76,top:{t:'tee',c:'#fff'}});G.P672={k:'k0'};G.p34Rec=(L,k)=>({look:L,key:k,wk:'walk',cyc:1});G.p34Hash=s=>s.length;G.p34Track=()=>({still:1,hd:0,dist:0});G.p34Out=(L,k)=>{G._lastPose=[k,L.look.item&&L.look.item.k,L.look.vest];return true};G.p34Err=e=>errs.push('p34 '+e);G.p34DirH=()=>0;
G.p34Player=()=>false;G.personBlockedAt=()=>null;G.drawPlayerPed=()=>{};G.interactNearbyPoi=()=>false;G.hudGoalText=()=>'חופשי';G.e3InView=()=>true;G.EDGES=[];G._NODE_BY_ID={};G.TYPES={local:{width:10}};G.g77S=()=>({chars:{}});G.P34={draw:()=>{}};G.p599Res=()=>2;
// הביקור במקום (הגג / היציע) — עולם מדומה מינימלי
G.updatePed=()=>{G._walked=(G._walked||0)+1};G.toggleVehicle=()=>'veh';G.Camera.update=function(){G._camDef=(G._camDef||0)+1};G.wldSkyPaint=()=>{};G.Targets={draw:()=>{}};
G.C4_BUILDINGS=[{id:'A5-OFFICE',x:100,y:3720,w:300,h:190,bld40:{H:44.6},entrance:{x:250,y:3920}}];G.BLD40={info:()=>({floors:12,H:44.6})};
G.A34D={standS:[200,2358,1050,2440],gates:[[420,2440],[625,2440],[830,2440]],stad:[200,1800,1050,2350]};G.PLC_POIS={'A5-OFFICE':{x:400,y:3815},'A3-STADIUM':{x:624,y:2491}};
G.PLC={n:{view:0,watch:0}};G.plcAct=a=>{G.PLC.n[a]++};G.plcMatchOn=()=>false;G.State.taxiRide=null;G.State.ferryRide=null;
G.g77S=()=>({chars:{'st-aharon':{name:'אהרון',color:'#7a5a3a'},'s9-yossi':{name:'יוסף',color:'#2f6fd0'}}});G.TCPOR={look:id=>({age:'elder',skin:'#e2b08a',hair:'bald',hairCol:'#ddd',beard:'full',beardCol:'#ddd',hat:'kippah',glasses:true,shirt:'#7a5a3a'})};
// 17.11 09:xx — המפתח של הגשר (S13-ST-G8 #2): 2 מכוניות על המפתח → התצפית מחכה
G.S13_LF={center:[7636,6731]};G._spanN=2;G.s13CarsOnSpan=()=>G._spanN;G.s13PlayerOnSpan=()=>0;
const src=fs.readFileSync(part,'utf8');const names=Object.keys(G);
const fn=new Function(...names,src+'\nreturn {SACT,p34Player,drawPlayerPed,interactNearbyPoi,hudGoalText,S9STORY,updatePed,toggleVehicle,plcAct};');
let X;try{X=fn(...names.map(k=>G[k]))}catch(e){console.log('LOAD ERROR',e.stack);process.exit(1)}
const A=X.SACT;
const c=A.check();console.log('check',JSON.stringify({ok:c.ok,n:c.n,bad:c.bad.slice(0,20),err:c.err,same:c.sameStory,money:c.sameMoney,kinds:c.kinds}));
console.log('span+layer(stub)',JSON.stringify({span:c.span,layer:c.layer,lookT:c.lookT}));
{const S={};G.window.TCBUSY={set:(k)=>{S[k]=1},clear:k=>{delete S[k]},blocks:k=>Object.keys(S).some(q=>q!=='card'&&q!==k)};G._spanN=0;const c2=A.check();console.log('layer(real-like)',JSON.stringify({ok:c2.ok,bad:c2.bad.slice(0,5),span:c2.span,layer:c2.layer}));delete G.window.TCBUSY}
const t=A.table();console.log('table',JSON.stringify({steps:t.steps,plain:t.plain,converted:t.converted,none0:t.storiesWithoutAction,none1:t.storiesWithoutActionNow}));
// מקצה לקצה מדומה: כרטיס → לחיצה → F → ציור כל פריים → התקדמות
function e2e(id,n){fl()['s9:'+id]=n;const s=ST[id].steps[n-1],p=reg[s.poi];G.PlayerPed.x=p.x;G.PlayerPed.y=p.y+4;G.PlayerProfile.mode='walk';
 const card=X.S9STORY.card(s.poi);const ok1=card.includes('← במשחק');let stopped=false;G._click({target:{closest:()=>({dataset:{s9Step:id}})},stopPropagation:()=>{stopped=true},preventDefault:noop});
 const cur=A.SA.cur;const r={id,n,card:ok1,stopped,armed:!!cur,k:cur&&cur.k,hud:X.hudGoalText()};let t0=Date.now();
 if(cur&&cur.k!=='via'){for(let q=0;q<(cur.q||1);q++){r['F'+q]=X.interactNearbyPoi();for(let f=0;f<10;f++){X.drawPlayerPed(Date.now());X.p34Player(Date.now(),false)}cur.t0-=cur.dur+10;X.drawPlayerPed(Date.now())}}else X.drawPlayerPed(Date.now());
 r.hud2=X.hudGoalText();r.pose=G._lastPose;r.step=G.S9STORY.step(id);r.carry=A.SA.carry&&A.SA.carry.nm;r.res=A.SA.res.length;return r}
for(const [id,n] of [['S9-ST-E4',2],['S9-ST-F3',3],['S9-ST-F3',4],['S12-ST-C1',2],['ZS-B4',1],['S14-ST-B7',2],['S9-ST-E5',1],['S13-ST-F8',3],['S15-ST-E0',2]])console.log(JSON.stringify(e2e(id,n)));
{const V=G.window.__TC_SACT;const vc=V.visCheck();console.log('visit',JSON.stringify(vc));
 // מקצה לקצה מדומה של הביקור: הכפתור (plcAct) → updatePed בכל פריים → E → חזרה
 G.PlayerPed.x=400;G.PlayerPed.y=3815;G.PlayerProfile.mode='walk';X.plcAct('view');const st=V.VIS.v&&V.VIS.v.ph;let n=0,seen=[];const T0=Date.now();
 const spin=ms=>{const e=Date.now()+ms;while(Date.now()<e){X.updatePed(.016);G.Camera.update(.016);X.drawPlayerPed(Date.now());const ph=V.VIS.v&&V.VIS.v.ph;if(seen[seen.length-1]!==ph)seen.push(ph);n++}};
 spin(7200);const hud=X.hudGoalText();const e=X.toggleVehicle();spin(6200);console.log('visit-e2e',JSON.stringify({start:st,seen,hud,e,end:!V.VIS.v,back:[Math.round(G.PlayerPed.x),Math.round(G.PlayerPed.y)],frames:n,err:V.VIS.err}))}
{const V=G.window.__TC_SACT;G.PlayerPed.x=624;G.PlayerPed.y=2491;X.plcAct('watch');const sp=ms=>{const e=Date.now()+ms;while(Date.now()<e){X.updatePed(.016);G.Camera.update(.016)}};sp(1500);const ph1=V.VIS.v&&V.VIS.v.ph;X.interactNearbyPoi();sp(3500);
 console.log('visit-early-exit',JSON.stringify({ph1,end:!V.VIS.v,back:[Math.round(G.PlayerPed.x),Math.round(G.PlayerPed.y)],err:V.VIS.err}))}
{const V=G.window.__TC_SACT;console.log('fig',JSON.stringify(V.figCheck()));const f=V.tcStepFig('st-aharon',{x:500,y:500},{until:9e9,src:'cut'});console.log('fig2',JSON.stringify({same:f===V.tcStepFig('st-aharon'),look:f.look,name:f.name,por:f.por}));V.tcStepFig('st-aharon',null)}
{const V=G.window.__TC_SACT,id='S15-ST-G0',n=2;fl()['s9:'+id]=n;A.SA.cur=null;const s=ST[id].steps[n-1],p=reg[s.poi];G.PlayerPed.x=p.x;G.PlayerPed.y=p.y+4;G.PlayerProfile.mode='walk';
 const c=V.arm(id,false);const r={k:c.k,R:c.R,area:c.area&&Math.round(c.area.r),dHide:Math.round(Math.hypot(c.pt.x-p.x,c.pt.y-p.y))};r.F_far=V.F();r.ph1=c.phase;r.hud1=X.hudGoalText();
 G.PlayerPed.x=c.pt.x+10;G.PlayerPed.y=c.pt.y;X.drawPlayerPed(Date.now());r.found=c.found;r.hud2=X.hudGoalText();r.F_near=V.F();r.ph2=c.phase;c.t0-=c.dur+10;X.drawPlayerPed(Date.now());r.step=G.S9STORY.step(id);r.carry=A.SA.carry&&A.SA.carry.nm;console.log('find',JSON.stringify(r))}
console.log('err',A.E.err,errs.slice(0,5));
