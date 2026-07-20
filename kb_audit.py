#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2028高考知识库 · 全库扫描审计脚本
扫描所有知识卡片，输出权威统计数据（JSON + 控制台摘要）
口径：知识卡片 = 六科 + 方法维度的学习卡片（不含英语单词复习词表/小测卷）
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).parent
SUBJECTS = ["语文", "数学", "英语", "物理", "化学", "生物", "方法"]
DIMENSIONS = ["核心知识网络", "典型题型与方法", "易错警示与辨析", "素材与拓展",
              "学习方法", "考试策略", "心理建设", "生理管理"]
EXCLUDE_NAMES = {"index.md"}
EXCLUDE_PREFIX = ("索引_",)


def parse_card(path: Path):
    """解析单张卡片的元数据字段"""
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-8", errors="replace")

    def field(name):
        m = re.search(r"\|\s*\*\*" + name + r"\*\*\s*\|\s*(.+?)\s*\|", text)
        return m.group(1).strip() if m else ""

    title_m = re.search(r"^#\s+(.+)$", text, re.M)
    title = title_m.group(1).strip() if title_m else path.stem

    status_raw = field("状态")
    if "✅" in status_raw or "已掌握" in status_raw:
        status = "已掌握"
    elif "❌" in status_raw or "未理解" in status_raw:
        status = "未理解"
    else:
        status = "待强化"

    return {
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "title": title,
        "source": field("来源"),
        "time_tag": field("时间标签"),
        "difficulty": field("难度"),
        "status": status,
        "exam_source": field("试卷来源"),
    }


def main():
    cards = []
    for subject in SUBJECTS:
        sdir = ROOT / subject
        if not sdir.exists():
            continue
        for md in sorted(sdir.rglob("*.md")):
            rel = md.relative_to(ROOT)
            parts = rel.parts
            # 排除英语单词复习系统
            if "单词复习" in parts:
                continue
            if md.name in EXCLUDE_NAMES or md.name.startswith(EXCLUDE_PREFIX):
                continue
            card = parse_card(md)
            # 从路径推断科目与维度
            card["subject"] = parts[0]
            card["dimension"] = parts[1] if len(parts) > 2 else "(根目录)"
            cards.append(card)

    # 统计
    stats = {}
    for c in cards:
        s = stats.setdefault(c["subject"], {"total": 0, "已掌握": 0, "待强化": 0, "未理解": 0,
                                            "dims": {d: 0 for d in DIMENSIONS}})
        s["total"] += 1
        s[c["status"]] += 1
        if c["dimension"] in s["dims"]:
            s["dims"][c["dimension"]] += 1
        else:
            s["dims"].setdefault("(其他)", 0)
            s["dims"]["(其他)"] += 1

    # 英语单词复习系统单独统计
    vocab = {}
    vdir = ROOT / "英语" / "单词复习"
    if vdir.exists():
        vocab["日期词表_md"] = len(list((vdir / "日期词表").glob("*.md"))) if (vdir / "日期词表").exists() else 0
        vocab["分组词表_md"] = len(list((vdir / "分组词表").glob("*.md"))) if (vdir / "分组词表").exists() else 0
        vocab["每日任务_md"] = len(list((vdir / "每日任务").glob("*.md"))) if (vdir / "每日任务").exists() else 0
        vocab["小测卷_html"] = len(list((vdir / "小测卷").glob("*.html"))) if (vdir / "小测卷").exists() else 0
        vocab["可打印小测卷_html"] = len(list((vdir / "可打印小测卷").glob("*.html"))) if (vdir / "可打印小测卷").exists() else 0

    # HTML 覆盖情况：有 md 无 html 的卡片
    missing_html = []
    for c in cards:
        html = ROOT / (c["path"][:-3] + ".html")
        if not html.exists():
            missing_html.append(c["path"])

    total = len(cards)
    st_total = {"已掌握": 0, "待强化": 0, "未理解": 0}
    for s in stats.values():
        for k in st_total:
            st_total[k] += s[k]

    result = {
        "total_cards": total,
        "status_total": st_total,
        "by_subject": stats,
        "vocab_system": vocab,
        "missing_html": missing_html,
        "cards": cards,
    }
    out = ROOT / "复盘追踪" / "_scan_result.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=" * 60)
    print(f"知识卡片总数（不含单词复习系统）: {total}")
    print(f"状态: 已掌握 {st_total['已掌握']} / 待强化 {st_total['待强化']} / 未理解 {st_total['未理解']}")
    print("-" * 60)
    for sub in SUBJECTS:
        if sub not in stats:
            print(f"{sub}: 0 张")
            continue
        s = stats[sub]
        dims = " | ".join(f"{k}:{v}" for k, v in s["dims"].items() if v)
        print(f"{sub}: 共{s['total']} (掌握{s['已掌握']}/强化{s['待强化']}/未懂{s['未理解']})  {dims}")
    print("-" * 60)
    print(f"单词复习系统: {vocab}")
    print(f"缺少HTML版本的卡片: {len(missing_html)} 张")
    for p in missing_html:
        print(f"  - {p}")
    print(f"\n详细结果已写入: {out}")


if __name__ == "__main__":
    main()
