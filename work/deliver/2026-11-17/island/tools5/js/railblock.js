 const PIER_BOX=SPAN.piers.map(([a,b])=>[a-2,PY[0]-NOSE,b+2,PY[1]+NOSE+WATER]);
 function railBlock(px,py){if(!w3IsSea(px,py))return null;
  for(const r of PIER_BOX)if(px>r[0]&&px<r[2]&&py>r[1]&&py<r[3])return 'עמוד הגשר של מעבר השיט';
  for(const {P} of WALL_P)if(polyD(px,py,P)<7)return 'קיר ההנחיה של מעבר השיט';
  for(const d of DOLPH)if(Math.hypot(px-d.x,py-d.y)<14)return 'הדולפין של מעבר השיט';
  if(py>YN-6&&py<YS+6&&px>6230&&!(px>CH.x0&&px<CH.x1))return 'גשר המסילות — עוברים רק במעבר השיט';
  for(const id of['ISL-ARC','ISL-BR']){const g=RAIL_SEG_BY_ID[id];if(!g)continue;const b=rlBBox(g);if(px<b.x0-40||px>b.x1+40||py<b.y0-40||py>b.y1+40)continue;if(id==='ISL-BR'&&py>ISL_OPEN.y0+8&&py<ISL_OPEN.y1-8)continue;if(polyD(px,py,g.pts)<36)return 'גשר מסילת האי'}
  return null}
