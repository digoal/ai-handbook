# 2.7 存储格式：宏块、微块、编码压缩

> **一句话**：数据在磁盘上按"宏块（IO 单位）→ 微块（存储单位）→ 编码行"三级组织，
> 支持行存与列存两种形态。

---

## 三级结构

```
数据文件
 └── 宏块 Macro Block   ~2MB   IO 与空间分配的单位
      └── 微块 Micro Block  16-64KB   压缩与缓存的单位
           └── 编码后的行数据
```

### 宏块（Macro Block）

- 定长（典型 2MB），是磁盘空间分配和 IO 的基本单位
- 有 `ObMacroBlockCommonHeader`
- 用 `MacroBlockId` 标识（`src/storage/blocksstable/ob_macro_block_id.h`）
- 管理者：`ObSharedMacroBlockMgr`、`ObMacroBlockMetaMgr`、`ObMacroSeqGenerator`

选 2MB 是个权衡：大了浪费空间和 IO 带宽，小了元信息开销大、寻址次数多。

### 微块（Micro Block）

- 变长（16-64KB），是**压缩和缓存**的单位
- 读一行只需要解压它所在的微块，不用解压整个宏块
- 读写：`ObMicroBlockReader` / `ObMicroBlockWriter`

微块的存在让"点查"变得可行——否则每次读一行都要解压 2MB。

---

## 行存 vs 列存

`ObRowStoreType` 枚举定义了存储形态：

| 类型 | 说明 |
|---|---|
| `FLAT_ROW_STORE` | 平铺行存，简单直接 |
| `CS_ENCODING_ROW_STORE` | 列式编码存储 |
| ... | 其他变体 |

**行存**适合 OLTP（取整行）；**列存**适合分析（只取几列，压缩率高）。
seekdb 继承了 OceanBase 的行列混存能力——
同一张表的不同 SSTable 可以用不同格式。

对 AI 场景，向量列往往很宽（384/768/1024 维），
存储格式的选择对 IO 影响很大。

---

## 编码

`src/storage/blocksstable/encoding/` 提供多种编码：

| 编码 | 适合的数据 |
|---|---|
| 字典编码（dict） | 重复值多的列，如枚举、状态 |
| RLE | 连续相同值 |
| 位压缩（bit packing） | 值域小的整数 |
| 整数编码 | 整数列的通用优化 |
| hex pack | 十六进制数据 |

编码在压缩**之前**做——先用编码消除结构冗余，
再用通用压缩算法压剩下的。两级叠加效果好于单用压缩。

---

## 压缩

参数 `default_compress_func`（`src/share/parameter/ob_parameter_seed.ipp`）：

| 值 | 说明 |
|---|---|
| `zstd_1.3.8` | 默认，压缩率与速度平衡好 |
| `zlib_1.0` | 兼容性好 |
| `none` | 不压缩，追求极致读性能 |

行格式 `default_row_format`：
`REDUNDANT` / `COMPACT` / `DYNAMIC` / `COMPRESSED` / `CONDENSED`。

---

## SSTable 与索引树

`ObSSTable`（`src/storage/blocksstable/ob_sstable.h`）
持有 `ObSSTableMeta`：

```
basic_meta_          基础元信息
data_root_info_      数据索引树根
macro_info_          宏块信息
column_ckm_struct_   列校验和
tx_ctx_              事务上下文
```

SSTable 内部有一棵**索引树**：从根块开始逐层定位到目标微块。
遍历用 `ObIndexBlockMacroIterator` / `ObIndexBlockDualMetaIterator`
（`src/storage/blocksstable/index_block/`）。

列校验和（`column_ckm_struct_`）用于校验数据完整性——
合并前后对比，能发现静默数据损坏。

---

## 缓存体系

存储层的缓存都基于 `ObKVCache`（`src/share/cache/`）：

| 缓存 | 缓存什么 |
|---|---|
| `ObMicroBlockCache` | 解压后的微块 |
| `ObRowCache` | 单行 |
| `ObBloomFilterCache` | 布隆过滤器 |
| `ObFuseRowCache` | 融合后的行 |

统一由 `ObBlockCacheSuite`（`ob_storage_cache_suite.h`）管理。

### 危险指针（Hazard Pointer）

`ObKVCache` 用**危险指针**做并发回收
（`ob_kvcache_hazard_pointer.cpp` / `ob_kvcache_hazard_version.cpp`）。

问题是：缓存项可能正被某个读线程使用，此时不能淘汰。
传统方案是加引用计数（有争用开销）；
危险指针让读者只需在线程局部标记"我在用这个"，
回收者扫描所有标记后再决定能不能删——读路径几乎无锁。

这是高并发读性能的关键设施之一。

---

## IO 层

`src/share/io/`：`ObIOManager`、`ObAsyncIOChannel`、
`ObIOCallback`、`ObIOTask`。

设备抽象在 `src/share/ob_local_device.cpp`、`ob_device_manager.cpp`——
这层抽象让 seekdb 能跑在本地盘、也能对接对象存储。

限流：`src/storage/throttle/`。

---

## 代码锚点

| 文件 | 职责 |
|---|---|
| `src/storage/blocksstable/ob_sstable.h` | `ObSSTable` |
| `src/storage/blocksstable/ob_sstable_meta.h` | `ObSSTableMeta` |
| `src/storage/blocksstable/ob_macro_block_id.h` | `MacroBlockId` |
| `src/storage/blocksstable/ob_shared_macro_block_manager.cpp` | 宏块管理 |
| `src/storage/blocksstable/ob_macro_block_meta_mgr.cpp` | 宏块元信息 |
| `src/storage/blocksstable/encoding/` | 各种编码 |
| `src/storage/blocksstable/index_block/` | SSTable 索引树 |
| `src/storage/blocksstable/ob_storage_cache_suite.h` | 缓存套件 |
| `src/share/cache/ob_kv_storecache.cpp` | KV Cache 主体 |
| `src/share/cache/ob_kvcache_hazard_pointer.cpp` | 危险指针 |
| `src/share/io/ob_io_manager.cpp` | IO 管理 |
| `src/share/ob_local_device.cpp` | 本地设备 |
| `src/storage/throttle/` | IO 限流 |
| `src/share/parameter/ob_parameter_seed.ipp` | `default_compress_func` 等 |

---

## 动手验证

看压缩算法选项：

```bash
grep -n "default_compress_func\|default_row_format" src/share/parameter/ob_parameter_seed.ipp
```

看有多少种编码：

```bash
ls src/storage/blocksstable/encoding/ | grep encoding | head -20
```

看 SSTable 元信息结构：

```bash
grep -n "basic_meta_\|data_root_info_\|macro_info_\|column_ckm_struct_" src/storage/blocksstable/ob_sstable_meta.h | head
```

---

## 延伸阅读

- 下一章：[2.8 事务与 MVCC](08-transaction-mvcc.md)
- [2.6 一行数据的一生](06-lsm-tree.md) —— SSTable 从哪来
- [1.7 部署与配置](../10-user/07-deploy-config.md) —— 压缩相关参数
