// src/greet.js
// 演示用途：含 var / console.log，方便 codemod 演示
var GREETING = 'Hello';
console.log(GREETING);

export function greet(name) {
  return `${GREETING}, ${name}!`;
}

export const VERSION = '1.0.0';