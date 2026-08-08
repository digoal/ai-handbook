# 3.3 编码规范

> **一句话**：seekdb 的规范比大多数 C++ 项目严格得多——禁 STL、禁异常、
> 禁智能指针、禁 `auto`、单入单出。而且新代码开始去掉 `Ob` 前缀了。

---

## 命名

### 传统约定

| 对象 | 规则 | 例子 |
|---|---|---|
| 类 | `Ob` + 大驼峰 | `ObSelectResolver` |
| 文件 | `ob_` + 小写下划线 | `ob_select_resolver.cpp` |
| 函数 / 变量 | 小写下划线 | `resolve_approx_clause` |
| 成员变量 | 小写下划线 + **尾下划线** | `snapshot_version_` |
| 宏 / 常量 | 全大写 | `OB_SUCCESS` |

头文件与实现一一对应：`src/<dir>/foo.h` ↔ `src/<dir>/foo.cpp`，
单元测试目录镜像 `src/`。

### ⚠️ 新规：新类不要加 `Ob` 前缀

仓库根目录的 `AGENTS.md` 给出了新约定：

> - New C++ classes, including interface classes, do not need the legacy `Ob` prefix.
> - Keep the `I` prefix for interface classes. For example, use `ICacheMemoryGetter`
>   instead of `ObICacheMemoryGetter`.
> - Do not rename existing types only to remove the `Ob` prefix unless the task
>   explicitly requires it.

翻译成实操：

| 情况 | 怎么做 |
|---|---|
| 写新类 | **不加** `Ob` 前缀 |
| 写新接口类 | 用 `I` 前缀，如 `ICacheMemoryGetter` |
| 改老代码 | **不要**为了去前缀而重命名 |

这条规则很新，代码库里绝大多数还是 `Ob` 开头。
两种风格会共存很长一段时间。

---

## 禁用清单

`docs/developer-guide/en/coding-convention.md` 明确禁止：

| 禁用 | 替代 | 原因 |
|---|---|---|
| **STL 容器** | `ObSEArray` / `ObHashMap` 等 | STL 分配不受 `ObMemAttr` 管控 |
| **C++ 异常** | 返回 `int` 错误码 | 性能与可控性 |
| **智能指针** | 手动管理 + `ObArenaAllocator` | 同上 |
| **`auto`** | 显式写类型 | 可读性 |
| **移动语义** | — | 规范制定时代较早 |
| **range-based for** | 传统 for 循环 | 同上 |
| **lambda** | 具名函数 / 函数对象 | 同上 |

> 💡 这份约定的基线可以追溯到 2018 年前后，风格相当保守。
> 而 `CMakeLists.txt` 里已经是 **C++20** 了——
> 你会在代码里看到新旧风格并存。**改老文件时跟随该文件的风格**，
> 这是《CLAUDE.md》里"match existing style"的实践。

---

## 控制流：单入单出

所有函数只有一个 `return`，在函数末尾。中间用 else-if 链串起来：

```cpp
int ObFoo::bar(const ObString &input, int64_t &out)
{
  int ret = OB_SUCCESS;
  ObArenaAllocator allocator;
  SomeType *obj = nullptr;

  if (OB_UNLIKELY(input.empty())) {
    ret = OB_INVALID_ARGUMENT;
    LOG_WARN("input is empty", K(ret));
  } else if (OB_ISNULL(obj = create_obj(allocator))) {
    ret = OB_ALLOCATE_MEMORY_FAILED;
    LOG_WARN("failed to create obj", K(ret));
  } else if (OB_FAIL(obj->init(input))) {
    LOG_WARN("failed to init", K(ret), K(input));
  } else if (OB_FAIL(obj->compute(out))) {
    LOG_WARN("failed to compute", K(ret));
  }

  return ret;
}
```

要在链中间执行一个无返回值的语句，用 `FALSE_IT`：

```cpp
} else if (FALSE_IT(x = compute_something())) {
  // 永远不会进来，只是为了执行赋值
} else if (OB_FAIL(next_step(x))) {
```

看着别扭，但一致性很高——读多了就习惯了。

---

## 错误日志的惯例

失败分支**必须**打日志，且带上 `K(ret)`：

```cpp
} else if (OB_FAIL(do_something())) {
  LOG_WARN("failed to do something", K(ret), K(relevant_var));
}
```

- 内部诊断用 `LOG_WARN`
- 要返回给客户端的错误用 `LOG_USER_ERROR`
- 把有助于定位的变量都 `K()` 进去

一个真实例子（`src/sql/engine/expr/ob_expr_ai/ob_expr_ai_embed.cpp`）：

```cpp
} else if (arg_model_id->is_null() || arg_content->is_null()) {
  ret = OB_INVALID_ARGUMENT;
  LOG_WARN("model id or content is null", K(ret));
  LOG_USER_ERROR(OB_INVALID_ARGUMENT, "ai_embed, model id or content is null");
  res.set_null();
}
```

注意它同时打了内部日志和用户错误——这是标准做法。

---

## 版权头

每个文件必须有 Apache 2.0 头（`coding-standard.md` 强制）：

```cpp
/*
 * Copyright (c) 2025 OceanBase.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
```

---

## 模块分层是硬约束

除了代码风格，还有一条**机器强制**的规范：模块只能依赖同层或更低层。

```
lib(0) → common/rpc/grpc(1) → share(2)
       → sql/storage/logservice/objit(3) → pl/libtable(4) → observer/rootserver(5)
```

违反会导致构建失败（`cmake/module_check/`）。
加新文件时先想清楚它属于哪一层。

详见 [0.3 代码地图](../00-orientation/03-code-map.md)。

---

## 常用宏速查

| 宏 | 用途 |
|---|---|
| `OB_SUCC(e)` / `OB_FAIL(e)` | 执行并判断 |
| `OB_ISNULL(p)` / `OB_NOT_NULL(p)` | 空指针 |
| `OB_UNLIKELY(c)` / `OB_LIKELY(c)` | 分支预测 |
| `FALSE_IT(e)` | else-if 链中执行语句 |
| `UNUSED(x)` | 标记未使用参数 |
| `K(x)` / `KP(p)` / `KPC(p)` | 日志打印 |
| `TO_STRING_KV(...)` | 让类支持 `K()` |
| `DISALLOW_COPY_AND_ASSIGN(T)` | 禁拷贝 |
| `OB_UNIS_VERSION(n)` | 序列化版本 |
| `INIT_SUCC(ret)` | `int ret = OB_SUCCESS` 的简写 |

---

## 贡献流程

`CONTRIBUTING.md` 与 `docs/developer-guide/en/contributing.md`：

1. 新功能**先写设计文档**（放 `docs/design/`）
2. Fork → 建分支 → 改代码
3. 保证 unittest / mysqltest 通过
4. 提 PR，走 CI（编译 + 4 路分片 mysqltest + CodeQL）
5. Review

---

## 代码锚点

| 文件 | 职责 |
|---|---|
| `AGENTS.md` | **新类去 `Ob` 前缀的新规** |
| `docs/developer-guide/en/coding-convention.md` | 命名、禁用清单、控制流 |
| `docs/developer-guide/en/coding-standard.md` | 正式规范 v1.0（2025-11-07） |
| `docs/developer-guide/en/container.md` | 容器与 `ObString` 语义 |
| `CONTRIBUTING.md` | 贡献流程 |
| `cmake/module_check/module_layers.conf` | 分层硬约束 |
| `deps/oblib/src/lib/ob_define.h` / `src/share/ob_define.h` | 宏定义 |

---

## 动手验证

看新规原文：

```bash
cat AGENTS.md
```

看禁用清单：

```bash
grep -niE "stl|exception|smart pointer|auto|lambda" docs/developer-guide/en/coding-convention.md | head
```

找一个标准 else-if 链范例：

```bash
sed -n '78,152p' src/sql/engine/expr/ob_expr_ai/ob_expr_ai_embed.cpp
```

统计代码库里还有多少 `Ob` 前缀的类（感受一下存量）：

```bash
grep -rho "class Ob[A-Za-z]*" src/ | sort -u | wc -l
```

---

## 延伸阅读

- 下一章：[3.4 调试武器库](04-debugging.md)
- [3.2 oblib 基础设施](02-oblib.md) —— 那些替代 STL 的容器
- [3.6 实战一：新增 SQL 函数](06-hands-on-sql-function.md) —— 把规范用起来
