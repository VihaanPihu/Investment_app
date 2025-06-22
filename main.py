import streamlit as st
import datetime
from app_package.niftyVSdxy import historical_data
from app_package.plot import plot_lines
from app_package.mutualFund import MF
from app_package.IndexValuation import IndexVal
#from app_package import historical_data,MF,plot_lines,IndexVal
import pandas as pd


symbol_map = {
    "NIFTY 50": ["NIFTY", 1272594],
    "BANK NIFTY": ["BANKNIFTY", 1272670],
    "Nifty100 Quality 30": ["NIFTYQLY30", 1274022],
    "Nifty Next 50": ["NIFTYJR", 1272613],
    "Nifty IT": ["CNXIT", 1272649],
    "Nifty FMCG": ["CNXFMCG", 1272711],
    "Nifty Smallcap 250": ["SMALLCA250", 1275142]
}


st.set_page_config(page_title="Investment App", page_icon="📈",layout="wide")

# Simulated tabs via sidebar radio
st.sidebar.title("📚 Navigation")
tab = st.sidebar.radio("Go to", ["🏠 Home", "📈 Indices Valuation", "🧾 Stock Fundamental", "🔍 Screener","Mutual Fund Screener"])

# Common dates
end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=365)

# 🏠 Home Tab
if tab == "🏠 Home":
    st.title("📊 Home Dashboard")

    tabs=st.tabs(["Nifty Vs Dollar","Nifty Vs Gold"])

    # Sidebar specific to Home
    st.sidebar.subheader("📅 Date Picker")
    start_date = st.sidebar.date_input("Start Date", value=start_date)
    end_date = st.sidebar.date_input("End Date", value=end_date)
    ma_len = st.sidebar.number_input("Select Moving Average Period", min_value=1, max_value=1000, value=44)
    with tabs[0]:
        # Historical data
        nifty_index = historical_data("^NSEI", start_date=start_date, end_date=end_date, interval="1D", ma_len=ma_len)
        dollar_index = historical_data("DX-Y.NYB", start_date=start_date, end_date=end_date, interval="1D", ma_len=ma_len)

        nifty_df = nifty_index.load_data()
        dollar_df = dollar_index.load_data()

        st.subheader("Nifty 50")
        fig_nifty=plot_lines(nifty_df, ["Close", f"{ma_len}_DMA"], labels=["Nifty 50", f"{ma_len} DMA"], title="Nifty 50 Index")
        st.plotly_chart(fig_nifty, use_container_width=True)


        st.subheader("Dollar Index")
        fig_dollar=plot_lines(dollar_df, ["Close", f"{ma_len}_DMA"], labels=["Dollar Index", f"{ma_len} DMA"], title="Dollar Index")
        st.plotly_chart(fig_dollar, use_container_width=True)
    with tabs[1]:
        st.write("coming soon")



# 📈 Indices Valuation
elif tab == "📈 Indices Valuation":
    st.title("📈 Indices Valuation")
    st.markdown("----")
    st.sidebar.markdown("-----")
    st.sidebar.subheader("📊 Valuation Controls")
    index = st.sidebar.selectbox("Select Index",options=["NIFTY 50","BANK NIFTY","Nifty100 Quality 30","Nifty Next 50","Nifty IT","Nifty FMCG","Nifty Smallcap 250"])
    params=st.sidebar.selectbox("Select Parameters ",options=["Index Price-Index DMA50-Index DMA200","Index PE-Median Index PE","Index PBV-Median Index PBV","Index Dividend Yield-Median Index Dividend Yield"])
    st.write(f"You selected: {index} with {(params.split('-')[0])}")
    index_obj=IndexVal()
    st.table(index_obj.topRatios(symbol_map[index][0]))
    plot_data=index_obj.params_plot(symbol_map[index][1],param=params)
    if params!="Index Price-Index DMA50-Index DMA200":
        fig_obj=plot_lines(plot_data,["Price","Mean"])
    else:
        fig_obj=plot_lines(plot_data,["Price"])
    st.plotly_chart(fig_obj)


# 🧾 Stock Fundamental
elif tab == "🧾 Stock Fundamental":
    st.title("🧾 Stock Fundamental Analysis")
    st.sidebar.subheader("🔍 Company Search")
    symbol = st.sidebar.text_input("Enter Stock Symbol")
    if symbol:
        st.write(f"Loading fundamentals for {symbol}...")

    

# 🔍 Screener
elif tab == "🔍 Screener":
    st.title("🔍 Stock Screener")
    st.sidebar.subheader("📋 Screener Criteria")
    min_pe = st.sidebar.number_input("Min PE", value=0)
    max_pe = st.sidebar.number_input("Max PE", value=30)
    st.write(f"Filtering stocks with PE between {min_pe} and {max_pe}")
    

elif tab == "Mutual Fund Screener":
    mf_obj=MF()
    st.title("🔍 Mutual Fund Screener")
    st.sidebar.markdown("-----")
    

    mf_list=mf_obj.readMF()
    code=st.sidebar.selectbox(label="Select MF to Analyse",options=mf_list)
    
    col1,col2=st.columns([1,1])
    with col1:
        st.subheader("Scheme Summary")
        st.dataframe(mf_obj.mfSchemeDetails(int(code)))
        
    with col2:
        st.subheader("Last 5 Day NAV")
        nav_df=mf_obj.get_historicalData(int(code))
        st.dataframe(nav_df.tail())
    

    fig_mf=plot_lines(nav_df, ["nav", "44 DMA"], labels=["NAV", "44 DMA"], title="Mutual Fund NAV")
    st.plotly_chart(fig_mf, use_container_width=True)

    st.sidebar.markdown("-----")
    st.sidebar.subheader("📋 Add New MF to WatchList")
    #https://raw.githubusercontent.com/NayakwadiS/mftool/master/data/Scheme_codes.txt
    new_mf=st.sidebar.text_input("Enter Scheme Code")
    if st.sidebar.button(label="Add"):
        mf_obj.addMF(new_mf)
        
    
        

