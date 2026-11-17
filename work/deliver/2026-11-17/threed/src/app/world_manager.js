// World Manager — שלד (התוכנית, סעיף 5): עיר = רשימת אזורים + מצייר; השחקן / הכסף / השמירה מחוץ לעיר, משותפים.
// באב־טיפוס יש עיר אחת ואזור אחד (B4). אזור נוסף = עוד קובץ נתונים מאותו מחולל (extract_zone) — בלי לגעת בקוד הציור.
export function makeWorldManager(shared) {
  const cities = new Map();      // id → { zones: Map(id → {data, bounds}), renderer: 'canvas34' | 'three', loaded: Set }
  let current = null;
  return {
    shared,                                        // { player, money, vehicles, missions, save } — משותף לכל הערים
    addCity(id, renderer) { cities.set(id, { id, renderer, zones: new Map(), loaded: new Set() }); return this },
    addZone(cityId, zoneId, data) { const z = data.zone_rect; cities.get(cityId).zones.set(zoneId, { id: zoneId, data, bounds: z }); return this },
    enter(cityId) { current = cities.get(cityId); return current },
    // אזורים שצריך בזיכרון סביב השחקן (3×3): טוענים את הקרובים, פורקים את הרחוקים
    streamAround(x, y, margin = 60, onLoad = () => {}, onUnload = () => {}) {
      if (!current) return;
      for (const z of current.zones.values()) { const [x0, y0, x1, y1] = z.bounds; const near = x > x0 - margin && x < x1 + margin && y > y0 - margin && y < y1 + margin;
        if (near && !current.loaded.has(z.id)) { current.loaded.add(z.id); onLoad(z) } else if (!near && current.loaded.has(z.id)) { current.loaded.delete(z.id); onUnload(z) } }
    },
    get city() { return current },
  };
}
