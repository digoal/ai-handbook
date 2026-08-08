// src/math.js
// 演示用途：var / let 混用，方便 codemod 改写
var PI = 3.14159;

export function circleArea(r) {
  let r2 = r * r;
  return PI * r2;
}

export function circumference(r) {
  return 2 * PI * r;
}