from pathlib import Path
import pandas as pd
import streamlit as st

ROOT=Path(__file__).parent; DATA=ROOT/'data'
st.set_page_config(page_title='安卓游戏机会榜', page_icon='🎮', layout='wide')
st.markdown('''<style>.stApp{background:#111216}.block-container{padding-top:2rem} h1,h2,h3{color:#f5f5f5}</style>''',unsafe_allow_html=True)
st.title('安卓游戏机会榜')
st.caption('自动发现热点 · 识别修改需求 · 评估开发价值')
def load(name):
    p=DATA/name
    return pd.read_csv(p).fillna('') if p.exists() else pd.DataFrame()
games=load('games.csv'); rankings=load('rankings.csv'); evidence=load('evidence.csv')
with st.sidebar:
    st.header('筛选')
    keyword=st.text_input('搜索游戏')
    stage=st.selectbox('生命周期',['全部','上线前','上线后'])
    st.caption('当前版本仅显示公开采集的可追溯数据。')
if keyword and not games.empty: games=games[games.name.str.contains(keyword,case=False,na=False)]
if stage!='全部' and not rankings.empty:
    rankings=rankings[rankings.lifecycle.str.contains('S1' if stage=='上线前' else 'S3',na=False)]
tabs=st.tabs(['新游潜力榜','上线后热度榜','修改需求榜','开发机会榜','数据源状态'])
def no_data(title): st.info(f'{title}：数据不足，暂不可评级。请先扩充可验证的 Android 指标和真实需求证据。')
with tabs[0]:
    pre=rankings[rankings.lifecycle.eq('S1')] if not rankings.empty else rankings
    no_data('新游潜力榜'); st.dataframe(pre, use_container_width=True, hide_index=True)
with tabs[1]:
    post=rankings[rankings.lifecycle.str.contains('S3',na=False)] if not rankings.empty else rankings
    no_data('上线后热度榜'); st.dataframe(post, use_container_width=True, hide_index=True)
with tabs[2]:
    no_data('修改需求榜'); st.caption('尚未接入合规的社区需求数据。AI/规则分析不会创建虚假证据。')
    st.dataframe(evidence[evidence.source.ne('steam')] if not evidence.empty else evidence, use_container_width=True, hide_index=True)
with tabs[3]:
    no_data('开发机会榜'); st.dataframe(rankings, use_container_width=True, hide_index=True)
with tabs[4]:
    logs=load('collection_log.csv'); st.subheader('采集日志'); st.dataframe(logs, use_container_width=True, hide_index=True)
    st.markdown('**限制说明**：Google Play 页面探针只能验证公开元数据；不会把累计安装档位当作近期下载。Steam 仅用于发现 PC→Android 候选，不能作为 Android 用户指标。')
st.divider(); st.subheader('已发现游戏')
if games.empty: st.warning('暂无快照。运行 `python scripts/collect.py && python scripts/score.py`。')
else:
    columns=[x for x in ['name','platform','android_status','developer','release_date','google_play_url','steam_url','collected_at'] if x in games]
    st.dataframe(games[columns],use_container_width=True,hide_index=True)
