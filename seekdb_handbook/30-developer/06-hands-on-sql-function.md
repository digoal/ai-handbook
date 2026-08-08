# 3.6 实战一：新增一个 SQL 内建函数

> **一句话**：跟着 `AI_EMBED` 走一遍——从函数名常量到语法、到表达式类、
> 到注册、到测试，一个内建函数要改 5 个地方。

---

## 为什么拿 `AI_EMBED` 当范例

它足够新（2025 年加的）、足够完整（有参数校验、有运行时状态、有错误处理），
而且代码量适中。把它拆开看一遍，你就知道加函数要动哪些文件。

---

## 全景：一个内建函数的 5 个落点

```
1. 函数名常量        deps/oblib/src/lib/ob_name_def.h
2. 表达式类型枚举    src/objit/include/objit/common/ob_item_type.h
3. 表达式实现        src/sql/engine/expr/<你的目录>/
4. 工厂注册          src/sql/engine/expr/ob_expr_operator_factory.cpp
5. 测试用例          tools/deploy/mysql_test/test_suite/<套件>/
```

（如果函数需要新语法——比如 `MATCH ... AGAINST` 那种——
还要动 `src/sql/parser/sql_parser_mysql_mode.y`。
但普通的 `func(a, b)` 形式不需要，走通用函数调用规则即可。）

---

## 第 1 步：定义函数名

`deps/oblib/src/lib/ob_name_def.h:1091`：

```cpp
#define N_AI_EMBED    "ai_embed"
```

这就是用户在 SQL 里写的名字。注意它在 **layer 0**（oblib），
因为上下各层都要用。

---

## 第 2 步：分配表达式类型枚举

`src/objit/include/objit/common/ob_item_type.h:915`：

```cpp
T_FUN_SYS_AI_EMBED = 2083,
T_FUN_SYS_AI_RERANK = 2084,
```

> ⚠️ 这个枚举值**显式写死了数字**。加新函数时要取一个没被占用的值，
> 通常接在最后。不要插在中间——会破坏兼容性。

---

## 第 3 步：写表达式类

放在 `src/sql/engine/expr/` 下（相关函数建议开子目录，
像 `ob_expr_ai/` 那样）。

### 头文件骨架

```cpp
class ObExprAIEmbed : public ObFuncExprOperator
{
public:
  explicit ObExprAIEmbed(common::ObIAllocator &alloc);
  virtual ~ObExprAIEmbed();

  // 1) 类型推导与参数校验
  virtual int calc_result_typeN(ObExprResType &type,
                                ObExprResType *types_stack,
                                int64_t param_num,
                                common::ObExprTypeCtx &type_ctx) const override;

  // 2) 实际求值
  static int eval_ai_embed(const ObExpr &expr, ObEvalCtx &ctx, ObDatum &res);

  // 3) 代码生成时挂上求值函数
  virtual int cg_expr(ObExprCGCtx &expr_cg_ctx,
                      const ObRawExpr &raw_expr,
                      ObExpr &rt_expr) const override;
private:
  DISALLOW_COPY_AND_ASSIGN(ObExprAIEmbed);
};
```

### 构造函数：声明元信息

`ob_expr_ai_embed.cpp:29`：

```cpp
ObExprAIEmbed::ObExprAIEmbed(common::ObIAllocator &alloc)
    : ObFuncExprOperator(alloc,
                        T_FUN_SYS_AI_EMBED,        // 类型枚举
                        N_AI_EMBED,                // 函数名
                        MORE_THAN_ZERO,            // 参数个数约定
                        NOT_VALID_FOR_GENERATED_COL,  // 能否用于生成列
                        NOT_ROW_DIMENSION)
{}
```

参数个数可以写具体数字，也可以用 `MORE_THAN_ZERO` 这类常量
（然后在 `calc_result_typeN` 里自己校验）。

### `calc_result_typeN`：类型推导 + 校验

这一步在**解析期**执行，决定返回类型，并对参数做类型转换要求。

```cpp
int ObExprAIEmbed::calc_result_typeN(ObExprResType &type,
                                     ObExprResType *types_stack,
                                     int64_t param_num,
                                     common::ObExprTypeCtx &type_ctx) const
{
  int ret = OB_SUCCESS;
  if (OB_UNLIKELY(param_num > 3 || param_num < 2)) {
    ObString func_name_(get_name());
    ret = OB_ERR_PARAM_SIZE;
    LOG_USER_ERROR(OB_ERR_PARAM_SIZE, func_name_.length(), func_name_.ptr());
  } else {
    // 要求参数 0、1 按 varchar 处理
    types_stack[MODEL_IDX].set_calc_type(ObVarcharType);
    types_stack[MODEL_IDX].set_calc_collation_type(CS_TYPE_UTF8MB4_BIN);
    types_stack[CONTENT_IDX].set_calc_type(ObVarcharType);
    types_stack[CONTENT_IDX].set_calc_collation_type(CS_TYPE_UTF8MB4_BIN);

    if (param_num == 3) {
      if (ob_is_integer_type(types_stack[DIM_IDX].get_type())) {
        types_stack[DIM_IDX].set_calc_type(ObIntType);
      } else {
        ret = OB_INVALID_ARGUMENT;
        LOG_USER_ERROR(OB_INVALID_ARGUMENT,
          "ai_embed, dimension parameter must be an integer, not a decimal or float");
      }
    }
    // 声明返回类型
    type.set_varchar();
    type.set_collation_type(CS_TYPE_UTF8MB4_BIN);
    type.set_collation_level(CS_LEVEL_COERCIBLE);
  }
  return ret;
}
```

要点：
- `set_calc_type()` 是**要求引擎把参数转成这个类型**，不是断言
- 参数个数、类型的校验都在这里做，尽量早报错
- `type.set_xxx()` 声明返回类型

### `eval_xxx`：运行时求值

```cpp
int ObExprAIEmbed::eval_ai_embed(const ObExpr &expr, ObEvalCtx &ctx, ObDatum &res)
{
  INIT_SUCC(ret);                      // int ret = OB_SUCCESS 的简写
  ObDatum *arg_model_id = nullptr;
  ObDatum *arg_content = nullptr;

  // 求值参数
  if (OB_FAIL(expr.eval_param_value(ctx, arg_model_id, arg_content))) {
    LOG_WARN("evaluate parameters failed", K(ret));
  } else if (arg_model_id->is_null() || arg_content->is_null()) {
    ret = OB_INVALID_ARGUMENT;
    LOG_USER_ERROR(OB_INVALID_ARGUMENT, "ai_embed, model id or content is null");
    res.set_null();
  } else {
    // 临时内存：随作用域自动回收
    ObEvalCtx::TempAllocGuard tmp_alloc_g(ctx);
    MultimodeAlloctor temp_allocator(tmp_alloc_g.get_allocator());
    // ... 业务逻辑 ...
    // 写结果
    if (OB_FAIL(ObAIFuncUtils::set_string_result(expr, ctx, res, result))) {
      LOG_WARN("fail to set string result", K(ret));
    }
  }
  return ret;
}
```

要点：
- 参数用 `expr.eval_param_value(ctx, ...)` 取，得到 `ObDatum*`
- **必须处理 NULL**
- 临时内存用 `ObEvalCtx::TempAllocGuard`，别自己 malloc
- 结果写进 `res`（`ObDatum`）

### `cg_expr`：代码生成期挂钩子

```cpp
int ObExprAIEmbed::cg_expr(ObExprCGCtx &expr_cg_ctx,
                           const ObRawExpr &raw_expr,
                           ObExpr &rt_expr) const
{
  int ret = OB_SUCCESS;
  rt_expr.eval_func_ = ObExprAIEmbed::eval_ai_embed;
  return ret;
}
```

这一步把静态函数指针挂到运行时表达式上。
需要向量化就再设 `eval_batch_func_`。

> 💡 `AI_EMBED` 的 `cg_expr` 里有一段被注释掉的代码，
> 上面写着 `// TODO: support schema version match in plan cache for ai func`。
> 说明这个函数与计划缓存的配合还没做完——这是读源码时的有用信号。

---

## 第 4 步：注册到工厂

`src/sql/engine/expr/ob_expr_operator_factory.cpp:1047`：

```cpp
REG_OP(ObExprAIEmbed);
```

`REG_OP` 宏（同文件 430 行）做三件事：

```cpp
NAME_TYPES[i].name_ = op.get_name();          // 名字 → 类型 映射
NAME_TYPES[i].type_ = op.get_type();
OP_ALLOC[op.get_type()] = alloc<OpClass>;     // 类型 → 构造器 映射
```

于是解析器看到 `ai_embed(...)` 就能查到 `T_FUN_SYS_AI_EMBED`，
执行期再按类型构造出对象。

> ⚠️ 有个容量上限 `EXPR_OP_NUM`，超了会 `LOG_ERROR_RET`。
> 加函数时如果注册失败，先看这个。

顺带一提，如果你的新函数和已有函数功能相同（只是换个名字），
用 `REG_SAME_OP` 宏可以避免重复代码。

---

## 第 5 步：写测试

在 `tools/deploy/mysql_test/test_suite/` 下找合适的套件
（新特性可以新建一个）：

```
t/my_func.test        输入
r/my_func.result      期望输出
```

参考 `ai_function/t/ai_prompt.test` 的写法——
它把正确用法、参数个数错误、类型错误、各种数据类型都覆盖了：

```sql
# 正确
select ai_prompt('{0}+{1}={2} 吗？请回答true或false','1');

# 无参数
--error 1582
select ai_prompt();

# 错误类型
--error 5083
select ai_prompt(1);

# 作用在表列上
create table t1 (nr char(5), a varchar(10), b BINARY(20), c VARBINARY(20));
insert into t1 values( 'a', 'b', "oExGTLHmkvIGQekFkd" , "oExGTLHmkvIGQekFkd");
select ai_prompt(nr) from t1;
drop table t1;
```

生成 `.result` 的办法：先跑一遍，把实际输出确认无误后存为期望值。

跑测试：

```bash
./tools/deploy/obd.sh mysqltest -n test \
  --test-dir ./mysql_test/test_suite/ai_function/t \
  --result-dir ./mysql_test/test_suite/ai_function/r \
  --test-set my_func
```

---

## 检查清单

改完对照一遍：

- [ ] `ob_name_def.h` 加了 `N_XXX` 常量
- [ ] `ob_item_type.h` 加了 `T_FUN_SYS_XXX` 枚举（取未占用的值，加在末尾）
- [ ] 表达式类实现了 `calc_result_typeN` / `eval_xxx` / `cg_expr`
- [ ] `ob_expr_operator_factory.cpp` 里 `REG_OP` 了
- [ ] `CMakeLists.txt` 收录了新 `.cpp`
- [ ] NULL 参数处理了
- [ ] 失败分支都有 `LOG_WARN(..., K(ret))`
- [ ] 用户可见的错误用了 `LOG_USER_ERROR`
- [ ] 版权头加了
- [ ] 新类**不加** `Ob` 前缀（见 `AGENTS.md`）
- [ ] mysqltest 用例覆盖了正常与异常路径

---

## 代码锚点

| 文件:行 | 职责 |
|---|---|
| `deps/oblib/src/lib/ob_name_def.h:1091` | `N_AI_EMBED "ai_embed"` |
| `src/objit/include/objit/common/ob_item_type.h:915` | `T_FUN_SYS_AI_EMBED = 2083` |
| `src/sql/engine/expr/ob_expr_ai/ob_expr_ai_embed.cpp:29` | 构造函数（元信息声明） |
| `src/sql/engine/expr/ob_expr_ai/ob_expr_ai_embed.cpp:43` | `calc_result_typeN` |
| `src/sql/engine/expr/ob_expr_ai/ob_expr_ai_embed.cpp:78` | `eval_ai_embed` |
| `src/sql/engine/expr/ob_expr_ai/ob_expr_ai_embed.cpp:154` | `cg_expr` |
| `src/sql/engine/expr/ob_expr_operator_factory.cpp:430` | `REG_OP` 宏 |
| `src/sql/engine/expr/ob_expr_operator_factory.cpp:1047` | `REG_OP(ObExprAIEmbed)` |
| `src/sql/engine/expr/ob_expr_operator.h:1062` | `ObFuncExprOperator` 基类 |
| `tools/deploy/mysql_test/test_suite/ai_function/t/ai_prompt.test` | 测试范例 |

---

## 动手验证

完整读一遍范例函数（约 194 行，很好读）：

```bash
cat src/sql/engine/expr/ob_expr_ai/ob_expr_ai_embed.cpp
```

看 `REG_OP` 到底做了什么：

```bash
sed -n '430,450p' src/sql/engine/expr/ob_expr_operator_factory.cpp
```

看已经注册了多少函数：

```bash
grep -c "REG_OP(" src/sql/engine/expr/ob_expr_operator_factory.cpp
```

找一个最简单的函数对照学习：

```bash
cat src/sql/engine/expr/ob_expr_acos.cpp
```

---

## 延伸阅读

- 下一章：[3.7 实战二：读懂并扩展向量索引](07-hands-on-vector-index.md)
- [2.4 一条 SELECT 的一生（下）](../20-architect/04-select-lifecycle-2.md) —— 表达式在执行期怎么被调度
- [3.3 编码规范](03-conventions.md)
