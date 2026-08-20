/**
 * 2028高考知识库 - 每用户学习进度
 *
 * 功能：
 *  - 卡片页三键标记（❌未理解 / ⚠️待强化 / ✅已掌握）
 *  - localStorage 本地多用户隔离（前缀 kb_）
 *  - 可选云端同步：6位同步码（Cloudflare Worker + KV），本地优先、后台同步
 *  - 索引页掌握角标、复盘追踪页个人仪表盘
 *
 * 数据模型：cards = { "<cardId>": { s: 0|1|2, t: epochMs } }
 * cardId = md 相对仓库根目录路径去 .md 后缀（由 build_site.py 注入 data-card-id）
 *
 * 渐进增强：本脚本加载失败/被禁用时，站点表现与静态版完全一致。
 */
(function () {
  'use strict';

  // ============ 配置 ============
  // 部署 Worker 后填入实际地址，例如 'https://gaokao-kb-sync.<account>.workers.dev'
  var API_BASE = 'https://gaokao-kb-sync.goodniuniu.workers.dev';
  var AUTO_SYNC_INTERVAL = 2 * 60 * 1000; // 2分钟
  var PREFIX = 'kb_';
  var USERS_KEY = PREFIX + 'users';
  var CURRENT_KEY = PREFIX + 'current_user';

  var STATUS = [
    { icon: '❌', label: '未理解', cls: 'bad' },
    { icon: '⚠️', label: '待强化', cls: 'warn' },
    { icon: '✅', label: '已掌握', cls: 'ok' },
  ];

  // ============ 工具 ============
  function $(id) { return document.getElementById(id); }
  function read(key, fallback) {
    try {
      var v = localStorage.getItem(key);
      return v === null ? fallback : v;
    } catch (e) { return fallback; }
  }
  function write(key, value) {
    try { localStorage.setItem(key, value); } catch (e) { /* 隐私模式等 */ }
  }
  function readJSON(key, fallback) {
    try {
      var v = localStorage.getItem(key);
      return v ? JSON.parse(v) : fallback;
    } catch (e) { return fallback; }
  }

  // 站点根 URL（由本脚本的 src 反推，兼容本地与 GitHub Pages）
  function rootUrl() {
    var s = document.querySelector('script[src*="assets/kb-progress.js"]');
    if (!s) return new URL('./', location.href);
    var src = s.getAttribute('src');
    var base = src.slice(0, src.indexOf('assets/kb-progress.js'));
    return new URL(base, location.href);
  }

  // 卡片链接 URL → cardId（去根路径、去 .html、解码）
  function urlToCardId(url) {
    var root = rootUrl();
    var p = url.pathname;
    if (p.indexOf(root.pathname) !== 0) return null;
    var rel = p.slice(root.pathname.length);
    if (!/\.html$/i.test(rel)) return null;
    rel = rel.replace(/\.html$/i, '');
    try { rel = decodeURIComponent(rel); } catch (e) { /* 保留原样 */ }
    return rel;
  }

  // ============ Storage ============
  var Storage = {
    getUsers: function () { return readJSON(USERS_KEY, {}); },
    currentId: function () { return read(CURRENT_KEY, null); },
    currentUser: function () {
      var id = this.currentId();
      return id ? this.getUsers()[id] || null : null;
    },
    ensureUser: function () {
      var id = this.currentId();
      if (id && this.getUsers()[id]) return id;
      id = 'u_' + Date.now() + '_' + Math.floor(Math.random() * 1000);
      var users = this.getUsers();
      users[id] = { id: id, name: '本地用户', createdAt: Date.now() };
      write(USERS_KEY, JSON.stringify(users));
      write(CURRENT_KEY, id);
      return id;
    },
    createUser: function (name) {
      var id = 'u_' + Date.now() + '_' + Math.floor(Math.random() * 1000);
      var users = this.getUsers();
      users[id] = { id: id, name: name || '本地用户', createdAt: Date.now() };
      write(USERS_KEY, JSON.stringify(users));
      write(CURRENT_KEY, id);
      return id;
    },
    switchUser: function (id) { write(CURRENT_KEY, id); },
    cardsKey: function () { return PREFIX + this.ensureUser() + '_cards'; },
    getCards: function () { return readJSON(this.cardsKey(), {}); },
    setCards: function (cards) { write(this.cardsKey(), JSON.stringify(cards)); },
    setStatus: function (cardId, s) {
      var cards = this.getCards();
      cards[cardId] = { s: s, t: Date.now() };
      this.setCards(cards);
      Sync.markPending();
    },
    getStatus: function (cardId) {
      var c = this.getCards()[cardId];
      return c && (c.s === 0 || c.s === 1 || c.s === 2) ? c.s : null;
    },
  };

  // ============ Sync ============
  var Sync = {
    pending: false,
    code: function () { return read(PREFIX + 'sync_code', ''); },
    lastSync: function () { return parseInt(read(PREFIX + 'last_sync', '0'), 10) || 0; },
    configured: function () { return API_BASE.indexOf('workers.dev') > 0 && !!this.code(); },
    apiCall: function (path, opts) {
      opts = opts || {};
      opts.headers = Object.assign({ 'Content-Type': 'application/json' }, opts.headers || {});
      return fetch(API_BASE + path, opts).then(function (r) {
        return r.text().then(function (text) {
          var data;
          try { data = JSON.parse(text); } catch (e) { throw new Error('服务器返回异常'); }
          if (!r.ok && r.status !== 409) throw new Error(data.error || ('HTTP ' + r.status));
          return data;
        });
      });
    },
    buildPayload: function () {
      return { cards: Storage.getCards(), baseSync: this.lastSync() };
    },
    markPending: function () {
      if (!this.configured()) return;
      this.pending = true;
    },
    // 注册：领同步码并上传本地进度
    register: function (name) {
      var self = this;
      return this.apiCall('/api/register', {
        method: 'POST', body: JSON.stringify({ name: name }),
      }).then(function (data) {
        if (!data.ok) throw new Error(data.error || '注册失败');
        write(PREFIX + 'sync_code', data.syncCode);
        write(PREFIX + 'sync_name', data.name || name);
        if (data.lastSync) write(PREFIX + 'last_sync', String(data.lastSync));
        // 注册后把本地已有进度传上去
        return self.uploadAll().then(function () { return data; });
      });
    },
    // 恢复：拉云端数据，与本地按卡片合并（取 t 新者），再回传
    restore: function (code) {
      var self = this;
      code = (code || '').trim().toUpperCase();
      return this.apiCall('/api/data/' + code, { method: 'GET' }).then(function (data) {
        if (!data.ok) throw new Error(data.error || '恢复失败');
        var cloud = (data.data && data.data.cards) || {};
        var merged = mergeCards(Storage.getCards(), cloud);
        Storage.setCards(merged);
        write(PREFIX + 'sync_code', code);
        write(PREFIX + 'sync_name', data.name || '');
        if (data.data && data.data.lastSync) write(PREFIX + 'last_sync', String(data.data.lastSync));
        self.pending = true;
        return self.uploadAll().then(function () { return data; });
      });
    },
    uploadAll: function () {
      var self = this;
      if (!this.configured()) { this.pending = false; return Promise.resolve(null); }
      return this.apiCall('/api/sync/' + this.code(), {
        method: 'POST', body: JSON.stringify(this.buildPayload()),
      }).then(function (data) {
        if (data.code === 'conflict') return self.resolveConflict();
        if (data.lastSync) write(PREFIX + 'last_sync', String(data.lastSync));
        self.pending = false;
        UI.refreshSyncHint();
        return data;
      }).catch(function (e) {
        // 网络失败保持 pending，下轮重试
        self.pending = true;
        UI.refreshSyncHint(e.message);
        return null;
      });
    },
    resolveConflict: function () {
      var self = this;
      return this.apiCall('/api/data/' + this.code(), { method: 'GET' }).then(function (data) {
        var cloud = (data.data && data.data.cards) || {};
        Storage.setCards(mergeCards(Storage.getCards(), cloud));
        if (data.data && data.data.lastSync) write(PREFIX + 'last_sync', String(data.data.lastSync));
        return self.uploadAll();
      });
    },
    startAutoSync: function () {
      var self = this;
      setInterval(function () { if (self.pending) self.uploadAll(); }, AUTO_SYNC_INTERVAL);
      window.addEventListener('beforeunload', function () {
        if (self.pending && self.configured() && navigator.sendBeacon) {
          navigator.sendBeacon(
            API_BASE + '/api/sync/' + self.code(),
            new Blob([JSON.stringify(self.buildPayload())], { type: 'application/json' })
          );
        }
      });
    },
  };

  // 多端合并：逐卡片取 t 新者
  function mergeCards(local, cloud) {
    var out = {};
    var k;
    for (k in cloud) { if (cloud.hasOwnProperty(k)) out[k] = cloud[k]; }
    for (k in local) {
      if (!local.hasOwnProperty(k)) continue;
      if (!out[k] || (local[k].t || 0) >= (out[k].t || 0)) out[k] = local[k];
    }
    return out;
  }

  // ============ UI ============
  var UI = {
    // ---- 卡片页：三键标记组件 ----
    initCardWidget: function () {
      var host = $('kb-progress-widget');
      var wrap = document.querySelector('[data-card-id]');
      if (!host || !wrap) return;
      var cardId = wrap.getAttribute('data-card-id');
      if (!cardId) return;

      var btns = document.createElement('div');
      btns.className = 'kb-progress';
      btns.innerHTML = '<span class="kb-progress__label">我的掌握：</span>' +
        STATUS.map(function (st, i) {
          return '<button type="button" class="kb-progress__btn" data-s="' + i + '">' +
            st.icon + ' ' + st.label + '</button>';
        }).join('');
      host.appendChild(btns);

      function refresh() {
        var cur = Storage.getStatus(cardId);
        btns.querySelectorAll('.kb-progress__btn').forEach(function (b) {
          var s = parseInt(b.getAttribute('data-s'), 10);
          b.classList.toggle('is-active', s === cur);
        });
        // 覆盖静态状态徽章（仅当用户标记过）
        var badge = document.querySelector('.kb-badges .kb-badge');
        if (badge && cur !== null) {
          badge.textContent = STATUS[cur].icon + STATUS[cur].label;
          badge.className = 'kb-badge kb-badge--' + STATUS[cur].cls;
        }
      }

      btns.addEventListener('click', function (e) {
        var b = e.target.closest('.kb-progress__btn');
        if (!b) return;
        var s = parseInt(b.getAttribute('data-s'), 10);
        // 再点一次当前状态 = 取消标记
        var cur = Storage.getStatus(cardId);
        if (cur === s) {
          var cards = Storage.getCards();
          delete cards[cardId];
          Storage.setCards(cards);
          Sync.markPending();
        } else {
          Storage.setStatus(cardId, s);
        }
        refresh();
        UI.refreshUserPanel();
      });
      refresh();
    },

    // ---- 索引页：掌握角标 ----
    initIndexBadges: function () {
      var links = document.querySelectorAll('.kb-list a.kb-item');
      if (!links.length) return;
      var cards = Storage.getCards();
      var marked = false;
      for (var k in cards) { if (cards.hasOwnProperty(k)) { marked = true; break; } }
      if (!marked) return; // 从未标记过就不扫
      links.forEach(function (a) {
        var cardId = urlToCardId(new URL(a.getAttribute('href'), location.href));
        if (!cardId) return;
        var c = cards[cardId];
        if (!c) return;
        var span = document.createElement('span');
        span.className = 'kb-item-status kb-item-status--' + c.s;
        span.textContent = STATUS[c.s].icon;
        span.title = '我的掌握：' + STATUS[c.s].label;
        a.appendChild(span);
      });
    },

    // ---- 导航栏：用户入口 + 弹层 ----
    initUserMenu: function () {
      var nav = document.querySelector('.kb-nav__links');
      if (!nav) return;
      var btn = document.createElement('a');
      btn.href = 'javascript:void 0';
      btn.id = 'kb-user-btn';
      btn.className = 'kb-user-btn';
      nav.appendChild(btn);

      var panel = document.createElement('div');
      panel.id = 'kb-user-panel';
      panel.className = 'kb-user-panel';
      panel.style.display = 'none';
      document.body.appendChild(panel);

      btn.addEventListener('click', function (e) {
        e.stopPropagation();
        var open = panel.style.display !== 'none';
        if (open) { panel.style.display = 'none'; return; }
        UI.renderUserPanel(panel);
        panel.style.display = 'block';
        var r = btn.getBoundingClientRect();
        panel.style.top = (r.bottom + window.scrollY + 6) + 'px';
        panel.style.right = Math.max(8, window.innerWidth - r.right) + 'px';
      });
      document.addEventListener('click', function (e) {
        if (!panel.contains(e.target) && e.target !== btn) panel.style.display = 'none';
      });
      this.refreshUserBtn();
    },

    refreshUserBtn: function () {
      var btn = $('kb-user-btn');
      if (!btn) return;
      var u = Storage.currentUser();
      var code = Sync.code();
      btn.textContent = '👤 ' + (u ? u.name : '进度') + (code ? ' ☁️' : '');
      btn.title = code ? ('已开启云同步，同步码 ' + code) : '本地进度（未开启云同步）';
    },

    renderUserPanel: function (panel) {
      var users = Storage.getUsers();
      var curId = Storage.ensureUser();
      var cards = Storage.getCards();
      var n = [0, 0, 0];
      Object.keys(cards).forEach(function (k) {
        var s = cards[k] && cards[k].s;
        if (s === 0 || s === 1 || s === 2) n[s]++;
      });
      var code = Sync.code();
      var syncOk = API_BASE.indexOf('workers.dev') > 0;

      var html = '<div class="kb-user-panel__sec">'
        + '<div class="kb-user-panel__stats">'
        + '<span>✅ ' + n[2] + '</span><span>⚠️ ' + n[1] + '</span><span>❌ ' + n[0] + '</span>'
        + '</div>'
        + '<div class="kb-user-panel__hint">已标记 ' + (n[0] + n[1] + n[2]) + ' 张卡片</div>'
        + '</div>';

      html += '<div class="kb-user-panel__sec"><div class="kb-user-panel__title">用户</div>';
      Object.keys(users).forEach(function (id) {
        var u = users[id];
        html += '<div class="kb-user-panel__user' + (id === curId ? ' is-current' : '')
          + '" data-uid="' + id + '">' + (id === curId ? '● ' : '○ ') + escapeHtml(u.name) + '</div>';
      });
      html += '<button class="kb-user-panel__btn" data-act="new-user">＋ 新建本地用户</button></div>';

      html += '<div class="kb-user-panel__sec"><div class="kb-user-panel__title">云同步</div>';
      if (!syncOk) {
        html += '<div class="kb-user-panel__hint">Worker 未部署，暂不可用</div>';
      } else if (code) {
        html += '<div class="kb-user-panel__hint">同步码：<b class="kb-user-panel__code">' + code + '</b>'
          + '<br><span id="kb-sync-hint">在其它设备输入此码即可恢复进度</span></div>'
          + '<button class="kb-user-panel__btn" data-act="sync-now">立即同步</button>';
      } else {
        html += '<button class="kb-user-panel__btn" data-act="register">注册同步码（开启云同步）</button>'
          + '<button class="kb-user-panel__btn" data-act="restore">输入同步码恢复</button>';
      }
      html += '</div>';

      panel.innerHTML = html;

      panel.querySelectorAll('[data-act]').forEach(function (b) {
        b.addEventListener('click', function () { UI.handleAction(b.getAttribute('data-act'), panel); });
      });
      panel.querySelectorAll('.kb-user-panel__user').forEach(function (d) {
        d.addEventListener('click', function () {
          Storage.switchUser(d.getAttribute('data-uid'));
          location.reload();
        });
      });
    },

    handleAction: function (act, panel) {
      if (act === 'new-user') {
        var name = prompt('新用户昵称：', '');
        if (name === null) return;
        Storage.createUser(name.trim() || '本地用户');
        location.reload();
      } else if (act === 'register') {
        var nm = prompt('用于云同步的昵称：', (Storage.currentUser() || {}).name || '');
        if (nm === null) return;
        Sync.register(nm.trim() || '学生').then(function (data) {
          alert('云同步已开启！\n你的同步码：' + data.syncCode + '\n请妥善保存，在其它设备输入此码即可恢复进度。');
          UI.refreshUserBtn();
          UI.renderUserPanel(panel);
        }).catch(function (e) { alert('注册失败：' + e.message); });
      } else if (act === 'restore') {
        var code = prompt('输入6位同步码（云端数据将与本地合并）：', '');
        if (code === null) return;
        Sync.restore(code).then(function () {
          alert('恢复成功！');
          location.reload();
        }).catch(function (e) { alert('恢复失败：' + e.message); });
      } else if (act === 'sync-now') {
        Sync.uploadAll().then(function (d) {
          if (d && d.ok) UI.refreshSyncHint('已同步 ✓');
        });
      }
    },

    refreshSyncHint: function (msg) {
      var el = $('kb-sync-hint');
      if (el && msg) el.textContent = msg;
    },

    refreshUserPanel: function () {
      var panel = $('kb-user-panel');
      if (panel && panel.style.display !== 'none') this.renderUserPanel(panel);
    },

    // ---- 复盘追踪页：个人仪表盘 ----
    initDashboard: function () {
      var host = $('kb-progress-dashboard');
      if (!host) return;
      var base = rootUrl();
      var s = document.createElement('script');
      s.src = base.href + 'assets/kb-cards.js';
      s.onload = function () { UI.renderDashboard(host); };
      s.onerror = function () { host.innerHTML = '<p class="kb-note">卡片清单（assets/kb-cards.js）未生成，请运行 build_site.py。</p>'; };
      document.head.appendChild(s);
    },

    renderDashboard: function (host) {
      var all = window.KB_CARDS || {};
      var cards = Storage.getCards();
      var subjects = {};
      var total = { n: 0, m: [0, 0, 0] };
      Object.keys(all).forEach(function (id) {
        var subj = all[id].s;
        if (!subjects[subj]) subjects[subj] = { n: 0, m: [0, 0, 0] };
        subjects[subj].n++;
        total.n++;
        var c = cards[id];
        if (c && (c.s === 0 || c.s === 1 || c.s === 2)) {
          subjects[subj].m[c.s]++;
          total.m[c.s]++;
        }
      });

      var pct = total.n ? Math.round(total.m[2] / total.n * 100) : 0;
      var html = '<div class="kb-dash">'
        + '<div class="kb-dash__head">'
        + '<div class="kb-dash__pct">' + pct + '%</div>'
        + '<div class="kb-dash__meta">全库 ' + total.n + ' 张 · ✅已掌握 ' + total.m[2]
        + ' · ⚠️待强化 ' + total.m[1] + ' · ❌未理解 ' + total.m[0] + '</div>'
        + '</div>';

      Object.keys(subjects).forEach(function (subj) {
        var d = subjects[subj];
        var p = d.n ? Math.round(d.m[2] / d.n * 100) : 0;
        html += '<div class="kb-dash__row">'
          + '<span class="kb-dash__subj">' + escapeHtml(subj) + '</span>'
          + '<span class="kb-dash__bar"><span class="kb-dash__fill" style="width:' + p + '%"></span></span>'
          + '<span class="kb-dash__num">' + d.m[2] + '/' + d.n + '</span>'
          + '</div>';
      });

      // 最近7天标记动态
      var week = Date.now() - 7 * 24 * 3600 * 1000;
      var recent = Object.keys(cards).filter(function (k) { return (cards[k].t || 0) > week; }).length;
      html += '<div class="kb-dash__foot">最近 7 天标记 ' + recent + ' 张'
        + (Sync.code() ? ' · 云同步已开启（' + Sync.code() + '）' : ' · 本地进度（点击右上角 👤 开启云同步）')
        + '</div></div>';
      host.innerHTML = html;
    },
  };

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  // ============ 女儿专区：每日一句 / 连续天数 / 成就徽章 ============
  // 仅在 build_site.py 注入的容器（#kb-daily-boost / #kb-streak / #kb-achievements）存在时渲染；
  // 全部数据由既有每用户进度（cards 的 s/t 字段）现场推导，不新增存储。
  var Boost = {
    QUOTES: [
      '你不需要很厉害才能开始，但你需要开始才能很厉害。',
      '错的每一道题，都是高考前替你挡的枪。',
      '慢慢来，比较快。',
      '每天进步1%，一年后是现在的37.8倍——数学不会骗人。',
      '苏炳添32岁才跑出9秒83，你的高二急什么。',
      '先做5分钟，不想做了再停。通常你会做下去。',
      '累了就休息，休息不是放弃，是充电。',
      '你唯一的对手是昨天的自己。',
      '睡觉也是一种复习——大脑在梦里替你归档。',
      '平台期是骗人的：积累会在某一天突然跳起来。',
      '今天不想努力也没关系，看一眼这句话就算你赢了。',
      '我生来就是高山而非溪流。——华坪女高誓词',
      '此生属于祖国，此生无怨无悔。——黄旭华',
      '人就像种子，要做一粒好种子。——袁隆平',
      '美丽的宇宙太空，以它的神秘和绚丽，召唤我们踏过平庸。——南仁东',
      '清澈的爱，只为中国。',
      '问渠那得清如许？为有源头活水来。',
      '操千曲而后晓声，观千剑而后识器。',
      '苟日新，日日新，又日新。',
      '允许今天不完美。',
      '错题是免费的情报。',
      '半山腰总是最挤的，你得去山顶看看。',
      '你现在多看的每一页，都是未来的底气。',
      '别慌，月亮也正在大海某处迷茫。',
    ],

    // 从进度数据推导统计
    stats: function () {
      var cards = Storage.getCards();
      var n = { total: 0, ok: 0, warn: 0, bad: 0, subj: {}, days: {} };
      Object.keys(cards).forEach(function (k) {
        var c = cards[k];
        if (!c || (c.s !== 0 && c.s !== 1 && c.s !== 2)) return;
        n.total++;
        n[['bad', 'warn', 'ok'][c.s]]++;
        var subj = k.split('/')[0];
        n.subj[subj] = true;
        var d = new Date(c.t || 0);
        n.days[d.getFullYear() + '-' + (d.getMonth() + 1) + '-' + d.getDate()] = true;
      });
      var sixSubj = ['语文', '数学', '英语', '物理', '化学', '生物'].filter(function (s) { return n.subj[s]; }).length;
      // 连续天数：从今天往回数；今天还没标记则从昨天起算（早晨访问不归零）
      var dayMs = 24 * 3600 * 1000;
      function keyOf(ts) {
        var d = new Date(ts);
        return d.getFullYear() + '-' + (d.getMonth() + 1) + '-' + d.getDate();
      }
      var today = new Date();
      var todayKey = keyOf(today);
      var start = n.days[todayKey] ? today.getTime() : today.getTime() - dayMs;
      var streak = 0;
      while (n.days[keyOf(start - streak * dayMs)]) streak++;
      n.sixSubj = sixSubj;
      n.dayCount = Object.keys(n.days).length;
      n.streak = streak;
      return n;
    },

    init: function () {
      var quote = $('kb-daily-boost');
      if (quote) {
        var dayIdx = Math.floor(Date.now() / 86400000);
        quote.textContent = '「' + this.QUOTES[dayIdx % this.QUOTES.length] + '」';
      }
      var st = $('kb-streak');
      if (st) {
        var n = this.stats();
        if (n.total > 0) {
          st.textContent = n.streak >= 1 ? ('🔥 连续 ' + n.streak + ' 天') : '🌱 今天是新的开始';
          st.title = '已标记 ' + n.total + ' 张卡片';
        }
      }
      this.renderAchievements();
    },

    ACHIEVEMENTS: [
      { icon: '🌱', name: '迈出第一步', desc: '标记第1张卡片', test: function (s) { return s.total >= 1; } },
      { icon: '🦁', name: '诚实的勇气', desc: '标出第1个「❌不会」', test: function (s) { return s.bad >= 1; } },
      { icon: '✨', name: '小有所成', desc: '第1张「✅已掌握」', test: function (s) { return s.ok >= 1; } },
      { icon: '🌈', name: '六科开花', desc: '六科都有标记', test: function (s) { return s.sixSubj >= 6; } },
      { icon: '🔟', name: '十全十美', desc: '10张✅已掌握', test: function (s) { return s.ok >= 10; } },
      { icon: '🔥', name: '七日之约', desc: '连续7天有标记', test: function (s) { return s.streak >= 7; } },
      { icon: '🏔️', name: '五十张里程', desc: '累计标记50张', test: function (s) { return s.total >= 50; } },
      { icon: '🌙', name: '细水长流', desc: '累计30天有标记', test: function (s) { return s.dayCount >= 30; } },
    ],

    renderAchievements: function () {
      var host = $('kb-achievements');
      if (!host) return;
      var n = this.stats();
      if (n.total === 0) return; // 未开始不显示，保持零压力
      var lit = 0;
      var html = this.ACHIEVEMENTS.map(function (a) {
        var on = a.test(n);
        if (on) lit++;
        return '<div class="gz-badge-item ' + (on ? 'is-lit' : 'is-dim') + '" title="' + (on ? '已点亮' : '继续探索即可点亮') + '">'
          + '<div class="gz-badge-item__icon">' + a.icon + '</div>'
          + '<div class="gz-badge-item__name">' + a.name + '</div>'
          + '<div class="gz-badge-item__desc">' + a.desc + '</div></div>';
      }).join('');
      host.innerHTML = '<div style="grid-column:1/-1;font-size:12.5px;color:#9d174d;font-weight:700;margin-bottom:0">'
        + '🏅 我的小成就（' + lit + '/' + this.ACHIEVEMENTS.length + ' 点亮）——标记卡片就会亮，纯属好玩</div>' + html;
    },
  };

  // ============ 启动 ============
  function init() {
    UI.initUserMenu();
    UI.initCardWidget();
    UI.initIndexBadges();
    UI.initDashboard();
    Boost.init();
    Sync.startAutoSync();
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
