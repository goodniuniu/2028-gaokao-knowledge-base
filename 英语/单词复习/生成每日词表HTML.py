# -*- coding: utf-8 -*-
"""
生成每日词表 HTML（助记版）

- 内容源：日期词表/*.md（49 个，md 不改动）
- 产物：  日期词表/{date}.html（同名，单文件内联 CSS/JS）
- 特性：  词性彩色标签 / 词根词缀拆解 / 当日词族速览 /
          主动回忆自测（释义默认隐藏）/ 掌握标记（localStorage 持久化）

用法：python 生成每日词表HTML.py
说明：路径一律相对脚本所在目录，严禁硬编码绝对路径。
"""
import io
import json
import os
import re
import sys
from html import escape

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATE_DIR = os.path.join(BASE_DIR, "日期词表")
QUIZ_DIR = os.path.join(BASE_DIR, "可打印小测卷")

# ---------------------------------------------------------------- 词性标签
POS_RE = re.compile(r'(?<![A-Za-z])(abbr|adj|adv|art|aux|conj|int|num|prep|pron|vi|vt|n|v)\.')
POS_CLASS = {
    "n": "pos-n",
    "v": "pos-v", "vt": "pos-v", "vi": "pos-v",
    "adj": "pos-adj", "adv": "pos-adv",
    "prep": "pos-gray", "conj": "pos-gray", "art": "pos-gray", "aux": "pos-gray",
    "num": "pos-num", "int": "pos-int", "abbr": "pos-abbr", "pron": "pos-pron",
}

# ---------------------------------------------------------------- 词根词缀表
# (前缀, 含义)；按长度从长到短匹配
PREFIXES = [
    ("inter", "相互"), ("trans", "跨越"), ("under", "不足/在下"), ("super", "超"),
    ("fore", "预先"), ("anti", "反对"), ("over", "过度"), ("dis", "不/相反"),
    ("mis", "错误"), ("pre", "预先"), ("sub", "下/次"),
    ("un", "不/非"), ("re", "再/重新"),
    ("in", "不/向内"), ("im", "不/向内"), ("il", "不/向内"), ("ir", "不/向内"),
    ("co", "共同"), ("ex", "向外"), ("en", "使"), ("em", "使"), ("be", "使"),
    ("a", "处于…状态"),
]
# 前缀匹配要求的最短剩余词干长度（避免 under→un+der 这类误判）
PREFIX_MIN_REST = {"a": 4, "un": 4}
# 虽以某前缀开头但不应拆解的常见词
PREFIX_EXC = {
    "under", "uncle", "until", "union", "unit", "united", "unity",
    "universe", "university", "index", "insect", "inner", "image",
    "imagine", "iron", "island", "into",
}
# a- 前缀误判率极高（although/anything/available…），改为白名单制：
# 只有确认是 a-（处于…状态）构词的词才拆解
PREFIX_A_WHITELIST = {
    "about", "above", "abroad", "ahead", "alike", "alive", "along",
    "aloud", "among", "around", "aside", "asleep", "awake", "aware",
    "away", "ashamed", "apart", "await", "arise", "arouse", "amid",
    "amuse", "ago", "alight", "afar", "astray", "afar", "afresh", "anew",
}
# co-/en-/em- 同样误判率高（cookie/cooker、enter/engine 等都不是前缀词），
# 改为白名单制：仅列出的确认为该前缀构词的词才拆解
PREFIX_CO_WHITELIST = {
    "cooperate", "cooperation", "coworker", "coexist", "coexistence",
    "coincide", "coincidence", "coordinate", "coordination", "coauthor",
    "cohere", "coherent", "cohesion", "coeducational",
}
PREFIX_EN_WHITELIST = {
    "enable", "encircle", "enclose", "encounter", "encourage",
    "encouragement", "enforce", "engage", "engagement", "enhance",
    "enjoy", "enlarge", "enrich", "enroll", "enrol", "ensure",
    "entitle", "environment",
    "employ", "employer", "employee", "employment", "embrace",
    "embarrass", "embarrassed", "embody", "empower",
}
# be- 例外：bed+ings 这类合成词不应拆
PREFIX_EXC |= {"beddings", "bedclothes", "beauty", "benefit", "belly",
               "beancurd", "better"}
# re-/pre- 高频误判词（reg-/rect- 为词根、pre 为词干一部分）
PREFIX_EXC |= {
    "regular", "rectangle", "ready", "real", "really", "reason", "recent",
    "region", "register", "religion", "restaurant", "realize", "realise",
    "regulation", "regulate", "regulator", "republic", "reading", "reach",
    "precious", "pretty", "pressure",
}
# in-/fore-/dis-/ex- 高频误判词
PREFIX_EXC |= {
    "india", "indian", "intelligence", "industry", "industrial",
    "forever", "foreign", "forest",
    "district", "extra",
}

# (后缀, 含义)；按长度从长到短匹配
SUFFIXES = [
    ("tion", "名词：动作/状态"), ("sion", "名词：动作/状态"),
    ("ment", "名词"), ("ness", "名词：性质"),
    ("ship", "名词：关系/状态"), ("hood", "名词：状态"),
    ("able", "形容词：可…的"), ("ible", "形容词：可…的"),
    ("less", "形容词：无/不"), ("ward", "副词：向…"),
    ("teen", "十几"), ("ful", "形容词：充满"), ("ous", "形容词"),
    ("ive", "形容词"), ("ity", "名词：性质"),
    ("ize", "动词：使…化"), ("ise", "动词：使…化"), ("ify", "动词：使…"),
    ("ist", "名词：人"), ("ism", "名词：主义"),
    ("al", "形容词"), ("ic", "形容词"), ("ly", "副词"),
    ("en", "动词：使变得"), ("th", "序数词"), ("ty", "名词：性质"),
    ("er", "名词：人/物"), ("or", "名词：人/物"),
]
# 以某后缀结尾但不应拆解的常见词（启发式纠错表，可按需补充）
SUFFIX_EXC = {
    "er": {"butter", "letter", "water", "paper", "offer", "dinner", "summer",
           "winter", "later", "either", "neither", "other", "mother", "father",
           "brother", "sister", "ever", "never", "over", "however", "remember",
           "under", "after", "number", "member", "rather", "whether", "together",
           "weather", "matter", "better", "center", "centre", "meter", "metre",
           "liter", "litre", "september", "october", "november", "december",
           "powder", "consider", "suffer", "chapter", "soldier", "officer",
           "leather", "character", "whenever", "whatever", "wherever",
           "whichever", "shelter", "differ", "latter", "hunger", "master",
           "wander", "supper", "partner", "saucer", "deliver", "laughter",
           "minister", "gather", "danger", "wonder", "litter", "answer",
           "whisper", "murder", "another", "finger", "manner", "pepper",
           "altogether", "ladder", "cancer", "corner", "border", "flower",
           "feather", "helicopter", "newspaper", "proper", "bitter",
           "shoulder", "quarter", "clever", "leftover", "easter", "grocer",
           "greengrocer", "carpenter", "hamburger", "butcher", "shower",
           "headmaster", "granddaughter"},
    "or": {"door", "floor", "error", "mirror", "horror", "terror", "color",
           "favor", "senior", "junior"},
    "ly": {"family", "july", "reply", "only", "early", "belly", "jelly",
           "silly", "holy", "fly", "smelly", "multiply"},
    "en": {"listen", "often", "sudden", "garden", "heaven", "golden", "broken",
           "spoken", "children", "kitchen", "chicken", "women", "eleven",
           "taken", "given", "written", "driven", "chosen", "fallen", "eaten",
           "beaten", "stolen", "frozen", "hidden", "ridden", "bitten"},
    "th": {"beneath", "month", "with", "both", "earth", "death", "worth",
           "truth", "health", "wealth", "path", "math", "maths", "cloth",
           "breath", "smooth", "tooth", "youth", "mouth", "south", "north"},
    "al": {"several", "animal", "capital", "hospital", "metal", "total",
           "vital", "final", "local", "royal", "legal", "usual", "special",
           "festival", "appeal", "cathedral"},
    "ic": {"music", "topic", "picnic", "panic", "clinic", "attic", "comic",
           "garlic", "arctic", "catholic", "pacific", "arithmetic"},
    "ist": {"twist", "fist", "mist", "wrist", "exist", "assist", "resist"},
    "ward": {"steward", "award", "reward", "coward"},
    "teen": {"canteen"},
    "ty": {"anxiety", "guilty", "beauty"},
    "tion": {"question", "mention"},
    "ment": {"element", "moment", "garment", "monument"},
    "ive": {"forgive", "survive"},
}


def analyze_affixes(word):
    """返回 (prefix_tuple, stem, suffix_tuple)；匹配不到返回 (None, word, None)。"""
    w = word.lower()
    if not w.isalpha():
        return None, word, None

    pre = None
    rest = w
    if len(w) >= 5 and w not in PREFIX_EXC:
        for p, meaning in PREFIXES:  # 已按长度降序
            min_rest = PREFIX_MIN_REST.get(p, 3)
            if not (w.startswith(p) and len(w) - len(p) >= min_rest):
                continue
            if p == "a" and w not in PREFIX_A_WHITELIST:
                continue
            if p == "co" and w not in PREFIX_CO_WHITELIST:
                continue
            if p in ("en", "em") and w not in PREFIX_EN_WHITELIST:
                continue
            pre = (p, meaning)
            rest = w[len(p):]
            break

    suf = None
    stem = rest
    min_word_len = 5 if pre else 6  # 有前缀时剩余部分可略短
    if len(rest) >= min_word_len:
        for s, meaning in SUFFIXES:  # 已按长度降序
            if (len(rest) - len(s) >= 3 and rest.endswith(s)
                    and w not in SUFFIX_EXC.get(s, ())):
                suf = (s, meaning)
                stem = rest[:len(rest) - len(s)]
                break

    return pre, stem, suf


def mnemonic_html(word):
    """生成助记拆解 HTML；匹配不到返回空串。"""
    pre, stem, suf = analyze_affixes(word)
    if not pre and not suf:
        return ""
    parts = []
    if pre:
        parts.append(f'<span class="affix affix-pre">{escape(pre[0])}-</span>'
                     f'<span class="affix-mean">({escape(pre[1])})</span>')
    parts.append(f'<span class="stem">{escape(stem)}</span>')
    if suf:
        parts.append(f'<span class="affix affix-suf">-{escape(suf[0])}</span>'
                     f'<span class="affix-mean">({escape(suf[1])})</span>')
    return '<span class="plus"> + </span>'.join(parts)


def markup_definition(def_escaped):
    """把释义中的词性缩写渲染成彩色标签，返回 (HTML, 有序去重词性列表)。"""
    tags = []

    def repl(m):
        t = m.group(1)
        if t not in tags:
            tags.append(t)
        return f'<span class="pos {POS_CLASS[t]}">{t}.</span>'

    return POS_RE.sub(repl, def_escaped), tags


# ---------------------------------------------------------------- md 解析
TITLE_RE = re.compile(r'^#\s*📅\s*(\d+月\d+日)（第(\d+)天）')
RANGE_RE = re.compile(r'第\s*(\d+)-(\d+)\s*词（共(\d+)词）')


def parse_md(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()

    date_str = day_num = None
    range_text = ""
    words = []  # (num, word, definition)

    for line in lines:
        m = TITLE_RE.match(line)
        if m:
            date_str, day_num = m.group(1), int(m.group(2))
        m = RANGE_RE.search(line)
        if m and not range_text:
            range_text = f"第 {m.group(1)}-{m.group(2)} 词（共{m.group(3)}词）"
        if line.startswith('|'):
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            if len(cells) >= 3 and cells[0].isdigit():
                words.append((int(cells[0]), cells[1], cells[2]))

    if not date_str or not words:
        raise ValueError(f"解析失败: {path}")
    return date_str, day_num, range_text, words


# ---------------------------------------------------------------- HTML 模板
PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__DATE__（第__DAY__天）单词词表 | 假期单词复习</title>
<style>
  * { box-sizing: border-box; }
  body { font-family: "Microsoft YaHei", "SimSun", sans-serif; margin: 0; background: #f5f7fa; color: #333; }
  .container { max-width: 1100px; margin: 0 auto; padding: 16px; }
  .header { text-align: center; padding: 26px 16px 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 12px; margin-bottom: 16px; }
  .header h1 { margin: 0; font-size: 22pt; }
  .header .sub { margin: 8px 0 0; font-size: 11pt; opacity: 0.9; }
  .nav-links { display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; margin: 14px 0 4px; }
  .nav-links a { text-decoration: none; padding: 6px 14px; border-radius: 6px; font-size: 10.5pt; background: rgba(255,255,255,0.18); color: #fff; border: 1px solid rgba(255,255,255,0.35); }
  .nav-links a:hover { background: rgba(255,255,255,0.32); }
  .mark-stats { display: flex; justify-content: center; gap: 14px; flex-wrap: wrap; margin: 10px 0 0; font-size: 10.5pt; }
  .mark-stats span { background: rgba(255,255,255,0.18); padding: 4px 12px; border-radius: 20px; }

  .toolbar { display: flex; gap: 8px; flex-wrap: wrap; align-items: center; background: white; padding: 10px 14px; border-radius: 10px; box-shadow: 0 2px 6px rgba(0,0,0,0.08); margin-bottom: 14px; }
  .toolbar button, .toolbar select { font-size: 10.5pt; padding: 6px 12px; border-radius: 6px; border: 1px solid #d0d0e0; background: #f6f7ff; color: #444; cursor: pointer; }
  .toolbar button:hover { background: #e8eaff; }
  .toolbar .btn-primary { background: #667eea; color: white; border-color: #667eea; }
  .toolbar .btn-primary:hover { background: #5a6fd6; }
  .toolbar .spacer { flex: 1; }

  .family-section { background: white; border-radius: 10px; box-shadow: 0 2px 6px rgba(0,0,0,0.08); padding: 14px 16px; margin-bottom: 14px; }
  .family-section h2 { margin: 0 0 10px; font-size: 13pt; color: #2c3e50; }
  .family-chips { display: flex; flex-wrap: wrap; gap: 8px; }
  .chip { background: linear-gradient(135deg, #eef1ff 0%, #f6efff 100%); border: 1px solid #d5dbf5; border-radius: 8px; padding: 8px 12px; font-size: 10pt; max-width: 100%; }
  .chip .chip-title { font-weight: bold; color: #5a6fd6; }
  .chip .chip-words { color: #555; }

  .table-wrap { overflow-x: auto; background: white; border-radius: 10px; box-shadow: 0 2px 6px rgba(0,0,0,0.08); }
  table { width: 100%; border-collapse: collapse; font-size: 10.5pt; }
  th { background: #667eea; color: white; padding: 9px 8px; text-align: left; font-size: 10pt; white-space: nowrap; }
  td { border-bottom: 1px solid #eee; padding: 8px; vertical-align: top; }
  tbody tr { cursor: pointer; }
  tbody tr:hover { background: #f4f6ff; }
  tbody tr.mark-know { background: #f2fbf4; }
  tbody tr.mark-know:hover { background: #e6f7ea; }
  tbody tr.mark-fuzzy { background: #fffaec; }
  tbody tr.mark-fuzzy:hover { background: #fff5d8; }
  tbody tr.mark-unknown { background: #fdf1f1; }
  tbody tr.mark-unknown:hover { background: #fbe4e4; }
  .col-num { width: 34px; color: #999; text-align: right; }
  .col-word { font-weight: bold; color: #2c3e50; white-space: nowrap; font-size: 11.5pt; }
  .col-tags { white-space: nowrap; }

  .pos { display: inline-block; font-size: 8.5pt; padding: 1px 6px; border-radius: 4px; margin: 0 3px 2px 0; color: #fff; font-weight: bold; }
  .pos-n { background: #3498db; }
  .pos-v { background: #27ae60; }
  .pos-adj { background: #e67e22; }
  .pos-adv { background: #9b59b6; }
  .pos-gray { background: #95a5a6; }
  .pos-num { background: #16a085; }
  .pos-int { background: #e91e63; }
  .pos-abbr { background: #795548; }
  .pos-pron { background: #5c6bc0; }

  .affix { font-weight: bold; }
  .affix-pre { color: #1976d2; }
  .affix-suf { color: #8e24aa; }
  .affix-mean { color: #888; font-size: 9pt; }
  .stem { color: #2c3e50; font-weight: bold; }
  .plus { color: #bbb; }
  .col-memo { font-size: 9.5pt; white-space: nowrap; }

  .def-placeholder { color: #aab; font-size: 9.5pt; font-style: italic; user-select: none; }
  tbody tr.show .def-placeholder { display: none; }
  .def-content { display: none; }
  tbody tr.show .def-content { display: block; }
  tbody.show-all .def-placeholder { display: none; }
  tbody.show-all .def-content { display: block; }

  .mark-btns { white-space: nowrap; }
  .mark-btns button { border: 1px solid #ddd; background: #fafafa; border-radius: 5px; cursor: pointer; font-size: 10pt; padding: 2px 5px; margin-right: 2px; opacity: 0.45; }
  .mark-btns button:hover { opacity: 1; }
  .mark-btns button.active { opacity: 1; border-color: #667eea; box-shadow: 0 0 0 1px #667eea inset; }
  .eye-btn { border: none; background: none; cursor: pointer; font-size: 11pt; padding: 2px 4px; opacity: 0.6; }
  .eye-btn:hover { opacity: 1; }

  .checklist { background: white; border-radius: 10px; box-shadow: 0 2px 6px rgba(0,0,0,0.08); padding: 14px 18px; margin-top: 14px; font-size: 10.5pt; }
  .checklist h2 { margin: 0 0 8px; font-size: 12.5pt; color: #2c3e50; }
  .checklist a { color: #667eea; }
  .footer { text-align: center; margin: 20px 0 10px; color: #999; font-size: 9.5pt; }

  @media (max-width: 600px) {
    .header h1 { font-size: 17pt; }
    table { font-size: 9.5pt; }
    th, td { padding: 6px 5px; }
    .col-memo { white-space: normal; }
    .toolbar { padding: 8px; }
  }
  @media print {
    body { background: white; }
    .toolbar, .nav-links, .mark-btns, .eye-btn, .family-section .hint { display: none !important; }
    .header { background: none; color: #333; border: 1px solid #ccc; }
    .def-placeholder { display: none !important; }
    .def-content { display: block !important; }
    tbody tr { break-inside: avoid; }
  }
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>📅 __DATE__（第__DAY__天）| 假期单词复习</h1>
    <p class="sub">__RANGE__ · 建议用时：晨读30分钟 + 晚测15分钟</p>
    <div class="nav-links">
      <a href="../假期复习总入口.html">🏠 返回总入口</a>
      <a href="../可打印小测卷/__DATE___小测.html">📝 小测卷</a>
      <a href="../可打印小测卷/__DATE___答案.html">📋 答案</a>
    </div>
    <div class="mark-stats" id="markStats">
      <span>✅ <b id="statKnow">0</b></span>
      <span>⚠️ <b id="statFuzzy">0</b></span>
      <span>❌ <b id="statUnknown">0</b></span>
      <span>未标记 <b id="statUnmarked">0</b></span>
    </div>
  </div>

  <div class="toolbar">
    <button class="btn-primary" onclick="showAll(true)">👁 全部显示</button>
    <button onclick="showAll(false)">🙈 全部隐藏</button>
    <select id="filterSelect" onchange="applyFilter()">
      <option value="all">全部单词</option>
      <option value="fuzzy">仅 ⚠️ 模糊</option>
      <option value="unknown">仅 ❌ 不认识</option>
      <option value="unmarked">仅未标记</option>
    </select>
    <span class="spacer"></span>
    <button onclick="resetMarks()">🔄 重置标记</button>
  </div>

__FAMILY__

  <div class="table-wrap">
    <table>
      <thead>
        <tr><th>#</th><th>单词</th><th>词性</th><th>助记拆解</th><th>释义（点击行显示）</th><th>掌握</th></tr>
      </thead>
      <tbody id="wordBody">
__ROWS__
      </tbody>
    </table>
  </div>

  <div class="checklist">
    <h2>✅ 当日复习清单</h2>
    <ul>
      <li>晨读：通读一遍，标记生词（点击行可显示/隐藏释义自测）</li>
      <li>晚测：遮盖释义，自测拼写与词义（用「全部隐藏」后逐行回忆）</li>
      <li>订正：错题记入 <a href="../进度追踪/错题本.md">错题本</a>，做完 <a href="../可打印小测卷/__DATE___小测.html">当日小测卷</a></li>
    </ul>
  </div>

  <div class="footer">2028高考英语词汇假期复习 | 广东新高考 · 词表助记版（由 生成每日词表HTML.py 生成）</div>
</div>

<script>
const STORE_KEY = 'vocab_mark___DATE__';
let marks = {};
try { marks = JSON.parse(localStorage.getItem(STORE_KEY) || '{}'); } catch (e) { marks = {}; }

function saveMarks() { localStorage.setItem(STORE_KEY, JSON.stringify(marks)); }

function rowState(tr) {
  const w = tr.getAttribute('data-word');
  return marks[w] || '';
}

function refreshRow(tr) {
  const st = rowState(tr);
  tr.classList.remove('mark-know', 'mark-fuzzy', 'mark-unknown');
  if (st) tr.classList.add('mark-' + st);
  tr.querySelectorAll('.mark-btns button[data-mark]').forEach(function (b) {
    b.classList.toggle('active', b.getAttribute('data-mark') === st);
  });
}

function refreshStats() {
  let know = 0, fuzzy = 0, unknown = 0, total = 0;
  document.querySelectorAll('#wordBody tr[data-word]').forEach(function (tr) {
    total++;
    const st = rowState(tr);
    if (st === 'know') know++;
    else if (st === 'fuzzy') fuzzy++;
    else if (st === 'unknown') unknown++;
  });
  document.getElementById('statKnow').textContent = know;
  document.getElementById('statFuzzy').textContent = fuzzy;
  document.getElementById('statUnknown').textContent = unknown;
  document.getElementById('statUnmarked').textContent = total - know - fuzzy - unknown;
}

function applyFilter() {
  const v = document.getElementById('filterSelect').value;
  document.querySelectorAll('#wordBody tr[data-word]').forEach(function (tr) {
    const st = rowState(tr);
    let show = true;
    if (v === 'fuzzy') show = (st === 'fuzzy');
    else if (v === 'unknown') show = (st === 'unknown');
    else if (v === 'unmarked') show = (st === '');
    tr.style.display = show ? '' : 'none';
  });
}

function showAll(on) {
  document.getElementById('wordBody').classList.toggle('show-all', on);
}

function resetMarks() {
  if (!confirm('确定清空本日（__DATE__）全部掌握标记？')) return;
  marks = {};
  saveMarks();
  document.querySelectorAll('#wordBody tr[data-word]').forEach(refreshRow);
  refreshStats();
  applyFilter();
}

document.getElementById('wordBody').addEventListener('click', function (e) {
  const tr = e.target.closest('tr[data-word]');
  if (!tr) return;
  const markBtn = e.target.closest('button[data-mark]');
  if (markBtn) {
    const w = tr.getAttribute('data-word');
    const m = markBtn.getAttribute('data-mark');
    if (marks[w] === m) delete marks[w]; else marks[w] = m;
    saveMarks();
    refreshRow(tr);
    refreshStats();
    applyFilter();
    return;
  }
  tr.classList.toggle('show');
});

document.querySelectorAll('#wordBody tr[data-word]').forEach(refreshRow);
refreshStats();
</script>
</body>
</html>
"""


def build_family_section(words):
    """当日词族速览：按共享前缀/后缀分组，仅保留 >=3 词的组。"""
    groups = {}  # key -> (title, [words])
    for _, word, _ in words:
        pre, _, suf = analyze_affixes(word)
        entries = []
        if pre:
            entries.append((f"{pre[0]}-", f"{pre[0]}-（{pre[1]}）"))
        elif suf:
            entries.append((f"-{suf[0]}", f"-{suf[0]}（{suf[1]}）"))
        for key, title in entries:
            groups.setdefault(key, (title, []))[1].append(word)

    big = sorted(((t, ws) for t, ws in groups.values() if len(ws) >= 3),
                 key=lambda x: -len(x[1]))
    if not big:
        return ""
    chips = []
    for title, ws in big:
        chips.append(
            f'<div class="chip"><span class="chip-title">{escape(title)} 家族（{len(ws)}词）</span>'
            f'<br><span class="chip-words">{escape(", ".join(ws))}</span></div>')
    return ('  <div class="family-section">\n'
            '    <h2>🧬 当日词族速览 <span class="hint" style="font-size:9pt;color:#999;font-weight:normal">'
            '（按共享前缀/后缀自动分组，成组记忆更高效）</span></h2>\n'
            f'    <div class="family-chips">{"".join(chips)}</div>\n'
            '  </div>\n')


def build_rows(words):
    rows = []
    for num, word, definition in words:
        word_e = escape(word)
        def_html, tags = markup_definition(escape(definition))
        tags_html = ''.join(f'<span class="pos {POS_CLASS[t]}">{t}.</span>' for t in tags)
        memo = mnemonic_html(word)
        rows.append(f'''        <tr data-word="{word_e}">
          <td class="col-num">{num}</td>
          <td class="col-word">{word_e}<button class="eye-btn" title="显示/隐藏释义">👁</button></td>
          <td class="col-tags">{tags_html}</td>
          <td class="col-memo">{memo}</td>
          <td class="col-def"><span class="def-placeholder">🔒 点击显示释义</span><span class="def-content">{def_html}</span></td>
          <td class="mark-btns">
            <button data-mark="know" title="认识">✅</button><button data-mark="fuzzy" title="模糊">⚠️</button><button data-mark="unknown" title="不认识">❌</button>
          </td>
        </tr>''')
    return '\n'.join(rows)


def render_page(date_str, day_num, range_text, words):
    html = PAGE_TEMPLATE
    html = html.replace('__DATE__', date_str)
    html = html.replace('__DAY__', str(day_num))
    html = html.replace('__RANGE__', escape(range_text))
    html = html.replace('__FAMILY__', build_family_section(words))
    html = html.replace('__ROWS__', build_rows(words))
    return html


def main():
    md_files = sorted(f for f in os.listdir(DATE_DIR)
                      if f.endswith('.md') and re.match(r'^\d+月\d+日\.md$', f))
    created = []
    warnings = []
    for fname in md_files:
        path = os.path.join(DATE_DIR, fname)
        date_str, day_num, range_text, words = parse_md(path)

        # 词数与 md 声明口径核对
        m = re.search(r'共(\d+)词', range_text)
        if m and int(m.group(1)) != len(words):
            warnings.append(f"{date_str}: 表头声明 {m.group(1)} 词，实际解析 {len(words)} 词")

        html = render_page(date_str, day_num, range_text, words)
        out_path = os.path.join(DATE_DIR, f"{date_str}.html")
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(html)
        created.append(out_path)

        # 导航链接目标存在性检查
        for suffix in ("_小测.html", "_答案.html"):
            target = os.path.join(QUIZ_DIR, f"{date_str}{suffix}")
            if not os.path.exists(target):
                warnings.append(f"{date_str}: 缺少链接目标 可打印小测卷/{date_str}{suffix}")

    print(f"已生成 {len(created)} 个词表 HTML → {DATE_DIR}")
    for w in warnings:
        print("⚠️ " + w)
    if not warnings:
        print("校验通过：词数与 md 一致，小测/答案链接目标均存在")


if __name__ == '__main__':
    main()
