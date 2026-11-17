export * from '../nm/node_modules/three/build/three.module.js';
import * as T from '../nm/node_modules/three/build/three.module.js';
export class WebGLRenderer { constructor() { this.shadowMap = {}; this.info = { render: { calls: 1, triangles: 1 }, memory: { geometries: 1, textures: 1 } } } setPixelRatio() {} setSize() {} render(s, c) { s.updateMatrixWorld(); c.updateMatrixWorld() } }
export class PMREMGenerator { fromScene() { return { texture: new T.Texture() } } }
