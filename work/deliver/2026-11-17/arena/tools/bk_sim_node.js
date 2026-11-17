// bk_sim_node.js — הרצה של הכדורסל של SPORT2 (024a) ב-node, בלי דפדפן: אילו אפשרויות של bkGen נתקעות (lastCatch רחוק מסוף המחצית). node bk_sim_node.js
const fs=require('fs');const src=fs.readFileSync('/home/user/tc_root/tc/pkg/work/src_game_t17_arena/parts/024a_sport2.js','utf8');
global.window={};const S2=new Function(src+'\nreturn SPORT2;')();const H=S2.H,BK=S2.BK;
const G={door:[367,3067],path:[[367,3067],[353,3072],[341,3073]]};
const P=[{name:'a',shirt:'#1f3f8a',shorts:'#f4f4f0',num:'#fff'},{name:'b',shirt:'#c0392b',shorts:'#1f2326',num:'#fff'}];
const V={none:{},pair:{pair:P},G:{G},sw:{sw:1},gs:{gs:24,play:200,tail:30},swG:{G,sw:1}};
for(const [k,O] of Object.entries(V)){let tot=0,stuck=0;for(let i=0;i<8;i++){const sd=(7000+i*10)*6007+36|0;const S=H.bkGen(sd,5,O);S2.simTo(S,S.dur);const lc=Math.max(0,...S.ev.filter(v=>v.k==='catch').map(v=>v.t));if(lc<S.ge-30)stuck++;const sc=S2.scoreAt(S,S.dur);tot+=sc[0]+sc[1];}console.log(k,'stuck',stuck,'/8 pts',tot);}
