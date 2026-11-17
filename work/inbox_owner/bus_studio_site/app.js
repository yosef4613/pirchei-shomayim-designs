'use strict';
(() => {
  const $ = id => document.getElementById(id);
  const ANGLES = Array.from({length:16},(_,index)=>index*22.5);
  const BRAND_NAMES={shibolet:'שיבולת',coffee:'קפה טורבו',fishing:'קרס וחכה',mall:'קניון טורבו'};
  const MODE_LABELS = {none:'רגיל',side:'מודעת צד',rear:'מודעה אחורית',wrap:'עטיפה מלאה'};
  const state = {angle:22.5,line:3,adMode:'side',door:0,night:false,brand:'shibolet',glassOpacity:.5,zoom:150,detailOpen:false,panX:.5,panY:.5};
  const galleryNodes=[];
  const zoomViews=[];
  const suppressScrollUntil=new WeakMap();
  let resizeFrame=0;
  let currentSvg='',toastTimer,galleryTimer,animationFrame=0,animationStarted=0,lastAnimationPaint=0,animating=false;
  const options=angle=>({...state,angle:angle==null?state.angle:angle});
  const angleLabel=angle=>`${Number(angle).toLocaleString('en-US',{maximumFractionDigits:1})}°`;
  const doorLabel=value=>value<=.01?'דלתות סגורות':value>=.99?'דלתות פתוחות':`דלתות פתוחות ${Math.round(value*100)}%`;
  function announce(text){$('studioAnnouncement').textContent=text;}
  function toast(text){clearTimeout(toastTimer);$('toast').textContent=text;$('toast').hidden=false;toastTimer=setTimeout(()=>{$('toast').hidden=true;},2600);}
  function setPressed(selector,key,value){document.querySelectorAll(selector).forEach(button=>button.setAttribute('aria-pressed',String(button.dataset[key]===String(value))));}
  function makeSvg(opt){if(!window.TurboBus||typeof window.TurboBus.renderSvg!=='function')return '';const markup=window.TurboBus.renderSvg(opt);return typeof markup==='string'&&markup.includes('<svg')?markup:'';}
  function drawOriginal(canvas,opt){if(!window.OriginalBus||typeof window.OriginalBus.draw!=='function')return false;try{window.OriginalBus.draw(canvas,opt);return true;}catch(error){console.error('Original bus preview:',error);return false;}}
  const brandName=()=>window.TurboBusBrands?.[state.brand]?.name||BRAND_NAMES[state.brand]||'שיבולת';
  function logoSvg(brand){
    if(!brand||typeof brand.logo!=='string'||!brand.logo.trim())return '';
    const content=brand.logo.trim();
    if(/^<svg\b/i.test(content))return content;
    const rawViewBox=Array.isArray(brand.logoViewBox)?brand.logoViewBox.join(' '):String(brand.logoViewBox||'0 0 316 211');
    const viewBox=/^[\d.\s,+-]+$/.test(rawViewBox)?rawViewBox:'0 0 316 211';
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${viewBox}" preserveAspectRatio="xMidYMid meet" aria-hidden="true">${content}</svg>`;
  }
  function renderBrandIdentity(){
    const all=window.TurboBusBrands||{},brand=all[state.brand]||{};
    $('selectedBrandName').textContent=brandName();
    $('selectedBrandTagline').textContent=brand.tagline||({shibolet:'סופרמרקט עירוני',coffee:'הקפה של העיר',fishing:'כל מה שצריך לדייג',mall:'כל העיר תחת גג אחד'}[state.brand]);
    const host=$('selectedBrandLogo');host.setAttribute('aria-label',`לוגו ${brandName()}`);
    const selectedLogo=logoSvg(brand);if(selectedLogo)host.innerHTML=selectedLogo;else host.textContent=brandName();
    document.querySelectorAll('.brand-option[data-brand]').forEach(button=>{const item=all[button.dataset.brand],swatch=button.querySelector('.brand-swatch'),markup=logoSvg(item);if(markup){swatch.innerHTML=markup;swatch.classList.add('has-logo');swatch.setAttribute('aria-hidden','true');}});
    const palette=Array.isArray(brand.palette)?brand.palette:Object.values(brand.palette||{}),colors=palette.map(v=>typeof v==='string'?v:v?.hex||v?.color).filter(v=>typeof v==='string'&&/^#[0-9a-f]{3,8}$/i.test(v)).slice(0,5);
    $('selectedBrandPalette').replaceChildren(...colors.map(color=>{const span=document.createElement('span');span.style.backgroundColor=color;span.title=color;span.setAttribute('aria-label',color);return span;}));
  }
  function syncZoomControls(){
    $('zoomSlider').value=state.zoom;$('zoomSlider').setAttribute('aria-valuetext',`${state.zoom} אחוזים`);$('zoomValue').textContent=`${state.zoom}%`;$('detailZoomValue').textContent=`${state.zoom}%`;
    document.querySelectorAll('[data-zoom-action]').forEach(button=>{button.disabled=button.dataset.zoomAction==='out'?state.zoom<=100:button.dataset.zoomAction==='in'?state.zoom>=400:false;});
    $('expandDetail').setAttribute('aria-expanded',String(state.detailOpen));
  }
  function placePan(view){
    const maxX=Math.max(0,view.viewport.scrollWidth-view.viewport.clientWidth),maxY=Math.max(0,view.viewport.scrollHeight-view.viewport.clientHeight);
    suppressScrollUntil.set(view.viewport,performance.now()+90);view.viewport.scrollLeft=maxX*state.panX;view.viewport.scrollTop=maxY*state.panY;
  }
  function syncPan(view){
    if(performance.now()<(suppressScrollUntil.get(view.viewport)||0))return;
    const maxX=view.viewport.scrollWidth-view.viewport.clientWidth,maxY=view.viewport.scrollHeight-view.viewport.clientHeight;
    if(maxX>1)state.panX=Math.max(0,Math.min(1,view.viewport.scrollLeft/maxX));
    if(maxY>1)state.panY=Math.max(0,Math.min(1,view.viewport.scrollTop/maxY));
    zoomViews.forEach(other=>{if(other!==view&&other.viewport.clientWidth>0)placePan(other);});
  }
  function updateZoomLayout(redraw=false){
    zoomViews.forEach(view=>{
      const width=view.viewport.clientWidth,height=view.viewport.clientHeight;if(!width||!height)return;
      const w=width*state.zoom/100,h=height*state.zoom/100;view.surface.style.width=`${w}px`;view.surface.style.height=`${h}px`;view.viewport.classList.toggle('is-zoomed',state.zoom>100);
      if(view.canvas){const ratio=Math.min(window.devicePixelRatio||1,2,4096/w,4096/h),cw=Math.max(1,Math.round(w*ratio)),ch=Math.max(1,Math.round(h*ratio));if(view.canvas.width!==cw||view.canvas.height!==ch){view.canvas.width=cw;view.canvas.height=ch;}}
      placePan(view);
    });
    if(redraw)drawOriginal($('originalCanvas'),{...options(),res:state.zoom>=150?6:4});
  }
  function setZoom(value,center=false){
    state.zoom=Math.max(100,Math.min(400,Math.round(Number(value)/5)*5));if(center){state.panX=.5;state.panY=.5;}syncZoomControls();updateZoomLayout(true);announce(`הגדלה ${state.zoom} אחוזים`);
  }
  function renderDetail(){
    if(!state.detailOpen)return;
    const host=$('detailBus');host.innerHTML=makeSvg(options());host.setAttribute('aria-label',`תצוגת פרטים — ${brandName()}, קו ${state.line}, זווית ${angleLabel(state.angle)}`);
    $('detailSummary').textContent=`קו ${state.line} · ${brandName()} · ${MODE_LABELS[state.adMode]}`;$('detailViewer').classList.toggle('is-night',state.night);updateZoomLayout(false);
  }
  function toggleDetail(open){
    state.detailOpen=!!open;$('detailViewer').hidden=!state.detailOpen;syncZoomControls();
    if(state.detailOpen){renderDetail();$('detailViewer').scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth',block:'start'});$('detailTitle').focus({preventScroll:true});}
    else $('expandDetail').focus({preventScroll:true});
  }
  function initZoom(){
    [['originalViewport','originalSurface','originalCanvas'],['newViewport','newSurface'],['detailViewport','detailSurface']].forEach(([viewportId,surfaceId,canvasId])=>{
      const view={viewport:$(viewportId),surface:$(surfaceId),canvas:canvasId?$(canvasId):null};zoomViews.push(view);let drag=null;
      view.viewport.addEventListener('scroll',()=>syncPan(view),{passive:true});
      view.viewport.addEventListener('pointerdown',event=>{if(state.zoom<=100||event.button!==0||event.pointerType==='touch')return;suppressScrollUntil.set(view.viewport,0);drag={x:event.clientX,y:event.clientY,left:view.viewport.scrollLeft,top:view.viewport.scrollTop};view.viewport.classList.add('is-dragging');view.viewport.setPointerCapture(event.pointerId);event.preventDefault();});
      view.viewport.addEventListener('pointermove',event=>{if(!drag)return;view.viewport.scrollLeft=drag.left-(event.clientX-drag.x);view.viewport.scrollTop=drag.top-(event.clientY-drag.y);suppressScrollUntil.set(view.viewport,0);syncPan(view);event.preventDefault();});
      const end=()=>{drag=null;view.viewport.classList.remove('is-dragging');};view.viewport.addEventListener('pointerup',end);view.viewport.addEventListener('pointercancel',end);view.viewport.addEventListener('lostpointercapture',end);
      view.viewport.addEventListener('dblclick',()=>setZoom(100,true));
      view.viewport.addEventListener('keydown',event=>{if(event.key==='+'||event.key==='='){event.preventDefault();setZoom(state.zoom+25);}else if(event.key==='-'){event.preventDefault();setZoom(state.zoom-25);}else if(event.key==='0'){event.preventDefault();setZoom(100,true);}});
    });
    const resized=()=>{cancelAnimationFrame(resizeFrame);resizeFrame=requestAnimationFrame(()=>updateZoomLayout(true));};
    if(typeof ResizeObserver==='function'){const observer=new ResizeObserver(resized);zoomViews.forEach(view=>observer.observe(view.viewport));}else window.addEventListener('resize',resized);
  }
  function renderHero(){
    updateZoomLayout(false);
    const opt={...options(),res:state.zoom>=150?6:4},alt=`קו ${state.line}, זווית ${angleLabel(state.angle)}, ${MODE_LABELS[state.adMode]}, ${doorLabel(state.door)}`;
    $('originalCanvas').setAttribute('aria-label',`הדגם הקיים — ${alt}`);$('newBus').setAttribute('aria-label',`העיצוב החדש — ${alt}`);
    $('originalError').hidden=drawOriginal($('originalCanvas'),opt);
    try{currentSvg=makeSvg(opt);if(currentSvg)$('newBus').innerHTML=currentSvg;else $('newBus').replaceChildren();$('newError').hidden=!!currentSvg;}catch(error){currentSvg='';$('newBus').replaceChildren();$('newError').hidden=false;console.error('New bus preview:',error);}
    $('summaryLine').textContent=`קו ${state.line}`;$('summaryAngle').textContent=angleLabel(state.angle);$('summaryMode').textContent=MODE_LABELS[state.adMode];
    $('brandCaption').textContent=state.adMode==='none'?'העיצוב החדש · ללא פרסומת':`${brandName()} · ${MODE_LABELS[state.adMode]}`;
    $('downloadSvg').disabled=!currentSvg;$('downloadSvgBottom').disabled=!currentSvg;document.querySelector('.comparison-section').classList.toggle('is-night',state.night);renderDetail();
  }
  function renderDoorPose(){
    const opt=options();
    if(window.TurboBus&&typeof window.TurboBus.updateDoor==='function'&&$('newBus').querySelector('svg')){
      window.TurboBus.updateDoor($('newBus'),state.door);if(state.detailOpen)window.TurboBus.updateDoor($('detailBus'),state.door);
      const alt=`קו ${state.line}, זווית ${angleLabel(state.angle)}, ${MODE_LABELS[state.adMode]}, ${doorLabel(state.door)}`;
      $('originalCanvas').setAttribute('aria-label',`הדגם הקיים — ${alt}`);
      $('newBus').setAttribute('aria-label',`העיצוב החדש — ${alt}`);
    }else renderHero();
  }
  function syncControls(){
    setPressed('[data-brand]','brand',state.brand);document.querySelectorAll('.brand-option').forEach(button=>button.classList.toggle('is-selected',button.dataset.brand===state.brand));syncZoomControls();
    setPressed('[data-line]','line',state.line);setPressed('[data-ad]','ad',state.adMode);setPressed('[data-angle]','angle',state.angle);
    $('nightSwitch').checked=state.night;$('nightLabel').textContent=state.night?'תאורת לילה':'תאורת יום';
    $('doorSlider').value=Math.round(state.door*100);$('doorValue').textContent=`${Math.round(state.door*100)}%`;$('doorSlider').setAttribute('aria-valuetext',doorLabel(state.door));
    $('glassSlider').value=Math.round(state.glassOpacity*100);$('glassValue').textContent=`${Math.round(state.glassOpacity*100)}%`;$('glassSlider').setAttribute('aria-valuetext',`${Math.round(state.glassOpacity*100)} אחוזים`);
    const glassAd=state.adMode==='wrap'||state.adMode==='side';$('glassSlider').disabled=!glassAd;$('glassGroup').classList.toggle('is-active',glassAd);$('glassHint').textContent=glassAd?'פרסומת חצי שקופה על החלונות והדלתות':'זמין במודעת צד ובעטיפה מלאה';
    galleryNodes.forEach(({button,angle})=>{const selected=angle===state.angle;button.classList.toggle('is-selected',selected);button.setAttribute('aria-pressed',String(selected));});
  }
  function renderGallery(){clearTimeout(galleryTimer);galleryNodes.forEach(({angle,canvas,svg})=>{const opt=options(angle);drawOriginal(canvas,opt);try{svg.innerHTML=makeSvg(opt);}catch(error){svg.replaceChildren();console.error('Bus angle preview:',angle,error);}});$('galleryState').textContent=`קו ${state.line} · ${MODE_LABELS[state.adMode]} · ${doorLabel(state.door)}`;}
  function scheduleGallery(){clearTimeout(galleryTimer);galleryTimer=setTimeout(()=>{if(!animating)renderGallery();},180);}
  function renderAll(quiet=false){syncControls();renderBrandIdentity();renderHero();if(!animating)renderGallery();if(!quiet)announce(`קו ${state.line}, ${MODE_LABELS[state.adMode]}, זווית ${angleLabel(state.angle)}`);}
  function selectAngle(angle,scroll=false){state.angle=angle;syncControls();renderHero();announce(`נבחרה זווית ${angleLabel(angle)}`);if(scroll)$('comparison').scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth',block:'start'});}
  function stopAnimation(refreshGallery=true){animating=false;cancelAnimationFrame(animationFrame);animationFrame=0;$('animateDoors').setAttribute('aria-pressed','false');$('animationIcon').setAttribute('href','#i-play');$('animationLabel').textContent='הנפשה';if(refreshGallery)renderGallery();}
  function animate(now){
    if(!animating)return;if(!animationStarted)animationStarted=now;
    if(now-lastAnimationPaint>=1000/24){const cycle=((now-animationStarted)/4800)%1;if(cycle<.15)state.door=0;else if(cycle<.4){const t=(cycle-.15)/.25;state.door=t*t*(3-2*t);}else if(cycle<.65)state.door=1;else if(cycle<.9){const t=(cycle-.65)/.25;state.door=1-t*t*(3-2*t);}else state.door=0;$('doorSlider').value=Math.round(state.door*100);$('doorValue').textContent=`${Math.round(state.door*100)}%`;$('doorSlider').setAttribute('aria-valuetext',doorLabel(state.door));renderDoorPose();lastAnimationPaint=now;}
    animationFrame=requestAnimationFrame(animate);
  }
  function startAnimation(){clearTimeout(galleryTimer);animating=true;animationStarted=0;lastAnimationPaint=0;$('animateDoors').setAttribute('aria-pressed','true');$('animationIcon').setAttribute('href','#i-pause');$('animationLabel').textContent='עצירה';animationFrame=requestAnimationFrame(animate);}
  function downloadSvg(){try{currentSvg=makeSvg(options())||currentSvg;}catch(error){console.error('Export bus preview:',error);}if(!currentSvg){toast('העיצוב עדיין אינו זמין להורדה.');return;}const blob=new Blob([currentSvg],{type:'image/svg+xml;charset=utf-8'}),url=URL.createObjectURL(blob),link=document.createElement('a');link.href=url;link.download=`Turbo_City_Line_${state.line}_${state.adMode}_${String(state.angle).replace('.','_')}deg.svg`;document.body.append(link);link.click();link.remove();setTimeout(()=>URL.revokeObjectURL(url),1500);}
  function makeGallery(){
    const anglesFragment=document.createDocumentFragment(),galleryFragment=document.createDocumentFragment();
    ANGLES.forEach((angle,index)=>{
      const angleButton=document.createElement('button');angleButton.type='button';angleButton.dataset.angle=angle;angleButton.textContent=angleLabel(angle);angleButton.setAttribute('aria-label',`זווית ${angleLabel(angle)}`);angleButton.setAttribute('aria-pressed',String(angle===state.angle));angleButton.addEventListener('click',()=>selectAngle(angle));anglesFragment.append(angleButton);
      const button=document.createElement('button');button.type='button';button.className='gallery-tile';button.setAttribute('aria-label',`הצגת השוואה בזווית ${angleLabel(angle)}`);button.setAttribute('aria-pressed',String(angle===state.angle));
      const head=document.createElement('span');head.className='gallery-tile-head';const label=document.createElement('strong');label.dir='ltr';label.textContent=angleLabel(angle);const number=document.createElement('span');number.textContent=String(index+1).padStart(2,'0');head.append(label,number);
      const pair=document.createElement('span');pair.className='gallery-pair';const before=document.createElement('span');before.className='gallery-shot gallery-before';const beforeLabel=document.createElement('span');beforeLabel.className='gallery-shot-label';beforeLabel.textContent='לפני';
      const canvas=document.createElement('canvas');canvas.width=560;canvas.height=360;canvas.setAttribute('aria-hidden','true');before.append(canvas,beforeLabel);
      const after=document.createElement('span');after.className='gallery-shot gallery-after';const afterLabel=document.createElement('span');afterLabel.className='gallery-shot-label';afterLabel.textContent='אחרי';const svg=document.createElement('span');svg.className='gallery-svg';svg.setAttribute('aria-hidden','true');after.append(svg,afterLabel);pair.append(before,after);button.append(head,pair);button.addEventListener('click',()=>selectAngle(angle,true));galleryFragment.append(button);galleryNodes.push({angle,button,canvas,svg});
    });$('angleOptions').replaceChildren(anglesFragment);$('angleGallery').replaceChildren(galleryFragment);
  }
  $('lineOptions').addEventListener('click',event=>{const button=event.target.closest('[data-line]');if(!button)return;state.line=Number(button.dataset.line);renderAll();});
  $('adOptions').addEventListener('click',event=>{const button=event.target.closest('[data-ad]');if(!button)return;state.adMode=button.dataset.ad;renderAll();});
  $('nightSwitch').addEventListener('change',event=>{state.night=event.target.checked;renderAll();});
  $('doorSlider').addEventListener('input',event=>{if(animating)stopAnimation(false);state.door=Number(event.target.value)/100;syncControls();renderDoorPose();scheduleGallery();});
  $('doorSlider').addEventListener('change',()=>{if(!animating)renderGallery();announce(doorLabel(state.door));});
  $('glassSlider').addEventListener('input',event=>{state.glassOpacity=Number(event.target.value)/100;syncControls();renderHero();scheduleGallery();});
  $('glassSlider').addEventListener('change',()=>{if(!animating)renderGallery();});
  $('animateDoors').addEventListener('click',()=>animating?stopAnimation():startAnimation());$('downloadSvg').addEventListener('click',downloadSvg);$('downloadSvgBottom').addEventListener('click',downloadSvg);
  $('angleOptions').addEventListener('keydown',event=>{if(!['ArrowLeft','ArrowRight','Home','End'].includes(event.key))return;const buttons=[...$('angleOptions').querySelectorAll('button')],current=buttons.indexOf(document.activeElement);if(current<0)return;event.preventDefault();const next=event.key==='Home'?0:event.key==='End'?buttons.length-1:(current+(event.key==='ArrowRight'?1:-1)+buttons.length)%buttons.length;buttons[next].focus();buttons[next].click();});
  document.addEventListener('visibilitychange',()=>{if(document.hidden&&animating)stopAnimation();});
  document.querySelectorAll('.brand-option[data-brand]').forEach(button=>button.addEventListener('click',()=>{if(!Object.hasOwn(BRAND_NAMES,button.dataset.brand))return;state.brand=button.dataset.brand;renderAll();}));
  document.querySelectorAll('[data-zoom-action]').forEach(button=>button.addEventListener('click',()=>{const action=button.dataset.zoomAction;if(action==='fit')setZoom(100,true);else setZoom(state.zoom+(action==='in'?25:-25));}));
  $('zoomSlider').addEventListener('input',event=>setZoom(Number(event.target.value)));
  $('expandDetail').addEventListener('click',()=>toggleDetail(!state.detailOpen));$('closeDetail').addEventListener('click',()=>toggleDetail(false));
  document.addEventListener('keydown',event=>{if(event.key==='Escape'&&state.detailOpen)toggleDetail(false);});
  makeGallery();initZoom();renderAll(true);
  window.TurboBusStudio={getState:()=>({...state,animating}),setState:next=>{stopAnimation(false);if(Number.isFinite(next.angle))state.angle=((next.angle%360)+360)%360;if([1,2,3].includes(Number(next.line)))state.line=Number(next.line);if(Object.hasOwn(MODE_LABELS,next.adMode))state.adMode=next.adMode;if(Number.isFinite(next.door))state.door=Math.max(0,Math.min(1,next.door));if(typeof next.night==='boolean')state.night=next.night;if(Number.isFinite(next.glassOpacity))state.glassOpacity=Math.max(0,Math.min(1,next.glassOpacity));if(Object.hasOwn(BRAND_NAMES,next.brand))state.brand=next.brand;if(Number.isFinite(next.zoom))state.zoom=Math.max(100,Math.min(400,Math.round(next.zoom/5)*5));if(typeof next.detailOpen==='boolean'){state.detailOpen=next.detailOpen;$('detailViewer').hidden=!state.detailOpen;}renderAll(true);},renderAll:()=>renderAll(true),stopAnimation:()=>stopAnimation(),setZoom:zoom=>setZoom(zoom),toggleDetail,downloadSvg};
})();
