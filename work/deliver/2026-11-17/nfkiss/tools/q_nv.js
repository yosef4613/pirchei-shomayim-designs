return (async()=>{const S=ms=>new Promise(r=>setTimeout(r,ms)),o={};
 await S(3000);
 try{
  o.dec=typeof tcNv64;o.logo={data:!!window.TCLOGO_DATA,z:window.TCLOGO_Z===null?'consumed':typeof window.TCLOGO_Z};
  const D=TCVREC.D,ent=[];for(const t in D.lines)for(const v in D.lines[t]){const r=D.lines[t][v];if(r&&typeof r[1]==='string')ent.push([t.slice(0,24),v,r[0],r[1]])}
  o.total=ent.length;o.enc=ent.filter(e=>e[3].charCodeAt(0)===94||e[3].charCodeAt(0)===126).length;o.hex=ent.filter(e=>e[3].charCodeAt(0)===126).length;o.plain=ent.length-o.enc;
  const vow=ent.filter(e=>e[3].charCodeAt(0)===94&&/[aeiouxyAEIOUXY]/.test(e[3])).length;o.vowelsInEncoded=vow;
  const ac=new OfflineAudioContext(1,48000,48000);let ok=0,bad=[],durErr=0,maxDiff=0;
  for(const e of ent){try{const b64=tcNv64(e[3]),bin=atob(b64),u=new Uint8Array(bin.length);for(let i=0;i<bin.length;i++)u[i]=bin.charCodeAt(i);
    const buf=await ac.decodeAudioData(u.buffer);const d=Math.abs(buf.duration-e[2]);maxDiff=Math.max(maxDiff,d);if(d>0.6)durErr++;ok++}catch(er){bad.push(e[0]+'|'+e[1]+': '+String(er).slice(0,60))}}
  o.decoded=ok;o.failed=bad.length;o.bad=bad.slice(0,5);o.durOff=durErr;o.maxDurDiff=+maxDiff.toFixed(2);
  try{o.brands={n:Object.keys(TC_BRANDS).length};const c=document.createElement('canvas');c.width=200;c.height=120;const g=c.getContext('2d');let drawn=0,berr=[];
   for(const k in TC_BRANDS){const P=TC_BRANDS[k].parts||{};for(const pk in P){try{TCB.draw(g,P[pk],0,0,200,120);drawn++}catch(er){berr.push(k+'.'+pk+': '+String(er).slice(0,60))}}}
   const px=g.getImageData(0,0,200,120).data;let nz=0;for(let i=3;i<px.length;i+=4)if(px[i])nz++;o.brands.drawn=drawn;o.brands.err=berr.slice(0,5);o.brands.nonEmptyPx=nz}catch(er){o.brandsExc=String(er).slice(0,200)}
  o.ok=o.dec==='function'&&o.failed===0&&o.plain===0&&o.vowelsInEncoded===0&&o.logo.data&&o.brands&&o.brands.err.length===0;
 }catch(e){o.exc=String(e&&e.stack||e).slice(0,600)}
 return o})()
