function greet(name) {
  return `hello, ${name}!`;
}

function farewell(name) {
  return `bye, ${name}`;
}

function main() {
  console.log(greet('codegraph'));
  console.log(farewell('reader'));
}

module.exports = { greet, farewell, main };
