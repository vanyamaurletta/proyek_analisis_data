# import pacakge
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# jumlah penyewaan sepeda tiap jam
# perubahan baru 
def create_hourly_bike_sharing_df(hours_df):
    hourly_bike_sharing_df =  hours_df.groupby(by="hour").agg({
        "counts": "sum"})
    return hourly_bike_sharing_df

# jumlah penyewaan sepeda oleh registered
def create_byregistered_df(days_df):
    count_registered_df =  days_df.groupby(by="dteday").agg({
      "registered": "sum"})
    count_registered_df = count_registered_df.reset_index()
    return count_registered_df

# jumlah penyewaan sepeda oleh casual
def create_bycasual_df(days_df):
    count_casual_df =  days_df.groupby(by="dteday").agg({
      "casual": "sum"})
    count_casual_df = count_casual_df.reset_index()
    return count_casual_df

# jumlah penyewaan sepeda (causal+registered)
def create_bycounts_df(days_df):
    count_counts_df =  days_df.groupby(by="dteday").agg({
      "counts": "sum"})
    count_counts_df = count_counts_df.reset_index()
    return count_counts_df

# jumlah penyewaan sepeda pada kondisi cuaca tertentu
def create_byweathersit_df(days_df):
    count_weathersit_df =  days_df.groupby(by="weathersit").agg({
      "counts": "sum"})
    count_weathersit_df = count_weathersit_df.reset_index()
    return count_weathersit_df

#  jumlah penyewaan pada workingday, holiday, dan weekday
def create_working_holiday_weekend(days_df):
    working_holiday_weekend = days_df.groupby(by=['workingday','holiday','weekday']).agg({
    'counts':'sum'
    })
    working_holiday_weekend = working_holiday_weekend.reset_index()
    return working_holiday_weekend

# read csv
days_df = pd.read_csv("/Users/vanyamaurletta/Downloads/proyek_analisis_data/dashboard/days.csv")
hours_df = pd.read_csv("/Users/vanyamaurletta/Downloads/proyek_analisis_data/dashboard/hours.csv")

days_df.sort_values(by="dteday", inplace=True)
days_df.reset_index(inplace=True)
days_df["dteday"] = pd.to_datetime(days_df["dteday"])

hours_df.sort_values(by="dteday", inplace=True)
hours_df.reset_index(inplace=True)
hours_df["dteday"] = pd.to_datetime(hours_df["dteday"])

min_days_date = days_df["dteday"].min()
max_days_date = days_df["dteday"].max()

min_hours_date = hours_df["dteday"].min()
max_hours_date = hours_df["dteday"].max()

# side bar 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://raw.githubusercontent.com/vanyamaurletta/BikeSharing/main/Bike-sharing-dataset/bikepic.jpg")

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_days_date,
        max_value=max_days_date,
        value=[min_days_date, max_days_date]
    )

# filter tanggal
main_days_df = days_df[(days_df["dteday"] >= str(start_date)) & 
                       (days_df["dteday"] <= str(end_date))]

main_hours_df = hours_df[(hours_df["dteday"] >= str(start_date)) & 
                        (hours_df["dteday"] <= str(end_date))]

# memanggil  helper function dengan filter tanggal yang sudah dibuat untuk kebuuthan visualisasi data
hourly_counts_df = create_hourly_bike_sharing_df(main_hours_df)
daily_counts_df = create_bycounts_df(main_days_df)
registered_counts_df = create_byregistered_df(main_days_df)
casual_counts_df = create_bycasual_df(main_days_df)
weathersit_counts_df = create_byweathersit_df(main_days_df)
working_holiday_counts_df = create_working_holiday_weekend(main_days_df)

# judul dashboard
st.header('Bike Sharing Rental Dashboard :sparkles:')

# subheader
st.subheader("Performa penyewaan sepeda pada tahun 2011-2012")
# grafik penyewaan sepeda harian dari 2011-2012
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    days_df["dteday"],
    days_df["counts"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)
 
#subheader
# grafik penyewaan sepeda harian dari filter tanggal yang diinginkan
st.subheader('Penyewaan sepeda harian')
col1, col2, col3 = st.columns(3)

with col1:
    total_registered = registered_counts_df.registered.sum()
    st.metric("Total Registered", value=total_registered)

with col2:
    total_casual = casual_counts_df.casual.sum()
    st.metric("Total Casual", value=total_casual)

with col3:
    total_counts = daily_counts_df.counts.sum()
    st.metric("Total Harian", value=total_counts)

st.subheader('Performa penyewaan sepeda harian')
fig, ax = plt.subplots(figsize=(16, 8))
plt.plot(daily_counts_df["dteday"],daily_counts_df["counts"], marker='o', linewidth=2, color="#72BCD4")
st.pyplot(fig)

# subheader
# grafik jam-jam terbaik dan terburuk pada rentang hari tertentu
st.subheader("Jam-jam terbaik dan terburuk penyewaan sepeda")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

colors1 = ["#FF7F50", "#FF7F50", "#FF7F50", "#FF7F50", "#FF7F50"]
sns.barplot(x="hour", y="counts", data=hourly_counts_df.sort_values(by="counts", ascending=False).head(5), palette=colors1, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Lima jam-jam terbaik penyewaan sepeda", loc="center", fontsize=15)
ax[0].tick_params(axis ='y', labelsize=12)

colors2 = ["#B8860B", "#B8860B", "#B8860B", "#B8860B", "#B8860B"]
sns.barplot(x="hour", y="counts", data=hourly_counts_df.sort_values(by="counts", ascending=True).head(5), palette=colors2, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].set_title("Lima jam-jam terburuk penyewaan sepeda", loc="center", fontsize=15)
ax[1].tick_params(axis='y', labelsize=12)

st.pyplot(fig)

# subheader
# grafik penyewaan sepeda berdasarkan kondisi cuaca pada rentang hari terentu
st.subheader('Jumlah penyewaan sepeda berdasarkan cuaca')
fig, ax = plt.subplots(figsize=(16, 8))
colors = ["#8B0000", "#E9967A", "#E9967A"]
sns.barplot(x='weathersit',
            y='counts',
            data=weathersit_counts_df,
            palette=colors)
st.pyplot(fig)

# subheader
# grafik penyewaan sepeda pada workingday, weekday, weekend di rentang hari tertentu
st.subheader('Perbandingan penyewaan sepeda pada hari kerja, hari libur, akhir minggu')
fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(data=working_holiday_counts_df,
            x="workingday",
            y="counts",
            hue="holiday",
            palette=["#8FBC8F", "#556B2F"],
            errorbar=None)
st.pyplot(fig)


