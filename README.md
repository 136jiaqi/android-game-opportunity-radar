# Android Game Opportunity Radar / 安卓游戏机会榜

一个面向 Android 单机游戏市场的可追溯机会发现 MVP。它将采集、快照、评分和 Streamlit 展示分离；没有证据时明确显示“数据不足”，绝不以模拟数据补榜。

## 当前真实数据链路

- **Steam Store API**：自动发现公开的“即将推出”游戏，取得名称、AppID、发布日期、开发商等 PC 侧候选信号。它不等于 Android 用户或下载数据。
- **Google Play 自动发现**：读取公开的免费游戏榜 HTML，提取包名后逐条补全公开详情。榜单位置仅作为发现信号，快照会保存来源、国家、抓取时间和当前榜位；绝不将其解释为近期下载量。页面结构变更、限流或详情失败均会记录在日志中。

TapTap、YouTube、Reddit、GameGuardian 及第三方市场数据尚未接入：接入前需要确认平台规则、授权 API 或采用 CSV 导入。没有这些真实证据时，修改需求榜和机会榜不会生成虚假分数。

## 本地运行

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/collect.py
python scripts/score.py
python -m pytest
python -m compileall .
streamlit run app.py
```

数据快照位于 `data/`，适合由 GitHub Actions 写回仓库、由 Streamlit Community Cloud 只读加载。请不要在 Streamlit 页面刷新时采集。

## 评分与可追溯性

评分权重在 `config/scoring.yaml`。每个未来分数都应同时有来源、采集时间、覆盖率、证据数量与置信度。`scripts/score.py` 当前只产出透明的“暂不可评级”记录，直至收集到合规的 Android 下载/增长/需求/商业化信号。

## 部署

将仓库推送到 GitHub 后，在 Streamlit Community Cloud 选择 `app.py`，Python 3.11+，依赖为 `requirements.txt`。工作流 `collect.yml` 每日 UTC 02:17 采集并提交快照；若分支保护不允许 Actions 直接写入，请改为提交 PR 或配置允许该机器人写入。

## 下一步

1. 为 Google Play 合规地引入可验证的榜单/预注册发现源或人工 CSV 导入。
2. 增加授权的社区数据导入，保存原文、链接、互动和需求分类。
3. 建立 Android 包名与 Steam AppID 的人工审核映射，避免仅按名称自动合并。
