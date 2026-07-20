import streamlit as st
import pandas as pd
import plotly.express as px
from textblob import TextBlob

st.set_page_config(page_title="Sales Dashboard",layout="wide")
df=pd.read_csv("data/sales_data.csv")
fb=pd.read_csv("data/feedback.csv")
import streamlit as st
import pandas as pd
import plotly.express as px
from textblob import TextBlob

st.set_page_config(page_title="Sales Dashboard", layout="wide")

# 👇 INSERT THESE TWO LINES HERE
st.title("📊 Sales Dashboard")
st.markdown("Analyze sales performance and customer feedback in one place.")

df = pd.read_csv("data/sales_data.csv")
fb = pd.read_csv("data/feedback.csv")

st.sidebar.header("Filters")
regions=st.sidebar.multiselect("Region",df.Region.unique(),default=list(df.Region.unique()))
cats=st.sidebar.multiselect("Category",df.Category.unique(),default=list(df.Category.unique()))
d=df[df.Region.isin(regions)&df.Category.isin(cats)]

rev=d["Revenue"].sum()
profit=d["Profit"].sum()
c1,c2=st.columns(2)
c1.metric("Revenue",f"${rev:,.0f}")
c2.metric("Profit",f"${profit:,.0f}")

st.plotly_chart(px.bar(d.groupby("Region",as_index=False)["Revenue"].sum(),x="Region",y="Revenue",title="Sales by Region"),use_container_width=True)
st.plotly_chart(px.bar(d.groupby("Category",as_index=False)["Revenue"].sum(),x="Category",y="Revenue",title="Sales by Category"),use_container_width=True)
m=d.groupby("Month",as_index=False)["Revenue"].sum()
st.plotly_chart(px.line(m,x="Month",y="Revenue",markers=True,title="Monthly Trend"),use_container_width=True)
top=d.groupby("Product",as_index=False)["Revenue"].sum().sort_values("Revenue",ascending=False).head(10)
st.plotly_chart(px.bar(top,x="Product",y="Revenue",title="Top Products"),use_container_width=True)

fb["Polarity"]=fb["Feedback"].apply(lambda x: TextBlob(str(x)).sentiment.polarity)
fb["Sentiment"]=fb["Polarity"].apply(lambda p:"Positive" if p>0 else "Negative" if p<0 else "Neutral")
st.subheader("Feedback Sentiment")
st.dataframe(fb)

