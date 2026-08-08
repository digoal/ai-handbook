// src/api.js
// 演示用途：多函数、无测试，方便 testgen 与多 agent 协作
var routes = {};

export function register(path, handler) {
  routes[path] = handler;
}

export async function handle(method, path, body) {
  var handler = routes[path];
  if (!handler) return { status: 404, body: { error: 'not found' } };
  return handler({ method, path, body });
}

export function list() {
  return Object.keys(routes);
}