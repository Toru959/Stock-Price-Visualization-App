import pandas as pd
import yfinance as yf
import altair as alt
import streamlit as st

# アプリケーションのタイトル
st.title('米国株価可視化アプリ')

# サイドバーの説明
st.sidebar.write("""
# GAFA株価
こちらは株価可視化ツールです。以下のオプションから表示日数を指定できます。
""")

# 表示日数選択の説明
st.sidebar.write("""
## 表示日数選択
""")

# スライダーで表示日数を選択
days = st.sidebar.slider('日数', 1, 50, 20)

st.write(f"""
### 過去 **{days}日間** のGAFA株価
""")

# 株価データを取得する関数
@st.cache_data
def get_data(days, tickers):
    df = pd.DataFrame()
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(period=f'{days}d')
        hist.index = hist.index.strftime('%d %B %Y')
        hist = hist[['Close']]
        hist.columns = [company]
        hist = hist.T
        hist.index.name = 'Name'
        df = pd.concat([df, hist])
    return df

# 株価の範囲指定の説明
st.sidebar.write("""
    ## 株価の範囲指定
""")
ymin, ymax = st.sidebar.slider(
    '範囲を指定してください',
    0.0, 3500.0, (0.0, 3500.0)
)

