/* Turbo City bus studio. Oblique vector renderer, one model for every size and angle. */
(()=>{'use strict';
const L=120,W=25.5,H=31.875,K=.6,TOP=32.775;
const COLORS={1:'#2f6fd0',2:'#2f9e5f',3:'#ee7d2d'};
const clamp=(n,a,b)=>Math.max(a,Math.min(b,n)),f=n=>Number(n.toFixed(5));
const BRANDS=window.TurboBusBrands||{};
const tone=(hex,n)=>{const c=hex.replace('#','');return '#'+[0,2,4].map(i=>{const v=parseInt(c.slice(i,i+2),16);return Math.round(clamp(n<=1?v*n:v+(255-v)*(n-1),0,255)).toString(16).padStart(2,'0');}).join('');};
const escape=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&apos;'}[c]));
let seq=0;
function renderSvg(options={}){
 const angle=Number(options.angle)||0,th=angle*Math.PI/180,cs=Math.cos(th),sn=Math.sin(th),line=+[1,2,3].find(x=>x===+options.line)||3;
 const mode=['none','side','rear','wrap'].includes(options.adMode)?options.adMode:'none',wrapped=mode==='wrap',open=clamp(+options.door||0,0,1),night=!!options.night;
 const brandKey=Object.hasOwn(BRANDS,options.brand)?options.brand:'shibolet',brand=BRANDS[brandKey];
 if(!brand)throw Error('Approved brand data is missing');
 const palette=brand.palette,approvedLogo=brand.logo,logoViewBox=brand.logoViewBox||'0 0 316 211';
 const glass=clamp(options.glassOpacity==null?.5:+options.glassOpacity,0,1),col=wrapped?palette.base:COLORS[line],id='tc'+(++seq)+'-',serial=line===3?'303':line===2?'201':'101';
 const url=s=>'url(#'+id+s+')',ref=s=>'#'+id+s;
 const P=(x,y,z=0)=>[f(x*cs-y*sn),f(x*sn+y*cs-K*z)];
 // The nose is curved across its width and swept back toward the roof.
 // It stays inside the existing 120 x 25.5 footprint and leaves both axles untouched.
 const roofZ=y=>{const t=clamp((Math.abs(y)-11.15)/1.6,0,1);return H-1.6*(1-Math.sqrt(1-t*t));};
 const noseX=(y,z)=>{const t=clamp((Math.abs(y)-8.75)/4,0,1);return 60-4.8*(1-Math.sqrt(1-t*t))-2.4*(z/H)**2;};
 const nosePoint=(u,v)=>{const y=(127.5-u)*.1,z=Math.min(H-v*.1,roofZ(y));return [noseX(y,z),y,z];};
 // The tail is a curved shell as well: broad central panel, rounded width shoulders,
 // roof rake and a tucked-under lower bumper, entirely inside the original footprint.
 const tailX=(y,z)=>{const t=clamp((Math.abs(y)-8.5)/4.25,0,1);return -60+4.1*(1-Math.sqrt(1-t*t))+1.5*(z/H)**2+.65*Math.exp(-(((z-2.3)/1.7)**2));};
 // Rear texture runs in the opposite lateral direction to the front, preserving reading order.
 const tailPoint=(u,v)=>{const y=(u-127.5)*.1,z=Math.min(H-v*.1,roofZ(y));return [tailX(y,z),y,z];};
 const pts=a=>a.map(p=>P(...p).join(',')).join(' ');
 const poly=(a,fill,stroke='none',sw=.08)=>`<polygon points="${pts(a)}" fill="${fill}" stroke="${stroke}" stroke-width="${sw}" stroke-linejoin="round"/>`;
 const line3=(a,b,stroke,width=.08)=>`<path d="M${P(...a)}L${P(...b)}" fill="none" stroke="${stroke}" stroke-width="${width}" stroke-linecap="round"/>`;
 const text=(x,y,s,size=11,color='#fff',anchor='middle',extra='')=>`<text x="${x}" y="${y}" text-anchor="${anchor}" fill="${color}" font-family="Arial, sans-serif" font-size="${size}" font-weight="700" ${extra}>${escape(s)}</text>`;
 const defs=`<defs>
 <linearGradient id="${id}body" x1="0" y1="0" x2="0" y2="1"><stop stop-color="${col}"/><stop offset=".13" stop-color="${col}"/><stop offset=".58" stop-color="${col}"/><stop offset="1" stop-color="#102c32"/></linearGradient>
 <linearGradient id="${id}paint" x1="0" y1="0" x2=".2" y2="1"><stop stop-color="#ffffff" stop-opacity=".3"/><stop offset=".35" stop-color="#ffffff" stop-opacity="0"/><stop offset=".7" stop-color="#000000" stop-opacity=".1"/><stop offset="1" stop-color="#000000" stop-opacity=".32"/></linearGradient>
 <linearGradient id="${id}glass" x1="0" y1="0" x2=".65" y2="1"><stop stop-color="${night?'#b5c9bb':'#284b61'}"/><stop offset=".43" stop-color="${night?'#6e9187':'#173747'}"/><stop offset=".44" stop-color="${night?'#54766d':'#386372'}"/><stop offset="1" stop-color="${night?'#203d43':'#091a24'}"/></linearGradient>
 <linearGradient id="${id}chrome" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#e6eef0"/><stop offset=".32" stop-color="#7f939d"/><stop offset=".5" stop-color="#f8fbfa"/><stop offset=".73" stop-color="#566773"/><stop offset="1" stop-color="#b5c5cb"/></linearGradient>
 <radialGradient id="${id}rim"><stop stop-color="#566670"/><stop offset=".2" stop-color="#e7ecee"/><stop offset=".63" stop-color="#6d7f89"/><stop offset=".82" stop-color="#f8fbfc"/><stop offset="1" stop-color="#4c606c"/></radialGradient>
 <linearGradient id="${id}mirrorGlass" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#476476"/><stop offset=".48" stop-color="#adc9d0"/><stop offset=".5" stop-color="#587786"/><stop offset="1" stop-color="#203d4e"/></linearGradient>
 <linearGradient id="${id}roof" x1="0" y1="0" x2="0" y2="1"><stop stop-color="${wrapped?tone(col,night?.65:1):night?'#7f99a4':'#edf0ec'}"/><stop offset=".4" stop-color="${wrapped?tone(col,night?.9:1.12):night?'#9bb1ba':'#fff'}"/><stop offset="1" stop-color="${wrapped?tone(col,night?.45:.72):night?'#526d7c':'#aab6bc'}"/></linearGradient>
 <linearGradient id="${id}beam" gradientUnits="userSpaceOnUse" x1="59" y1="0" x2="82" y2="0"><stop stop-color="#ebf7ff" stop-opacity=".52"/><stop offset=".25" stop-color="#d6eaff" stop-opacity=".3"/><stop offset="1" stop-color="#b5d4ff" stop-opacity="0"/></linearGradient>
 <radialGradient id="${id}whiteGlow"><stop stop-color="#ffffff" stop-opacity=".95"/><stop offset=".22" stop-color="#e9f7ff" stop-opacity=".65"/><stop offset="1" stop-color="#b4d9ff" stop-opacity="0"/></radialGradient>
 <radialGradient id="${id}redGlow"><stop stop-color="#ffb1a0" stop-opacity=".9"/><stop offset=".2" stop-color="#ff493e" stop-opacity=".65"/><stop offset="1" stop-color="#ff2222" stop-opacity="0"/></radialGradient>
 <radialGradient id="${id}amberGlow"><stop stop-color="#fff0b3" stop-opacity=".9"/><stop offset=".22" stop-color="#ffc468" stop-opacity=".6"/><stop offset="1" stop-color="#ff9f2e" stop-opacity="0"/></radialGradient>
 <filter id="${id}lightGlow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="2.8"/><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>
 <filter id="${id}beamSoft" x="-30%" y="-100%" width="160%" height="300%"><feGaussianBlur stdDeviation=".6"/></filter>
 <linearGradient id="${id}adbg" x1="0" y1="0" x2="1" y2=".7"><stop stop-color="${palette.deep}"/><stop offset=".5" stop-color="${palette.base}"/><stop offset="1" stop-color="${tone(palette.deep,.8)}"/></linearGradient>
 <radialGradient id="${id}tomato" cx=".3" cy=".25"><stop stop-color="#ffad72"/><stop offset=".28" stop-color="#ff4d28"/><stop offset=".75" stop-color="#c31813"/><stop offset="1" stop-color="#7a150e"/></radialGradient>
 <radialGradient id="${id}pepper" cx=".3" cy=".3"><stop stop-color="#fff68a"/><stop offset=".4" stop-color="#ffd629"/><stop offset="1" stop-color="#c47800"/></radialGradient>
 <linearGradient id="${id}leaf" x2="1" y2="1"><stop stop-color="#c7eb43"/><stop offset=".4" stop-color="#58a936"/><stop offset="1" stop-color="#074b29"/></linearGradient>
 <g id="${id}logo">${approvedLogo}</g>
 <g id="${id}produce">${produce(id)}</g>
 <g id="${id}sideAd" data-ad-width="560" data-ad-height="176"><rect x="145" y="102" width="560" height="176" rx="5" fill="${palette.deep}" stroke="${palette.accent}" stroke-width="2"/>
 <path d="M149 248Q410 293 701 235M149 263Q410 303 701 250" fill="none" stroke="${palette.ribbon}" stroke-width="6" opacity=".8"/>
 <svg x="159" y="110" width="530" height="160" viewBox="${logoViewBox}" preserveAspectRatio="xMidYMid meet"><use href="${ref('logo')}"/></svg></g>
 <g id="${id}art"><rect width="1200" height="319" fill="${url('adbg')}"/>
 <path d="M0 259Q230 338 580 247T1200 196L1200 229Q965 206 590 284T0 285Z" fill="${palette.ribbon}"/>
 <path d="M0 279Q250 346 620 273T1200 230L1200 239Q967 224 622 286T0 290Z" fill="${palette.accent}"/>
 <path d="M0 306Q450 346 750 293T1200 264" fill="none" stroke="#f5e6a0" stroke-width="3" opacity=".7"/>
 <svg x="305" y="51" width="534" height="260" viewBox="${logoViewBox}" preserveAspectRatio="xMidYMid meet"><use href="${ref('logo')}"/></svg>
 ${brandKey==='shibolet'?`<use href="${ref('produce')}" transform="translate(925 115) scale(.53)"/>`:brand.decoration||''}
 </g>
 </defs>`;
 const sideMat=y=>{const p=P(-L/2,y,H);return `matrix(${f(cs*.1)} ${f(sn*.1)} 0 ${f(K*.1)} ${p[0]} ${p[1]})`};
 const endMat=x=>{const p=P(x,-W/2,H);return `matrix(${f(-sn*.1)} ${f(cs*.1)} 0 ${f(K*.1)} ${p[0]} ${p[1]})`};
 const tailSideX=v=>f((tailX(W/2,H-v*.1)+60)*10);
 const basePath=`M${tailSideX(16)+12} 16H1108Q1128 16 1130 37L1150 255Q1155 282 1152 289Q1151 296 1141 296H1020A60 60 0 0 0 900 296H264A60 60 0 0 0 144 296H${tailSideX(296)+12}Q${tailSideX(296)} 296 ${tailSideX(284)} 284L${tailSideX(260)} 260L${tailSideX(200)} 200L${tailSideX(130)} 130L${tailSideX(55)} 55Q${tailSideX(16)} 16 ${tailSideX(16)+12} 16Z`;
 const surfaces=[];
 const queue=(depth,svg)=>surfaces.push({depth,svg});
 // Tyres and rims are discs on the original axle coordinates; nothing changes the world footprint.
 for(const x of [-39.6,36])for(const side of [-1,1]){
  const y=side*12.65,visible=side*cs>-.02;
  if(!visible)continue;
  const p=P(x,y,5.1),m=`matrix(${f(cs*.1)} ${f(sn*.1)} 0 ${f(-K*.1)} ${p[0]} ${p[1]})`;
  const bolts=Array.from({length:10},(_,i)=>{const a=i*Math.PI/5;return `<circle cx="${f(Math.cos(a)*20)}" cy="${f(Math.sin(a)*20)}" r="2.7" fill="#26343f"/>`}).join('');
  queue(K*(x*sn+y*cs)+5.1,`<g transform="${m}"><circle r="51" fill="#0e1419" stroke="#04090b" stroke-width="3"/><circle r="46" fill="#17232d" stroke="#394751" stroke-width="2"/><circle r="36" fill="${url('rim')}" stroke="#a4b5be" stroke-width="1.5"/><circle r="26" fill="#71848f"/>${bolts}<circle r="13" fill="${url('chrome')}"/><circle r="6" fill="#778c99"/><path d="M-36-24A44 44 0 0 1 28-34" fill="none" stroke="#65737c" stroke-width="2"/></g>`);
 }
 const sideFace=side=>{
  const y=side*W/2,doors=side===1,[frontX,backX]=[1032,624];
  const art=`<g${side<0?' transform="translate(1200 0) scale(-1 1)"':''}><use href="${ref('art')}"/></g>`;
  const sideAd=`<g${side<0?' transform="translate(850 0) scale(-1 1)"':''}><use href="${ref('sideAd')}"/></g>`;
  let s=`<g transform="${sideMat(y)}"><defs><clipPath id="${id}side${side}"><path d="${basePath}"/></clipPath><clipPath id="${id}glass${side}"><rect x="28" y="34" width="1144" height="139" rx="9"/></clipPath></defs><g clip-path="${url('side'+side)}"><path d="${basePath}" fill="${url('body')}"/>`;
  if(wrapped)s+=art;
  if(mode==='side')s+=sideAd;
  if(night)s+=`<path d="${basePath}" fill="#03172d" opacity=".23"/>`;
  s+=`<rect x="23" y="27" width="1153" height="150" rx="11" fill="#08141e"/><g clip-path="${url('glass'+side)}"><rect x="28" y="34" width="1144" height="139" fill="${url('glass')}"/>`;
  for(let i=0;i<9;i++){
   const x=52+i*123;
   s+=`<path d="M${x+20} 46h66v75h-66z" fill="${night?'#d5c9a6':'#315364'}" opacity="${night?'.56':'.24'}"/><path d="M${x+25} 113h58v30h-58z" fill="#142633"/><path d="M${x+20} 48l40-8v72l-40 14z" fill="#7995a3" opacity=".13"/>`;
   if(night)s+=`<rect x="${x+8}" y="37" width="92" height="3.5" rx="1.5" fill="#fff1bc" filter="${url('lightGlow')}"/>`;
  }
  s+=`<path d="M50 38H410L270 171H30ZM562 38H820L680 171H422ZM1040 38H1180L1065 171H910Z" fill="#d1e3e9" opacity="${night?'.04':'.15'}"/>`;
  if(wrapped)s+=`<g opacity="${glass}">${art}</g>`;
  if(mode==='side')s+=`<g data-side-ad-glass="true" opacity="${glass}">${sideAd}</g>`;
  s+='</g>';
  for(let i=1;i<=9;i++)s+=`<path d="M${i*123+12} 32v145" stroke="#12232f" stroke-width="7"/><path d="M${i*123+14} 35v135" stroke="#72939e" stroke-width="1.2" opacity=".7"/>`;
  s+=`<path d="M20 181h1159" stroke="#d1e3df" stroke-opacity=".7" stroke-width="3"/><path d="M18 287h1159" stroke="#121b22" stroke-width="13"/><path d="M25 279h1150" stroke="#dce7e8" stroke-opacity=".6" stroke-width="2"/>`;
  if(!wrapped&&mode!=='side'){
   s+=`<path d="M20 235Q390 255 600 214T1170 199" fill="none" stroke="#fff" stroke-opacity=".22" stroke-width="14"/><path d="M20 246Q390 267 600 226T1170 211" fill="none" stroke="#e9f0ed" stroke-opacity=".5" stroke-width="3"/>`;
  }
  // Rear service panel, low-floor seams and marker lamps.
  s+=`<rect x="34" y="194" width="106" height="63" rx="4" fill="#102a31" opacity=".65"/>`;
  for(let i=0;i<8;i++)s+=`<path d="M42 ${202+i*6}h89" stroke="#87a5a6" stroke-width="2" opacity=".65"/>`;
  for(const x of [278,572,795,1115])s+=`<path d="M${x} 188v83" stroke="#112b36" stroke-opacity=".65" stroke-width="1.6"/>`;
  for(const x of [42,296,828,1143])s+=`<rect x="${x}" y="273" width="12" height="4" rx="1.5" fill="#ffbd62"/>`;
  s+=`<path d="M25 23h1080" stroke="#fff" stroke-opacity=".45" stroke-width="3"/><rect width="1200" height="319" fill="${url('paint')}"/>`;
  if(doors){
   for(const [dx,dw,index] of [[backX-49,98,0],[frontX-46,92,1]]){
    s+=`<g><rect x="${dx-4}" y="24" width="${dw+8}" height="275" rx="5" fill="#071219" stroke="#98a9aa" stroke-width="3"/><rect x="${dx+8}" y="252" width="${dw-16}" height="39" fill="${night?'#81744e':'#374750'}"/><path d="M${dx+10} 266h${dw-20}m-${dw-20} 13h${dw-20}" stroke="${night?'#fff2b4':'#e7b340'}" stroke-width="3"/><path d="M${dx+17} 60v190m${dw-34} 0V60" stroke="#bdb685" stroke-width="3" opacity=".65"/>`;
    for(let leaf=0;leaf<2;leaf++){
     const lx=dx+leaf*dw/2,shift=(leaf?1:-1)*open*dw*.44;
     s+=`<g data-door-leaf="${leaf?1:-1}" data-door-travel="${dw*.44}" transform="translate(${shift} 0)"><defs><clipPath id="${id}leaf${index}${leaf}"><rect x="${lx+1}" y="27" width="${dw/2-2}" height="267" rx="2"/></clipPath></defs><g clip-path="${url('leaf'+index+leaf)}"><rect x="${lx}" y="26" width="${dw/2}" height="269" fill="${col}"/><rect x="${lx+5}" y="36" width="${dw/2-10}" height="201" rx="2" fill="${url('glass')}"/><path d="M${lx+8} 45l${dw/2-17} 0v60l-${dw/2-17} 35z" fill="#ccdfdf" opacity=".12"/>`;
     if(wrapped||mode==='side'){s+=`<use href="${ref(wrapped?'art':'sideAd')}"/><rect x="${lx+5}" y="36" width="${dw/2-10}" height="201" fill="${url('glass')}" opacity="${1-glass}"/>`;}
     s+=`<path d="M${lx+2} 29v261M${lx+dw/2-2} 29v261" stroke="#b8c8cd" stroke-width="2"/><path d="M${lx+6} 238h${dw/2-12}" stroke="#d8e4e3" stroke-width="2"/><rect x="${leaf?lx+5:lx+dw/2-9}" y="180" width="3" height="28" rx="1" fill="#dde8e4"/><path d="M${lx+6} 287h${dw/2-12}" stroke="#ffce59" stroke-width="3"/></g></g>`;
    }
    s+=`<path d="M${dx-3} 24h${dw+6}" stroke="#d9e5e2" stroke-width="4"/><path d="M${dx-3} 299h${dw+6}" stroke="#0d2029" stroke-width="5"/></g>`;
   }
  }
  const ledX=doors?766:355;
  s+=`<g${side<0?` transform="translate(${2*ledX+205} 0) scale(-1 1)"`:''}>${led(ledX,41,205,38,line,'מסוף E3',id,night,text)}</g><g${side<0?' transform="translate(2240 0) scale(-1 1)"':''}>${text(1120,267,serial,17,'#f3f5df')}</g>`;
  s+=`</g><path d="${basePath}" fill="none" stroke="#152a33" stroke-width="2.2"/></g>`;
  return s;
 };
 if(cs>.0001)queue(K*(W/2*cs)+H/2,sideFace(1));
 if(cs<-.0001)queue(K*(-W/2*cs)+H/2,sideFace(-1));
 const endFace=front=>{
  let s=`<g id="${id+(front?'frontPaint':'rearPaint')}"><rect width="255" height="296" fill="${col}"/><rect width="255" height="296" fill="${url('paint')}"/>`;
  if(front){
   s+=`<path d="M45 11H210Q246 11 248 47L246 154Q244 188 216 190H39Q11 188 9 154L7 47Q9 11 45 11Z" fill="#081920"/><path d="M35 64Q127 53 220 64L232 149Q230 176 211 177H44Q25 176 23 149Z" fill="${url('glass')}"/><path d="M37 68h94L48 169H28z" fill="#bed9dc" opacity=".18"/><path d="M127 62v109" stroke="#101e26" stroke-width="5"/><path d="M36 161l67-35m18 35l70-35" stroke="#0b171e" stroke-width="4" stroke-linecap="round"/><path d="M37 19Q127 7 217 19" fill="none" stroke="#d8e8e7" stroke-width="2.4" opacity=".55"/>`;
   if(wrapped)s+=`<path d="M9 196Q130 249 246 189v47Q129 262 9 228Z" fill="${palette.ribbon}"/><path d="M10 236Q115 270 245 232" fill="none" stroke="${palette.accent}" stroke-width="6"/>`;
   s+=led(22,26,211,35,line,'מסוף E3',id,night,text);
   s+=`<path d="M87 207Q127 201 168 207L174 230Q128 238 81 230Z" fill="#18303b"/><path d="M92 213h70m-70 7h70m-70 7h70" stroke="#7b949e" stroke-width="2"/><path d="M7 248Q127 267 248 248L242 283Q127 301 13 283Z" fill="#112733"/><path d="M14 240Q36 241 64 250L60 266Q33 266 17 257Z" fill="#091c25" stroke="#728d9a" stroke-width="2"/><path d="M191 250Q219 241 241 240L238 257Q222 266 195 266Z" fill="#091c25" stroke="#728d9a" stroke-width="2"/><path d="M20 249Q37 249 56 256m143 0q19-7 36-7" fill="none" stroke="${night?'#fffef5':'#e8f5f2'}" stroke-width="5.5" stroke-linecap="round" ${night?`filter="${url('lightGlow')}"`:''}/><circle cx="37" cy="253" r="6" fill="${night?'#fffef7':'#dcecf0'}"/><circle cx="218" cy="253" r="6" fill="${night?'#fffef7':'#dcecf0'}"/><path d="M20 270h35m145 0h35" stroke="${night?'#f8ffe6':'#d2f1ee'}" stroke-width="3"/><rect x="103" y="267" width="49" height="13" rx="2" fill="#f5d265"/><path d="M22 286Q127 303 233 286" fill="none" stroke="#758c96" stroke-width="2"/>`;
  }else{
   s+=`<path d="M40 18H215Q242 18 243 43V90Q241 111 221 112H34Q14 111 12 90V43Q13 18 40 18Z" fill="#0c202a"/><path d="M23 65Q127 59 232 65L230 94Q128 109 25 94Z" fill="${url('glass')}"/><path d="M42 21Q127 12 213 21" fill="none" stroke="#c8dcdf" stroke-width="2" opacity=".6"/>`+led(60,28,135,29,line,'',id,night,text);
   if(mode==='rear'||wrapped)s+=`<rect x="42" y="122" width="171" height="115" rx="3" fill="${palette.deep}" stroke="${palette.accent}" stroke-width="1.8"/><svg x="44" y="122" width="167" height="114" viewBox="${logoViewBox}"><use href="${ref('logo')}"/></svg>`;
   else{for(let i=0;i<9;i++)s+=`<path d="M45 ${132+i*9}h165" stroke="#18343e" stroke-width="4"/>`;s+=text(127,116,'TURBO CITY',13,'#e5eef0');}
   s+=`<path d="M9 240Q127 252 246 240L241 282Q127 300 14 282Z" fill="#122734"/><path d="M20 285Q127 301 235 285" fill="none" stroke="#839ca6" stroke-width="2.5"/><path d="M20 243Q127 254 235 243" fill="none" stroke="#d5e4e6" stroke-opacity=".5" stroke-width="1.8"/><rect x="107" y="264" width="43" height="13" rx="2" fill="#f2c747"/>`;
   for(const lx of [16,223])s+=`<rect x="${lx}" y="126" width="16" height="113" rx="7" fill="#16212a"/><rect x="${lx+3}" y="131" width="10" height="49" rx="4" fill="${night?'#ff5e4b':'#d33c31'}" ${night?`filter="${url('lightGlow')}"`:''}/><rect x="${lx+3}" y="187" width="10" height="21" rx="3" fill="#e2e9dd"/><rect x="${lx+3}" y="214" width="10" height="19" rx="3" fill="#e4973b"/>`;
   s+=text(127,254,serial,14,'#f7f3dd');
  }
  s+='</g>';return s;
 };
 const frontPaint=endFace(true),rearPaint=endFace(false),frontClips=[];
 // Map one continuous front design onto the curved shell, with affine triangles.
 const uv=[0,3,8,15,25,40,85,127.5,170,215,230,240,247,252,255],vv=[0,55,130,200,260,296];
 const expandedPolygon=tri=>{
  const n=tri.length,edges=tri.map((p,i)=>{const q=tri[(i+1)%n],nx=q[1]-p[1],ny=p[0]-q[0],len=Math.hypot(nx,ny);return [nx,ny,nx*p[0]+ny*p[1]+.8*len];});
  return edges.map((a,i)=>{const b=edges[(i+n-1)%n],d=a[0]*b[1]-b[0]*a[1];return [f((a[2]*b[1]-b[2]*a[1])/d),f((a[0]*b[2]-b[0]*a[2])/d)];}).map(p=>p.join(',')).join(' ');
 };
 const affine=(tri,point=nosePoint)=>{const [a,b,c]=tri,[u0,v0]=a,[u1,v1]=b,[u2,v2]=c,[x0,y0]=P(...point(u0,v0)),[x1,y1]=P(...point(u1,v1)),[x2,y2]=P(...point(u2,v2)),d=(u1-u0)*(v2-v0)-(u2-u0)*(v1-v0);const A=((x1-x0)*(v2-v0)-(x2-x0)*(v1-v0))/d,B=((y1-y0)*(v2-v0)-(y2-y0)*(v1-v0))/d,C=((u1-u0)*(x2-x0)-(u2-u0)*(x1-x0))/d,D=((u1-u0)*(y2-y0)-(u2-u0)*(y1-y0))/d;return `matrix(${[A,B,C,D,x0-A*u0-C*v0,y0-B*u0-D*v0].map(f).join(' ')})`;};
 for(let i=0;i<uv.length-1;i++)for(let j=0;j<vv.length-1;j++){
  const u0=uv[i],u1=uv[i+1],v0=vv[j],v1=vv[j+1],a=nosePoint(u0,(v0+v1)/2),b=nosePoint(u1,(v0+v1)/2),dxdy=(b[0]-a[0])/(b[1]-a[1]),rake=4.8*((a[2]+b[2])/2)/H**2;
  if(K*(sn-dxdy*cs)+rake<.0001)continue;
  const panels=j===0&&(i<3||i>10)?[[[u0,v0],[u1,v0],[u1,v1]],[[u0,v0],[u1,v1],[u0,v1]]]:[[[u0,v0],[u1,v0],[u1,v1],[u0,v1]]];
  for(const tri of panels){
   const tag=`nose${i}-${j}-${frontClips.length}`,coords=expandedPolygon(tri),world=tri.map(p=>nosePoint(...p)),depth=world.reduce((s,p)=>s+K*(p[0]*sn+p[1]*cs)+p[2],0)/tri.length;
   frontClips.push(`<clipPath id="${id+tag}"><polygon points="${coords}"/></clipPath>`);
   const shade=.04+.16*Math.abs((a[1]+b[1])/2)/(W/2);
   queue(depth,`<g data-nose-panel="true" transform="${affine(tri)}" clip-path="${url(tag)}"><use href="${ref('frontPaint')}"/><rect width="255" height="296" fill="#082534" opacity="${f(shade)}"/></g>`);
  }
 }
 for(let i=0;i<uv.length-1;i++)for(let j=0;j<vv.length-1;j++){
  const u0=uv[i],u1=uv[i+1],v0=vv[j],v1=vv[j+1],a=tailPoint(u0,(v0+v1)/2),b=tailPoint(u1,(v0+v1)/2),dxdy=(b[0]-a[0])/(b[1]-a[1]),y=(a[1]+b[1])/2,z=(a[2]+b[2])/2,rake=(tailX(y,z+.01)-tailX(y,z-.01))/.02;
  if(K*(-sn+dxdy*cs)+rake<.0001)continue;
  const panels=j===0&&(i<3||i>10)?[[[u0,v0],[u1,v0],[u1,v1]],[[u0,v0],[u1,v1],[u0,v1]]]:[[[u0,v0],[u1,v0],[u1,v1],[u0,v1]]];
  for(const tri of panels){
   const tag=`tail${i}-${j}-${frontClips.length}`,world=tri.map(p=>tailPoint(...p)),depth=world.reduce((s,p)=>s+K*(p[0]*sn+p[1]*cs)+p[2],0)/tri.length;
   frontClips.push(`<clipPath id="${id+tag}"><polygon points="${expandedPolygon(tri)}"/></clipPath>`);
   queue(depth,`<g data-tail-panel="true" transform="${affine(tri,tailPoint)}" clip-path="${url(tag)}"><use href="${ref('rearPaint')}"/><rect width="255" height="296" fill="#082534" opacity="${f(.04+.16*Math.abs(y)/(W/2))}"/></g>`);
  }
 }
 // Assemble the roof as one surface layer: far AC units must not sort under its plane.
 const roof=[];
 const roofBoundary=[...uv.map(u=>{const y=(u-127.5)*.1;return [tailX(y,roofZ(y)),y,roofZ(y)];}),...uv.map(u=>{const y=(127.5-u)*.1;return [noseX(y,roofZ(y)),y,roofZ(y)];})];
 const centralRoof=[...uv.map(u=>{const y=clamp((u-127.5)*.1,-11.15,11.15);return [tailX(y,H),y,H];}),...uv.map(u=>{const y=clamp((127.5-u)*.1,-11.15,11.15);return [noseX(y,H),y,H];})];
 roof.push(poly(centralRoof,url('roof'),'#8ba2a8',.1));
 for(const side of [-1,1])for(const [y0,y1] of [[11.15,11.75],[11.75,12.35],[12.35,12.75]]){const a=y0*side,b=y1*side;roof.push(poly([[tailX(a,roofZ(a)),a,roofZ(a)],[noseX(a,roofZ(a)),a,roofZ(a)],[noseX(b,roofZ(b)),b,roofZ(b)],[tailX(b,roofZ(b)),b,roofZ(b)]],url('roof'),'#7d999f',.05));}
 const roofMat=()=>{const p=P(-60,-W/2,H+.02);return `matrix(${f(cs*.1)} ${f(sn*.1)} ${f(-sn*.1)} ${f(cs*.1)} ${p[0]} ${p[1]})`};
 if(wrapped)roof.push(`<g clip-path="${url('roofClip')}"><g transform="${roofMat()}"><path d="M0 31Q450 140 1200 54v38Q500 188 0 61Z" fill="${palette.accent}"/><path d="M0 195Q700 71 1200 182" fill="none" stroke="${palette.ribbon}" stroke-width="29"/><svg x="730" y="38" width="260" height="180" viewBox="${logoViewBox}"><use href="${ref('logo')}"/></svg></g></g>`);
 const box=(x0,x1,y0,y1,z0,z1)=>{
  const a=[];
  a.push({d:z1+K*((x0+x1)/2*sn+(y0+y1)/2*cs),s:poly([[x0,y0,z1],[x1,y0,z1],[x1,y1,z1],[x0,y1,z1]],'#e3e8e6','#71858d',.1)});
  if(cs>0)a.push({d:(z0+z1)/2+K*((x0+x1)/2*sn+y1*cs),s:poly([[x0,y1,z0],[x1,y1,z0],[x1,y1,z1],[x0,y1,z1]],'#9bafb5','#5a727e',.08)});
  if(cs<0)a.push({d:(z0+z1)/2+K*((x0+x1)/2*sn+y0*cs),s:poly([[x0,y0,z0],[x1,y0,z0],[x1,y0,z1],[x0,y0,z1]],'#bccbd0','#71858d',.08)});
  if(sn>0)a.push({d:(z0+z1)/2+K*(x1*sn+(y0+y1)/2*cs),s:poly([[x1,y0,z0],[x1,y1,z0],[x1,y1,z1],[x1,y0,z1]],'#b1c2c6','#71858d',.08)});
  if(sn<0)a.push({d:(z0+z1)/2+K*(x0*sn+(y0+y1)/2*cs),s:poly([[x0,y0,z0],[x0,y1,z0],[x0,y1,z1],[x0,y0,z1]],'#8ba0a9','#71858d',.08)});
  a.sort((m,n)=>m.d-n.d);for(const q of a)roof.push(q.s);
 };
 const roofUnits=[[-21,13,-7,7,TOP],[-46,-32,-6.5,6.5,H+.55],[26,41,-6.5,6.5,H+.5]];
 roofUnits.sort((a,b)=>((a[0]+a[1])-(b[0]+b[1]))*sn);
 for(const [x0,x1,y0,y1,z1] of roofUnits){
  box(x0,x1,y0,y1,H,z1);
  for(let x=x0+1.2;x<x1-.5;x+=1.2)roof.push(line3([x,y0+1,z1+.02],[x,y1-1,z1+.02],'#718890',.17));
 }
 // Roof seam highlights, located inside the original width and height envelope.
 for(const yy of [-10.7,10.7])roof.push(line3([-55,yy,H+.04],[55,yy,H+.04],wrapped?tone(palette.base,1.25):'#fff',.14));
 // Two external rear-view mirrors, with raised arms, solid housings and reflective rear faces.
 // Their protrusions are visual attachments; the body dimensions and axle coordinates stay unchanged.
 for(const side of [-1,1]){
  const yc=side*(side===1?18.2:17.2),x0=54.7,x1=56.5,y0=yc-1.35,y1=yc+1.35,z0=side===1?18.9:20.1,z1=25.9;
  const depth=(x,y,z)=>K*(x*sn+y*cs)+z;
  const arm=`M${P(50.2,side*12.4,26.9)}Q${P(51.6,side*16.1,28.7)} ${P(54.3,yc,27.9)}L${P(55.6,yc,25.2)}`;
  queue(depth(53,yc,27.1),`<g data-mirror="${side}"><path d="${arm}" fill="none" stroke="#11202a" stroke-width=".72" stroke-linecap="round" stroke-linejoin="round"/><path d="${arm}" fill="none" stroke="#8ba0aa" stroke-width=".16" stroke-linecap="round" opacity=".8"/></g>`);
  if(Math.abs(sn)>.0001){
   const front=sn>0,x=front?x1:x0,p=P(x,y0,z1),m=`matrix(${f(-sn)} ${f(cs)} 0 ${K} ${p[0]} ${p[1]})`;
   queue(depth(x,yc,(z0+z1)/2),`<g data-mirror="${side}" transform="${m}"><rect width="2.7" height="${f(z1-z0)}" rx=".48" fill="#0b1720" stroke="#344956" stroke-width=".12"/>${front?`<path d="M.5 .7Q1.4 .3 2.2 .7" fill="none" stroke="#7f949d" stroke-width=".15"/>`:`<rect x=".25" y=".35" width="2.2" height="${f(z1-z0-.7)}" rx=".3" fill="${url('mirrorGlass')}"/><path d="M.5 .65L1.8 .5 .8 ${f(z1-z0-1)}H.45Z" fill="#e3f2f4" opacity=".25"/>`}</g>`);
  }
  const ys=cs>0?y1:y0;
  queue(depth((x0+x1)/2,ys,(z0+z1)/2),`<g data-mirror="${side}">${poly([[x0,ys,z0],[x1,ys,z0],[x1,ys,z1],[x0,ys,z1]],'#182c38','#6f8792',.08)}</g>`);
  queue(depth((x0+x1)/2,yc,z1),`<g data-mirror="${side}">${poly([[x0,y0,z1],[x1,y0,z1],[x1,y1,z1],[x0,y1,z1]],'#354e5b','#7c939c',.08)}</g>`);
 }
 surfaces.sort((a,b)=>a.depth-b.depth);
 const shadow=poly([[-60,-12,0],[60,-12,0],[60,12,0],[-60,12,0]],'#071b27');
 let groundLight='',flares='';
 if(night){
  const gm=`matrix(${f(cs)} ${f(sn)} ${f(-sn)} ${f(cs)} 0 0)`;
  groundLight=`<g data-light-beams="true" transform="${gm}" filter="${url('beamSoft')}">`;
  for(const side of [-1,1]){const y=side*9.05;groundLight+=`<path d="M59.8 ${y-1.3}Q71 ${y-3} 82 ${y-7.5}L82 ${y+7.5}Q71 ${y+3} 59.8 ${y+1.3}Z" fill="${url('beam')}"/><ellipse cx="-61" cy="${side*10}" rx="3.4" ry="4" fill="${url('redGlow')}" opacity=".28"/>`;}
  for(const x of [2.4,43.2])groundLight+=`<ellipse data-step-light="true" cx="${x}" cy="15.5" rx="6" ry="4.5" fill="${url('amberGlow')}" opacity=".24"/>`;
  groundLight+='</g>';
  const flare=(x,y,z,type,r,core)=>{const p=P(x,y,z);return `<g data-lamp="${type}"><circle cx="${p[0]}" cy="${p[1]}" r="${r}" fill="${url(type+'Glow')}"/><circle cx="${p[0]}" cy="${p[1]}" r="${core}" fill="${type==='red'?'#ff9a7d':type==='amber'?'#ffe7a2':'#fffff0'}"/></g>`;};
  for(const side of [-1,1]){
   const y=side*9.05,z=6.575,x=noseX(y,z),d=(noseX(y+.01,z)-noseX(y-.01,z))/.02;
   if(K*(sn-d*cs)+.035>0)flares+=flare(x,y,z,'white',3.6,.42);
   if(sn<-.01)flares+=flare(tailX(side*10.35,16.4),side*10.35,16.4,'red',2.9,.3);
   if(side*cs>.01)for(const x of [-55.2,-29.8,23.4,53.3])flares+=flare(x,side*12.78,4.55,'amber',1.05,.13);
  }
 }
 const extraDefs=`<defs>${frontPaint}${rearPaint}${frontClips.join('')}<clipPath id="${id}roofClip"><polygon points="${pts(roofBoundary)}"/></clipPath></defs>`;
 const svg=`<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="-85 -90 170 170" width="1000" height="1000" role="img" aria-label="אוטובוס עירוני משופר, ${escape(brand.name)}, זווית ${f(angle)} מעלות, קו ${line}" data-angle="${f(angle)}" data-mode="${mode}" data-brand="${brandKey}" data-night="${night}"><title>אוטובוס העיר — ${escape(brand.name)} — ${f(angle)}°</title><desc>מודל וקטורי אחד בכל 16 הזוויות. מעטפת 120×25.5, צירי גלגלים ‎−39.6 ו־36, חזית מעוגלת ושמשה נטויה. ${wrapped?'עטיפה מלאה עם שכבה שקופה על הזכוכית והדלתות.':''}${night?' פנסים דולקים, אלומות אור ותא נוסעים מואר.':''}</desc>${defs}${extraDefs}${groundLight}<g opacity="${night?'.34':'.13'}" transform="translate(2 2)">${shadow}</g>${surfaces.map(s=>s.svg).join('')}<g data-roof="true">${roof.join('')}</g>${flares}</svg>`;
 return svg;
}
function led(x,y,w,h,line,destination,id,night,text){
 const dot=[];for(let a=x+5;a<x+w-3;a+=5)for(let b=y+5;b<y+h-3;b+=5)dot.push(`<circle cx="${a}" cy="${b}" r=".65" fill="#d9a53a" opacity=".14"/>`);
 return `<g><rect x="${x-2}" y="${y-2}" width="${w+4}" height="${h+4}" rx="5" fill="#5b7278"/><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="4" fill="#101c1c"/>${dot.join('')}<g ${night?`filter="url(#${id}lightGlow)"`:''}>${text(x+w-19,y+h*.75,line,h*.72,night?'#ffe693':'#efbd53')}${destination?text(x+w*.43,y+h*.71,destination,h*.43,night?'#ffe693':'#efbd53'):''}</g></g>`;
}
function produce(id){
 const u=n=>'url(#'+id+n+')';let a=`<g><ellipse cx="110" cy="311" rx="166" ry="20" fill="#05250e" opacity=".45"/><path d="M70 63L85 20 143 14 162 51 150 194 69 190Z" fill="#e9f1df" stroke="#a4b7af" stroke-width="2"/><path d="M85 20L107 42 162 51 143 14Z" fill="#c2d5e0"/><path d="M107 42v127l43 25 12-143Z" fill="#9fc0d3"/><path d="M78 72h26v61H75Z" fill="#12735b"/><path d="M103 21l23-4 2 12-20 4Z" fill="#e4a447"/>`;
 for(let i=0;i<7;i++){let x=156+i*10;a+=`<path d="M${x} 214Q${x-34} 80 ${x+14} ${54+i*8}Q${x+48} 160 ${x+12} 236Z" fill="${u('leaf')}" stroke="#c0d955" stroke-width="1.2"/><path d="M${x+5} 201L${x+15} ${72+i*8}" stroke="#e1ed85" stroke-width="1.5" opacity=".8"/>`;}
 a+=`<path d="M13 215C-24 168-2 131 36 146C58 130 84 148 82 180C104 208 84 252 50 250C31 264 7 248 13 215Z" fill="${u('pepper')}"/><path d="M35 146Q23 123 43 108L51 113Q32 127 45 149" fill="#3b7423"/>`;
 for(const [x,y,r] of [[86,238,51],[172,263,42],[-2,274,35]])a+=`<circle cx="${x}" cy="${y}" r="${r}" fill="${u('tomato')}"/><path d="M${x-18} ${y-r+9}l14 2 7-14 3 14 17 1-15 6 5 10-12-7-11 8 3-12Z" fill="#367c25"/><ellipse cx="${x-r*.3}" cy="${y-r*.35}" rx="${r*.17}" ry="${r*.07}" fill="#ffe6ae" opacity=".35"/>`;
 a+=`<path d="M229 273C218 174 211 116 237 101C261 117 267 175 268 258C257 296 238 310 229 273Z" fill="${u('leaf')}"/><path d="M240 119Q228 206 247 281" fill="none" stroke="#8fbd53" stroke-width="3"/>`;
 for(let i=0;i<20;i++){const x=206+(i%5)*8,y=263+Math.floor(i/5)*10;a+=`<circle cx="${x}" cy="${y}" r="8" fill="${['#4e315c','#70406a','#8b5582','#4a3151'][i%4]}"/><circle cx="${x-2}" cy="${y-2}" r="1.7" fill="#b48da1"/>`;}
 return a+'</g>';
}
function updateDoor(host,value){const n=clamp(+value||0,0,1);for(const leaf of host.querySelectorAll('[data-door-leaf]'))leaf.setAttribute('transform',`translate(${f(+leaf.dataset.doorLeaf*n*+leaf.dataset.doorTravel)} 0)`);}
window.TurboBus={renderSvg,updateDoor,info:{length:L,width:W,height:H,top:TOP,projectionK:K,wheels:[{u:-39.6,r:5.1,hw:12.65},{u:36,r:5.1,hw:12.65}],source:'S7F282 · LV-BS-01 / C34',approvedSource:'Turbo_City_Set1_Code_Proof (1).html · all 4 approved logos',brands:Object.keys(BRANDS),roundedNose:true,roundedTail:true,mirrors:2,sideAdSize:{width:560,height:176},nightLighting:true,vectorOnly:true}};
})();
