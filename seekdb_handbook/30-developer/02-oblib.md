# 3.2 oblib 基础设施：内存、容器、日志

> **一句话**：seekdb 不用 STL、不用智能指针、不用异常。
> 它有自己一整套 layer-0 基础设施，先看懂这套，才读得动上层代码。

---

## 为什么要先学这个

打开任意一个 seekdb 源文件，你会看到这样的代码：

```cpp
int ObSomething::do_work(const ObString &input)
{
  int ret = OB_SUCCESS;
  ObArenaAllocator allocator;
  ObSEArray<int64_t, 8> ids;
  if (OB_FAIL(prepare(input))) {
    LOG_WARN("failed to prepare", K(ret), K(input));
  } else if (OB_FAIL(ids.push_back(1))) {
    LOG_WARN("push back failed", K(ret));
  }
  return ret;
}
```

这里面**没有一样东西是标准 C++**：`int ret` 而非异常、
`ObSEArray` 而非 `std::vector`、`OB_FAIL` 而非 if 判断、
`K(ret)` 是个宏。不熟悉这套约定，读代码会寸步难行。

这些都在 layer 0：`deps/oblib/src/lib/`。

---

## 错误处理：返回码 + 单出口

**seekdb 不使用 C++ 异常。** 所有函数返回 `int` 错误码。

```cpp
#define OB_SUCC(statement)  (OB_LIKELY(OB_SUCCESS == (ret = (statement))))
#define OB_FAIL(statement)  (OB_UNLIKELY(OB_SUCCESS != (ret = (statement))))
```

标准写法是 **else-if 链**，保证单一出口：

```cpp
int ret = OB_SUCCESS;
if (OB_FAIL(step1())) {
  LOG_WARN("step1 failed", K(ret));
} else if (OB_FAIL(step2())) {
  LOG_WARN("step2 failed", K(ret));
} else if (OB_ISNULL(ptr)) {
  ret = OB_ERR_UNEXPECTED;
  LOG_WARN("null ptr", K(ret));
} else {
  // 正常逻辑
}
return ret;
```

常用宏：

| 宏 | 作用 |
|---|---|
| `OB_SUCC(expr)` | 执行并判断成功 |
| `OB_FAIL(expr)` | 执行并判断失败 |
| `OB_ISNULL(p)` | 空指针判断 |
| `OB_NOT_NULL(p)` | 非空判断 |
| `OB_UNLIKELY` / `OB_LIKELY` | 分支预测提示 |
| `FALSE_IT(expr)` | 在 else-if 链里执行无返回值语句 |

错误码定义在 `src/share/ob_errno.def`，用 perl 脚本生成头文件。

---

## 内存管理

这是 seekdb 最有特色的部分。核心思想：
**每一次分配都要说清楚"谁分配的、给谁用的"**。

### `ObMemAttr` 三元组

```cpp
void *ptr = ob_malloc(size, ObMemAttr(tenant_id, ctx_id, "MyLabel"));
```

| 字段 | 含义 |
|---|---|
| `tenant_id` | 租户 ID（seekdb 单租户，但机制保留） |
| `ctx_id` | 内存上下文 ID，用于分类统计 |
| `label` | 字符串标签，出现在内存诊断视图里 |

这三元组让 `__all_virtual_memory_info` 能精确报告
"哪个模块用了多少内存"——排查内存泄漏时极其有用。

### 分配器家族

| 分配器 | 位置 | 特点 |
|---|---|---|
| `ObArenaAllocator` | `lib/allocator/page_arena.h` | **最常用**。只分配不释放，析构时统一回收 |
| `ObMallocAllocator` | `lib/alloc/ob_malloc_allocator.cpp` | 全局主分配器 |
| `ObTenantCtxAllocator` | `lib/alloc/ob_ctx_allocator.cpp` | 按 ctx 隔离 |
| `ObFIFOAllocator` | `lib/allocator/ob_fifo_allocator.cpp` | FIFO 释放模式 |
| `ObConcurrentFIFOAllocator` | `lib/allocator/ob_concurrent_fifo_allocator.cpp` | 并发版 |
| `ObSliceAlloc` | `lib/allocator/ob_slice_alloc.h` | 定长切片 |
| `ObVSliceAlloc` | `lib/allocator/ob_vslice_alloc.h` | 变长切片 |

**`ObArenaAllocator` 是新手最该掌握的**：

```cpp
ObArenaAllocator allocator;          // 栈上
char *buf = (char *)allocator.alloc(1024);
// ... 用 buf ...
// 函数返回时 allocator 析构，内存一次性归还，不用手动 free
```

适合"一次请求内分配很多小块，请求结束一起释放"的场景——
这正好是 SQL 执行的模式。

### 常用宏

```cpp
OB_NEW(ObSomeClass, "Label", ctor_args...);   // 分配 + 构造
OB_DELETE(ObSomeClass, "Label", ptr);          // 析构 + 释放
```

### 诊断

`ObMemoryDump`（`lib/alloc/memory_dump.cpp`）是个单线程池，
周期性遍历所有 label 和 ctx，产出统计数据，
供 `__all_virtual_memory_info` 查询。

---

## 容器：禁用 STL

`docs/developer-guide/en/coding-convention.md` 明确规定
**禁止使用 STL 容器**。原因是 STL 的内存分配不受 `ObMemAttr` 体系管控，
无法做租户隔离和精细统计。

替代品在 `lib/container/` 和 `lib/hash/`：

| STL | seekdb 替代 | 说明 |
|---|---|---|
| `std::vector` | `ObArray<T>` | 堆分配数组 |
| `std::vector`（小尺寸） | **`ObSEArray<T, N>`** | 栈上预留 N 个元素，超了才上堆 |
| `std::vector`（性能敏感） | `ObFastArray<T, N>` | 更激进的优化 |
| `std::unordered_map` | `ObHashMap<K, V>` | |
| `std::unordered_set` | `ObHashSet<K>` | |
| `std::string` | **`ObString`** | ⚠️ 见下 |
| `std::list` | `ObDList` / `ObList` | |
| `std::priority_queue` | `ObHeap` | |
| `std::bitset` | `ObBitmap` / `ObBitSet` | |

### `ObSEArray` 是主力

```cpp
ObSEArray<int64_t, 8> ids;    // 前 8 个元素在栈上，第 9 个开始走堆
ids.push_back(42);
```

`SE` = Small Efficient。绝大多数场景元素很少，
这个设计避免了堆分配——这是 seekdb 里出现频率最高的容器。

### ⚠️ `ObString` 不拥有内存

这是**最容易踩的坑**：

```cpp
class ObString {
  int32_t buffer_size_;
  int32_t data_length_;
  char   *ptr_;        // 只是个指针，不负责生命周期
};
```

- **不拥有**底层内存，只是一个 (指针, 长度) 视图
- **没有结尾 `\0`**，不能直接当 C 字符串用
- 长度是 `int32_t`
- 你必须自己保证 `ptr_` 指向的内存在 `ObString` 使用期间有效

这更接近 `std::string_view` 而非 `std::string`。
函数返回 `ObString` 时，务必确认它指向的 buffer 由谁持有。

---

## 日志

### 基本用法

每个 `.cpp` 文件开头声明模块：

```cpp
#define USING_LOG_PREFIX SQL_ENG
```

然后：

```cpp
LOG_INFO("something happened", K(var1), K(var2));
LOG_WARN("failed to do X", K(ret), KP(ptr), KCSTRING(cstr));
LOG_ERROR("fatal", K(ret));
LOG_USER_ERROR(OB_INVALID_ARGUMENT, "详细说明");   // 返回给客户端
```

### `K()` 宏族

这是 seekdb 日志的精髓——自动打印"变量名 = 值"：

| 宏 | 用途 |
|---|---|
| `K(x)` | 打印 `x=<值>`，需要类型实现 `to_string` |
| `KP(p)` | 打印指针地址 |
| `KPC(p)` | 解引用指针再打印 |
| `KCSTRING(s)` | C 字符串 |
| `KR(ret)` | 错误码，附带错误名 |

自定义类要支持 `K()`，实现 `TO_STRING_KV` 宏即可：

```cpp
TO_STRING_KV(K_(field1), K_(field2));
```

（`K_(x)` 用于成员变量，会打印 `x` 并访问 `x_`。）

### 7 个日志级别

`lib/oblog/ob_log_level.h`：

`DEBUG` / `TRACE` / `WDIAG` / `EDIAG` / `INFO` / `WARN` / `ERROR`

`WDIAG` 和 `EDIAG` 是 OceanBase 特有的**诊断**级别：
记录错误现场供事后分析，但不意味着服务出问题了。
内核代码里 `LOG_WARN` 极其常见，大多属于诊断性质。

### 模块 ID

`lib/oblog/ob_log_module.ipp` 定义了模块常量：
`CLIENT`、`CLOG`、`COMMON`、`LIB`、`RPC`、`RS`、`SERVER`、
`SHARE`、`SQL`、`STORAGE`、`TRANS` 等。
`USING_LOG_PREFIX` 就是选其中之一。

---

## 其他值得知道的

| 目录 | 内容 |
|---|---|
| `lib/charset/` | 字符集与排序规则 |
| `lib/compress/` | zstd / zlib / lz4 压缩 |
| `lib/json/` | JSON 处理 |
| `lib/net/` | `ObAddr` 等网络类型 |
| `lib/lock/` | 各种锁，含 `TCRWLock`（向量索引用它） |
| `lib/thread/` | 线程池 |
| `lib/time/` | 时间工具 |
| `lib/**vector/**` | **VSAG 向量库适配层** |
| `lib/wait_event/` | 等待事件统计 |
| `lib/signal/` | 信号处理与崩溃捕获 |

---

## 代码锚点

| 文件 | 职责 |
|---|---|
| `deps/oblib/src/lib/allocator/page_arena.h` | `ObArenaAllocator` |
| `deps/oblib/src/lib/alloc/ob_malloc_allocator.cpp` | `ObMallocAllocator` |
| `deps/oblib/src/lib/alloc/ob_ctx_allocator.cpp` | `ObTenantCtxAllocator` |
| `deps/oblib/src/lib/alloc/memory_dump.cpp` | 内存统计采集 |
| `deps/oblib/src/lib/allocator/ob_malloc.h` | `ob_malloc` / `OB_NEW` 等 |
| `deps/oblib/src/lib/container/ob_se_array.h` | `ObSEArray` |
| `deps/oblib/src/lib/container/ob_array.h` | `ObArray` |
| `deps/oblib/src/lib/hash/ob_hashmap.h` | `ObHashMap` |
| `deps/oblib/src/lib/string/ob_string.h` | `ObString`（非拥有语义） |
| `deps/oblib/src/lib/oblog/ob_log_module.h` | `LOG_*` 宏族 |
| `deps/oblib/src/lib/oblog/ob_log_module.ipp` | 模块 ID 列表 |
| `deps/oblib/src/lib/oblog/ob_log_level.h` | 7 个日志级别 |
| `deps/oblib/src/lib/oblog/ob_log_print_kv.h` | `K()` 宏实现 |
| `deps/oblib/src/lib/ob_errno.h` | 错误码 |
| `deps/oblib/src/lib/vector/ob_vsag_adaptor.h` | VSAG 适配层 |
| `docs/developer-guide/en/memory.md` | 官方内存文档 |
| `docs/developer-guide/en/container.md` | 官方容器文档 |
| `docs/developer-guide/en/logging.md` | 官方日志文档 |

---

## 动手验证

看 `ObString` 为什么不能当 C 字符串用：

```bash
grep -n -A 10 "class ObString" deps/oblib/src/lib/string/ob_string.h | head -20
```

看 `K()` 宏怎么实现的：

```bash
grep -n "define K(" deps/oblib/src/lib/oblog/ob_log_print_kv.h
```

看日志模块 ID 全集：

```bash
grep -n "LOG_MOD_BEGIN\|DEFINE_LOG_SUB_MOD" deps/oblib/src/lib/oblog/ob_log_module.ipp | head -20
```

找一个真实的 else-if 链范例：

```bash
sed -n '78,152p' src/sql/engine/expr/ob_expr_ai/ob_expr_ai_embed.cpp
```

---

## 延伸阅读

- 下一章：[3.3 编码规范](03-conventions.md)
- [1.8 可观测性](../10-user/08-observability.md) —— 内存诊断视图怎么用
- 官方文档：`docs/developer-guide/zh/memory.md`（中文版）
