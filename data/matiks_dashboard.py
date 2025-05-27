import pandas as pd
import streamlit as st
import plotly.express as px

df = pd.read_csv("matiks_data.csv")

df['Signup_Date'] = pd.to_datetime(df['Signup_Date'], format='%d-%b-%Y')
df['Last_Login'] = pd.to_datetime(df['Last_Login'], format='%d-%b-%Y')

st.set_page_config(page_title="Matiks Dashboard", layout="wide")

st.title("📊 Matiks User & Revenue Dashboard")

with st.expander("🔍 Preview Dataset"):
    st.dataframe(df.head())

st.header("📅 User Activity Over Time")
dau = df.groupby('Last_Login')['User_ID'].nunique().reset_index(name='DAU')
fig_dau = px.line(dau, x='Last_Login', y='DAU', title='Daily Active Users (DAU)')
st.plotly_chart(fig_dau, use_container_width=True)

st.header("💸 Revenue Trends")
revenue = df.groupby('Last_Login')['Total_Revenue_USD'].sum().reset_index()
fig_revenue = px.line(revenue, x='Last_Login', y='Total_Revenue_USD', title='Total Revenue by Date')
st.plotly_chart(fig_revenue, use_container_width=True)

st.header("📱 Revenue by Device Type")
device_rev = df.groupby('Device_Type')['Total_Revenue_USD'].sum().reset_index()
fig_device = px.bar(device_rev, x='Device_Type', y='Total_Revenue_USD', title='Revenue by Device')
st.plotly_chart(fig_device, use_container_width=True)

st.header("🌟 Revenue by Subscription Tier")
tier_rev = df.groupby('Subscription_Tier')['Total_Revenue_USD'].sum().reset_index()
fig_tier = px.bar(tier_rev, x='Subscription_Tier', y='Total_Revenue_USD', title='Revenue by Subscription Tier')
st.plotly_chart(fig_tier, use_container_width=True)

st.header("🎮 Revenue by Game Mode")
mode_rev = df.groupby('Preferred_Game_Mode')['Total_Revenue_USD'].sum().reset_index()
fig_mode = px.bar(mode_rev, x='Preferred_Game_Mode', y='Total_Revenue_USD', title='Revenue by Game Mode')
st.plotly_chart(fig_mode, use_container_width=True)

with st.expander("🎯 Filter & Explore More"):
    game_selected = st.selectbox("Select Game Title", df['Game_Title'].unique())
    filtered_df = df[df['Game_Title'] == game_selected]
    st.write(f"Total Users for {game_selected}: {filtered_df['User_ID'].nunique()}")
    st.dataframe(filtered_df[['User_ID', 'Signup_Date', 'Last_Login', 'Total_Revenue_USD']].head())

st.header("⚠️ Churn Risk Users")
churn_cutoff = df['Last_Login'].max() - pd.Timedelta(days=30)
churn_df = df[df['Last_Login'] < churn_cutoff]

st.write(f"Churn-risk users: {churn_df.shape[0]} out of {df.shape[0]}")
st.dataframe(churn_df[['User_ID', 'Last_Login', 'Total_Play_Sessions', 'Total_Revenue_USD']].sort_values(by='Last_Login'))

st.header("💰 High-Value Users")
top_users = df[df['Total_Revenue_USD'] > df['Total_Revenue_USD'].quantile(0.95)]
st.write(f"Top 5% Revenue Users: {top_users.shape[0]}")

fig_high_value = px.histogram(top_users, x='Device_Type', color='Subscription_Tier', barmode='group',
                              title='High Revenue Users by Device & Tier')
st.plotly_chart(fig_high_value, use_container_width=True)

st.dataframe(top_users[['User_ID', 'Total_Revenue_USD', 'Subscription_Tier', 'Preferred_Game_Mode']])