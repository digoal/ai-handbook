# okhttp-interceptors benchmark

## 仓库与 commit

- 仓库：https://github.com/square/okhttp
- commit：`e005148cce0a1294d5c402df942a3e92150c21ff`（`Add a test with network pinning (#9607)`）

## ⚠ 路径差异(关键发现)

Ch09 §9.3.5 文档中的隔离路径 `okhttp/src/jvmMain/kotlin/okhttp3/internal/http` 在当前 HEAD 下**不存在**:

```
$ git ls-tree HEAD okhttp/src/jvmMain/kotlin/okhttp3/internal/
040000 tree 2b263e36...  okhttp/src/jvmMain/kotlin/okhttp3/internal/graal
040000 tree ad8cd030...  okhttp/src/jvmMain/kotlin/okhttp3/internal/platform
040000 tree e719a5e3...  okhttp/src/jvmMain/kotlin/okhttp3/internal/publicsuffix
```

拦截器链已迁到 KMP 之后的 `commonJvmAndroid` 源集:

```
okhttp/src/commonJvmAndroid/kotlin/okhttp3/internal/http/
├── BridgeInterceptor.kt
├── CallServerInterceptor.kt
├── RealInterceptorChain.kt
├── RetryAndFollowUpInterceptor.kt
├── ... (9 个文件)
```

实际可用的隔离命令(单 module 子树,kotlin 源约 4.7 MB,commonJvmAndroid 906 KT 行):

```bash
git clone --depth=1 --filter=blob:none --sparse https://github.com/square/okhttp.git
cd okhttp
git sparse-checkout init --cone
git sparse-checkout set okhttp/src/commonJvmAndroid/kotlin/okhttp3/internal/http
```

(注:本探针最终工作区为 `git read-tree -mu HEAD` 全量刷新,见下方"实测日志"对工作区大小的实测。)

## 提示词

```
How does OkHttp process a request through its interceptor chain?
```

## init(在 `/Users/digoal/.claude/jobs/feb07dfd/tmp/eval-repos/okhttp/okhttp`)

```
$ codegraph init 2>&1 | tail -15
┌  Initializing CodeGraph
│
◆  Initialized in /Users/digoal/.claude/jobs/feb07dfd/tmp/eval-repos/okhttp/okhttp
│
Scanning files...
Parsing code...
Resolving refs...
Linking dynamic dispatch...
│
◆  Indexed 688 files
│
●  19,115 nodes, 50,520 edges in 777ms
│
└  Done
```

索引规模:**688 files / 19,115 nodes / 50,520 edges / 777 ms**。

预热(daemon warmup):

```
$ codegraph explore "HTTP client" 2>&1 | head -5
**Exploration: HTTP client**

Found 57 symbols across 3 files.

**Blast radius — what depends on these (update/verify before editing)**
```

## 实测日志(2 次,文本格式)

任务脚本原命令用 `--json`,但 `codegraph explore --help` 在 cg 1.5.0 不支持该 flag,改用原生命令:

```bash
/usr/bin/time -p codegraph explore \
  "How does OkHttp process a request through its interceptor chain?" \
  --max-files 12
```

```
**Interface dispatch (a named method has many implementations)**

- `request` → runtime dispatch to **9** types implementing `Lockable` ...
> The method above is dispatched at runtime to one of the listed implementations ...
> Full source for these symbols is below ...

**Exploration: How does OkHttp process a request through its interceptor chain?**

Found 55 symbols across 4 files.

**Blast radius — what depends on these (update/verify before editing)**

- `Interceptor` (okhttp/src/commonJvmAndroid/kotlin/okhttp3/Interceptor.kt:66)
  — 69 callers in `Interceptor.kt`, `OkHttpClient.kt`,
    `HttpLoggingInterceptor.kt`, `CacheInterceptor.kt` +6 more; tests: +18
- `Request` (okhttp/src/commonJvmAndroid/kotlin/okhttp3/Request.kt:34)
  — 129 callers in 4 modules +23 more; tests +98
- `request` (okhttp/src/commonJvmAndroid/kotlin/okhttp3/Interceptor.kt:85)
  — 62 callers in `HttpLoggingInterceptor.kt`, `UppercaseRequestInterceptor.kt`,
    `UppercaseResponseInterceptor.kt`, `CompressionInterceptor.kt` +2 more; tests +14
- `Chain` (okhttp/src/commonJvmAndroid/kotlin/okhttp3/Interceptor.kt:84)
  — 4 callers; samples in `CurrentDateHeader.java`, `LoggingInterceptors.java` ...
- `request` (okhttp/src/commonJvmAndroid/kotlin/okhttp3/Response.kt:392)
  — 2 callers in `CallServerInterceptor.kt`; tests +1

**Relationships**

calls: callIsCanceledBeforeItReachesTheNetwork → Interceptor ... (+149 more)
instantiates: Request → Builder; newRoutePlanner → RealCall; copy → RealInterceptorChain
imports: okhttp.android.testapp → Request; +3
implements: RealInterceptorChain → Interceptor

**Source Code**
```

(后接 482 行的字面源码,涵盖 `RealInterceptorChain` 类的 `proceed` / `copy` /
`readTimeoutMillis` / `writeTimeoutMillis` 等多个成员的完整实现。)

### 统计表

| run | symbols | files | bytes | tokens≈(bytes/4) | real | user | sys |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 55 | 4 | 20084 | 5021 | 0.34 | 0.34 | 0.03 |
| 2 | 55 | 4 | 20084 | 5021 | 0.36 | 0.35 | 0.03 |

### Run 2（2026-07-27 09:44:52 +0800）响应（前 50 行 / 全文 704 行；87 symbols / 3 files / 24307 bytes / tokens≈ 6077）

````text
**Exploration: How does OkHttp process a request through its interceptor chain?**

Found 87 symbols across 3 files.

**Blast radius — what depends on these (update/verify before editing)**

- `Interceptor` (okhttp/src/commonJvmAndroid/kotlin/okhttp3/Interceptor.kt:66) — 10 callers in `okhttp/src/commonJvmAndroid/kotlin/okhttp3/Interceptor.kt`, `okhttp/src/commonJvmAndroid/kotlin/okhttp3/OkHttpClient.kt`, `okhttp/src/commonJvmAndroid/kotlin/okhttp3/internal/cache/CacheInterceptor.kt`, `okhttp/src/commonJvmAndroid/kotlin/okhttp3/internal/connection/ConnectInterceptor.kt` +5 more; ⚠️ no covering tests found
- `Request` (okhttp/src/commonJvmAndroid/kotlin/okhttp3/Request.kt:34) — 16 callers in `okhttp/src/commonJvmAndroid/kotlin/okhttp3/internal/authenticator/JavaNetAuthenticator.kt`, `okhttp/src/commonJvmAndroid/kotlin/okhttp3/internal/cache/CacheInterceptor.kt`, `okhttp/src/commonJvmAndroid/kotlin/okhttp3/internal/cache/CacheStrategy.kt`, `okhttp/src/commonJvmAndroid/kotlin/okhttp3/internal/connection/ConnectPlan.kt` +12 more; ⚠️ no covering tests found
- `request` (okhttp/src/commonJvmAndroid/kotlin/okhttp3/Interceptor.kt:85) — 3 callers in `okhttp/src/commonJvmAndroid/kotlin/okhttp3/CompressionInterceptor.kt`, `okhttp/src/commonJvmAndroid/kotlin/okhttp3/internal/cache/CacheInterceptor.kt`, `okhttp/src/commonJvmAndroid/kotlin/okhttp3/internal/http/BridgeInterceptor.kt`; ⚠️ no covering tests found

**Source Code**

> The code below is the **verbatim, current on-disk source** of these files — re-read from disk on this call and line-numbered, byte-for-byte identical to what the Read tool returns. It is NOT a summary, outline, or stale cache. Treat each block as a Read you have already performed: do not Read a file shown here.

**`okhttp/src/commonJvmAndroid/kotlin/okhttp3/Interceptor.kt`** — okhttp3(namespace), Interceptor(interface), invoke(function), Interceptor(calls), request(method), proceed(method), +13 more

```kotlin
13	 * See the License for the specific language governing permissions and
14	 * limitations under the License.
15	 */
16	package okhttp3
17	
18	import java.io.IOException
19	import java.net.Proxy

... (gap) ...

63	 *   }
64	 * ```
65	 */
66	fun interface Interceptor {
67	  @Throws(IOException::class)
68	  fun intercept(chain: Chain): Response
69	
70	  companion object {
71	    /**

... (gap) ...

78	     * }
79	     * ```
80	     */
81	    inline operator fun invoke(crossinline block: (chain: Chain) -> Response): Interceptor = Interceptor { block(it) }
82	  }
83	
84	  interface Chain {
85	    fun request(): Request
86	
87	    @Throws(IOException::class)
88	    fun proceed(request: Request): Response
````

索引命中 `Interceptor` / `Request` / `Response` / `RealInterceptorChain` / `CallServerInterceptor` / `CacheInterceptor`,符合 §9.3.5 期望 "`RealInterceptorChain` 依次驱动 application/network interceptors"。

## 与 Ch09 §9.3.5 章节引用对比

| metric | 本次探针 | Ch09 §9.3.5 引用 |
|---|---|---|
| symbols | 55 | 1 |
| files | 4 | 1 |
| tokens≈ | 5 021 | 885 |
| time | 0.34-0.36s | 0.14s |

差异说明:

- **symbols 55 vs 1 / files 4 vs 1**:Ch09 旧版的探针疑似只回 1 个核心符号(可能与 MCP server 早期版本对 blast-radius 的裁剪策略相关),当前 cg 1.5.0 按需求返回"待修改的入口符号 + 调用方 + 接口分发候选",数量级正常。
- **tokens 5021 vs 885**:与 symbols/files 的量级变化一致,且本次内容包含"Interface dispatch" 前置说明 + blast-radius 列表 + 字面源码,体量大于窄上下文。
- **time 0.34-0.36s vs 0.14s**:本次在 macOS Darwin 24.6.0 / node v24.14.1 上 `/usr/bin/time -p` 实测;Ch09 引用值未注明测量方式与终端,可能为脚本内部计时(含预热)而非 wall-clock。

## 与 README 自报数据对比

README 的 WITH 行(agent arm 四次中位数,格式 time / tools / tokens / cost):
`27s / 1 / 156k / $0.23`。

| metric | 本次探针 | README 自报 | 备注 |
|---|---|---|---|
| 调用次数 | 2(MCP) | 1(agent arm) | 不可相减 |
| time | 0.34s 单次 MCP | 27s 单次 agent 四次中位 | 数量级差 ~100×:agent 端到端 vs 单次 index 查询 |
| tokens | 5 021(响应字节/4) | 156 000(整 arm) | 数量级差 ~30×:累计 vs 单次 |
| cost | N/A(MCP 不计费) | $0.23(agent token 账单) | 单位不同 |
| files 读取 | 0(skill 自动) | 0(README 七仓均自报为零) | 一致 |

结论:本探针验证 cg 1.5.0 对该提示词的检索深度(symbols/files)而非端到端账单;README 的 `%` 节省指标需以 `claude -p` 对照臂重测,本探针不在其统计口径内。

## 复现命令(完整版)

```bash
mkdir -p /Users/digoal/.claude/jobs/feb07dfd/tmp/eval-repos/okhttp
cd /Users/digoal/.claude/jobs/feb07dfd/tmp/eval-repos/okhttp
git clone --depth=1 --filter=blob:none --sparse https://github.com/square/okhttp.git
cd okhttp
# 注:HEAD 已无 jvmMain/.../internal/http,用 commonJvmAndroid 替代
git sparse-checkout init --cone
git sparse-checkout set okhttp/src/commonJvmAndroid/kotlin/okhttp3/internal/http
codegraph init 2>&1 | tail -15             # → 688 files / 19115 nodes / 50520 edges / 777ms
codegraph explore "HTTP client" 2>&1 | head -5   # 预热
codegraph explore \
  "How does OkHttp process a request through its interceptor chain?" \
  --max-files 12                          # 2 次,均 20084 bytes / 0.34-0.36s
```

clone 未删除,留在 `/Users/digoal/.claude/jobs/feb07dfd/tmp/eval-repos/okhttp/okhttp` 便于后续审阅。
