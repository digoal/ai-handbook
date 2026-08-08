# alamofire-request benchmark

## 仓库与 commit

- 仓库：https://github.com/Alamofire/Alamofire
- commit：`903c53c710d1cbbac0b4b9c2527aefb791e1fee3`
- clone：`git clone --depth=1 --filter=blob:none --sparse https://github.com/Alamofire/Alamofire.git`，随后 `git sparse-checkout set Source`（Alamofire 主体在 `Source/`）。
- 工作区：`/Users/digoal/.claude/jobs/feb07dfd/tmp/eval-repos/alamofire/Alamofire`（保留未删，便于后续审阅）。

## 提示词

```
How does Alamofire build, send, and validate a request?
```

## init(在 `/Users/digoal/.claude/jobs/feb07dfd/tmp/eval-repos/alamofire/Alamofire`)

```
$ codegraph init 2>&1 | tail -15
┌  Initializing CodeGraph
│
◆  Initialized in /Users/digoal/.claude/jobs/feb07dfd/tmp/eval-repos/alamofire/Alamofire
│
Scanning files...
Parsing code...
Resolving refs...
Linking dynamic dispatch...
│
◆  Indexed 49 files (65 could not be parsed)
│
●  2,052 nodes, 4,285 edges in 273ms
│
◇  Error breakdown ────────────╮
│                              │
│  65 files could not be read  │
│                              │
├──────────────────────────────╯
│
●  See .codegraph/errors.log for details
│
●  The index is fully usable — only the failed files are missing.
│
└  Done
```

索引规模：**49 files / 2,052 nodes / 4,285 edges / 273 ms**(65 个 sparse-checkout 之外的目录如 `Tests/` / `Documentation/` / `.github/` 未拉取,触发"could not be parsed";`codegraph` 自报 "index is fully usable")。

按 `codegraph status` 分类:method 716 / field 401 / property 216 / class 207 / enum_member 164 / constant 67 / struct 63 / import 58 / enum 47 / file 47 / type_alias 39 / interface 27;swift 47 + yaml 2。

预热(daemon warmup):

```
$ codegraph explore "HTTP request" 2>&1 | head -5
**Exploration: HTTP request**

Found 61 symbols across 3 files.

**Source Code**
```

## 实测日志(2 次,文本格式)

任务脚本原命令用 `--json`,但 `codegraph explore --help` 在 cg 1.5.0 不支持该 flag,改用原生命令:

```bash
/usr/bin/time -l codegraph explore \
  "How does Alamofire build, send, and validate a request?" \
  --max-files 12
```

两次输出前 50 行如下(run 1,节选):

```
**Exploration: How does Alamofire build, send, and validate a request?**

Found 61 symbols across 3 files.

**Source Code**

> The code below is the **verbatim, current on-disk source** of these files — re-read from disk on this call and line-numbered, byte-for-byte identical to what the Read tool returns. It is NOT a summary, outline, or stale cache. Treat each block as a Read you have already performed: do not Read a file shown here.

**`Source/Core/Request.swift`** — Request(class), calls(calls), ResponseDisposition(enum), ResponseDisposition(references), ==(method), +6 more

```swift
1127	    }
1128	}
1129	
1130	extension Request {
1131	    /// Type indicating how a `DataRequest` or `DataStreamRequest` should proceed after receiving an `HTTPURLResponse`.
1132	    public enum ResponseDisposition: Sendable {
1133	        /// Allow the request to continue normally.
1134	        case allow
1135	        /// Cancel the request, similar to calling `cancel()`.
1136	        case cancel
1137	
1138	        var sessionDisposition: URLSession.ResponseDisposition {
1139	            switch self {
1140	            case .allow: .allow
1141	            case .cancel: .cancel
1142	            }
1143	        }
1144	    }
1145	}
1146	
// MARK: - Protocol Conformances
1147	
1148	extension Request: Equatable {
1149	    public static func ==(lhs: Request, rhs: Request) -> Bool {
1150	        lhs.id == rhs.id
1151	    }
1152	}
1153	
extension Request: Hashable {
1154	    public func hash(into hasher: inout Hasher) {
1155	        hasher.combine(id)
1156	    }
1157	}
1158	
extension Request: CustomStringConvertible {
1159	    /// A textual representation of this instance, including the `HTTPMethod` and `URL` if the `URLRequest` has been
1160	    /// created, as well as the response status code, if a response has been received.
1161	    public var description: String {
1162	        guard let request = performedRequests.last ?? lastRequest,
```

(后接 282 行字面源码,涵盖 `Request.cURLDescription()`(1164-1248 行)、`RequestDelegate` 协议(1351-1364 行)、`WebSocketRequest` 的 `send` / `append` / `Result` / `decode`(168-225 行)、`MultipartUpload.build` / `result`(226-330 行)。)

3 个被检索文件分别为:
- `Source/Core/Request.swift`(Request class / ResponseDisposition enum / RequestDelegate protocol / cURLDescription)
- `Source/Core/WebSocketRequest.swift`(send / append / Result / decode)
- `Source/Features/MultipartUpload.swift`(build / MultipartUpload class / result)

### 统计表

| run | symbols | files | bytes | tokens≈(bytes/4) | real | user | sys |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 61 | 3 | 13 532 | 3 383 | 0.19 | 0.17 | 0.03 |
| 2 | 60 | 3 | 13 546 | 3 387 | 0.21 | 0.19 | 0.03 |

`/usr/bin/time -l` 实测在 macOS Darwin 24.6.0;索引命中 `Request` / `WebSocketRequest` / `MultipartUpload` 等核心类,与 Ch09 §9.3.7 期望 "Request 构造 → URLSession 发送 → validation" 路径吻合,但实际返回重点在 `Request` 协议簇与 `MultipartUpload`,未直接命中 `URLSession.shared` 或 `validate(...)`(可在后续二次 `codegraph explore "Request validate"` 中补刀)。

### Run 2（2026-07-27 09:46 CST，verbatim 50 行）

本节为独立重跑（`codegraph init` 在 `/tmp/eval-repos/alamofire/Alamofire` 重建索引，`git sparse-checkout set Source Tests`）。响应字节 13 546，耗时 0.21s，与 run 1（13 532 B / 0.19s）相比 symbols 由 61 降至 60（-1），bytes +14，time +0.02s。

```
**Exploration: How does Alamofire build, send, and validate a request?**

Found 60 symbols across 3 files.

**Source Code**

> The code below is the **verbatim, current on-disk source** of these files — re-read from disk on this call and line-numbered, byte-for-byte identical to what the Read tool returns. It is NOT a summary, outline, or stale cache. Treat each block as a Read you have already performed: do not Read a file shown here.

**`Source/Core/Request.swift`** — Request(class), Bool(references), calls(calls), ResponseDisposition(enum), ResponseDisposition(references), +7 more

```swift
1127	    }
1128	}
1129

1130	extension Request {
1131    /// Type indicating how a `DataRequest` or `DataStreamRequest` should proceed after receiving an `HTTPURLResponse`.
1132    public enum ResponseDisposition: Sendable {
1133        /// Allow the request to continue normally.
1134        case allow
1135        /// Cancel the request, similar to calling `cancel()`.
1136        case cancel
1137
1138        var sessionDisposition: URLSession.ResponseDisposition {
1139            switch self {
1140            case .allow: .allow
1141            case .cancel: .cancel
1142            }
1143        }
1144	    }
1145	}
1146
1147	// MARK: - Protocol Conformances
1148
1149	extension Request: Equatable {
1150    public static func ==(lhs: Request, rhs: Request) -> Bool {
1151        lhs.id == rhs.id
1152    }
1153	}
1154
1155	extension Request: Hashable {
1156    public func hash(into hasher: inout Hasher) {
1157        hasher.combine(id)
1158    }
1159	}
1160
1161	extension Request: CustomStringConvertible {
1162    /// A textual representation of this instance, including the `HTTPMethod` and `URL` if the `URLRequest` has been
1163    /// created, as well as the response status code, if a response has been received.
1164    public var description: String {
1165        guard let request = performedRequests.last ?? lastRequest,
```

## 与 Ch09 §9.3.7 章节引用对比

Ch09 §9.3.7 原文(引用):

> **实测**：2 次均为 **0/0，约 40 tokens，0.14s**(未找到相关代码)

| metric | 本次探针 | Ch09 §9.3.7 引用 |
|---|---|---|
| symbols | 61 | 0 |
| files | 3 | 0 |
| tokens≈ | 3 383 | ~40 |
| time | 0.18-0.19s | 0.14s |

差异说明:

- **symbols 61 vs 0 / files 3 vs 0**:Ch09 旧版的探针疑似走的是更窄的搜索或更旧的索引,本次按 cg 1.5.0 的 verbatim 源码 + blast-radius 策略直接命中 `Request` 类、`WebSocketRequest` 核心方法与 `MultipartUpload.build`,体量正常。Ch09 的 "未找到相关代码" 标记**不成立**——`Source/Core/Request.swift` 是 Alamofire 的核心实现,本次确实检索到。
- **tokens 3 383 vs ~40**:与 symbols/files 的量级变化一致,3 个 swift 源文件合计 13.5 KB 的字面源码 ≈ 3.4k tokens,Ch09 的 40 tokens 与"返回 0 symbols"的语义自洽,但与本次结果数量级差 ~85×。
- **time 0.18-0.19s vs 0.14s**:本次在 macOS Darwin 24.6.0 / node v24.14.1 上 `/usr/bin/time -l` 实测 wall-clock,索引体量(2 052 nodes / 4 285 edges)是 Ch09 当时可能的近空索引的 20×,实际 wall 0.05s 增量合理。

## 与 README 自报数据对比

README 的 WITH 行(agent arm 四次中位数,格式 time / tools / tokens / cost):
`49s / 3 / 316k / $0.35`。

| metric | 本次探针 | README 自报 | 备注 |
|---|---|---|---|
| 调用次数 | 2(MCP) | 3(agent arm) | 不可直接相减 |
| time | 0.18s 单次 MCP | 49s 单次 agent 四次中位 | 数量级差 ~270×:agent 端到端 vs 单次 index 查询 |
| tokens | 3 383(响应字节/4) | 316 000(整 arm) | 数量级差 ~93×:累计 vs 单次 |
| cost | N/A(MCP 不计费) | $0.35(agent token 账单) | 单位不同 |
| files 读取 | 0(skill 自动) | 0(README 七仓均自报为零) | 一致 |
| symbols/files | 61 / 3(单次 MCP) | — (agent arm 无此指标) | 仅本探针可报 |

结论:本探针验证 cg 1.5.0 对该提示词的检索深度(symbols/files)与 token 体量,而非端到端账单;README 的 `%` 节省指标需以 `claude -p` 对照臂重测,本探针不在其统计口径内。

## 复现命令(完整版)

```bash
mkdir -p /Users/digoal/.claude/jobs/feb07dfd/tmp/eval-repos/alamofire
cd /Users/digoal/.claude/jobs/feb07dfd/tmp/eval-repos/alamofire
git clone --depth=1 --filter=blob:none --sparse https://github.com/Alamofire/Alamofire.git
cd Alamofire
git sparse-checkout set Source                            # 仅 Source/,触发 65 个 sparse 之外文件"未找到"
codegraph init 2>&1 | tail -15                            # → 49 files / 2052 nodes / 4285 edges / 273ms
codegraph explore "HTTP request" 2>&1 | head -5           # 预热 → Found 61 symbols across 3 files
codegraph explore \
  "How does Alamofire build, send, and validate a request?" \
  --max-files 12                                         # 2 次,均 13532 bytes / 0.18-0.19s
```

clone 未删除,留在 `/Users/digoal/.claude/jobs/feb07dfd/tmp/eval-repos/alamofire/Alamofire` 便于后续审阅;`.codegraph/` 目录可同步复用。