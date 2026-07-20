#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
根据 kb_audit.py 的扫描结果重建《知识掌握状态表.md》
- 全量覆盖所有知识卡片（按科目分区、连续编号）
- 保留旧表中已有人工备注与复盘日期（按卡片名称匹配）
- 保留图例、广东卷追踪、复盘记录、周复盘清单等静态章节
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).parent
SCAN = ROOT / "复盘追踪" / "_scan_result.json"
OLD = ROOT / "复盘追踪" / "知识掌握状态表.md"

SUBJECT_ORDER = ["语文", "数学", "英语", "物理", "化学", "生物", "方法"]
DIM_ORDER = ["核心知识网络", "典型题型与方法", "易错警示与辨析", "素材与拓展",
             "学习方法", "考试策略", "心理建设", "生理管理", "(根目录)"]
SUBJECT_TITLE = {
    "语文": "语文（新高考Ⅰ卷·广东）",
    "数学": "数学（新高考Ⅰ卷·广东）",
    "英语": "英语（新高考Ⅰ卷·广东 + 广东听说）",
    "物理": "物理（广东省自主命题）",
    "化学": "化学（广东省自主命题）",
    "生物": "生物（广东省自主命题）",
    "方法": "方法（跨学科通用学习策略）",
}
STATUS_ICON = {"已掌握": "✅已掌握", "待强化": "⚠️待强化", "未理解": "❌未理解"}


def norm(s):
    return re.sub(r"[\s：:（）()·\-—_、，,。.]", "", s)


def load_old_notes():
    """从旧状态表提取 卡片名称 -> (备注, 复盘日期)"""
    notes = {}
    if not OLD.exists():
        return notes
    text = OLD.read_text(encoding="utf-8")
    for line in text.splitlines():
        m = re.match(r"\|\s*\d+\s*\|(.+?)\|(.+?)\|(.+?)\|(.+?)\|(.+?)\|(.+?)\|(.+?)\|(.+?)\|", line)
        if not m:
            continue
        name = m.group(1).strip()
        review_date = m.group(7).strip()
        note = m.group(8).strip()
        notes[norm(name)] = (note, review_date)
    return notes


def main():
    data = json.loads(SCAN.read_text(encoding="utf-8"))
    cards = data["cards"]
    old_notes = load_old_notes()

    def sort_key(c):
        return (SUBJECT_ORDER.index(c["subject"]),
                DIM_ORDER.index(c["dimension"]) if c["dimension"] in DIM_ORDER else 99,
                c["path"])

    cards.sort(key=sort_key)

    matched, total_notes = 0, len(old_notes)
    sections = []
    idx = 0
    for sub in SUBJECT_ORDER:
        sub_cards = [c for c in cards if c["subject"] == sub]
        if not sub_cards:
            continue
        lines = [f"## {'三四五六七八九'[SUBJECT_ORDER.index(sub)]}、{SUBJECT_TITLE[sub]}", "",
                 "| 序号 | 卡片名称 | 维度 | 时间标签 | 难度 | 状态 | 来源 | 复盘日期 | 备注 |",
                 "|------|----------|------|----------|------|------|------|----------|------|"]
        for c in sub_cards:
            idx += 1
            key = norm(c["title"])
            note, review = "", "—"
            # 精确匹配，其次互包含匹配
            hit = old_notes.get(key)
            if not hit:
                for k, v in old_notes.items():
                    if k and (k in key or key in k):
                        hit = v
                        break
            if hit:
                note, review = hit
                matched += 1
            tag = c["time_tag"] or ("#" + c["path"].split("_")[0] if "_" in c["path"] else "—")
            src = c["source"][:40] + ("…" if len(c["source"]) > 40 else "")
            lines.append(
                f"| {idx} | {c['title']} | {c['dimension']} | {tag} | {c['difficulty'] or '—'} "
                f"| {STATUS_ICON[c['status']]} | {src or '—'} | {review} | {note} |")
        sections.append("\n".join(lines))

    # 统计
    st = data["status_total"]
    guangdong = sum(1 for c in cards if "广东" in (c.get("exam_source", "") + c.get("source", "")))

    header = f"""# 📊 知识掌握状态表

> 本表用于追踪每张知识卡片的掌握状态，支持每周复盘。
> **更新规则**：每次复盘后更新，重点关注 `#广东特色` `#广东卷` 来源的卡片掌握情况。
> **重建说明**：2026-07-20 由 `kb_audit.py` + `build_status_table.py` 全量重建，覆盖全部 {data['total_cards']} 张知识卡片（旧表仅覆盖约30张），已保留原有人工备注 {matched} 条。

---

## 一、状态图例

| 状态 | 图标 | 含义 |
|------|------|------|
| 已掌握 | ✅ | 完全理解，能独立解题，无盲区 |
| 待强化 | ⚠️ | 基本理解，偶有失误或速度偏慢 |
| 未理解 | ❌ | 概念模糊，无法独立解题，需重学 |

---

## 二、广东卷重点追踪

> 复盘时需重点关注以下标签的卡片（当前全库含"广东"来源的卡片共 **{guangdong}** 张）：

| 标签 | 适用科目 | 追踪要点 |
|------|----------|----------|
| `#广东选择性考试` | 物化生 | 广东自主命题真题，必须掌握 |
| `#新高考Ⅰ卷·广东` | 语数英 | 广东考区真题，必须掌握 |
| `#广东特色` | 物化生 | 情境化命题、本地科技素材 |
| `#广东情境` | 物理 | 情境化物理模型提取 |
| `#广东工艺` | 化学 | 工艺流程类题目 |
| `#广东长句` | 生物 | 长句表达类题目 |
| `#广东听说` | 英语 | 人机对话听说考试 |
| `#广东思辨` | 语文 | 作文思辨性特征 |

---

## 三、各科状态分布总览（2026-07-20 校准）

| 科目 | 总卡片数 | 已掌握 ✅ | 待强化 ⚠️ | 未理解 ❌ |
|------|----------|----------|----------|----------|
"""
    for sub in SUBJECT_ORDER:
        s = data["by_subject"].get(sub)
        if not s:
            continue
        header += f"| {sub} | {s['total']} | {s['已掌握']} | {s['待强化']} | {s['未理解']} |\n"
    header += f"| **合计** | **{data['total_cards']}** | **{st['已掌握']}** | **{st['待强化']}** | **{st['未理解']}** |\n"
    header += "\n> ⚠️ 注意：全部卡片仍处于待强化状态，尚无一张确认掌握。建议尽快进行首次正式复盘，让状态产生区分度。\n\n---\n"

    footer = f"""
---

## 十、复盘记录

| 复盘次数 | 复盘日期 | 新增卡片数 | 广东卷卡片数 | 状态变更数 | 重点复习 |
|----------|----------|------------|--------------|------------|----------|
| 1 | 2025-06-26 | 12 | 12 | 0 | 物理4张+化学4张+生物4张核心知识网络入库，重点补齐物化生基础短板 |
| 2 | 2025-06-26 | 2 | 0 | 0 | 数学一题多解思维卡+方法体系21天自救计划入库，完善应试策略层 |
| 3 | 2026-07-20 | 审计校准 | {guangdong} | 0 | 状态表全量重建（92张全覆盖），统一统计口径，修正时间轴 |

---

## 十一、周复盘检查清单

每次复盘时，逐项确认：

- [ ] 浏览本周新增的知识卡片
- [ ] 回顾上周标记为 ❌未理解 的卡片，确认是否已掌握
- [ ] 回顾上周标记为 ⚠️待强化 的卡片，确认是否需要继续强化
- [ ] 检查是否有卡片需要从 ✅ 降级到 ⚠️（遗忘）
- [ ] **重点检查广东卷相关卡片**：`#广东选择性考试` `#新高考Ⅰ卷·广东` `#广东特色` 等
- [ ] **英语听说检查**：确认 `#广东听说` 卡片是否按计划复习
- [ ] **等级赋分提醒**：物化生科目确认基础题是否扎实（赋分制下基础题差距会被放大）
- [ ] 统计各科状态分布，更新 [00_知识库总索引.md](../00_知识库总索引.md)
- [ ] 制定下周重点复习计划（针对 ❌ 和 ⚠️，优先广东卷）
- [ ] 在「复盘记录」中新增一行记录

---

> 🔔 提示：每周复盘提醒已设置，请保持知识库动态更新，关注广东卷命题特色，让积累真正转化为能力。
> 🔧 本表可由 `python build_status_table.py` 重新生成（基于 `python kb_audit.py` 的扫描结果）。
"""

    out = header + "\n" + "\n\n---\n\n".join(sections) + "\n" + footer
    OLD.write_text(out, encoding="utf-8")
    print(f"状态表已重建: 共 {idx} 张卡片，匹配保留旧备注 {matched}/{total_notes} 条")
    print(f"含广东来源卡片: {guangdong} 张")


if __name__ == "__main__":
    main()
