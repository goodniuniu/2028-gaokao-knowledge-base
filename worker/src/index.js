/**
 * 2028高考知识库 - Cloudflare Worker 后端
 * 提供每用户学习进度的注册、同步 API
 * 数据存储在 Cloudflare KV 中
 *
 * 数据模型（与 vocab 项目的 SRS 不同，这里只有卡片三态）：
 *   code:<同步码> → { userId, name, syncCode, createdAt }
 *   data:<同步码> → { cards: { "<cardId>": { s: 0|1|2, t: epochMs } }, lastSync }
 *     cardId = md 相对仓库根目录路径去 .md 后缀
 *     s: 0=❌未理解 1=⚠️待强化 2=✅已掌握
 *     t: 该卡片状态最后更新时间戳（多端合并按 t 取新）
 *   rl:<ip>:<分钟桶> → 限流计数
 */

// CORS 头
const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
  'Access-Control-Max-Age': '86400',
};

const JSON_HEADERS = {
  'Content-Type': 'application/json',
  ...CORS_HEADERS,
};

// JSON 响应
function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: JSON_HEADERS,
  });
}

// 生成同步码（6位字母数字，易记忆）
// 使用加密安全随机数；chars 长度 32 是 2 的幂，取模无偏
function generateSyncCode() {
  const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'; // 去掉易混淆的 IO01
  const buf = new Uint32Array(6);
  crypto.getRandomValues(buf);
  let code = '';
  for (let i = 0; i < 6; i++) {
    code += chars[buf[i] % chars.length];
  }
  return code;
}

// 生成用户 ID
function generateUserId() {
  return 'u_' + Date.now() + '_' + Math.floor(Math.random() * 10000);
}

// 验证同步码格式
function isValidSyncCode(code) {
  return /^[A-Z2-9]{6}$/.test(code);
}

// ---- 简易限流（KV 固定窗口计数，按 IP 每分钟）----
// 只加在枚举敏感接口（check/register/data），常规 /api/sync 不限，
// 以免正常使用的计数写入耗尽 KV 免费写额度。
async function isRateLimited(env, request, limitPerMinute) {
  const ip = request.headers.get('CF-Connecting-IP') || 'unknown';
  const bucket = Math.floor(Date.now() / 60000);
  const key = 'rl:' + ip + ':' + bucket;
  const count = parseInt((await env.KB_KV.get(key)) || '0', 10);
  if (count >= limitPerMinute) return true;
  await env.KB_KV.put(key, String(count + 1), { expirationTtl: 180 });
  return false;
}

// ---- /api/sync 请求体校验 ----
// 返回 null 表示合法，否则返回错误信息
const MAX_BODY_BYTES = 512 * 1024;   // 512KB（260张卡的全量数据 < 100KB）
const MAX_CARDS = 5000;              // 卡片条目数上限（现库 260 张，留足余量）
const MAX_CARD_ID_LEN = 300;

function validateCards(cards) {
  const keys = Object.keys(cards);
  if (keys.length > MAX_CARDS) return 'cards 超过 ' + MAX_CARDS + ' 条上限';
  for (const k of keys) {
    if (k.length > MAX_CARD_ID_LEN) return 'cardId 过长';
    const c = cards[k];
    if (!c || typeof c !== 'object') return 'cards 条目格式非法';
    if (!Number.isInteger(c.s) || c.s < 0 || c.s > 2) return 'cards 状态值非法（须为 0/1/2）';
    if (typeof c.t !== 'number' || c.t < 0) return 'cards 时间戳非法';
  }
  return null;
}

function validateSyncBody(body) {
  if (!body || typeof body !== 'object' || Array.isArray(body)) {
    return '请求体必须是 JSON 对象';
  }
  if (body.cards != null) {
    if (typeof body.cards !== 'object' || Array.isArray(body.cards)) {
      return 'cards 必须是对象';
    }
    const err = validateCards(body.cards);
    if (err) return err;
  }
  if (body.baseSync != null && typeof body.baseSync !== 'number') return 'baseSync 必须是数字';
  return null;
}

// 同步恢复页面 HTML（内联，不走CDN缓存）
// 写入 localStorage 的 key 格式与知识库前端 assets/kb-progress.js 一致
const SYNC_PAGE_HTML = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>恢复学习进度 - 2028高考知识库</title>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif; background:#f0f2f5; color:#333; display:flex; justify-content:center; align-items:center; min-height:100vh; padding:20px; }
.card { background:#fff; border-radius:16px; padding:32px 24px; max-width:380px; width:100%; box-shadow:0 4px 24px rgba(0,0,0,0.08); text-align:center; }
.icon { font-size:48px; margin-bottom:12px; }
h1 { font-size:20px; margin-bottom:6px; }
.desc { font-size:14px; color:#888; margin-bottom:24px; line-height:1.5; }
input { width:100%; padding:14px; font-size:20px; text-align:center; letter-spacing:4px; border:2px solid #e0e0e0; border-radius:10px; text-transform:uppercase; margin-bottom:16px; }
input:focus { outline:none; border-color:#4f6df5; }
button { width:100%; padding:14px; font-size:16px; border:none; border-radius:10px; cursor:pointer; font-weight:600; transition:all .2s; }
.btn-primary { background:#4f6df5; color:#fff; }
.btn-primary:hover { background:#3d5de0; }
.btn-primary:disabled { background:#ccc; cursor:not-allowed; }
.result { margin-top:16px; padding:14px; border-radius:8px; font-size:14px; display:none; }
.result.success { background:#e8f5e9; color:#2e7d32; display:block; }
.result.error { background:#fbe9e7; color:#c62828; display:block; }
.result.loading { background:#e3f2fd; color:#1565c0; display:block; }
.stats { margin-top:12px; font-size:13px; color:#666; }
.stats div { margin:4px 0; }
.link { margin-top:20px; font-size:13px; }
.link a { color:#4f6df5; text-decoration:none; }
</style>
</head>
<body>
<div class="card">
<div class="icon">☁️</div>
<h1>恢复学习进度</h1>
<p class="desc">输入6位同步码，从云端恢复你的知识卡片掌握进度</p>
<input type="text" id="code" placeholder="同步码" maxlength="6" autocomplete="off" />
<button class="btn-primary" id="btn" onclick="doRestore()">恢复数据</button>
<div class="result" id="result"></div>
<div class="stats" id="stats" style="display:none"></div>
<div class="link"><a href="https://goodniuniu.github.io/2028-gaokao-knowledge-base/">→ 前往知识库</a></div>
</div>
<script>
function showResult(msg, type) {
  var el = document.getElementById('result');
  el.textContent = msg;
  el.className = 'result ' + type;
}
async function doRestore() {
  var code = document.getElementById('code').value.trim().toUpperCase();
  if (!code || code.length !== 6) { showResult('请输入6位同步码', 'error'); return; }
  var btn = document.getElementById('btn');
  btn.disabled = true;
  btn.textContent = '恢复中...';
  showResult('正在从云端拉取数据...', 'loading');
  try {
    var resp = await fetch('/api/data/' + code, { method: 'GET' });
    var text = await resp.text();
    var data;
    try { data = JSON.parse(text); } catch(e) {
      throw new Error('服务器返回异常，请稍后重试');
    }
    if (!resp.ok || data.ok === false) {
      throw new Error(data.error || '恢复失败 (HTTP ' + resp.status + ')');
    }
    showResult('数据拉取成功！正在写入本地...', 'loading');

    // 写入 localStorage（跟知识库前端 kb-progress.js 相同的 key 格式）
    var PREFIX = 'kb_';
    var uid = 'u_' + Date.now() + '_' + Math.floor(Math.random() * 1000);

    // 创建用户
    var users = JSON.parse(localStorage.getItem(PREFIX + 'users') || '{}');
    users[uid] = { id: uid, name: data.name, createdAt: Date.now() };
    localStorage.setItem(PREFIX + 'users', JSON.stringify(users));
    localStorage.setItem(PREFIX + 'current_user', uid);

    // 写入进度数据
    var d = data.data || {};
    localStorage.setItem(PREFIX + uid + '_cards', JSON.stringify(d.cards || {}));

    // 保存同步码
    localStorage.setItem(PREFIX + 'sync_code', code);
    localStorage.setItem(PREFIX + 'sync_name', data.name);
    if (d.lastSync) localStorage.setItem(PREFIX + 'last_sync', String(d.lastSync));

    // 显示统计
    var cards = d.cards || {};
    var n = [0, 0, 0];
    Object.keys(cards).forEach(function(k) { var s = cards[k] && cards[k].s; if (s===0||s===1||s===2) n[s]++; });
    var stats = document.getElementById('stats');
    stats.innerHTML = '<div>用户: <b>' + data.name + '</b></div>'
      + '<div>已标记卡片: <b>' + Object.keys(cards).length + '</b> 张</div>'
      + '<div>✅已掌握: <b>' + n[2] + '</b> · ⚠️待强化: <b>' + n[1] + '</b> · ❌未理解: <b>' + n[0] + '</b></div>';
    stats.style.display = 'block';

    showResult('恢复成功！点击下方链接进入知识库', 'success');
    btn.textContent = '前往知识库';
    btn.disabled = false;
    btn.onclick = function() { window.location.href = 'https://goodniuniu.github.io/2028-gaokao-knowledge-base/'; };
  } catch(e) {
    console.error('恢复失败:', e);
    showResult(e.message, 'error');
    btn.disabled = false;
    btn.textContent = '恢复数据';
  }
}
document.getElementById('code').addEventListener('keydown', function(e) {
  if (e.key === 'Enter') doRestore();
});
document.getElementById('code').focus();
</script>
</body>
</html>`;

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;
    const method = request.method;

    // Origin 白名单门禁：防止恶意网站借用户浏览器调用/枚举 API
    // （凭证在 URL 而非 Cookie，无 Origin 的非浏览器请求如 curl 不受限）
    // wrangler.toml [vars] ALLOWED_ORIGINS 配置，逗号分隔；未配置或为 * 时不限制
    // Origin: null（字符串 "null"）单独放行（PWA/WebView/严格隐私模式等合法场景）
    const origin = request.headers.get('Origin');
    const allowedOrigins = (env.ALLOWED_ORIGINS || '*');
    if (origin && origin !== 'null' && allowedOrigins !== '*') {
      const allowed = allowedOrigins.split(',').map(s => s.trim());
      const isLocalDev = /^https?:\/\/(localhost|127\.0\.0\.1)(:\d+)?$/.test(origin);
      if (!allowed.includes(origin) && !isLocalDev) {
        return json({ ok: false, error: 'Origin not allowed' }, 403);
      }
    }

    // 处理 CORS 预检
    if (method === 'OPTIONS') {
      return new Response(null, { headers: CORS_HEADERS });
    }

    // 健康检查
    if (path === '/' || path === '/api/health') {
      return json({ ok: true, service: 'gaokao-kb-sync', time: Date.now() });
    }

    // ---- 同步恢复页面（不走CDN缓存，确保最新） ----
    if (path === '/sync') {
      return new Response(SYNC_PAGE_HTML, {
        headers: {
          'Content-Type': 'text/html; charset=utf-8',
          'Cache-Control': 'no-cache, no-store, must-revalidate',
          ...CORS_HEADERS,
        },
      });
    }

    // ---- 注册新用户 ----
    // POST /api/register
    // body: { name: string }
    // 返回: { syncCode, userId, name, lastSync }
    if (path === '/api/register' && method === 'POST') {
      try {
        if (await isRateLimited(env, request, 5)) {
          return json({ ok: false, error: '请求过于频繁，请稍后再试' }, 429);
        }

        const body = await request.json();
        const name = (body.name || '学生').toString().slice(0, 20);

        // 生成唯一同步码（最多重试5次）
        let syncCode, attempts = 0;
        do {
          syncCode = generateSyncCode();
          attempts++;
          const existing = await env.KB_KV.get('code:' + syncCode);
          if (!existing) break;
        } while (attempts < 5);

        const userId = generateUserId();
        const now = Date.now();
        const userData = {
          userId,
          name,
          syncCode,
          createdAt: now,
        };

        await env.KB_KV.put('code:' + syncCode, JSON.stringify(userData));

        // 初始化空数据
        const emptyData = {
          cards: {},
          lastSync: now,
        };
        await env.KB_KV.put('data:' + syncCode, JSON.stringify(emptyData));

        return json({ ok: true, syncCode, userId, name, lastSync: now });
      } catch (e) {
        return json({ ok: false, error: '注册失败: ' + e.message }, 500);
      }
    }

    // ---- 用同步码获取数据 ----
    // GET /api/data/:syncCode
    // 返回: { ok, name, userId, createdAt, data }
    const dataMatch = path.match(/^\/api\/data\/([A-Z2-9]{6})$/);
    if (dataMatch && method === 'GET') {
      try {
        if (await isRateLimited(env, request, 20)) {
          return json({ ok: false, error: '请求过于频繁，请稍后再试' }, 429);
        }

        const syncCode = dataMatch[1];
        const userMeta = await env.KB_KV.get('code:' + syncCode);
        if (!userMeta) {
          return json({ ok: false, error: '同步码不存在' }, 404);
        }
        const meta = JSON.parse(userMeta);
        const dataStr = await env.KB_KV.get('data:' + syncCode);
        const data = dataStr ? JSON.parse(dataStr) : null;

        return json({
          ok: true,
          name: meta.name,
          userId: meta.userId,
          createdAt: meta.createdAt,
          data,
        });
      } catch (e) {
        return json({ ok: false, error: '获取数据失败: ' + e.message }, 500);
      }
    }

    // ---- 上传/同步数据 ----
    // POST /api/sync/:syncCode
    // body: { cards, baseSync }
    // baseSync: 客户端最后一次见到的云端 lastSync，用于多设备冲突检测
    // 返回: { ok, lastSync }；冲突时 409 { ok:false, code:'conflict', lastSync }
    const syncMatch = path.match(/^\/api\/sync\/([A-Z2-9]{6})$/);
    if (syncMatch && method === 'POST') {
      try {
        const syncCode = syncMatch[1];
        const userMeta = await env.KB_KV.get('code:' + syncCode);
        if (!userMeta) {
          return json({ ok: false, error: '同步码不存在' }, 404);
        }

        // 大小限制（恶意超大 payload 会耗尽 KV 存储与请求额度）
        const contentLength = parseInt(request.headers.get('Content-Length') || '0', 10);
        if (contentLength > MAX_BODY_BYTES) {
          return json({ ok: false, error: '数据过大，超过 512KB 上限' }, 413);
        }

        const text = await request.text();
        if (text.length > MAX_BODY_BYTES) {
          return json({ ok: false, error: '数据过大，超过 512KB 上限' }, 413);
        }

        let body;
        try {
          body = JSON.parse(text);
        } catch(e) {
          return json({ ok: false, error: '请求体不是合法的 JSON' }, 400);
        }
        const invalid = validateSyncBody(body);
        if (invalid) {
          return json({ ok: false, error: '数据校验失败: ' + invalid }, 400);
        }

        // 冲突检测：云端数据若在 baseSync 之后被其他设备更新，拒绝覆盖
        const existingStr = await env.KB_KV.get('data:' + syncCode);
        const existing = existingStr ? JSON.parse(existingStr) : null;
        const baseSync = typeof body.baseSync === 'number' ? body.baseSync : null;
        if (baseSync !== null && existing && typeof existing.lastSync === 'number'
          && existing.lastSync > baseSync) {
          return json({
            ok: false,
            code: 'conflict',
            error: '云端数据已被其他设备更新',
            lastSync: existing.lastSync,
          }, 409);
        }

        const now = Date.now();

        const dataToSave = {
          cards: body.cards || {},
          lastSync: now,
        };

        await env.KB_KV.put('data:' + syncCode, JSON.stringify(dataToSave));

        return json({ ok: true, lastSync: now });
      } catch (e) {
        return json({ ok: false, error: '同步失败: ' + e.message }, 500);
      }
    }

    // ---- 检查同步码是否存在 ----
    // GET /api/check/:syncCode
    // 返回: { ok, exists }（不回显用户名，避免用户枚举）
    const checkMatch = path.match(/^\/api\/check\/([A-Z2-9]{6})$/);
    if (checkMatch && method === 'GET') {
      try {
        if (await isRateLimited(env, request, 10)) {
          return json({ ok: false, error: '请求过于频繁，请稍后再试' }, 429);
        }

        const syncCode = checkMatch[1];
        const userMeta = await env.KB_KV.get('code:' + syncCode);
        if (!userMeta) {
          return json({ ok: true, exists: false });
        }
        return json({ ok: true, exists: true });
      } catch (e) {
        return json({ ok: false, error: e.message }, 500);
      }
    }

    // 404
    return json({ ok: false, error: 'Not found: ' + path }, 404);
  },
};
