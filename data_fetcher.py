# data_fetcher.py
import requests
import numpy as np
import pandas as pd
from datetime import datetime


NASA_DATA_START_YEAR = 1981

def clean_nasa_value(value):

    return np.nan if value == -999 else value

def get_nasa_weather_for_single_year(city_coords, date_str):

    url = (
        f"https://power.larc.nasa.gov/api/temporal/daily/point"
        f"?start={date_str}&end={date_str}"
        f"&latitude={city_coords['lat']}&longitude={city_coords['lon']}"
        f"&community=SB&parameters=T2M,RH2M,WS2M,PRECTOTCORR,PS,ALLSKY_SFC_SW_DWN"
        f"&format=JSON"
    )
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            params = data.get("properties", {}).get("parameter", {})
            return {
                "temperature": clean_nasa_value(params.get("T2M", {}).get(str(date_str), -999)),
                "humidity": clean_nasa_value(params.get("RH2M", {}).get(str(date_str), -999)),
                "wind_speed": clean_nasa_value(params.get("WS2M", {}).get(str(date_str), -999)),
                "precipitation": clean_nasa_value(params.get("PRECTOTCORR", {}).get(str(date_str), -999)),
                "pressure": clean_nasa_value(params.get("PS", {}).get(str(date_str), -999)),
                "solar_radiation": clean_nasa_value(params.get("ALLSKY_SFC_SW_DWN", {}).get(str(date_str), -999))
            }
    except:
        pass
    return None

def get_multi_year_weather_data(city_coords, target_date):

    historical_data = {}
    for year in range(NASA_DATA_START_YEAR, target_date.year):
        historical_date = target_date.replace(year=year)
        date_str = historical_date.strftime("%Y%m%d")
        data = get_nasa_weather_for_single_year(city_coords, date_str)
        if data:
            historical_data[year] = data
        else:
            if not historical_data:
                st.warning(f"Could not find data for year {year}. The archive for this location might start later.")
            break
    return historical_data

def predict_weather_and_get_trend(historical_data, target_year):

    if not historical_data or len(historical_data) < 2:
        return None, None

    years_list = list(historical_data.keys())
    years_for_fit = np.array(years_list).reshape(-1, 1)
    
    prediction = {}
    trend_parameters = {}
    
    for param in ['temperature', 'humidity', 'wind_speed', 'precipitation', 'pressure', 'solar_radiation']:
        values = np.array([historical_data[y][param] for y in years_list])
        
        valid_indices = ~np.isnan(values)
        if np.sum(valid_indices) < 2:
            prediction[param] = np.nan
            trend_parameters[param] = {'slope': np.nan, 'intercept': np.nan}
            continue
            
        clean_years = years_for_fit[valid_indices]
        clean_values = values[valid_indices]
        
        try:
            slope, intercept = np.polyfit(clean_years.flatten(), clean_values, 1)
            predicted_value = slope * target_year + intercept
            
            prediction[param] = predicted_value

            trend_parameters[param] = {'slope': slope, 'intercept': intercept}
        except:
            prediction[param] = np.nan
            trend_parameters[param] = {'slope': np.nan, 'intercept': np.nan}
            
    return prediction, trend_parameters

def get_nasa_weather(city_coords, date):

    historical_data = get_multi_year_weather_data(city_coords, date)
    if not historical_data:
        return None, None, None
        
    predicted_weather, trend_params = predict_weather_and_get_trend(historical_data, date.year)
    return predicted_weather, historical_data, trend_params



def create_weather_dataframe(weather_data):

    if not weather_data:
        return pd.DataFrame()
    
    weather_df = pd.DataFrame.from_dict(weather_data, orient='index')
    weather_df.index.name = 'Date'
    weather_df.reset_index(inplace=True)
    weather_df['Date'] = pd.to_datetime(weather_df['Date']).dt.strftime('%Y-%m-%d')
    weather_df = weather_df.rename(columns={
        'temperature': 'Temperature (°C)',
        'humidity': 'Humidity (%)',
        'wind_speed': 'Wind Speed (m/s)',
        'precipitation': 'Precipitation (mm)',
        'pressure': 'Pressure (hPa)',
        'solar_radiation': 'Solar Radiation (W/m²)'
    })
    return weather_df