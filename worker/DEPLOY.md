# Worker 部署指南（gaokao-kb-sync）

> 本 Worker 为知识库提供「每用户学习进度」的云端同步，架构复刻自 `gaokao-english-vocab/worker`。
> API 端点一致：`/api/register` `/api/data/:code` `/api/sync/:code` `/api/check/:code` `/api/health`，另有 `/sync` 恢复页。

## 一、前置条件

- Cloudflare 账号（与 vocab 项目同账号即可）
- 本机已安装 Node.js；首次使用执行 `cd worker && npm install`
- wrangler 已登录：`npx wrangler login`（浏览器授权）

## 二、创建 KV namespace（一次性）

```bash
cd worker
npx wrangler kv namespace create KB_KV
```

输出形如：

```
{ binding = "KB_KV", id = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" }
```

把 `id` 填入 `wrangler.toml` 的 `[[kv_namespaces]]` 的 `id = "..."`（替换 `REPLACE_WITH_KV_NAMESPACE_ID`）。

## 三、部署

```bash
npx wrangler deploy
```

部署成功后得到 Worker URL，形如：

```
https://gaokao-kb-sync.<account-subdomain>.workers.dev
```

## 四、接入前端

把 Worker URL 填入知识库前端 `assets/kb-progress.js` 顶部的 `API_BASE` 常量。

## 五、验证

```bash
# 健康检查
curl https://<worker-url>/api/health

# 注册（保存返回的 syncCode）
curl -X POST https://<worker-url>/api/register -H "Content-Type: application/json" -d '{"name":"测试"}'

# 上传进度
curl -X POST https://<worker-url>/api/sync/<SYNC_CODE> -H "Content-Type: application/json" \
  -d '{"cards":{"数学/核心知识网络/测试卡":{"s":2,"t":1234567890000}}}'

# 拉取
curl https://<worker-url>/api/data/<SYNC_CODE>

# 恢复页（浏览器打开）
https://<worker-url>/sync
```

## 六、数据模型

| Key | Value |
|-----|-------|
| `code:<6位同步码>` | `{ userId, name, syncCode, createdAt }` |
| `data:<6位同步码>` | `{ cards: { "<cardId>": { s, t } }, lastSync }` |
| `rl:<ip>:<分钟桶>` | 限流计数（TTL 180s） |

- `cardId` = 卡片 md 相对仓库根目录路径去 `.md` 后缀（如 `数学/核心知识网络/高一筑基_数学_核心知识网络_函数零点与函数模型`）
- `s`：0=❌未理解 1=⚠️待强化 2=✅已掌握；`t`：该卡状态最后更新时间戳（多端合并按 t 取新）
- **注意：卡片 md 改名/移动目录 = cardId 变化 = 该卡的每用户进度失联**

## 七、运维

```bash
# 查看 KV 键
npx wrangler kv key list --binding=KB_KV
# 查看某用户数据
npx wrangler kv key get --binding=KB_KV "data:<SYNC_CODE>"
```
