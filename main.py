import yfinance as yf
import plotly.graph_objects as go
import streamlit as st

NAME = 'ETH-USD'
INIT_USD = 1000000

if 'usd' not in st.session_state:
    st.session_state.usd = INIT_USD
    
if 'eth' not in st.session_state:
    st.session_state.eth = 0

st.set_page_config(layout='wide')

def get_data():
    return yf.download(tickers=NAME, period='3h', interval='1m')

data = get_data()

col1, col2 = st.columns([3, 1])

with col1:  
    fig = go.Figure([
        go.Scatter(x=data.index, y=data['Close'])
    ])

    st.header('%s %.4f' % (NAME, float(data.iloc[-1]['Close'])))

    fig.update_layout(height=800)

    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.header('사고 팔기')
    
    buy_amount = st.number_input('몇개를 매수할까요', min_value=0, value=0)
    
    current_price = float(data.iloc[-1]['Close'])
    
    if st.button('사자'):
        data = get_data()
        current_price = float(data.iloc[-1]['Close'])
        
        buy_price = buy_amount * current_price
        
        if st.session_state.usd >= buy_amount: # 구매가능
            st.session_state.eth += buy_amount
            st.session_state.usd -= buy_price
        else: # 돈이 모자르다
            st.warning('돈이 부족합니다.')
            
    sell_amount = st.number_input('몇개를 매도할까요', min_value=0, value=0)
    
    if st.button('팔자'):
        data = get_data()
        current_price = float(data.iloc[-1]['Close'])
        
        if st.session_state.eth >= sell_amount: # 매도가능
            sell_price = sell_amount * current_price
            
            st.session_state.eth -= sell_amount
            st.session_state.usd += sell_price
        else: # 팔 수 없음
            st.warning('이더리움이 부족합니다.')
    
    st.subheader('나의 USD %.2f' % st.session_state.usd)
    st.subheader('나의 ETH %d' % st.session_state.eth)
    
    total_in_usd = st.session_state.usd + st.session_state.eth * current_price
    profit = (total_in_usd - INIT_USD) / INIT_USD * 100
    
    st.subheader('손익 %.2f%%' % profit)
    