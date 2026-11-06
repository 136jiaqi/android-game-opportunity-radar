import streamlit as st
from pathlib import Path
import pandas as pd
st.title('数据源状态')
p=Path(__file__).parents[1]/'data/collection_log.csv'
if p.exists(): st.dataframe(pd.read_csv(p),use_container_width=True,hide_index=True)
else: st.info('尚未运行采集。')
st.markdown('Google Play：公开 HTML 元数据探针（部分字段）。Steam：公开 Store API（候选发现和 PC 元数据）。TapTap、YouTube、Reddit、GameGuardian：尚未接入；需先确认 API 授权/访问规则或使用 CSV 导入。')
