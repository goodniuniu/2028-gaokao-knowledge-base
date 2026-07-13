# -*- coding: utf-8 -*-
"""
批量生成假期单词复习材料
- 49个日期词表 (.md)
- 49个小测卷 HTML
- 49个答案 HTML
- 1个总入口 HTML
- 更新总计划文件
"""
import os
import sys
import io
from datetime import datetime, timedelta

# 强制UTF-8输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE_DIR = r"C:\Users\user\WPSDrive\203612604\WPS云盘\申悦文档\AI辅助\2028高考知识库\英语\单词复习"
RAW_FILE = os.path.join(BASE_DIR, "高中词汇_乱序_raw.txt")
DATE_DIR = os.path.join(BASE_DIR, "日期词表")
QUIZ_DIR = os.path.join(BASE_DIR, "可打印小测卷")
PLAN_FILE = os.path.join(BASE_DIR, "单词复习总计划.md")
INDEX_FILE = os.path.join(BASE_DIR, "假期复习总入口.html")

START_DATE = datetime(2025, 7, 13)
END_DATE = datetime(2025, 8, 30)
TOTAL_DAYS = 49
TOTAL_WORDS = 6008

WORDS_PER_DAY_FIRST_30 = 123
WORDS_PER_DAY_LAST_19 = 122


def load_words():
    """加载单词数据"""
    words = []
    with open(RAW_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('\t')
            word = parts[0].strip()
            definition = parts[1].strip() if len(parts) > 1 else ""
            words.append((word, definition))
    return words


def format_date_mmdd(date):
    return f"{date.month:02d}月{date.day:02d}日"


def generate_date_wordlists(words):
    """任务1：生成49个日期词表"""
    os.makedirs(DATE_DIR, exist_ok=True)
    word_idx = 0
    files_created = []

    for day in range(TOTAL_DAYS):
        current_date = START_DATE + timedelta(days=day)
        date_str = format_date_mmdd(current_date)
        day_num = day + 1

        if day < 30:
            count = WORDS_PER_DAY_FIRST_30
        else:
            count = WORDS_PER_DAY_LAST_19

        start_idx = word_idx + 1
        end_idx = min(word_idx + count, len(words))
        day_words = words[word_idx:end_idx]
        word_idx = end_idx

        # 构建表格行
        table_rows = []
        for i, (word, definition) in enumerate(day_words, 1):
            table_rows.append(f"| {i} | {word} | {definition} | ☐ |")

        md_content = f"""# 📅 {date_str}（第{day_num}天）| 假期单词复习

> **范围**：第 {start_idx}-{end_idx} 词（共{len(day_words)}词）
> **建议用时**：晨读30分钟 + 晚测15分钟

---

| # | 单词 | 释义 | 自测 ☐ |
|---|------|------|--------|
{chr(10).join(table_rows)}

---

## 当日复习清单
- [ ] 晨读：通读一遍，标记生词
- [ ] 晚测：遮盖释义，自测拼写与词义
- [ ] 订正：错题记入 [错题本](../进度追踪/错题本.md)
"""
        filepath = os.path.join(DATE_DIR, f"{date_str}.md")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(md_content)
        files_created.append(filepath)

    return files_created


def generate_quiz_html(words):
    """任务2：生成小测卷HTML和答案HTML"""
    os.makedirs(QUIZ_DIR, exist_ok=True)
    files_created = []
    word_idx = 0

    for day in range(TOTAL_DAYS):
        current_date = START_DATE + timedelta(days=day)
        date_str = format_date_mmdd(current_date)
        day_num = day + 1

        if day < 30:
            count = WORDS_PER_DAY_FIRST_30
        else:
            count = WORDS_PER_DAY_LAST_19

        start_idx = word_idx
        end_idx = min(word_idx + count, len(words))
        day_words = words[start_idx:end_idx]
        word_idx = end_idx

        # 构建4列表格（小测卷 - 隐藏释义）
        quiz_rows = []
        for i in range(0, len(day_words), 4):
            row_words = day_words[i:i+4]
            cells = []
            for j, (word, _) in enumerate(row_words):
                cells.append(f'<td><div class="word">{word}</div><div class="blank"></div></td>')
            # 补齐4列
            while len(cells) < 4:
                cells.append('<td></td>')
            quiz_rows.append("<tr>" + "".join(cells) + "</tr>")

        quiz_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>{date_str} 单词小测</title>
<style>
  @page {{ size: A4; margin: 15mm; }}
  @media print {{
    .no-print {{ display: none; }}
    .page-break {{ page-break-after: always; }}
    button {{ display: none; }}
  }}
  body {{ font-family: "Microsoft YaHei", "SimSun", sans-serif; font-size: 11pt; margin: 20px; }}
  .header {{ text-align: center; border-bottom: 2px solid #333; padding-bottom: 10px; margin-bottom: 15px; }}
  .header h2 {{ margin: 0 0 10px 0; color: #2c3e50; }}
  .info {{ display: flex; justify-content: space-between; margin: 10px 0; font-size: 12pt; }}
  .info span {{ flex: 1; text-align: center; }}
  table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
  td {{ border: 1px solid #ccc; padding: 8px; width: 25%; vertical-align: top; }}
  .word {{ font-weight: bold; font-size: 12pt; color: #2c3e50; margin-bottom: 4px; }}
  .blank {{ height: 36px; border-bottom: 1px dashed #999; }}
  .footer {{ text-align: center; font-size: 9pt; color: #666; margin-top: 20px; border-top: 1px solid #ddd; padding-top: 10px; }}
  .btn-print {{ background: #3498db; color: white; border: none; padding: 10px 24px; font-size: 14pt; border-radius: 4px; cursor: pointer; margin: 15px auto; display: block; }}
  .btn-print:hover {{ background: #2980b9; }}
  .btn-answer {{ background: #27ae60; color: white; border: none; padding: 8px 18px; font-size: 12pt; border-radius: 4px; cursor: pointer; margin: 10px auto; display: block; text-decoration: none; }}
</style>
</head>
<body>
  <div class="header">
    <h2>📝 单词小测卷</h2>
    <div class="info">
      <span>日期：{date_str}（第{day_num}天）</span>
      <span>姓名：__________</span>
      <span>得分：__________/{len(day_words)}</span>
    </div>
  </div>
  <button class="no-print btn-print" onclick="window.print()">🖨️ 打印小测卷</button>
  <a class="no-print btn-answer" href="{date_str}_答案.html">📖 查看答案</a>
  <table>
{chr(10).join(quiz_rows)}
  </table>
  <div class="footer">2028高考英语词汇假期复习 | 广东新高考</div>
</body>
</html>"""

        # 构建答案版HTML（显示释义）
        answer_rows = []
        for i in range(0, len(day_words), 4):
            row_words = day_words[i:i+4]
            cells = []
            for j, (word, definition) in enumerate(row_words):
                cells.append(f'<td><div class="word">{word}</div><div class="def">{definition}</div></td>')
            while len(cells) < 4:
                cells.append('<td></td>')
            answer_rows.append("<tr>" + "".join(cells) + "</tr>")

        answer_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>{date_str} 单词小测 - 答案</title>
<style>
  @page {{ size: A4; margin: 15mm; }}
  @media print {{
    .no-print {{ display: none; }}
    button {{ display: none; }}
  }}
  body {{ font-family: "Microsoft YaHei", "SimSun", sans-serif; font-size: 10pt; margin: 20px; }}
  .header {{ text-align: center; border-bottom: 2px solid #27ae60; padding-bottom: 10px; margin-bottom: 15px; }}
  .header h2 {{ margin: 0 0 10px 0; color: #27ae60; }}
  .info {{ display: flex; justify-content: space-between; margin: 10px 0; font-size: 12pt; }}
  .info span {{ flex: 1; text-align: center; }}
  table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
  td {{ border: 1px solid #ccc; padding: 6px; width: 25%; vertical-align: top; }}
  .word {{ font-weight: bold; font-size: 11pt; color: #2c3e50; }}
  .def {{ font-size: 9pt; color: #555; margin-top: 4px; line-height: 1.4; }}
  .footer {{ text-align: center; font-size: 9pt; color: #666; margin-top: 20px; border-top: 1px solid #ddd; padding-top: 10px; }}
  .btn-print {{ background: #27ae60; color: white; border: none; padding: 10px 24px; font-size: 14pt; border-radius: 4px; cursor: pointer; margin: 15px auto; display: block; }}
  .btn-print:hover {{ background: #219a52; }}
  .btn-back {{ background: #3498db; color: white; border: none; padding: 8px 18px; font-size: 12pt; border-radius: 4px; cursor: pointer; margin: 10px auto; display: block; text-decoration: none; }}
</style>
</head>
<body>
  <div class="header">
    <h2>📖 单词小测卷 - 参考答案</h2>
    <div class="info">
      <span>日期：{date_str}（第{day_num}天）</span>
      <span>共 {len(day_words)} 词</span>
      <span></span>
    </div>
  </div>
  <button class="no-print btn-print" onclick="window.print()">🖨️ 打印答案</button>
  <a class="no-print btn-back" href="{date_str}_小测.html">📝 返回小测卷</a>
  <table>
{chr(10).join(answer_rows)}
  </table>
  <div class="footer">2028高考英语词汇假期复习 | 广东新高考</div>
</body>
</html>"""

        quiz_path = os.path.join(QUIZ_DIR, f"{date_str}_小测.html")
        answer_path = os.path.join(QUIZ_DIR, f"{date_str}_答案.html")

        with open(quiz_path, 'w', encoding='utf-8') as f:
            f.write(quiz_html)
        with open(answer_path, 'w', encoding='utf-8') as f:
            f.write(answer_html)

        files_created.extend([quiz_path, answer_path])

    return files_created


def generate_index_html():
    """任务3：生成总入口HTML"""
    calendar_cells = []
    for day in range(TOTAL_DAYS):
        current_date = START_DATE + timedelta(days=day)
        date_str = format_date_mmdd(current_date)
        day_num = day + 1

        calendar_cells.append(f"""    <div class="day-card">
      <div class="day-header">{date_str}</div>
      <div class="day-num">第{day_num}天</div>
      <div class="day-links">
        <a href="日期词表/{date_str}.md" class="link-vocab">📖 词表</a>
        <a href="可打印小测卷/{date_str}_小测.html" class="link-quiz">📝 小测</a>
        <a href="可打印小测卷/{date_str}_答案.html" class="link-ans">📋 答案</a>
      </div>
      <div class="day-check">
        <input type="checkbox" id="check{day_num}" onchange="updateProgress()">
        <label for="check{day_num}">已完成</label>
      </div>
    </div>""")

    index_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>2028高考英语词汇假期复习总入口</title>
<style>
  * {{ box-sizing: border-box; }}
  body {{ font-family: "Microsoft YaHei", "SimSun", sans-serif; margin: 0; padding: 0; background: #f5f7fa; color: #333; }}
  .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
  .header {{ text-align: center; padding: 30px 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 12px; margin-bottom: 25px; }}
  .header h1 {{ margin: 0; font-size: 28pt; }}
  .header p {{ margin: 10px 0 0; font-size: 14pt; opacity: 0.9; }}
  .stats {{ display: flex; justify-content: center; gap: 30px; margin: 20px 0; flex-wrap: wrap; }}
  .stat-box {{ background: white; padding: 15px 30px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); text-align: center; }}
  .stat-box .num {{ font-size: 24pt; font-weight: bold; color: #667eea; }}
  .stat-box .label {{ font-size: 11pt; color: #666; }}
  .progress-bar {{ background: #e0e0e0; border-radius: 20px; height: 24px; margin: 15px auto; max-width: 600px; overflow: hidden; }}
  .progress-fill {{ background: linear-gradient(90deg, #667eea, #764ba2); height: 100%; width: 0%; border-radius: 20px; transition: width 0.5s; text-align: center; color: white; line-height: 24px; font-size: 11pt; }}
  .calendar {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 12px; margin-top: 20px; }}
  .day-card {{ background: white; border-radius: 10px; padding: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.08); transition: transform 0.2s; }}
  .day-card:hover {{ transform: translateY(-3px); box-shadow: 0 4px 12px rgba(0,0,0,0.15); }}
  .day-header {{ font-weight: bold; font-size: 13pt; color: #2c3e50; text-align: center; }}
  .day-num {{ font-size: 10pt; color: #888; text-align: center; margin: 4px 0; }}
  .day-links {{ display: flex; flex-direction: column; gap: 4px; margin: 8px 0; }}
  .day-links a {{ text-decoration: none; padding: 5px 8px; border-radius: 5px; font-size: 10pt; text-align: center; }}
  .link-vocab {{ background: #e3f2fd; color: #1976d2; }}
  .link-quiz {{ background: #fff3e0; color: #f57c00; }}
  .link-ans {{ background: #e8f5e9; color: #388e3c; }}
  .day-check {{ text-align: center; margin-top: 6px; font-size: 10pt; }}
  .day-check input {{ cursor: pointer; }}
  .btn-bar {{ text-align: center; margin: 20px 0; }}
  .btn-bar button {{ background: #667eea; color: white; border: none; padding: 12px 30px; font-size: 13pt; border-radius: 6px; cursor: pointer; margin: 5px; }}
  .btn-bar button:hover {{ background: #5a6fd6; }}
  .footer {{ text-align: center; margin-top: 30px; padding: 15px; color: #888; font-size: 10pt; }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>📚 2028高考英语词汇假期复习</h1>
    <p>假期：2025年7月13日 ~ 8月30日 | 共49天 | 6008词</p>
  </div>

  <div class="stats">
    <div class="stat-box">
      <div class="num" id="totalDays">49</div>
      <div class="label">总天数</div>
    </div>
    <div class="stat-box">
      <div class="num" id="completedDays">0</div>
      <div class="label">已完成</div>
    </div>
    <div class="stat-box">
      <div class="num" id="remainingDays">49</div>
      <div class="label">剩余天数</div>
    </div>
  </div>

  <div class="progress-bar">
    <div class="progress-fill" id="progressFill">0%</div>
  </div>

  <div class="btn-bar">
    <button onclick="window.print()">🖨️ 打印计划表</button>
    <button onclick="resetProgress()">🔄 重置进度</button>
  </div>

  <div class="calendar">
{chr(10).join(calendar_cells)}
  </div>

  <div class="footer">
    2028高考英语词汇假期复习 | 广东新高考 | 打印建议使用Chrome浏览器
  </div>
</div>

<script>
function updateProgress() {{
  const checkboxes = document.querySelectorAll('input[type="checkbox"]');
  const checked = document.querySelectorAll('input[type="checkbox"]:checked');
  const completed = checked.length;
  const total = checkboxes.length;
  const percent = Math.round((completed / total) * 100);

  document.getElementById('completedDays').textContent = completed;
  document.getElementById('remainingDays').textContent = total - completed;
  const fill = document.getElementById('progressFill');
  fill.style.width = percent + '%';
  fill.textContent = percent + '%';

  // 保存到localStorage
  const saved = [];
  checkboxes.forEach((cb, idx) => {{ if (cb.checked) saved.push(idx); }});
  localStorage.setItem('vocab_progress', JSON.stringify(saved));
}}

function resetProgress() {{
  if (!confirm('确定要重置所有进度吗？')) return;
  document.querySelectorAll('input[type="checkbox"]').forEach(cb => cb.checked = false);
  updateProgress();
}}

function loadProgress() {{
  const saved = localStorage.getItem('vocab_progress');
  if (saved) {{
    const indices = JSON.parse(saved);
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    indices.forEach(i => {{ if (checkboxes[i]) checkboxes[i].checked = true; }});
    updateProgress();
  }}
}}

window.onload = loadProgress;
</script>
</body>
</html>"""

    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(index_html)
    return INDEX_FILE


def update_plan_file():
    """任务4：更新总计划文件"""
    # 生成49天计划表
    plan_rows = []
    for day in range(TOTAL_DAYS):
        current_date = START_DATE + timedelta(days=day)
        date_str = format_date_mmdd(current_date)
        day_num = day + 1

        if day < 30:
            count = WORDS_PER_DAY_FIRST_30
            start_w = day * WORDS_PER_DAY_FIRST_30 + 1
            end_w = (day + 1) * WORDS_PER_DAY_FIRST_30
        else:
            count = WORDS_PER_DAY_LAST_19
            start_w = 30 * WORDS_PER_DAY_FIRST_30 + (day - 30) * WORDS_PER_DAY_LAST_19 + 1
            end_w = 30 * WORDS_PER_DAY_FIRST_30 + (day - 30 + 1) * WORDS_PER_DAY_LAST_19

        plan_rows.append(
            f"| {date_str} | 第{day_num}天 | 第{start_w}-{end_w}词 | {count}词 | [词表](日期词表/{date_str}.md) | [小测](可打印小测卷/{date_str}_小测.html) | [答案](可打印小测卷/{date_str}_答案.html) | | | | |"
        )

    plan_content = f"""# 高考英语单词假期复习总计划

> **目标**：假期完成高中英语词汇（6008词）一轮复习
> **适用**：2028广东新高考英语（新高考Ⅰ卷笔试 + 广东听说）
> **假期**：2025年7月13日 ~ 8月30日，共49天
> **策略**：新学+滚动复习，配合每日小测

---

## 一、复习计划表（按日期排列）

| 日期 | 天数 | 词汇范围 | 词数 | 词表 | 小测卷 | 答案 | 自测正确率 | 小测正确率 | 完成标记 |
|------|------|----------|------|------|--------|------|-----------|-----------|----------|
{chr(10).join(plan_rows)}

---

## 二、每日学习流程（约30-45分钟）

### 早晨：新学（15分钟）
1. 打开当天分组词表
2. 快速浏览当天单词，重点标记不熟悉的词
3. 对不熟的词抄写2遍+朗读3遍

### 中午：自测（10分钟）
1. 遮住释义，看单词说中文意思
2. 能秒反应的画 ✅，犹豫的画 ⚠️，不会的画 ❌
3. 重点复习 ⚠️ 和 ❌ 的词

### 晚上：小测（10-15分钟）
1. 打印或打开当天小测卷（抽全部当天词汇）
2. 对照答案批改，记录正确率
3. 把错题词加入"错题本"

---

## 三、快速导航

- 📅 [假期复习总入口](假期复习总入口.html) - 日历视图+进度追踪
- 📁 [日期词表目录](日期词表/)
- 📝 [可打印小测卷目录](可打印小测卷/)
- 📊 [进度追踪/错题本](进度追踪/错题本.md)

---

## 四、广东高考特别提示

- 广东新高考Ⅰ卷英语笔试**不含听力**，词汇考查侧重**阅读理解和写作应用**
- 写作（应用文+读后续写）需要**主动词汇**（能拼写、能造句），不只是认识
- 建议每天选5个词**造句**，训练写作应用能力
- **广东听说考试**（20分）需要口语词汇发音准确，建议每天朗读当天词汇

---

> 每周日复盘一次，统计本周正确率趋势，调整复习策略。
"""

    with open(PLAN_FILE, 'w', encoding='utf-8') as f:
        f.write(plan_content)
    return PLAN_FILE


def main():
    print("=" * 60)
    print("开始生成假期单词复习材料")
    print("=" * 60)

    print("\n[1/4] 加载单词数据...")
    words = load_words()
    print(f"  ✓ 共加载 {len(words)} 个单词")

    print("\n[2/4] 生成49个日期词表...")
    wordlist_files = generate_date_wordlists(words)
    print(f"  ✓ 已生成 {len(wordlist_files)} 个词表文件")

    print("\n[3/4] 生成49个小测卷HTML + 49个答案HTML...")
    quiz_files = generate_quiz_html(words)
    print(f"  ✓ 已生成 {len(quiz_files)} 个HTML文件")

    print("\n[4/4] 生成总入口页面和更新总计划...")
    index_file = generate_index_html()
    plan_file = update_plan_file()
    print(f"  ✓ 总入口页面: {index_file}")
    print(f"  ✓ 总计划文件: {plan_file}")

    print("\n" + "=" * 60)
    print("全部生成完成！")
    print("=" * 60)
    print(f"\n生成文件统计：")
    print(f"  - 日期词表 (.md): {len(wordlist_files)} 个")
    print(f"  - 小测卷+答案 (.html): {len(quiz_files)} 个")
    print(f"  - 总入口页面: 1 个")
    print(f"  - 总计划文件: 1 个")
    print(f"  - 总计: {len(wordlist_files) + len(quiz_files) + 2} 个文件")


if __name__ == "__main__":
    main()
