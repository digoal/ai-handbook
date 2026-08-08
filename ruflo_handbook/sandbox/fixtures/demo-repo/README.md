# demo-repo

最小演示项目，用于 ruflo 手册的沙箱 hands-on 验证。

## 结构

```
demo-repo/
├── package.json
├── src/
│   ├── greet.js        # 简单函数，演示 codemod 改 var → const
│   ├── greet.test.js   # 单元测试
│   ├── math.js         # 含 var / let 混用
│   └── api.js          # REST 风格 API（用于演示多文件重构）
└── README.md
```

## 用途

- 章节 02：验证 `ruflo init` 在此目录下正常工作
- 章节 03：演示 hooks 自动接管 Claude Code 行为
- 章节 04：触发 codemod（`var` → `const`）路径
- 章节 06：多 agent 并行重构 `math.js` 与 `api.js`
- 章节 07：记忆 store/search 跨项目验证
- 章节 14：场景剧本的目标项目

## 故意引入的"问题"

- `src/greet.js` 中有 `console.log`（演示 codemod `remove-console`）
- `src/math.js` 中有 `var` 声明（演示 codemod `var-to-const`）
- `src/api.js` 中无单元测试（演示 testgen 自动生成）