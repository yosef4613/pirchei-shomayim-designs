import './dom.js';
import '../../src/app/main.js';
setTimeout(() => console.log('TD', JSON.stringify(globalThis.__TD && globalThis.__TD())), 200);
