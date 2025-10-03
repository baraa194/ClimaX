# 🌍 ClimaX 

## 📖 Overview  
ClimaX is a **smart activity planning dashboard** that combines **NASA POWER weather data** with **AI-powered recommendations** to help users plan their daily or weekly activities based on climate conditions.  

Users simply enter their activities (e.g., swimming, gardening, gym), and the system recommends the best time or day to perform them considering:  
- 🌡️ Temperature  
- 💧 Humidity  
- 💨 Wind speed  
- ☔ Precipitation  
- ☀️ Solar radiation  

It also provides **trend analysis** using decades of historical NASA data to predict weather patterns for the chosen date.  

---

## ✨ Features  
✅ Select city (currently supports Cairo, London, Tokyo, New York, Sydney)  
✅ **Daily Plan** → activities grouped into Morning / Afternoon / Evening  
✅ **Weekly Plan** → distributes activities across the week (Mon–Sun)  
✅ Predicted weather data based on historical climate trends (1981 onwards)  
✅ Interactive graphs showing **temperature trends over years**  
✅ **Smart AI Recommendations** powered by Ollama LLM  
✅ Clean and responsive UI built with **Streamlit**  

---

## 🖼️ Screenshots  

### 🔹 Home Page – Select options  
![Home](https://github.com/baraa194/ClimaX/raw/main/2.png)

### 🔹 Daily Plan – Example activities  
![Daily](https://github.com/baraa194/ClimaX/raw/main/3.png)

### 🔹 Trend Analysis – Temperature over years  
![Trend](https://github.com/baraa194/ClimaX/raw/main/4.png)

### 🔹 Recommendations – AI Recommendations of activities
![Weekly](https://github.com/baraa194/ClimaX/raw/main/5.png)

### 🔹 Predicted Weather Data Table  
![Predicted](https://github.com/baraa194/ClimaX/raw/main/7.png)

### 🔹 Weekly Plan – Distributed activities  && Prediction of week
<p align="center">
  <img src="https://github.com/baraa194/ClimaX/raw/main/8.png" width="45%">
  <img src="https://github.com/baraa194/ClimaX/raw/main/6.png" width="45%">
</p>




---

## ⚙️ Tech Stack  
- **Python 3.11+**  
- **Streamlit** for the interactive dashboard  
- **Pandas, NumPy, Matplotlib** for data analysis & visualization  
- **NASA POWER API** for historical climate data  
- **Ollama LLM** for generating smart activity recommendations  

---

## 🚀 Run Locally  

1. Clone the repository:  
```bash
git clone https://github.com/baraa194/ClimaX.git

