import matplotlib.pyplot as plot    # digunakan untuk membuat grafik visual data
import pandas as pd                 # digunakan untuk melakukan  data manipulation dan analisis
import seaborn as ulpipi            # digunakan untuk membuat grafik statistik
import streamlit as lit             # digunakan untuk membuat dashboard
import datetime                     # digunakan untuk melakukan kalkulasi tanggal

ulpipi.set_style('darkgrid')


# Menyiapkan Function

# Function rental harian keseluruhan
def daily_rent_data(df):
    daily_rent = df.groupby(by='dteday').agg({
        'cnt': 'sum'
    }).reset_index()

    return daily_rent

# Function rental harian (kasual)
def casual_rent_data(df):
    daily_casual = df.groupby(by='dteday').agg({
        'casual': 'sum'
    }).reset_index()

    return daily_casual

# Function rental harian (terdaftar)
def registered_rent_data(df):
    daily_registered = df.groupby(by='dteday').agg({
        'registered': 'sum'
    }).reset_index()

    return daily_registered

# Function berdasarkan musim
def season_rent_data(df):
    season_rent = df.groupby(by='season').agg({
        'cnt': 'sum'
    }).reset_index()

    return season_rent

# Function berdasarkan hari
def weekday_rent_data(df):
    weekday_rent = df.groupby(by='weekday').agg({
        'cnt': 'sum'
    }).reset_index()

    return weekday_rent

# Funtion berdasarkan hari kerja
def workingday_rent_data(df):
    workingday_rent = df.groupby(by='workingday').agg({
        'cnt': 'sum'
    }).reset_index()

    return workingday_rent

# Function berdasarkan cuaca
def weather_rent_data(df):
    weather_rent = df.groupby(by='weathersit').agg({
        'cnt': 'sum'
    }).reset_index()

    return weather_rent

# Function berdasarkan bulan
def monthly_rent_data(df):
    monthly_rent = df.groupby(by='mnth').agg({
        'cnt': 'sum'
    }).reset_index()

    return monthly_rent

# Function berdasarkan tahun
def annual_rent_data(df):
    annual_rent = df.groupby(by='yr').agg({
        'cnt': 'sum'
    }).reset_index()

    return annual_rent

# Function berdasarkan holiday
def holiday_rent_data(df):
    holiday_rent = df.groupby(by='holiday').agg({
        'cnt': 'sum'
    }).reset_index()

    return holiday_rent

    

# Load dataset
data_hari = pd.read_csv('dashboard/fixed_dataset.csv')
data_hari["dteday"] = pd.to_datetime(data_hari["dteday"])

# Filter tanggal
min_date = data_hari["dteday"].min().date()
max_date = data_hari["dteday"].max().date()

with lit.sidebar:
    lit.image('dashboard/icon.jpg')

    start_date, end_date = lit.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = data_hari[(data_hari['dteday'] >= pd.to_datetime(start_date)) & 
                          (data_hari['dteday'] <= pd.to_datetime(end_date))]

# Memanggil Function yang telah dibuat
daily_rent = daily_rent_data(main_df)
casual_rent = casual_rent_data(main_df)
registered_rent = registered_rent_data(main_df)
seasonal_rent = season_rent_data(main_df)
weekdaily_rent = season_rent_data(main_df)
workingdaily_rent = workingday_rent_data(main_df)
weatherly_rent = weather_rent_data(main_df)
month_rent = monthly_rent_data(main_df)
annually_rent = annual_rent_data(main_df)
holi_rent = holiday_rent_data(main_df)


# Konten utama

lit.header("Bike Rental and Sharing Dashboard")

# Informasi penyewa secar menyeluruh
lit.subheader('Renter Information')
kol1, kol2, kol3 = lit.columns(3)

with kol1:
    daily_casual = casual_rent['casual'].sum()
    lit.metric('Casual Renter Total:', value= daily_casual)

with kol2:
    daily_registered = registered_rent['registered'].sum()
    lit.metric('Registered Renter Total:', value=daily_registered)

with kol3:
    daily_total = daily_rent['cnt'].sum()
    lit.metric('Total User:', value=daily_total)

fig, total_plot = plot.subplots(figsize=(10, 5))
total_plot.plot(
    main_df["dteday"],
    main_df["cnt"],
    marker='x', 
    linewidth=2,
    color="deepskyblue"
)
total_plot.tick_params(axis='y', labelsize=10)
total_plot.tick_params(axis='x', labelsize=5)

lit.pyplot(fig)

with lit.expander("Lihat Penjelasan"):
    lit.write(
        """Total jumlah transaksi penyewaan sepeda dimulai pada
        tanggal 01 Januari 2011 hingga 31 Desember 2012
        """
    )

# Informasi Casual dan Registered
lit.subheader("Casual and Registered Renter Information")
tabcas, tabreg = lit.tabs(["Casual", "Registered"])

# Casual
with tabcas:
    figcas, axis1 = plot.subplots(figsize=(10, 5))
    ulpipi.lineplot(
        x='dteday',
        y='casual',
        data=main_df,
        color='dodgerblue'
    )
    axis1.set_title("Casual Renter")
    axis1.set_xlabel('Casual')
    axis1.set_ylabel('Jumlah Penyewaan Sepeda')
    lit.pyplot(figcas)

    with lit.expander("Lihat Penjelasan"):
        lit.write(
            """Plot transaksi penyewaan sepeda pada penyewa kasual
              dimulai dari Januari, 2011 hingga Desember 2012"""
        )

# Registered
with tabreg:
    figreg, axis2 = plot.subplots(figsize=(10, 5))
    ulpipi.lineplot(
        x='dteday',
        y='registered',
        data=main_df,
        color='royalblue'
    )
    axis2.set_title("Registered Renter")
    axis2.set_xlabel('Registered')
    axis2.set_ylabel('Jumlah Penyewaan Sepeda')
    lit.pyplot(figreg)

    with lit.expander("Lihat Penjelasan"):
        lit.write(
            """Plot transaksi penyewaan sepeda pada penyewa terdaftar 
            dimulai dari Januari 2011 hingga Desember 2012"""
        )

# Informasi tiap bulanan dan tahunan
lit.subheader("Monthly and Annual Renter Information")
tab1, tab2 = lit.tabs(["Bulanan", 'Tahunan'])

# Bulanan
with tab1:
    fig1, ax1 = plot.subplots(figsize=(12, 5))
    ulpipi.lineplot(
        x='mnth',
        y='cnt',
        data=main_df,
        color='aqua'
    )
    ax1.set_title("Monthly Engagement")
    ax1.set_xlabel('Month')
    ax1.set_ylabel('Jumlah Penyewaan Sepeda')
    lit.pyplot(fig1)

    with lit.expander("Lihat Penjelasan"):
        lit.write(
            """Total jumlah transaksi penyewaan sepeda pada bulan Januari hingga Desember."""
        )

# Tahunan
with tab2:
    fig2, ax2 = plot.subplots(figsize=(10, 5))
    ulpipi.barplot(
        x='yr',
        y='cnt',
        data=main_df,
        color='lightskyblue'
    )
    ax2.set_title("Annual Engagement")
    ax2.set_xlabel('Year')
    ax2.set_ylabel('Jumlah Penyewaan Sepeda')
    lit.pyplot(fig2)

    with lit.expander("Lihat Penjelasan"):
        lit.write(
            """Total jumlah transaksi penyewaan sepeda pada tahun 2011 dan 2012."""
        )

# Informasi seputar weekday, workingday, dan holiday
urutan_hari = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
main_df['weekday'] = pd.Categorical(main_df['weekday'], categories=urutan_hari, ordered=True)

lit.subheader("Weekday, Workingday and Holiday Impacts on Renter Engagement")
weektab, worktab, holitab = lit.tabs(["Weekday", "Workingday", "Holiday"])

# Weekday
with weektab:
    figweek, axi1 = plot.subplots(figsize=(10, 5))
    ulpipi.lineplot(
        x='weekday',
        y='cnt',
        data=main_df,
        color='darkblue'
    )
    axi1.set_title("Daily Renter")
    axi1.set_xlabel('Day')
    axi1.set_ylabel('Jumlah Penyewaan Sepeda')
    lit.pyplot(figweek)

    with lit.expander("Lihat Penjelasan"):
        lit.write(
            """Total jumlah transaksi penyewaan sepeda berdasarkan hari."""
        )

# Workingday
with worktab:
    figwork, axi2 = plot.subplots(figsize=(10, 5))
    ulpipi.barplot(
        x='workingday',
        y='cnt',
        data=main_df,
        color='darkmagenta'
    )
    axi2.set_title("Working Day Data")
    axi2.set_xlabel('Working Day / Weekend')
    axi2.set_ylabel('Jumlah Penyewaan Sepeda')
    lit.pyplot(figwork)

    with lit.expander("Lihat Penjelasan"):
        lit.write(
            """Total jumlah transaksi penyewaan sepeda pada berdasarkan 
            hari kerja atau akhir pekan."""
        )

# Holiday
with holitab:
    figholi, axi3 = plot.subplots(figsize=(10, 5))
    ulpipi.barplot(
        x='holiday',
        y='cnt',
        data=main_df,
        color='rebeccapurple'
    )
    axi3.set_title("Holiday? Or Not?")
    axi3.set_xlabel('Holiday?')
    axi3.set_ylabel('Jumlah Penyewaan Sepeda')
    lit.pyplot(figholi)

    with lit.expander("Lihat Penjelasan"):
        lit.write(
            """Total jumlah transaksi penyewaan sepeda pada berdasarkan 
            hari libur atau bukan."""
        )

# Informasi seputar cuaca dan musim

lit.subheader("Weather Situation and Season")
weatab, seatab = lit.tabs(["Weather", "Season"])

# Cuaca
with weatab:
    figwea, a1 = plot.subplots(figsize=(10, 5))
    ulpipi.barplot(
        x='weathersit',
        y='cnt',
        data=main_df,
        color='turquoise'
    )
    a1.set_title("Weather Impact")
    a1.set_xlabel('Weather')
    a1.set_ylabel('Jumlah Penyewaan Sepeda')
    lit.pyplot(figwea)

    with lit.expander("Lihat Penjelasan"):
        lit.write(
            """Total jumlah transaksi penyewaan sepeda berdasarkan cuaca."""
        )

# Musim
with seatab:
    figsea, a2 = plot.subplots(figsize=(10, 5))
    ulpipi.barplot(
        x='season',
        y='cnt',
        data=main_df,
        color='cyan'
    )
    a2.set_title("Season Impact")
    a2.set_xlabel('Season')
    a2.set_ylabel('Jumlah Penyewaan Sepeda')
    lit.pyplot(figsea)

    with lit.expander("Lihat Penjelasan"):
        lit.write(
            """Total jumlah transaksi penyewaan sepeda berdasarkan musim."""
        )
