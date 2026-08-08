// src/greet.test.js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { greet, VERSION } from './greet.js';

test('greet returns greeting with name', () => {
  assert.equal(greet('world'), 'Hello, world!');
});

test('VERSION is set', () => {
  assert.equal(typeof VERSION, 'string');
});