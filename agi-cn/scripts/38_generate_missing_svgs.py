#!/usr/bin/env python3
"""生成缺失的 SVG 图:
- fig-25-1: 如何使用 Google Cloud Console 访问 AgentSpace
- fig-25-3: Google 的预制提示库
- fig-25-4: 自定义智能体的提示
- fig-25-5: AgentSpace 高级能力
- fig-25-6: 与智能体对话的用户界面
- fig-28-1: 编程专家示例
"""
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path("/Users/digoal/new/tmp/tmp1/agi-translation")
SVG_DIR = ROOT / "output" / "agi-zh-by-chapter" / "svg"


def make_svg(title: str, elements_xml: str) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" width="800" height="600">
  <style>
    .title {{ font-family: sans-serif; font-size: 20px; font-weight: bold; text-anchor: middle; fill: #111827; }}
    .label {{ font-family: sans-serif; font-size: 14px; text-anchor: middle; fill: #111827; }}
    .sublabel {{ font-family: sans-serif; font-size: 12px; text-anchor: middle; fill: #6B7280; }}
    .box {{ fill: #DBEAFE; stroke: #1F2937; stroke-width: 1.5; rx: 8; ry: 8; }}
    .arrow {{ stroke: #374151; stroke-width: 2; fill: none; marker-end: url(#arrowhead); }}
  </style>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#374151"/>
    </marker>
  </defs>
  <rect width="800" height="600" fill="#FFFFFF"/>
  <text x="400" y="40" class="title">{title}</text>
  {elements_xml}
</svg>
"""


def write_svg(name: str, title: str, elements_xml: str):
    svg = make_svg(title, elements_xml)
    # 验证 SVG 合法性
    try:
        ET.fromstring(svg)
    except ET.ParseError as e:
        print(f"  ✗ {name}: SVG 非法 - {e}")
        return False
    (SVG_DIR / f"{name}.svg").write_text(svg, encoding='utf-8')
    print(f"  ✓ {name}.svg")
    return True


# ============== Ch 25 SVG ==============

# fig-25-1: Google Cloud Console → AI Applications → AgentSpace
fig_25_1 = """
  <rect x="50" y="100" width="180" height="100" class="box"/>
  <text x="140" y="145" class="label">Google Cloud</text>
  <text x="140" y="165" class="label">Console</text>
  <line x1="230" y1="150" x2="320" y2="150" class="arrow"/>
  <rect x="320" y="100" width="180" height="100" class="box"/>
  <text x="410" y="145" class="label">AI Applications</text>
  <text x="410" y="165" class="sublabel">(在导航菜单中)</text>
  <line x1="500" y1="150" x2="590" y2="150" class="arrow"/>
  <rect x="590" y="100" width="180" height="100" class="box"/>
  <text x="680" y="145" class="label">AgentSpace</text>
  <text x="680" y="165" class="sublabel">(企业版)</text>
  <text x="400" y="280" class="sublabel">点击顺序:Console → AI Applications → AgentSpace</text>
  <text x="400" y="320" class="sublabel">进入 AgentSpace 后可使用 Agent Designer 配置智能体</text>
  <text x="400" y="360" class="sublabel">或浏览预制提示库与已部署的智能体</text>
"""

# fig-25-3: Google 的预制提示库
fig_25_3 = """
  <rect x="300" y="100" width="200" height="60" class="box"/>
  <text x="400" y="135" class="label">预制提示库</text>
  <rect x="80" y="220" width="140" height="50" class="box"/>
  <text x="150" y="250" class="label">研究助手</text>
  <rect x="240" y="220" width="140" height="50" class="box"/>
  <text x="310" y="250" class="label">会议摘要</text>
  <rect x="400" y="220" width="140" height="50" class="box"/>
  <text x="470" y="250" class="label">文档问答</text>
  <rect x="560" y="220" width="140" height="50" class="box"/>
  <text x="630" y="250" class="label">销售分析</text>
  <rect x="160" y="320" width="140" height="50" class="box"/>
  <text x="230" y="350" class="label">客户支持</text>
  <rect x="320" y="320" width="140" height="50" class="box"/>
  <text x="390" y="350" class="label">邮件草稿</text>
  <rect x="480" y="320" width="140" height="50" class="box"/>
  <text x="550" y="350" class="label">数据洞察</text>
  <text x="400" y="450" class="sublabel">Google 提供的常用提示模板集合</text>
  <text x="400" y="475" class="sublabel">用户可选择预制模板或基于此创建自定义提示</text>
"""

# fig-25-4: 自定义智能体的提示
fig_25_4 = """
  <rect x="100" y="120" width="600" height="280" class="box"/>
  <text x="400" y="155" class="label">自定义提示编辑器</text>
  <line x1="150" y1="180" x2="650" y2="180" stroke="#6B7280" stroke-width="1"/>
  <text x="150" y="215" class="sublabel">提示名称:</text>
  <rect x="280" y="195" width="350" height="30" fill="#F3F4F6" stroke="#9CA3AF"/>
  <text x="295" y="215" class="sublabel">"我的研究助手"</text>
  <text x="150" y="255" class="sublabel">指令:</text>
  <rect x="280" y="235" width="350" height="80" fill="#F3F4F6" stroke="#9CA3AF"/>
  <text x="295" y="260" class="sublabel">"你是一名专业研究员,擅长总结科学论文..."</text>
  <text x="150" y="345" class="sublabel">知识库:</text>
  <rect x="280" y="325" width="120" height="30" fill="#F3F4F6" stroke="#9CA3AF"/>
  <text x="340" y="345" class="sublabel">✓ 文献数据库</text>
  <rect x="420" y="325" width="120" height="30" fill="#F3F4F6" stroke="#9CA3AF"/>
  <text x="480" y="345" class="sublabel">✓ 内部 Wiki</text>
  <text x="400" y="450" class="sublabel">用户可在 Agent Designer 中编写自定义提示</text>
  <text x="400" y="475" class="sublabel">并指定使用的知识库与外部工具</text>
"""

# fig-25-5: AgentSpace 高级能力
fig_25_5 = """
  <rect x="300" y="80" width="200" height="60" class="box"/>
  <text x="400" y="115" class="label">AgentSpace 高级能力</text>
  <rect x="80" y="200" width="140" height="80" class="box"/>
  <text x="150" y="235" class="label">数据存储</text>
  <text x="150" y="255" class="sublabel">自有数据</text>
  <rect x="240" y="200" width="140" height="80" class="box"/>
  <text x="310" y="235" class="label">知识图谱</text>
  <text x="310" y="255" class="sublabel">Google KG</text>
  <rect x="400" y="200" width="140" height="80" class="box"/>
  <text x="470" y="235" class="label">Web 界面</text>
  <text x="470" y="255" class="sublabel">对外发布</text>
  <rect x="560" y="200" width="140" height="80" class="box"/>
  <text x="630" y="235" class="label">分析监控</text>
  <text x="630" y="255" class="sublabel">使用情况</text>
  <rect x="160" y="340" width="140" height="80" class="box"/>
  <text x="230" y="375" class="label">企业 SSO</text>
  <text x="230" y="395" class="sublabel">身份认证</text>
  <rect x="320" y="340" width="140" height="80" class="box"/>
  <text x="390" y="375" class="label">A2A 协议</text>
  <text x="390" y="395" class="sublabel">智能体互通</text>
  <rect x="480" y="340" width="140" height="80" class="box"/>
  <text x="550" y="375" class="label">角色权限</text>
  <text x="550" y="395" class="sublabel">RBAC</text>
  <text x="400" y="500" class="sublabel">企业级智能体平台的核心能力集合</text>
"""

# fig-25-6: 用户界面
fig_25_6 = """
  <rect x="50" y="80" width="700" height="440" class="box"/>
  <text x="400" y="115" class="label">AgentSpace 聊天界面</text>
  <line x1="50" y1="140" x2="750" y2="140" stroke="#6B7280" stroke-width="1"/>
  <rect x="70" y="160" width="120" height="40" fill="#EFF6FF" stroke="#3B82F6"/>
  <text x="130" y="185" class="sublabel">研究助手</text>
  <rect x="70" y="220" width="120" height="40" fill="#F3F4F6"/>
  <text x="130" y="245" class="sublabel">会议摘要</text>
  <rect x="70" y="280" width="120" height="40" fill="#F3F4F6"/>
  <text x="130" y="305" class="sublabel">文档问答</text>
  <rect x="220" y="160" width="510" height="280" fill="#FAFAFA" stroke="#9CA3AF"/>
  <rect x="240" y="180" width="220" height="60" fill="#FFFFFF" stroke="#E5E7EB" rx="8"/>
  <text x="350" y="205" class="sublabel">用户:帮我总结最新的</text>
  <text x="350" y="225" class="sublabel">季度财报。</text>
  <rect x="490" y="260" width="220" height="60" fill="#DBEAFE" stroke="#3B82F6" rx="8"/>
  <text x="600" y="285" class="sublabel">助手:以下是 Q3 财报</text>
  <text x="600" y="305" class="sublabel">主要摘要...</text>
  <rect x="220" y="460" width="450" height="40" fill="#FFFFFF" stroke="#9CA3AF"/>
  <text x="445" y="485" class="sublabel">输入消息...</text>
  <rect x="680" y="460" width="50" height="40" fill="#3B82F6"/>
  <text x="705" y="485" class="label" fill="#FFFFFF">发送</text>
"""

# fig-28-1: 编程专家示例
fig_28_1 = """
  <rect x="300" y="80" width="200" height="60" class="box"/>
  <text x="400" y="115" class="label">编程专家团队</text>
  <rect x="80" y="200" width="140" height="100" class="box"/>
  <text x="150" y="240" class="label">主程序员</text>
  <text x="150" y="260" class="sublabel">生成代码</text>
  <rect x="240" y="200" width="140" height="100" class="box"/>
  <text x="310" y="240" class="label">评审员</text>
  <text x="310" y="260" class="sublabel">质量审查</text>
  <rect x="400" y="200" width="140" height="100" class="box"/>
  <text x="470" y="240" class="label">文档员</text>
  <text x="470" y="260" class="sublabel">注释生成</text>
  <rect x="560" y="200" width="140" height="100" class="box"/>
  <text x="630" y="240" class="label">测试员</text>
  <text x="630" y="260" class="sublabel">用例编写</text>
  <rect x="300" y="370" width="200" height="80" class="box"/>
  <text x="400" y="405" class="label">人类开发者</text>
  <text x="400" y="425" class="sublabel">(架构主导)</text>
  <line x1="300" y1="450" x2="150" y2="300" class="arrow"/>
  <line x1="340" y1="450" x2="310" y2="300" class="arrow"/>
  <line x1="400" y1="450" x2="470" y2="300" class="arrow"/>
  <line x1="460" y1="450" x2="630" y2="300" class="arrow"/>
  <text x="400" y="510" class="sublabel">人类设定方向与高层架构,智能体团队执行战术性任务</text>
"""


def main():
    print("=== 生成缺失 SVG ===\n")
    write_svg("fig-25-1", "如何访问 AgentSpace", fig_25_1)
    write_svg("fig-25-3", "Google 预制提示库", fig_25_3)
    write_svg("fig-25-4", "自定义智能体提示", fig_25_4)
    write_svg("fig-25-5", "AgentSpace 高级能力", fig_25_5)
    write_svg("fig-25-6", "AgentSpace 聊天界面", fig_25_6)
    write_svg("fig-28-1", "编程专家团队示例", fig_28_1)
    print("\n=== 完成 ===")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
