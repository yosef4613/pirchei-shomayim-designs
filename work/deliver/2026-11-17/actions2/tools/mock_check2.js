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

G.exitVehicle=()=>{if(G.PlayerProfile.mode!=='vehicle')return false;G.PlayerProfile.mode='walk';G.PlayerPed.x=G.PlayerCar.x+30;G.PlayerPed.y=G.PlayerCar.y;return true};
G.enterVehicle=()=>{G.PlayerProfile.mode='vehicle';return true};G.personDirection=()=>0;G.g77Bubble=(a,t,o)=>{G._bub=(G._bub||[]);G._bub.push(t)};G.MISSION_DEFS={'M-ST-1-6':{name:'הדואר'}};

G._dlg=[];G._jobs=[];G._shows=[];G.g77DlgOpen=(id,mode)=>{G._dlg.push(id);G._open={id,mode};return true};G.g77DlgClose=()=>{G._open=null};
G.startMission=id=>{G._jobs.push(id);G.PlayerProfile.activeMission={id}};G.TCSHOW={FILMS:[{id:'born-of-sea',title:'נולד בים'}],PLAYS:[],open:(k,i,o)=>{G._shows.push(k+':'+i);return true},close:()=>{},get on(){return false}};
const MSD={dialogs:{'d-1':{who:'st-shimon'}},chapters:[{id:'1',missions:[{id:'1-2',giver:'st-shimon',steps:[{talk:'d-1',at:'E4-CONTROL',r:200}]},{id:'1-6',giver:'st-shimon',steps:[{job:'M-ST-1-6',at:'E4-CONTROL',r:220}]},{id:'1-7',steps:[{show:'film:born-of-sea',at:'E4-CONTROL',r:200}]}]}]};
G.TCSTORY={D:MSD,E:{qa:null,allowJob:null,cool:{}},cur(){const m=G.PlayerProfile.story.main;if(!m||!m.mi)return null;const mi=MSD.chapters[0].missions.find(q=>q.id===m.mi);return mi?{mi:m.mi,step:m.step,s:mi.steps[m.step]}:null},M(){return G.PlayerProfile.story.main},bring(id){const p=reg[id];if(!p)return false;G.PlayerProfile.mode='vehicle';G.PlayerCar.x=p.x+40;G.PlayerCar.y=p.y;return{x:p.x}}};
G.g77S=()=>({chars:{'st-aharon':{name:'אהרון',color:'#7a5a3a'},'s9-yossi':{name:'יוסף',color:'#2f6fd0'},'st-shimon':{name:'שמעון',color:'#1f7a8a'}},get open(){return G._open}});
const src=fs.readFileSync(part,'utf8');const names=Object.keys(G);
const fn=new Function(...names,src+'\nreturn {SACT,p34Player,drawPlayerPed,interactNearbyPoi,hudGoalText,S9STORY,updatePed,toggleVehicle,plcAct,g77DlgOpen,startMission};');
let X;try{X=fn(...names.map(k=>G[k]))}catch(e){console.log('LOAD ERROR',e.stack);process.exit(1)}
const A=X.SACT;

const V=G.window.__TC_SACT;
const c=A.check();console.log('check',JSON.stringify({ok:c.ok,n:c.n,bad:c.bad.slice(0,25),err:c.err,same:c.sameStory,money:c.sameMoney,kinds:c.kinds,noAuto:c.noAuto,anim:c.anim,drive:c.drive}));
const pc=V.plainCheck();console.log('plain',JSON.stringify({ok:pc.ok,n:pc.n,adv:pc.adv,walk:pc.walk,shake:pc.shake,talk:pc.talk,phone:pc.phone,bad:pc.bad.slice(0,10)}));
const mc=V.msCheck();console.log('ms',JSON.stringify(mc));
// real-time: the main-story talk — the engine calls g77DlgOpen when you stop near → blocked, ring; F → walk + shake + talk → the dialog
{G.PlayerProfile.story.main={v:1,mi:'1-2',step:0};const p=reg['E4-CONTROL'];G.PlayerProfile.mode='vehicle';G.PlayerCar.x=p.x+40;G.PlayerCar.y=p.y;const r0=X.g77DlgOpen('d-1','talk');const armed=!!V.MS.cur;const F1=X.interactNearbyPoi();
 const spin=ms=>{const e=Date.now()+ms;const seen=[];while(Date.now()<e){X.updatePed(.016);X.drawPlayerPed(Date.now());const q=V.PS.q;const k=q&&q.steps[q.i]&&(q.steps[q.i].p||q.steps[q.i].k);if(k&&seen[seen.length-1]!==k)seen.push(k)}return seen};
 const seen=spin(7000);console.log('ms-e2e',JSON.stringify({r0,armed,F1,seen,dlg:G._dlg,mode:G.PlayerProfile.mode,ps:!!V.PS.q,bub:G._bub,err:A.E.err}))}
// real-time: an action (take) with a cancel by a key in the middle
{const id='S9-ST-E4',n=2;fl()['s9:'+id]=n;A.SA.cur=null;A.SA.carry=null;const s=ST[id].steps[n-1],p=reg[s.poi];G.PlayerPed.x=p.x+30;G.PlayerPed.y=p.y+4;G.PlayerProfile.mode='walk';V.arm(id,true);
 const F1=X.interactNearbyPoi();const ph1=A.SA.cur&&A.SA.cur.phase;G.window._key&&0;V.psStop('key');const ph2=A.SA.cur&&A.SA.cur.phase;const F2=X.interactNearbyPoi();
 const e=Date.now()+4000;const seen=[];while(Date.now()<e){X.updatePed(.016);X.drawPlayerPed(Date.now());const q=V.PS.q;const k=q&&q.steps[q.i]&&(q.steps[q.i].p||q.steps[q.i].k);if(k&&seen[seen.length-1]!==k)seen.push(k)}
 console.log('take-e2e',JSON.stringify({F1,ph1,ph2,F2,seen,step:G.S9STORY.step(id),carry:A.SA.carry&&A.SA.carry.nm,err:A.E.err}))}
// the waiting figure: alive (wait / wave), turning
console.log('fig',JSON.stringify(V.figCheck()));
console.log('err',A.E.err,errs.slice(0,5));
