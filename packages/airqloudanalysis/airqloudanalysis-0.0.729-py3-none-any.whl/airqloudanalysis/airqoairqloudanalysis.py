import json
import numpy as np
from pandas import json_normalize
import requests
import pandas as pd
import time
import glob
import os
from os import read

#Other important libaries for datetime + timezone, OS for interacting with the operating system, requests for sending HTTP requests, BeautifulSoup for web scrapping
#Str to datetime library
from pytz import all_timezones
from datetime import datetime, timedelta
from dateutil import parser
from datetime import date# @title Neccessary libraries
from datetime import datetime
#python libraries needed
from collections import defaultdict

# Data processing libraries
import json
import numpy as np
from pandas import json_normalize
import requests
import pandas as pd
import time

#Other important libaries for datetime + timezone, OS for interacting with the operating system, requests for sending HTTP requests, BeautifulSoup for web scrapping
#Str to datetime library
from pytz import all_timezones
from datetime import datetime, timedelta
from dateutil import parser
from datetime import date
import datetime
#Datetime modifier libraries
import matplotlib.units as munits
import matplotlib.dates as mdates

#Visualization Libraries
import seaborn as sns
import matplotlib.pyplot as plt

#Interactive Plots Libraries
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot#importing libraries from plotly offline
import cufflinks as cf
init_notebook_mode(connected=True)#connecting javascript to notebook to allow access visualization
cf.go_offline()
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
#Datetime modifier libraries
import matplotlib.units as munits
import matplotlib.dates as mdates

#Visualization Libraries
import seaborn as sns
import matplotlib.pyplot as plt

#Interactive Plots Libraries
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot#importing libraries from plotly offline
import cufflinks as cf
init_notebook_mode(connected=True)#connecting javascript to notebook to allow access visualization
cf.go_offline()
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#Other lib picked as I created the notebook
from re import X

converter = mdates.ConciseDateConverter()
munits.registry[np.datetime64] = converter
munits.registry[datetime.date] = converter

"""# Data initialisation functions
## Data processing"""
#Function to preprocess the datasets from the API
def preprocessing(df):
    # df.drop(columns=['field8'], inplace=True)
    # Convert str columns to float
    for col in ['field1', 'field2', 'field3', 'field4', 'field7']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Drop rows where any of the important columns have NaN values
    df = df.dropna(subset=["field1", "field2", "field3", "field4", "field7"])

    # Rename columns for clarity
    df = df.rename(columns={
        "field1": "Sensor1 PM2.5_CF_1_ug/m3",
        "field2": "Sensor1 PM10_CF_1_ug/m3",
        "field3": "Sensor2 PM2.5_CF_1_ug/m3",
        "field4": "Sensor2 PM10_CF_1_ug/m3",
        "field5": "Latitude",
        "field6": "Longitude",
        "field7": "Battery Voltage"
    })

    # Datetime data preprocessing
    df['created_at'] = pd.to_datetime(df['created_at'].apply(lambda x: parser.parse(x)))  # str to datetime type
    df['Date'] = df['created_at'].dt.date

    # Drop the extra Latitude and Longitude columns as they're not needed for further analysis
    df.drop(['Latitude', 'Longitude'], axis=1, inplace=True)

    # Calculate the mean PM2.5 and PM10 values
    df["Mean PM2.5"] = (df["Sensor1 PM2.5_CF_1_ug/m3"] + df["Sensor2 PM2.5_CF_1_ug/m3"]) / 2
    df["Mean PM10"] = (df["Sensor1 PM10_CF_1_ug/m3"] + df["Sensor2 PM10_CF_1_ug/m3"]) / 2

    # Drop the 'entry_id' column if it's not necessary
    df.drop(columns=["entry_id"], inplace=True, errors='ignore')

    # Reset index for neatness
    df.reset_index(drop=True, inplace=True)

    return df
# preprocessing(data)


"""## Create the weekly data"""
def calculate_days_between(start, end):
    # Convert the date strings to datetime objects
    start_date = datetime.strptime(start, '%Y-%m-%d')
    end_date = datetime.strptime(end, '%Y-%m-%d')

    # Calculate the difference in days
    delta = end_date - start_date

    # Return the difference in days
    return delta.days

def create_dates(start, end):
    # Parse the input dates   
    start_date = pd.to_datetime(start)
    end_date = pd.to_datetime(end)

    # Calculate the total number of days between the start and end dates
    total_days = calculate_days_between(start, end)

    # Calculate how many full 8-day intervals fit, and the remainder
    full_intervals = total_days // 8
    remainder = total_days % 8
    
    # Generate the main part of the date range with '8D' frequency
    if full_intervals > 0:
        main_range = pd.date_range(start=start_date, periods=full_intervals + 1, freq='8D')
    else:
        main_range = pd.Series([start_date])
    
    # Handle the remainder: create the final date as `start_date + total_days` and append
    if remainder > 0:
        last_date = start_date + pd.Timedelta(days=total_days)
        full_range = pd.concat([pd.Series(main_range), pd.Series([last_date])], ignore_index=True)
    else:
        full_range = pd.Series(main_range)

    # Create a DataFrame with the generated date range
    df = pd.DataFrame(full_range, columns=['Date'])
    
    # Recalculate the number of days between the first and last date in the DataFrame
    if not df.empty:
        first_date_in_df = df['Date'].iloc[0].strftime('%Y-%m-%d')
        last_date_in_df = df['Date'].iloc[-1].strftime('%Y-%m-%d')
        days_between_df_dates = calculate_days_between(first_date_in_df, last_date_in_df)
    else:
        days_between_df_dates = 0
        first_date_in_df = start
        last_date_in_df = end

    return df, days_between_df_dates, first_date_in_df, last_date_in_df
# df, days_between_df_dates, first_date_in_df, last_date_in_df = create_dates(start, end)


"""
Retriving the data by fetching the max number of records at a time
"""
from datetime import datetime
def fetch_all_records(channel_id, api_key, start_date, end_date):
    current_end = end_date  # Start fetching from the end date
    all_data = []  # List to store all fetched data

    #converting channel_id to string
    channel_id = str(channel_id)

    while True:
        # Generate the URL for the current chunk
        url = (
            f"https://thingspeak.com/channels/{channel_id}/feeds.json?"
            f"start={start_date}T00:00:00Z&end={current_end}T23:59:59Z&api_key={api_key}&results=8000"
        )
        response = requests.get(url)
        data = response.json()

        # Get the feeds from the response
        feeds = data.get("feeds", [])
        if not feeds:
            print("No more feeds to fetch.")
            break

        # Append feeds to the all_data list
        all_data.extend(feeds)

        # Check if the number of feeds is less than the maximum limit (8000)
        if len(feeds) < 8000:
            print(f"Fetched {len(feeds)} records in the last batch. All records retrieved.")
            break

        # Get the timestamp of the first record in this chunk
        first_timestamp = feeds[0]["created_at"]
        first_datetime = datetime.strptime(first_timestamp, "%Y-%m-%dT%H:%M:%SZ")

        # Stop if the first record's timestamp is earlier than or equal to the start_date
        if first_datetime <= datetime.strptime(start_date, "%Y-%m-%d"):
            print("Fetched all records up to the start date.")
            break

        # Update the end time for the next request
        current_end = first_datetime.strftime("%Y-%m-%dT%H:%M:%S")
        print(f"Fetching next chunk up to {current_end}")

    # Convert the collected data into a Pandas DataFrame
    df = pd.DataFrame(all_data)

    # Check if 'entry_id' column exists before dropping NAs
    if 'entry_id' in df.columns:
        # delete na entry_id
        df = df.dropna(subset=['entry_id'])

        # organise based i=on entry_id
        df = df.sort_values(by='entry_id')
        df.reset_index(drop=True, inplace=True)

        # delete duplicate entry_id
        df = df.drop_duplicates(subset='entry_id', keep='first')
        df.reset_index(drop=True, inplace=True)
    else:
        # print row without entry_id
        print("Warning: 'entry_id' column not found in the data.")

    # print(df)
    return df



"""## URL functions"""
#Function to generate the url for the APIs from thingspeak
def url( ID, key, start, end):
  url = 'https://thingspeak.com/channels/'+str(ID)+'/feeds.json?start='+str(start)+'T00:00:00Z&end='+str(end)+'T23:59:59Z&api_key='+str(key)
  return url
# url(123456, 'ABCD1234', start, end)

#Function to generate the last url for the APIs from thingspeak for the time off functionality
def lastUrl(ID, key):
  lastUrl = 'https://thingspeak.com/channels/' + str(ID) + '/feeds.json?api_key=' + str(key) + '&results=1'
  # lastUrl = 'https://thingspeak.com/channels/' + str(ID) + '/feeds/last.json?api_key=' + str(key)
  return lastUrl
# lastUrl(123456, 'ABCD1234')


"""## DataFrame airqloud formation"""
"""## by API"""
baseApiURL = "https://api.airqo.net/api/v2/devices"

def getDeviceData(token):
  url = f"{baseApiURL}?token={token}"
  response = requests.request("GET", url)
  # print(response.json())
  return response.json()
#getDeviceData("your_token")

def getSiteData(token):
#   url = str(baseApiURL) + "/metadata/grids?token=" + str(token)
  url = str(baseApiURL) + "/grids/summary?token=" + str(token)
  response = requests.request("GET", url)
  # print(response.json())
  return response.json()
#getSiteData("your_token")

def decryptData(token, data):
    url = f"{baseApiURL}/decrypt/bulk?token={token}"

    response = requests.post(url, json=data)

    if response.status_code == 200:
        # print(response.json())
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None
#decryptData("your_token", "your_data")

def processSiteData(token):
    # Fetch site data
    site_data = getSiteData(token)

    if site_data.get('success') and 'grids' in site_data:
        grids = site_data['grids']
        data = [{"name": grid["name"], "admin_level": grid["admin_level"]} for grid in grids]

        df = pd.DataFrame(data)
        grouped_df = df.groupby('admin_level').apply(lambda x: x[['name']].reset_index(drop=True))

        return grouped_df
    else:
        print("Error: No grids data available")
        return pd.DataFrame()
#grouped_df=processSiteData("your_token")

def airqloudlist_api(token, airQlouds):
    device_data = getDeviceData(token)

    data_list = []

    if device_data.get("success"):
        devices = device_data.get("devices", [])

        # Process each device  "category": "lowcost",
        for device in devices:
          if device.get("category") == "lowcost" or device.get("category") == None:
            long_name = device.get("long_name")
            device_number = device.get("device_number")
            readKey = device.get("readKey")

            # Process each grid entry within a device
            for grid in device.get("grids", []):
                grid_id = grid.get("_id")
                grid_name = grid.get("name")
                admin_level = grid.get("admin_level")

                for airQloud in airQlouds:
                  if airQloud in grid_name:
                    #AirQloud Append the processed data to the list
                    data_list.append({
                        "Device Number": long_name,
                        "Device ID": str(device_number) if device_number is not None else None,
                        "Read Key": readKey,
                        "grid_id": grid_id,
                        "grid_name": grid_name,
                        "admin_level": admin_level
                    })
    else:
        print("Error fetching device data")

    df = pd.DataFrame(data_list)
    df = df.dropna(subset=["Device ID"])
    df = df.dropna(subset=["Read Key"])

    # Data encryption
    encryption_data = []
    for _, row in df.iterrows():
        encryption_data.append({
            "encrypted_key": row["Read Key"],
            "device_number": int(row["Device ID"])
        })

    # Decrypt the read keys
    decrypted_data = decryptData(token, encryption_data)

    if decrypted_data and decrypted_data.get('decrypted_keys'):
        decrypted_keys = [decrypted.get('decrypted_key') for decrypted in decrypted_data['decrypted_keys']]

        if len(decrypted_keys) == len(df):
            df["Decrypted Read Key"] = decrypted_keys
        else:
            print("Mismatch between decrypted keys and DataFrame length")

    df = df.drop(columns=["Read Key"])
    df = df.rename(columns={"Decrypted Read Key": "Read Key", "grid_name":"AirQloud", "grid_id" : "AirQloud ID", "admin_level" : "AirQloud Type"})

    return df
# df = airqloudlist_api(token)

"""## by google drive"""
def airqloudlist(filepath, excelfile, airQlouds, deviceNames):
  dfs = []
  # Check if both lists are empty
  if len(airQlouds) > 0 and len(deviceNames) > 0:
    return "airQlouds and deviceNames  can not both have data"

  # Check if either list is empty
  if len(airQlouds) > 0:
    for sheet_name in excelfile.sheet_names:
      for AirQloud in airQlouds: 
        if sheet_name == AirQloud:
          df = pd.read_excel(filepath, sheet_name=sheet_name)
          df['AirQloud'] = sheet_name
          df = df[['Device Number', 'Read Key', 'Device ID', 'AirQloud']]
          df = df.astype({'Device Number': str, 'Read Key': str, 'Device ID': str, 'AirQloud': str})
          dfs.append(df)

    AQData = pd.concat(dfs, ignore_index=True)
    return AQData

  elif len(deviceNames) > 0:
    for sheet_name in excelfile.sheet_names:
      df = pd.read_excel(filepath, sheet_name=sheet_name)
      df['AirQloud'] = sheet_name
      df = df[['Device Number', 'Read Key', 'Device ID', 'AirQloud']]
      df = df.astype({'Device Number': str, 'Read Key': str, 'Device ID': str, 'AirQloud': str})
      dfs.append(df)

    AQData = pd.concat(dfs, ignore_index=True)
    # Create a new DataFrame to store the filtered rows
    filtered_data = []
    for index, row in AQData.iterrows():
      deviceNumber = row['Device Number']
      if deviceNumber in deviceNames: # Check if the device number is in the list of device names
        filtered_data.append(row)
    # Create a DataFrame from the filtered rows
    AQData = pd.DataFrame(filtered_data)
    return AQData
  else:
    return "either airQlouds or deviceNames must have data"
# AQData = airqloudlist(file_path, excel_file, airQlouds, deviceNames)


"""## initializing dataframe"""
def process_data(df, start, end):
    all_data = []  # List to store data for all devices

    for index, row in df.iterrows():
        deviceNumber = row['Device Number']
        readKey = row['Read Key']
        deviceID = row['Device ID']
        deviceDataFrame = pd.DataFrame()  # Initialize an empty DataFrame for each device

        # Fetch the raw data for this device
        raw_data = fetch_all_records(deviceID, readKey, start, end)

        # Preprocess the data
        if raw_data.empty:
            print(f"No data found for Device Number {deviceNumber}")
            continue  # Skip empty datasets

        # Preprocessing the raw data
        deviceDataFrame = preprocessing(raw_data)

        # Check if deviceDataFrame is not empty
        if not deviceDataFrame.empty:
            # Add Device Number as a column
            deviceDataFrame['Device Number'] = deviceNumber
            all_data.append(deviceDataFrame)  # Append the processed data to the list
            print("Done", deviceNumber)
        else:
            print(f"No valid data for Device Number {deviceNumber}")

    # Concatenate all device data into one DataFrame
    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
    else:
        final_df = pd.DataFrame()  # If all_data is empty, return an empty DataFrame

    # Merge with the original AQData based on 'Device Number'
    if not final_df.empty:
        final_df = pd.merge(final_df, df, on=['Device Number'], how='left')
    else:
        print("Final DataFrame is empty after concatenation.")

    return final_df
# final_df = process_data(AQData, start, end)

def process_data_function(df, startdate, enddate, airqlouds_csv):
    additional_data = []

    for airqloud in df['AirQloud'].unique():
        airqloud_df = df[df['AirQloud'] == airqloud]
        airqloud_name = f"*{airqloud}*"
        matching_file = glob.glob(os.path.join(airqlouds_csv, airqloud_name))
        
        if matching_file:
            existing_data = pd.read_csv(matching_file[0])
            existing_start = existing_data['Date'].min()
            existing_end = existing_data['Date'].max()

            # dates are aligned with the existing data
            if existing_start == startdate and existing_end == enddate:
                return existing_data

            # data starts after startdate and ends after enddate
            if startdate > existing_start and enddate > existing_end:
                new_data = process_data(airqloud_df, existing_end, enddate)
                additional_data.append(new_data)
                updated_data = pd.concat([existing_data, new_data])

            # data starts before startdate and ends before enddate    
            elif startdate < existing_start and enddate < existing_end:
                new_data = process_data(airqloud_df, startdate, existing_start)
                additional_data.append(new_data)
                updated_data = pd.concat([existing_data, new_data])

            # data starts after startdate and ends before enddate
            elif startdate > existing_start and enddate < existing_end:
                new_data_start = process_data(airqloud_df, existing_end, enddate)
                new_data_end = process_data(airqloud_df, startdate, existing_start)
                additional_data.extend([new_data_start, new_data_end])
                updated_data = pd.concat([new_data_start, existing_data, new_data_end])

            # data starts before startdate and ends after enddate
            elif startdate < existing_start and enddate > existing_end:
                pass

            finaldf = pd.concat([existing_data] + additional_data) if additional_data else existing_data
            # get the data in the range of the startdate and enddate
            finaldf = finaldf[(finaldf['Date'] >= startdate) & (finaldf['Date'] <= enddate)]

# def process_data_function(df, startdate, enddate, airqlouds_csv):
#     #  for deviceNumber in df['Device Number'].unique():
#     for airqloud in df['AirQloud'].unique():
#         filename = f"{airqlouds_csv}/{startdate}_{enddate}_{airqloud}.csv"
#         try:
#             existing_data = pd.read_csv(filename)
#             existing_start = existing_data['Date'].min()
#             existing_end = existing_data['Date'].max()

#             if existing_start == startdate and existing_end == enddate:
#                 return existing_data

#             additional_data = []

#             if startdate > existing_start and enddate > existing_end:
#                 new_data = process_data(df, existing_end, enddate)
#                 additional_data.append(new_data)
#                 updated_data = pd.concat([existing_data, new_data])


# def process_data_function(df, startdate, enddate, airqloud):
#     filename = f"/content/drive/MyDrive/{startdate}_{enddate}_{airqloud}.csv"
    
#     try:
#         existing_data = pd.read_csv(filename)
#         existing_start = existing_data['timestamp'].min()
#         existing_end = existing_data['timestamp'].max()
        
#         if existing_start == startdate and existing_end == enddate:
#             return existing_data  # Return as DataFrame
        
#         additional_data = []
        
#         if startdate > existing_start and enddate > existing_end:
#             new_data = fetch_data(existing_end, enddate, airqloud)
#             additional_data.append(new_data)
#             new_filename = f"/content/drive/MyDrive/{startdate}_{enddate}_{airqloud}.csv"
#             updated_data = pd.concat([existing_data, new_data])
#             updated_data.to_csv(new_filename, index=False)
        
#         elif startdate < existing_start and enddate < existing_end:
#             new_data = fetch_data(startdate, existing_start, airqloud)
#             additional_data.append(new_data)
#             new_filename = f"/content/drive/MyDrive/{startdate}_{enddate}_{airqloud}.csv"
#             updated_data = pd.concat([new_data, existing_data])
#             updated_data.to_csv(new_filename, index=False)
        
#         elif startdate > existing_start and enddate < existing_end:
#             new_data_start = fetch_data(existing_end, enddate, airqloud)
#             new_data_end = fetch_data(startdate, existing_start, airqloud)
#             additional_data.extend([new_data_start, new_data_end])
#             new_filename = f"/content/drive/MyDrive/{startdate}_{enddate}_{airqloud}.csv"
#             updated_data = pd.concat([new_data_start, existing_data, new_data_end])
#             updated_data.to_csv(new_filename, index=False)
        
#         elif startdate < existing_start and enddate > existing_end:
#             pass  # No action needed
        
#         return pd.concat([existing_data] + additional_data) if additional_data else existing_data
#     except FileNotFoundError:
#         new_data = fetch_data(startdate, enddate, airqloud)
#         new_data.to_csv(filename, index=False)
#         return new_data


"""## Device time off"""
def timeLastPost(df):
    results = []
    for index, row in df.iterrows():
        deviceNumber = row['Device Number']
        readKey = row['Read Key']
        deviceID = row['Device ID']
        airqloud = row['AirQloud']
        last = lastUrl(deviceID, readKey)

        # Fetch data from the API
        try:
            lastData = requests.get(last)
            lastData = lastData.json()
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            print(f"Error fetching data for Device ID {deviceID}: {e}")
            continue  # Skip to the next row

        # Check if 'feeds' exists and is not empty
        if 'feeds' not in lastData or not lastData['feeds']:
            print(f"No data found in feeds for Device ID {deviceID}")
            continue  # Skip to the next row

        # Extract and parse the created_at timestamp
        created_at_str = lastData['feeds'][0]['created_at']
        created_at = datetime.strptime(created_at_str, '%Y-%m-%dT%H:%M:%SZ')

        current_time = datetime.utcnow()
        time_difference = current_time - created_at
        time_diff_flag = 1 if time_difference < timedelta(days=1) else 0


        results.append({
            'Device Number': deviceNumber,
            'Time Difference Flag': time_diff_flag,
            'Time Difference': time_difference,
            'AirQloud': airqloud
        })

    result_df = pd.DataFrame(results)
    return result_df
# device_time_diff = timeLastPost(AQData)


"""## Uptime variable  initialisation"""
# Function to calculate the average uptime of the devices
def calculate_uptime(df, start, end):
    # Initialize lists to store results
    average_device_uptime = []
    average_completeness_lst = []
    device_uptime = []
    device_completeness = []
    device_list = []
    airqloud_list = []
    optimal_completeness_lst = []
    good_completeness_lst = []
    fair_completeness_lst = []
    poor_completeness_lst = []
    sensor_error = []
    error_dfs = []

    # Iterate over unique device numbers
    for deviceNumber in df['Device Number'].unique():
        # Filter data for the current device
        device_df = df[df['Device Number'] == deviceNumber]

        # Convert 'created_at' column to datetime
        device_df['created_at'] = pd.to_datetime(device_df['created_at'])

        # Extract date and hour
        device_df['date'] = device_df['created_at'].dt.date
        device_df['hour'] = device_df['created_at'].dt.hour
        device_df['timestamp'] = device_df['created_at'].dt.strftime('%Y-%m-%d %H')
        device_df['Error margin'] = np.abs(device_df['Sensor1 PM2.5_CF_1_ug/m3'] - device_df['Sensor2 PM2.5_CF_1_ug/m3'])

        # Group by date and count unique hours for uptime
        uptime_df = device_df.groupby('date')['hour'].nunique().reset_index(name='uptime')
        completeness_df = device_df.groupby(['timestamp']).size().reset_index(name='data_entries')
        # error = magnitude('Sensor1 PM2.5_CF_1_ug/m3' - 'Sensor2 PM2.5_CF_1_ug/m3')
        error_df = device_df.groupby(['timestamp'])['Error margin'].mean().reset_index(name='error')


        # Calculate average uptime
        # average_uptime = round(uptime_df['uptime'].mean(), 2)
        # calculate average uptime is the sum of the uptime divided by the number of days between the start and end date which are strings
        average_uptime = round(uptime_df['uptime'].sum() / (aqa.calculate_days_between(start, end) + 1), 2)
        average_completeness = round(completeness_df['data_entries'].mean(), 2)
        average_error = round(error_df['error'].mean(), 2)

        # Calculate completeness categories
        optimal_count = completeness_df[completeness_df['data_entries'] > 18].shape[0]
        good_count = completeness_df[(completeness_df['data_entries'] >= 15) & (completeness_df['data_entries'] <= 18)].shape[0]
        fair_count = completeness_df[(completeness_df['data_entries'] >= 10) & (completeness_df['data_entries'] <= 14)].shape[0]
        poor_count = completeness_df[(completeness_df['data_entries'] >= 1) & (completeness_df['data_entries'] <= 9)].shape[0]

        # Append results to lists
        device_list.append(deviceNumber)
        airqloud_list.append(device_df['AirQloud'].iloc[0])
        average_device_uptime.append(average_uptime)
        device_uptime.append(uptime_df)
        device_completeness.append(completeness_df)
        average_completeness_lst.append(average_completeness)
        optimal_completeness_lst.append(optimal_count)#(round(((optimal_count/(optimal_count + good_count + fair_count + poor_count)) * 100),2))
        good_completeness_lst.append(good_count)#(round(((good_count/(optimal_count + good_count + fair_count + poor_count)) * 100),2))
        fair_completeness_lst.append(fair_count)#(round(((fair_count/(optimal_count + good_count + fair_count + poor_count)) * 100),2))
        poor_completeness_lst.append(poor_count)#(round(((poor_count/(optimal_count + good_count + fair_count + poor_count)) * 100),2))
        sensor_error.append(average_error)
        error_dfs.append(error_df)

    # Create final DataFrame to return
    result_df = pd.DataFrame({
        'Device Number': device_list,
        'Average Uptime': average_device_uptime,
        'Device Uptime': device_uptime,
        'Sensor Error' : error_dfs,
        'Average Sensor Error': sensor_error,
        'Device Completeness': device_completeness,
        'Average Completeness': average_completeness_lst,
        'Optimal Completeness': optimal_completeness_lst,
        'Good Completeness': good_completeness_lst,
        'Fair Completeness': fair_completeness_lst,
        'Poor Completeness': poor_completeness_lst
    })

    return result_df
# final_uptime_data = calculate_uptime(final_df, start, end)





"""# General summary
 This shows the uptime summary of different networks like devices on and off plus the uptime
## All airqloud summary
"""
def create_summary_df(AQData, time_last_post_df, calculate_uptime_df):
    # Ensure AQData is a DataFrame
    if not isinstance(AQData, pd.DataFrame):
        raise ValueError("AQData must be a pandas DataFrame")

    # Merge the DataFrames on 'Device Number' using outer joins
    summary_df = AQData.merge(time_last_post_df[['Device Number', 'Time Difference Flag', 'Time Difference']],
                              on='Device Number', how='outer')
    summary_df = summary_df.merge(calculate_uptime_df[[
        'Device Number',
        'Average Completeness',
        'Average Uptime',
        'Average Sensor Error',
        'Sensor Error',
        'Optimal Completeness',
        'Good Completeness',
        'Fair Completeness',
        'Poor Completeness'
        ]], on='Device Number', how='outer')

    # Extract relevant columns from AQData
    summary_df = summary_df[[
        'Device Number',
        'AirQloud',
        'Average Uptime',
        'Average Sensor Error',
        'Sensor Error',
        'Average Completeness',
        'Optimal Completeness',
        'Good Completeness',
        'Fair Completeness',
        'Poor Completeness',
        'Time Difference Flag',
        'Time Difference'
        ]]

    return summary_df
# summary_df = create_summary_df(AQData, device_time_diff, final_uptime_data)


"""## Off devices"""
def print_devices_with_time_diff_flag_zero(df, airQlouds, deviceNames):
    # Check if both lists are empty
    if len(airQlouds) > 0 and len(deviceNames) > 0:
      return "airQlouds and deviceNames  can not both have data"

    # Ensure df is a DataFrame
    if not isinstance(df, pd.DataFrame):
        raise ValueError("df must be a pandas DataFrame")

    # Filter the DataFrame to only include rows where Time Difference Flag is 0
    filtered_df = df[df['Time Difference Flag'] == 0]

    if len(airQlouds) > 0:
      # Group by AirQloud and print the devices
      for airqloud, group, time_diff in filtered_df.groupby('AirQloud'):
        print(f"AirQloud: {airqloud}")
        for device in group['Device Number']:
            # print(f"  Device Number: {device}")
            print(f"  Device Number: {device} --> {time_diff}")

        print("------------------------")
        print("")

    elif len(deviceNames) > 0:
      # Group by AirQloud and print the devices
      print("Off line devices")
      for airqloud, group in filtered_df.groupby('Device Number'):
        for device in group['Device Number']:
            print(f"  Device Number: {device}")
        print("")
    else:
      return "either airQlouds or deviceNames must have data"
# print_devices_with_time_diff_flag_zero(summary_df, airQlouds, deviceNames)

def print_devices_with_time_diff_flag_zero_api(df, airQlouds, deviceNames):
    # Check if both lists are populated
    if len(airQlouds) > 0 and len(deviceNames) > 0:
        return "airQlouds and deviceNames cannot both have data"
    # Ensure df is a DataFrame
    if not isinstance(df, pd.DataFrame):
        raise ValueError("df must be a pandas DataFrame")
    # Filter the DataFrame to only include rows where Time Difference Flag is 0
    filtered_df = df[df['Time Difference Flag'] == 0]
    if len(airQlouds) > 0:
        # Filter for specific AirQlouds
        airQloud_filtered_df = filtered_df[filtered_df['AirQloud'].isin(airQlouds)]
        return airQloud_filtered_df[['AirQloud', 'Device Number']].drop_duplicates()
    elif len(deviceNames) > 0:
        # Filter for specific Device Names
        device_filtered_df = filtered_df[filtered_df['Device Number'].isin(deviceNames)]
        return device_filtered_df[['AirQloud', 'Device Number']].drop_duplicates()
    else:
        return "Either airQlouds or deviceNames must have data"
# off_devices = print_devices_with_time_diff_flag_zero_api(summary_df, airQlouds, deviceNames)

"""## CSV export for the summary"""
def export_summary_csv(summary_df, output_file, airQlouds, deviceNames):
    # Check if both lists are empty
    if len(airQlouds) > 0 and len(deviceNames) > 0:
        return "airQlouds and deviceNames cannot both have data"

    # Ensure summary_df is a DataFrame
    if not isinstance(summary_df, pd.DataFrame):
        raise ValueError("summary_df must be a pandas DataFrame")

    # Fill NaN values in Average Uptime with 0
    summary_df['Average Uptime'] = summary_df['Average Uptime'].fillna(0)

    # Group by AirQloud or Device Number and calculate the required metrics
    if len(airQlouds) > 0:
        summary_grouped = summary_df.groupby('AirQloud').agg(
            Off=('Time Difference Flag', lambda x: (x == 0).sum()),
            On=('Time Difference Flag', lambda x: (x == 1).sum()),
            Uptime=('Average Uptime', lambda x: round((x.mean() / 24) * 100, 2)),
            Average_Sensor_Error=('Average Sensor Error', lambda x: round(x.mean(), 2)),
            Completeness=('Average Completeness', lambda x: round(x.mean(), 2)),
            Optimal=('Optimal Completeness', 'mean'),
            Good=('Good Completeness', 'mean'),
            Fair=('Fair Completeness', 'mean'),
            Poor=('Poor Completeness', 'mean')
        ).reset_index()

    elif len(deviceNames) > 0:
        summary_grouped = summary_df.groupby('Device Number').agg(
            Uptime=('Average Uptime', lambda x: round((x.mean() / 24) * 100, 2)),
            Off=('Time Difference Flag', lambda x: (x == 0).sum()),
            On=('Time Difference Flag', lambda x: (x == 1).sum()),
            Average_Sensor_Error=('Average Sensor Error', lambda x: round(x.mean(), 2)),
            Completeness=('Average Completeness', lambda x: round(x.mean(), 2)),
            Optimal=('Optimal Completeness', 'mean'),
            Good=('Good Completeness', 'mean'),
            Fair=('Fair Completeness', 'mean'),
            Poor=('Poor Completeness', 'mean')
        ).reset_index()

    else:
        return "Either airQlouds or deviceNames must have data"

    # Calculate the Total Completeness as the sum of means of Optimal, Good, Fair, and Poor
    summary_grouped['Total Completeness'] = (
        summary_grouped['Optimal'] +
        summary_grouped['Good'] +
        summary_grouped['Fair'] +
        summary_grouped['Poor']
    )

    # Convert Optimal, Good, Fair, and Poor to percentages of the Total Completeness
    summary_grouped['Optimal'] = round((summary_grouped['Optimal'] / summary_grouped['Total Completeness']) * 100, 2)
    summary_grouped['Good'] = round((summary_grouped['Good'] / summary_grouped['Total Completeness']) * 100, 2)
    summary_grouped['Fair'] = round((summary_grouped['Fair'] / summary_grouped['Total Completeness']) * 100, 2)
    summary_grouped['Poor'] = round((summary_grouped['Poor'] / summary_grouped['Total Completeness']) * 100, 2)

    summary_grouped = summary_grouped.drop(columns=['Total Completeness'])
    summary_grouped = summary_grouped.rename(columns={
        'Off': 'Devices Off',
        'On': 'Devices On',
        'Completeness': 'Hourly Completeness',
        'Optimal': 'Optimal Completeness (%)',
        'Good': 'Good Completeness (%)',
        'Fair': 'Fair Completeness (%)',
        'Poor': 'Poor Completeness (%)'
    })
    summary_grouped.fillna(0, inplace=True)

    # Export the summary DataFrame to a CSV file
    summary_grouped.to_csv(output_file, index=False)

    return summary_grouped
# output_file = 'summary.csv'
# summary_grouped = export_summary_csv(summary_df, output_file, airQlouds, deviceNames)

def export_summary_csv_api(summary_df, airQlouds, deviceNames):
    # Check if both lists are empty
    if len(airQlouds) > 0 and len(deviceNames) > 0:
      return "airQlouds and deviceNames  can not both have data"
    # Ensure summary_df is a DataFrame
    if not isinstance(summary_df, pd.DataFrame):
        raise ValueError("summary_df must be a pandas DataFrame")
    # Group by AirQloud or device Number and calculate the required metrics
    if len(airQlouds) > 0:
      summary_grouped = summary_df.groupby('AirQloud').agg(
        Off=('Time Difference Flag', lambda x: (x == 0).sum()),
        On=('Time Difference Flag', lambda x: (x == 1).sum()),
        Uptime=('Average Uptime', lambda x: round((x.mean() / 24) * 100, 2)),
        Average_Sensor_Error=('Average Sensor Error', lambda x: round(x.mean(), 2)),
        Completeness=('Average Completeness', lambda x: round(x.mean(), 2)),
        Optimal=('Optimal Completeness', 'mean'),
        Good=('Good Completeness', 'mean'),
        Fair=('Fair Completeness', 'mean'),
        Poor=('Poor Completeness', 'mean')
      ).reset_index()
    elif len(deviceNames) > 0:
      summary_grouped = summary_df.groupby('Device Number').agg(
        Uptime=('Average Uptime', lambda x: round((x.mean() / 24) * 100, 2)),
        Off=('Time Difference Flag', lambda x: (x == 0).sum()),
        On=('Time Difference Flag', lambda x: (x == 1).sum()),
        Average_Sensor_Error=('Average Sensor Error', lambda x: round(x.mean(), 2)),
        Completeness=('Average Completeness', lambda x: round(x.mean(), 2)),
        Optimal=('Optimal Completeness', 'mean'),
        Good=('Good Completeness', 'mean'),
        Fair=('Fair Completeness', 'mean'),
        Poor=('Poor Completeness', 'mean')
      ).reset_index()
    else:
      return "either airQlouds or deviceNames must have data"
    # Calculate the Total Completeness as the sum of means of Optimal, Good, Fair, and Poor
    summary_grouped['Total Completeness'] = (
        summary_grouped['Optimal'] +
        summary_grouped['Good'] +
        summary_grouped['Fair'] +
        summary_grouped['Poor']
    )
    # Convert Optimal, Good, Fair, and Poor to percentages of the Total Completeness
    summary_grouped['Optimal'] = round((summary_grouped['Optimal'] / summary_grouped['Total Completeness']) * 100, 2)
    summary_grouped['Good'] = round((summary_grouped['Good'] / summary_grouped['Total Completeness']) * 100, 2)
    summary_grouped['Fair'] = round((summary_grouped['Fair'] / summary_grouped['Total Completeness']) * 100, 2)
    summary_grouped['Poor'] = round((summary_grouped['Poor'] / summary_grouped['Total Completeness']) * 100, 2)
    summary_grouped = summary_grouped.drop(columns=['Total Completeness'])
    summary_grouped = summary_grouped.rename(columns={
        'Off': 'Devices Off',
        'On': 'Devices On',
        'Completeness': 'Hourly Completeness',
        'Optimal': 'Optimal Completeness (%)',
        'Good': 'Good Completeness (%)',
        'Fair': 'Fair Completeness (%)',
        'Poor': 'Poor Completeness (%)'
        })
    summary_grouped.fillna(0, inplace=True)
    return summary_grouped
# summary_grouped = export_summary_csv_api(summary_df, airQlouds, deviceNames)

"""## Average device uptime over period"""
def plot_uptime_by_device(summary_df):
    if not isinstance(summary_df, pd.DataFrame):
        raise ValueError("summary_df must be a pandas DataFrame")

    uptime_data = summary_df.groupby('Device Number').agg(
        Uptime=('Average Uptime', lambda x: round((x.mean() / 24) * 100, 2))
    ).reset_index()

    fig = px.bar(uptime_data, x='Device Number', y='Uptime', title='Uptime for Each Device',
                 labels={'Uptime': 'Uptime (%)', 'Device Number': 'Device Number'},
                 text='Uptime')

    fig.update_layout(height=600, width=1200, showlegend=False,)
    fig.show(renderer='colab')
# plot_uptime_by_device(summary_df)

def plot_uptime_by_device_api(summary_df):
    if not isinstance(summary_df, pd.DataFrame):
        raise ValueError("summary_df must be a pandas DataFrame")
    uptime_data = summary_df.groupby('Device Number').agg(
        Uptime=('Average Uptime', lambda x: round((x.mean() / 24) * 100, 2))
    ).reset_index()
    return uptime_data
# uptime_data = plot_uptime_by_device_api(summary_df)

"""## Uptime
### Weekly uptime """
def calculate_daily_uptime_per_device(final_df, AQData, start, end):
    weekly_df, analysis_duration, first_date_in_df, last_date_in_df = create_dates(start, end)

    # Merging the dataframes on 'Device Number'
    final_df = pd.merge(final_df, AQData, on='Device Number', how='right')

    # Filling NaN values with zero
    final_df.fillna(0, inplace=True)

    # Ensure 'created_at' is in datetime format
    # final_df['created_at'] = pd.to_datetime(final_df['created_at'], errors='coerce')
    final_df['created_at'] = pd.to_datetime(final_df['created_at'], errors='coerce', utc=True)

    # Extract date and hour from 'created_at'
    final_df['Date'] = final_df['created_at'].dt.date
    final_df['Hour'] = final_df['created_at'].dt.hour

    # Group by 'Device Number', 'Date', and 'Hour' to calculate hourly uptime
    hourly_uptime = final_df.groupby(['Device Number', 'Date', 'Hour']).size().reset_index(name='Count')

    # Group by 'Device Number' and 'Date' to calculate daily uptime (number of hours with data)
    daily_uptime = hourly_uptime.groupby(['Device Number', 'Date']).size().reset_index(name='Daily Uptime (hours)')

    # Ensure that we have a complete set of dates for each device
    all_devices = final_df['Device Number'].unique()
    date_range = pd.date_range(start=final_df['Date'].min(), end=final_df['Date'].max())

    # Create a MultiIndex from all combinations of devices and dates
    all_index = pd.MultiIndex.from_product([all_devices, date_range], names=['Device Number', 'Date'])

    # Reindex the daily uptime dataframe to include all dates for each device
    daily_uptime = daily_uptime.set_index(['Device Number', 'Date']).reindex(all_index, fill_value=0).reset_index()

    # Filter the data for the specified date range
    start_date = pd.to_datetime(first_date_in_df)
    end_date = pd.to_datetime(last_date_in_df)
    daily_uptime = daily_uptime[(daily_uptime['Date'] >= start_date) & (daily_uptime['Date'] <= end_date)]


    return daily_uptime
# daily_uptime = calculate_daily_uptime_per_device(final_df, AQData, start, end)

def calculate_weekly_average_uptime(final_df, AQData, airQlouds, deviceNames, start, end):
    # Check if both lists are empty
    if len(airQlouds) > 0 and len(deviceNames) > 0:
      return "airQlouds and deviceNames  can not both have data"

    # Calculate daily uptime per device
    daily_uptime = calculate_daily_uptime_per_device(final_df, AQData, start, end)

    # Convert 'Date' to datetime to extract the week
    daily_uptime['Date'] = pd.to_datetime(daily_uptime['Date'])
    daily_uptime['Week'] = daily_uptime['Date'].dt.to_period('W').apply(lambda r: r.start_time)

    # Merge the daily uptime with the original dataframe to get 'AirQloud'
    merged_df = daily_uptime.merge(final_df[['Device Number', 'AirQloud']].drop_duplicates(), on='Device Number')

    if len(airQlouds) > 0:
      # Group by 'AirQloud' and 'Week' to calculate the weekly average uptime
      weekly_uptime = merged_df.groupby(['AirQloud', 'Week'])['Daily Uptime (hours)'].mean().reset_index(name='Weekly Average Uptime (hours)')

    elif len(deviceNames) > 0:
      # Group by 'Device Number' and 'Week' to calculate the weekly average uptime
      weekly_uptime = merged_df.groupby(['Device Number', 'Week'])['Daily Uptime (hours)'].mean().reset_index(name='Weekly Average Uptime (hours)')
    else:
      return "either airQlouds or deviceNames must have data"

    # Convert the weekly average uptime to a percentage
    weekly_uptime['Weekly Average Uptime (%)'] = (weekly_uptime['Weekly Average Uptime (hours)'] / 24) * 100

    return weekly_uptime
# weekly_average_uptime = calculate_weekly_average_uptime(final_df, AQData, airQlouds, deviceNames, start, end)

def format_weekly_uptime_output(weekly_uptime, airQlouds, deviceNames):
    # Check if both lists are empty
    if len(airQlouds) > 0 and len(deviceNames) > 0:
      return "airQlouds and deviceNames  can not both have data"

    if len(airQlouds) > 0:
      # Pivot the table to get weeks as columns and AirQlouds as rows
      pivot_table = weekly_uptime.pivot(index='AirQloud', columns='Week', values='Weekly Average Uptime (%)')

    elif len(deviceNames) > 0:
      # Pivot the table to get weeks as columns and AirQlouds as rows
      pivot_table = weekly_uptime.pivot(index='Device Number', columns='Week', values='Weekly Average Uptime (%)')

    else:
      return "either airQlouds or deviceNames must have data"

    # Reset the index to make 'AirQloud' a column
    pivot_table.reset_index(inplace=True)

    return pivot_table
# formatted_weekly_uptime = format_weekly_uptime_output(weekly_average_uptime, airQlouds, deviceNames)


"""### Weekly uptime trends"""
def plot_weekly_uptime(pivot_table, airQlouds, deviceNames):
    if len(airQlouds) > 0 and len(deviceNames) > 0:
      return "airQlouds and deviceNames  can not both have data"

    if len(airQlouds) > 0:
      melted_df = pd.melt(pivot_table, id_vars=['AirQloud'], var_name='Week', value_name='Weekly Average Uptime (%)')

      fig = px.bar(melted_df, x='AirQloud', y='Weekly Average Uptime (%)', color='Week',
                 barmode='group', labels={'x': 'AirQloud', 'y': 'Weekly Average Uptime (%)'},
                 title='Weekly Average Uptime (%) per AirQloud',
                 hover_name='AirQloud', hover_data=['Week', 'Weekly Average Uptime (%)'])

    elif len(deviceNames) > 0:
      melted_df = pd.melt(pivot_table, id_vars=['Device Number'], var_name='Week', value_name='Weekly Average Uptime (%)')

      fig = px.bar(melted_df, x='Device Number', y='Weekly Average Uptime (%)', color='Week',
                 barmode='group', labels={'x': 'Device Number', 'y': 'Weekly Average Uptime (%)'},
                 title='Weekly Average Uptime (%) per Device Number',
                 hover_name='Device Number', hover_data=['Week', 'Weekly Average Uptime (%)'])

    else:
      return "either airQlouds or deviceNames must have data"

    fig.update_layout(height=600, width=1200, showlegend=False)
    fig.show(renderer='colab')
# plot_weekly_uptime(formatted_weekly_uptime, airQlouds, deviceNames)


"""## Sensor error margin
### Weekly sensor  error margin"""
def calculate_daily_error_margin_per_device(df):
    # Ensure 'created_at' is in datetime format
    df['created_at'] = pd.to_datetime(df['created_at'])

    # Calculate the error margin
    df['error_margin'] = np.abs(df['Sensor1 PM2.5_CF_1_ug/m3'] - df['Sensor2 PM2.5_CF_1_ug/m3'])

    # Extract date from 'created_at'
    df['Date'] = df['created_at'].dt.date

    # Group by 'Device Number' and 'Date' to calculate daily error margin
    daily_error_margin = df.groupby(['Device Number', 'Date', 'AirQloud'])['error_margin'].mean().reset_index(name='Daily Error Margin')

    return daily_error_margin
# daily_error_margin = calculate_daily_error_margin_per_device(final_df)

def calculate_weekly_average_error_margin(df, airQlouds, deviceNames):
    # Check if both lists are empty
    if len(airQlouds) > 0 and len(deviceNames) > 0:
      return "airQlouds and deviceNames  can not both have data"

    # Calculate daily error margin per device
    daily_error_margin = calculate_daily_error_margin_per_device(df)

    # Convert 'Date' to datetime to extract the week
    daily_error_margin['Date'] = pd.to_datetime(daily_error_margin['Date'])
    daily_error_margin['Week'] = daily_error_margin['Date'].dt.to_period('W').apply(lambda r: r.start_time)

    if len(airQlouds) > 0:
      # Group by 'AirQloud' and 'Week' to calculate the weekly average error margin
      weekly_error_margin = daily_error_margin.groupby(['AirQloud', 'Week'])['Daily Error Margin'].mean().reset_index(name='Weekly Average Error Margin')

    elif len(deviceNames) > 0:
      # Group by 'Device Number' and 'Week' to calculate the weekly average error margin
      weekly_error_margin = daily_error_margin.groupby(['Device Number', 'Week'])['Daily Error Margin'].mean().reset_index(name='Weekly Average Error Margin')

    else:
      return "either airQlouds or deviceNames must have data"

    return weekly_error_margin
# weekly_error_margin = calculate_weekly_average_error_margin(final_df, airQlouds, deviceNames)

def format_weekly_error_margin_output(weekly_error_margin, airQlouds, deviceNames):
    # Check if both lists are empty
    if len(airQlouds) > 0 and len(deviceNames) > 0:
      return "airQlouds and deviceNames  can not both have data"

    if len(airQlouds) > 0:
      # Pivot the table to get weeks as columns and AirQlouds as rows
      pivot_table = weekly_error_margin.pivot(index='AirQloud', columns='Week', values='Weekly Average Error Margin')

    elif len(deviceNames) > 0:
      # Pivot the table to get weeks as columns and AirQlouds as rows
      pivot_table = weekly_error_margin.pivot(index='Device Number', columns='Week', values='Weekly Average Error Margin')

    else:
      return "either airQlouds or deviceNames must have data"

    # Reset the index to make 'AirQloud' a column
    pivot_table.reset_index(inplace=True)

    return pivot_table
# formatted_weekly_error_margin = format_weekly_error_margin_output(weekly_error_margin, airQlouds, deviceNames)


"""### Weekly sensor error margin trends"""
def plot_weekly_error(pivot_table, airQlouds, deviceNames):
    if len(airQlouds) > 0 and len(deviceNames) > 0:
      return "airQlouds and deviceNames  can not both have data"

    if len(airQlouds) > 0:
      melted_df = pd.melt(pivot_table, id_vars=['AirQloud'], var_name='Week', value_name='Weekly Average Error Margin')

      fig = px.bar(melted_df, x='AirQloud', y='Weekly Average Error Margin', color='Week',
                 barmode='group', labels={'x': 'AirQloud', 'y': 'Weekly Average Error Margin'},
                 title='Weekly Average Error Margin per AirQloud',
                 hover_name='AirQloud', hover_data=['Week', 'Weekly Average Error Margin'])

    elif len(deviceNames) > 0:
      melted_df = pd.melt(pivot_table, id_vars=['Device Number'], var_name='Week', value_name='Weekly Average Error Margin')

      fig = px.bar(melted_df, x='Device Number', y='Weekly Average Error Margin', color='Week',
                 barmode='group', labels={'x': 'Device Number', 'y': 'Weekly Average Error Margin'},
                 title='Weekly Average Error Margin per Device',
                 hover_name='Device Number', hover_data=['Week', 'Weekly Average Error Margin'])

    fig.update_layout(height=600, width=1200, showlegend=False)
    fig.show(renderer='colab')
# plot_weekly_error(formatted_weekly_error_margin, airQlouds, deviceNames)


"""## Device completeness
### Weekly device completeness"""
def calculate_daily_completeness_per_device(df):
    # Ensure 'created_at' is in datetime format
    df['created_at'] = pd.to_datetime(df['created_at'])

    # Extract date and hour from 'created_at'
    df['Date'] = df['created_at'].dt.date
    df['Hour'] = df['created_at'].dt.hour

    # Group by 'Device Number', 'Date', and 'Hour' to calculate hourly completeness
    hourly_completeness = df.groupby(['Device Number', 'Date', 'Hour']).size().reset_index(name='Count')

    # Group by 'Device Number' and 'Date' to calculate daily completeness (average number of entries per hour)
    daily_completeness = hourly_completeness.groupby(['Device Number', 'Date'])['Count'].mean().reset_index(name='Daily Completeness (entries/hour)')

    return daily_completeness
# daily_completeness = calculate_daily_completeness_per_device(final_df)

def calculate_weekly_average_completeness(df, airQlouds, deviceNames):
    # Check if both lists are empty
    if len(airQlouds) > 0 and len(deviceNames) > 0:
      return "airQlouds and deviceNames  can not both have data"

    # Calculate daily completeness per device
    daily_completeness = calculate_daily_completeness_per_device(df)

    # Convert 'Date' to datetime to extract the week
    daily_completeness['Date'] = pd.to_datetime(daily_completeness['Date'])
    daily_completeness['Week'] = daily_completeness['Date'].dt.to_period('W').apply(lambda r: r.start_time)

    # Merge the daily completeness with the original dataframe to get 'AirQloud'
    merged_df = daily_completeness.merge(df[['Device Number', 'AirQloud']].drop_duplicates(), on='Device Number')

    if len(airQlouds) > 0:
      # Group by 'AirQloud' and 'Week' to calculate the weekly average completeness
      weekly_completeness = merged_df.groupby(['AirQloud', 'Week'])['Daily Completeness (entries/hour)'].mean().reset_index(name='Weekly Average Completeness (entries/hour)')

    elif len(deviceNames) > 0:
      # Group by 'Device Number' and 'Week' to calculate the weekly average completeness
      weekly_completeness = merged_df.groupby(['Device Number', 'Week'])['Daily Completeness (entries/hour)'].mean().reset_index(name='Weekly Average Completeness (entries/hour)')

    else:
      return "either airQlouds or deviceNames must have data"

    return weekly_completeness
# weekly_completeness = calculate_weekly_average_completeness(final_df, airQlouds, deviceNames)

def format_weekly_completeness_output(weekly_completeness, airQlouds, deviceNames):
    # Check if both lists are empty
    if len(airQlouds) > 0 and len(deviceNames) > 0:
      return "airQlouds and deviceNames  can not both have data"

    if len(airQlouds) > 0:
      # Pivot the table to get weeks as columns and AirQlouds as rows
      pivot_table = weekly_completeness.pivot(index='AirQloud', columns='Week', values='Weekly Average Completeness (entries/hour)')

    elif len(deviceNames) > 0:
      # Pivot the table to get weeks as columns and AirQlouds as rows
      pivot_table = weekly_completeness.pivot(index='Device Number', columns='Week', values='Weekly Average Completeness (entries/hour)')

    else:
      return "either airQlouds or deviceNames must have data"

    # Reset the index to make 'AirQloud' a column
    pivot_table.reset_index(inplace=True)

    return pivot_table
# formatted_weekly_completeness = format_weekly_completeness_output(weekly_completeness, airQlouds, deviceNames)


"""### Weekly data completeness trend"""
def plot_weekly_completness(pivot_table, airQlouds, deviceNames):
    # Check if both lists are empty
    if len(airQlouds) > 0 and len(deviceNames) > 0:
        return "airQlouds and deviceNames cannot both have data"

    if len(airQlouds) > 0:
        melted_df = pd.melt(pivot_table, id_vars=['AirQloud'], var_name='Week', value_name='Weekly Average Completeness (entries/hour)')

        fig = px.bar(melted_df, x='AirQloud', y='Weekly Average Completeness (entries/hour)', color='Week',
                     barmode='group', labels={'x': 'AirQloud', 'y': 'Weekly Average Completeness (entries/hour)'},
                     title='Weekly Average Completeness (entries/hour) per AirQloud',
                     hover_name='AirQloud', hover_data=['Week', 'Weekly Average Completeness (entries/hour)'])

    elif len(deviceNames) > 0:
        melted_df = pd.melt(pivot_table, id_vars=['Device Number'], var_name='Week', value_name='Weekly Average Completeness (entries/hour)')

        fig = px.bar(melted_df, x='Device Number', y='Weekly Average Completeness (entries/hour)', color='Week',
                     barmode='group', labels={'x': 'Device Number', 'y': 'Weekly Average Completeness (entries/hour)'},
                     title='Weekly Average Completeness (entries/hour) per Device',
                     hover_name='Device Number', hover_data=['Week', 'Weekly Average Completeness (entries/hour)'])

    else:
        return "either airQlouds or deviceNames must have data"

    fig.update_layout(height=600, width=1200, showlegend=False)
    fig.show(renderer='colab')
# plot_weekly_completness(formatted_weekly_completeness, airQlouds, deviceNames)






"""# Device specifics
 This shows the specific details of the each of the selected devices selected

## Sensor health

### Regplot/Scatterplot

#### Description:
This has the intra sensor scatter plots along with the regression lines for the before and after maintenance along with the line of fit equations and R-squared values visible if you hover over the lines.


To do:

Regression + R Squared value on the hover text
Size of the markers"""
def device_data_api(dataFrame, maintenenceDate):
    # Ensure the 'created_at' column is in datetime format and timezone-aware
    dataFrame['created_at'] = pd.to_datetime(dataFrame['created_at']).dt.tz_localize(None)
    # dataFrame['created_at'] = pd.to_datetime(dataFrame['created_at'], errors='coerce', utc=True)
    # Convert maintenanceDate to datetime if it's not already
    maintenenceDate = pd.to_datetime(maintenenceDate)
    # Initialize an empty list to store the result data
    results = []
    # Extract unique device numbers
    deviceNumbers = dataFrame['Device Number'].unique()
    for deviceNumber in deviceNumbers:
        # Filter data for the current device
        device_df = dataFrame[dataFrame['Device Number'] == deviceNumber]
        # Data before maintenance
        before_df = device_df[device_df['created_at'] <= maintenenceDate][['Device Number', 'created_at', 'Sensor1 PM2.5_CF_1_ug/m3', 'Sensor2 PM2.5_CF_1_ug/m3', 'Battery Voltage', 'AirQloud', 'AirQloud ID', 'AirQloud Type']]
        before_df['Status'] = 'Before'

        ## Sensor health
        # Data after maintenance
        after_df = device_df[device_df['created_at'] > maintenenceDate][['Device Number', 'created_at', 'Sensor1 PM2.5_CF_1_ug/m3', 'Sensor2 PM2.5_CF_1_ug/m3', 'Battery Voltage', 'AirQloud', 'AirQloud ID', 'AirQloud Type']]
        after_df['Status'] = 'After'
        # Append both before and after data to the results
        results.append(before_df)
        results.append(after_df)
    # Concatenate the results into a single DataFrame
    result_df = pd.concat(results, ignore_index=True)
    return result_df
# device_data_apiss = device_data_api(final_df, maintenenceDate)



def regSensor_correlation(dataFrame, maintenenceDate):
    # Extract unique device numbers
    deviceNumbers = dataFrame['Device Number'].unique()

    num_devices = len(deviceNumbers)
    num_cols = 3  # Number of columns in the subplot grid
    num_rows = (num_devices + num_cols - 1) // num_cols  # Number of rows in the subplot grid, rounding up

    fig = make_subplots(rows=num_rows, cols=num_cols, subplot_titles=deviceNumbers)

    for i, deviceNumber in enumerate(deviceNumbers):
        device_df = dataFrame[dataFrame['Device Number'] == deviceNumber]
        row = i // num_cols + 1
        col = i % num_cols + 1

        s1 = device_df[device_df['Date'] <= maintenenceDate]
        s2 = device_df[device_df['Date'] > maintenenceDate]

        # Scatter plot for before maintenance
        scatter_before = go.Scatter(
            x=s1['Sensor1 PM2.5_CF_1_ug/m3'],
            y=s1['Sensor2 PM2.5_CF_1_ug/m3'],
            mode='markers',
            name='Before',
            marker=dict(color='blue', size=3),
            hoverinfo='text',
            hovertext=[f"({x:.2f}, {y:.2f})" for x, y in zip(s1['Sensor1 PM2.5_CF_1_ug/m3'], s1['Sensor2 PM2.5_CF_1_ug/m3'])]
        )
        fig.add_trace(scatter_before, row=row, col=col)

        # Scatter plot for after maintenance
        scatter_after = go.Scatter(
            x=s2['Sensor1 PM2.5_CF_1_ug/m3'],
            y=s2['Sensor2 PM2.5_CF_1_ug/m3'],
            mode='markers',
            name='After',
            marker=dict(color='red', size=3),
            hoverinfo='text',
            hovertext=[f"({x:.2f}, {y:.2f})" for x, y in zip(s2['Sensor1 PM2.5_CF_1_ug/m3'], s2['Sensor2 PM2.5_CF_1_ug/m3'])]
        )
        fig.add_trace(scatter_after, row=row, col=col)

        # Scatter plot
        scatter = go.Scatter(
            x=device_df['Sensor1 PM2.5_CF_1_ug/m3'],
            y=device_df['Sensor2 PM2.5_CF_1_ug/m3'],
            mode='markers',
            name=f'{deviceNumber}',
            marker=dict(color='red', size=3),
            hoverinfo='text',
            hovertext=[f"({x:.2f}, {y:.2f})" for x, y in zip(device_df['Sensor1 PM2.5_CF_1_ug/m3'], device_df['Sensor2 PM2.5_CF_1_ug/m3'])]
        )

        fig.add_trace(scatter, row=row, col=col)

        # Calculate and plot regression line
        try:
            if not s1.empty:
                reg_before = np.polyfit(s1['Sensor1 PM2.5_CF_1_ug/m3'], s1['Sensor2 PM2.5_CF_1_ug/m3'], 1)
                x_range_before = np.linspace(min(s1['Sensor1 PM2.5_CF_1_ug/m3']), max(s1['Sensor1 PM2.5_CF_1_ug/m3']), 100)
                y_range_before = np.polyval(reg_before, x_range_before)
                rsquared_before = np.corrcoef(s1['Sensor1 PM2.5_CF_1_ug/m3'], s1['Sensor2 PM2.5_CF_1_ug/m3'])[0, 1] ** 2
                fig.add_trace(go.Scatter(x=x_range_before, y=y_range_before, mode='lines', line=dict(color='blue', width=2), name='Before',
                                         hoverinfo='text', hovertext=f"y = {reg_before[0]:.2f}x + {reg_before[1]:.2f}, R-Squared = {rsquared_before:.2f}"), row=row, col=col)

            if not s2.empty:
                reg_after = np.polyfit(s2['Sensor1 PM2.5_CF_1_ug/m3'], s2['Sensor2 PM2.5_CF_1_ug/m3'], 1)
                x_range_after = np.linspace(min(s2['Sensor1 PM2.5_CF_1_ug/m3']), max(s2['Sensor1 PM2.5_CF_1_ug/m3']), 100)
                y_range_after = np.polyval(reg_after, x_range_after)
                rsquared_after = np.corrcoef(s2['Sensor1 PM2.5_CF_1_ug/m3'], s2['Sensor2 PM2.5_CF_1_ug/m3'])[0, 1] ** 2
                fig.add_trace(go.Scatter(x=x_range_after, y=y_range_after, mode='lines', line=dict(color='red', width=2), name='After',
                                         hoverinfo='text', hovertext=f"y = {reg_after[0]:.2f}x + {reg_after[1]:.2f}, R-Squared = {rsquared_after:.2f}"), row=row, col=col)
        except np.linalg.LinAlgError as e:
            print(f"Error calculating regression for device {deviceNumber}: {e}")

        fig.update_xaxes(title_text='Sensor1 PM2.5_CF_1_ug/m3', row=row, col=col)
        fig.update_yaxes(title_text='Sensor2 PM2.5_CF_1_ug/m3', row=row, col=col)

    fig.update_layout(height=400*num_rows, width=1200, showlegend=False)

    fig.show(renderer="colab")
# regSensor_correlation(final_df, maintenenceDate)


"""### Error Margin
#### Description:
 E.g. Acceptable range 5<=e<=-5 at any piont of time

To do:

Try also using *boxplots* to show distribution of error margin. Boxplots will isolate outliers well in this case"""
def error_margin(dataFrame, end, maintenenceDate):
    # Convert 'created_at' to datetime if it's not already and convert to UTC timezone
    dataFrame['created_at'] = pd.to_datetime(dataFrame['created_at']).dt.tz_convert('UTC')

    # Convert end date to datetime and localize to UTC
    end_date = pd.to_datetime(end).tz_localize('UTC')

    # Filter data for the last 2 weeks up to the end date
    start_date = end_date - pd.DateOffset(weeks=2)
    filtered_df = dataFrame[(dataFrame['created_at'] >= start_date) & (dataFrame['created_at'] <= end_date)]

    # Calculate error margin between Sensor1 and Sensor2 PM2.5 readings
    filtered_df['Error Margin'] = abs(filtered_df['Sensor1 PM2.5_CF_1_ug/m3'] - filtered_df['Sensor2 PM2.5_CF_1_ug/m3'])

    # Extract unique device numbers from filtered data
    deviceNumbers = filtered_df['Device Number'].unique()

    num_devices = len(deviceNumbers)
    num_cols = 3  # Number of columns in the subplot grid
    num_rows = (num_devices + num_cols - 1) // num_cols  # Number of rows in the subplot grid, rounding up

    fig = make_subplots(rows=num_rows, cols=num_cols, subplot_titles=deviceNumbers)

    for i, deviceNumber in enumerate(deviceNumbers):
        device_df = filtered_df[filtered_df['Device Number'] == deviceNumber]
        row = i // num_cols + 1
        col = i % num_cols + 1

        s1 = device_df[device_df['Date'] <= maintenenceDate]
        s2 = device_df[device_df['Date'] > maintenenceDate]

        if not s1.empty:
          # Plot error margin with color differentiation
          error_margin1 = (s1['Sensor1 PM2.5_CF_1_ug/m3'] - s1['Sensor2 PM2.5_CF_1_ug/m3'])
          fig.add_trace(go.Scatter(x=s1['created_at'], y=error_margin1, mode='markers', name='Error Margin Before', marker=dict(size=1, color='blue')), row=row, col=col)
          fig.add_trace(go.Scatter(x=s1['created_at'], y=np.zeros_like(s1['created_at']), mode='markers', name='Before', marker=dict(size=5, color='green')), row=row, col=col)

        if not s2.empty:
          error_margin2 = (s2['Sensor1 PM2.5_CF_1_ug/m3'] - s2['Sensor2 PM2.5_CF_1_ug/m3'])
          fig.add_trace(go.Scatter(x=s2['created_at'], y=error_margin2, mode='markers', name='Error Margin After', marker=dict(size=1, color='red')), row=row, col=col)
          fig.add_trace(go.Scatter(x=s2['created_at'], y=np.zeros_like(s2['created_at']), mode='markers', name='After', marker=dict(size=5, color='green')), row=row, col=col)


        # Plot black lines at positive and negative 5
        fig.add_trace(go.Scatter(x=s1['created_at'], y=np.full_like(s1['created_at'], 5), mode='lines', name='Positive 5', line=dict(color='black', width=1, dash='dash')), row=row, col=col)
        fig.add_trace(go.Scatter(x=s1['created_at'], y=np.full_like(s1['created_at'], -5), mode='lines', name='Negative 5', line=dict(color='black', width=1, dash='dash')), row=row, col=col)
        fig.add_trace(go.Scatter(x=s2['created_at'], y=np.full_like(s2['created_at'], 5), mode='lines', name='Positive 5', line=dict(color='black', width=1, dash='dash')), row=row, col=col)
        fig.add_trace(go.Scatter(x=s2['created_at'], y=np.full_like(s2['created_at'], -5), mode='lines', name='Negative 5', line=dict(color='black', width=1, dash='dash')), row=row, col=col)

        # Update axes labels
        fig.update_xaxes(title_text='Date', row=row, col=col)
        fig.update_yaxes(title_text='Sensor Error Margin', row=row, col=col)

    fig.update_layout(height=300 * num_rows, width=1200, showlegend=False)
    fig.show(renderer="colab")
# error_margin(final_df, end, maintenenceDate)


"""### Box plot for the sensor error margin
#### Description:
This contains details of the sensor errors for before and after highlighting the
* Max
* Min
* Median
* 1st, 2nd, 3rd and 4th quaters"""
def error_margin_boxplot(dataFrame, end, maintenenceDate):
    # Calculate error margin between Sensor1 and Sensor2 PM2.5 readings
    dataFrame['Error Margin'] = abs(dataFrame['Sensor1 PM2.5_CF_1_ug/m3'] - dataFrame['Sensor2 PM2.5_CF_1_ug/m3'])

    # Extract unique device numbers from filtered data
    deviceNumbers = dataFrame['Device Number'].unique()

    num_devices = len(deviceNumbers)
    num_cols = 3  # Number of columns in the subplot grid
    num_rows = (num_devices + num_cols - 1) // num_cols  # Number of rows in the subplot grid, rounding up

    fig = make_subplots(rows=num_rows, cols=num_cols, subplot_titles=deviceNumbers)

    for i, deviceNumber in enumerate(deviceNumbers):
        device_df = dataFrame[dataFrame['Device Number'] == deviceNumber]
        row = i // num_cols + 1
        col = i % num_cols + 1

        s1 = device_df[device_df['Date'] <= maintenenceDate]
        s2 = device_df[device_df['Date'] > maintenenceDate]

         # Calculate error margin between Sensor1 and Sensor2
        error_margin1 = (s1['Sensor1 PM2.5_CF_1_ug/m3'] - s1['Sensor2 PM2.5_CF_1_ug/m3'])
        error_margin2 = (s2['Sensor1 PM2.5_CF_1_ug/m3'] - s2['Sensor2 PM2.5_CF_1_ug/m3'])


        # Plot box plots for error margin
        fig.add_trace(go.Box(y=error_margin1, name='Error Margin Before', marker_color='blue'), row=row, col=col)
        fig.add_trace(go.Box(y=error_margin2, name='Error Margin After', marker_color='red'), row=row, col=col)

        # Update axes labels
        fig.update_xaxes(title_text='Maintenance', row=row, col=col)
        fig.update_yaxes(title_text='Sensor Error Margin', row=row, col=col)

    fig.update_layout(height=400 * num_rows, width=1200, showlegend=False)
    fig.show(renderer="colab")
# error_margin_boxplot(final_df, end, maintenenceDate)


"""### Average sensor error
To do:
Try play with marker size
- Plot straight line at the minimum error margin i.e plot two lines at -5 and +5 and +10 -10
"""
def daily_error_margin(dataFrame, maintenenceDate):
    # Extract unique device numbers
    deviceNumbers = dataFrame['Device Number'].unique()

    num_devices = len(deviceNumbers)
    num_cols = 3  # Number of columns in the subplot grid
    num_rows = (num_devices + num_cols - 1) // num_cols  # Number of rows in the subplot grid, rounding up

    fig = make_subplots(rows=num_rows, cols=num_cols, subplot_titles=deviceNumbers)

    for i, deviceNumber in enumerate(deviceNumbers):
        device_df = dataFrame[dataFrame['Device Number'] == deviceNumber]
        row = i // num_cols + 1
        col = i % num_cols + 1

        s1 = device_df[device_df['Date'] <= maintenenceDate]
        s2 = device_df[device_df['Date'] > maintenenceDate]

         # Calculate absolute error margin between Sensor1 and Sensor2
        s1['error_margin_before'] = np.abs(s1['Sensor1 PM2.5_CF_1_ug/m3'] - s1['Sensor2 PM2.5_CF_1_ug/m3'])
        s2['error_margin_after'] = np.abs(s2['Sensor1 PM2.5_CF_1_ug/m3'] - s2['Sensor2 PM2.5_CF_1_ug/m3'])

        # Group by hourly and calculate average error margin for both before and after maintenance
        s1['timestamp'] = s1['created_at'].dt.strftime('%Y-%m-%d %H') #('%Y-%m-%d') daily average
        s2['timestamp'] = s2['created_at'].dt.strftime('%Y-%m-%d %H') #('%Y-%m-%d') daily average
        hourly_avg_error_margin_before = s1.groupby('timestamp').agg({'error_margin_before': 'mean'}).reset_index()
        hourly_avg_error_margin_after = s2.groupby('timestamp').agg({'error_margin_after': 'mean'}).reset_index()

        # Plot hourly average error margin for both before and after maintenance
        fig.add_trace(go.Scatter(x=hourly_avg_error_margin_before['timestamp'], y=hourly_avg_error_margin_before['error_margin_before'], mode='lines+markers', name='Hourly Avg Error Margin Before', marker=dict(color='blue', size = 1)), row=row, col=col) #mode changed to markers
        fig.add_trace(go.Scatter(x=hourly_avg_error_margin_after['timestamp'], y=hourly_avg_error_margin_after['error_margin_after'], mode='lines+markers', name='Hourly Avg Error Margin After', marker=dict(color='red')), row=row, col=col)

        # Add horizontal lines at positive and negative 5
        fig.add_hline(y=5, line=dict(color='black', width=1, dash='dash'), row=row, col=col)

        # Update axes labels
        fig.update_xaxes(title_text='Date', row=row, col=col)
        fig.update_yaxes(title_text='Hourly Sensor Error Margin', row=row, col=col)

    fig.update_layout(height=400 * num_rows, width=1200, showlegend=False)
    fig.show(renderer="colab")
# daily_error_margin(final_df, maintenenceDate)

"""### Daily average sensor error tablular"""
def daily_error_margin_pivot(dataFrame):
    # Calculate error margin
    dataFrame['error_margin'] = np.abs(dataFrame['Sensor1 PM2.5_CF_1_ug/m3'] - dataFrame['Sensor2 PM2.5_CF_1_ug/m3'])
    dataFrame['Date'] = dataFrame['created_at'].dt.date

    # Group by 'Device Number' and 'Date', calculate daily average error margin
    daily_avg_error_margin = dataFrame.groupby(['Device Number', 'Date'])['error_margin'].mean().reset_index()

    # Pivot the dataframe to have dates as columns and daily error margins as values
    pivoted_df = daily_avg_error_margin.pivot(index='Device Number', columns='Date', values='error_margin').reset_index()

    # Rename the columns for better readability (optional)
    pivoted_df.columns.name = None  # Remove the 'Date' from column headers

    return pivoted_df
# pivoted_error_margin_df = daily_error_margin_pivot(final_df)


"""### Intra-Sensor Correlation Matrix
#### Description:
This plot is for the intra sensor correlation of any device in an AirQloud
To do:
Define the ylim to be between -1 and 1"""
def sensor_correlation(final_data):
    deviceNumbers = final_data['Device Number'].unique()
    num_devices = len(deviceNumbers)
    num_cols = 3  # Number of columns in the subplot grid
    num_rows = (num_devices + 2) // 3  # Number of rows in the subplot grid, rounding up

    fig = make_subplots(rows=num_rows, cols=num_cols, subplot_titles=deviceNumbers)

    for i, deviceNumber in enumerate(deviceNumbers):
        device_df = final_data[final_data['Device Number'] == deviceNumber]

        device_df = device_df[['Sensor1 PM2.5_CF_1_ug/m3', 'Sensor2 PM2.5_CF_1_ug/m3', 'Date']].groupby(['Date']).corr().round(4) * 100
        device_df.reset_index(inplace=True)
        device_df = device_df.drop(device_df[device_df['level_1'] == 'Sensor2 PM2.5_CF_1_ug/m3'].index)
        device_df.drop(['level_1', 'Sensor1 PM2.5_CF_1_ug/m3'], axis=1, inplace=True)
        device_df = device_df.rename(columns={"Sensor2 PM2.5_CF_1_ug/m3": "R"})

        s1 = device_df[device_df['R'] <= 98.5]  # Before maintenance
        s2 = device_df[device_df['R'] > 98.5]  # After maintenance

        row = i // num_cols + 1
        col = i % num_cols + 1

        fig.add_trace(go.Scatter(x=s1['Date'], y=s1['R'], mode='lines+markers', marker_symbol='asterisk-open', marker_line_color="midnightblue",
                                 marker_size=15, name=f'{deviceNumber} R-Before', line=dict(color='blue')), row=row, col=col)
        fig.add_trace(go.Scatter(x=s2['Date'], y=s2['R'], mode='lines+markers', marker_symbol='hash-open', marker_line_color="midnightblue",
                                 marker_size=15, marker_line_width=2, name=f'{deviceNumber} R-After', line=dict(color='red')), row=row, col=col)

        # Update axes labels
        fig.update_xaxes(title_text='Date', row=row, col=col)
        fig.update_yaxes(title_text='Sensor Correlation (%)', row=row, col=col)

    fig.update_layout(height=400 * num_rows, width=1200, showlegend=False)
    fig.show(renderer="colab")
# sensor_correlation(final_df)


"""## Battery Voltage/ SOC/ SOH
### Battery Voltage Timeseries
* This is plotted for the device battery voltage Vs time to show the battery performance
"""
def battery_voltage(dataFrame, end, maintenenceDate):
    # Convert 'created_at' to datetime if it's not already and convert to UTC timezone
    dataFrame['created_at'] = pd.to_datetime(dataFrame['created_at']).dt.tz_convert('UTC')

    # Convert end date to datetime and localize to UTC
    end_date = pd.to_datetime(end).tz_localize('UTC')

    # Filter data for the last 2 weeks up to the end date
    start_date = end_date - pd.DateOffset(weeks=2)
    filtered_df = dataFrame[(dataFrame['created_at'] >= start_date) & (dataFrame['created_at'] <= end_date)]

    # Extract unique device numbers from filtered data
    deviceNumbers = filtered_df['Device Number'].unique()

    num_devices = len(deviceNumbers)
    num_cols = 3  # Number of columns in the subplot grid
    num_rows = (num_devices + num_cols - 1) // num_cols  # Number of rows in the subplot grid, rounding up

    fig = make_subplots(rows=num_rows, cols=num_cols, subplot_titles=deviceNumbers)

    for i, deviceNumber in enumerate(deviceNumbers):
        device_df = filtered_df[filtered_df['Device Number'] == deviceNumber]
        row = i // num_cols + 1
        col = i % num_cols + 1

        s1 = device_df[device_df['Date'] <= maintenenceDate]
        s2 = device_df[device_df['Date'] > maintenenceDate]

        # Convert timestamps to Unix time
        s1_unix_time = s1['created_at'].astype(np.int64) // 10**9
        s2_unix_time = s2['created_at'].astype(np.int64) // 10**9

        if not s1_unix_time.empty:
            # Calculate regression lines
            reg_before = np.polyfit(s1_unix_time, s1['Battery Voltage'], 1)
            fig.add_trace(go.Scatter(x=s1['created_at'], y=s1['Battery Voltage'], mode='markers', name='Before', marker=dict(size=1, color='blue')), row=row, col=col)

        if not s2_unix_time.empty:
            reg_after = np.polyfit(s2_unix_time, s2['Battery Voltage'], 1)
            fig.add_trace(go.Scatter(x=s2['created_at'], y=s2['Battery Voltage'], mode='markers', name='After', marker=dict(size=2, color='red')), row=row, col=col)


        x_range = np.linspace(s1_unix_time.min(), s2_unix_time.max(), 100)
        # Update axes labels
        fig.update_xaxes(title_text='Date', row=row, col=col)
        fig.update_yaxes(title_text='Battery Voltage', row=row, col=col)

    fig.update_layout(height=300 * num_rows, width=1200, showlegend=False)
    fig.show(renderer="colab")
# battery_voltage(final_df, end, maintenenceDate)


"""### C-Rate
#### Description:
+ This contains the **mean hourly** rate of the change of the battery with time (dV/dt)
+ This graphs explain how long it takes to charge and discharge
+ Expected charge vs discharge sequence chart?
+ What is the time that the battery experiences sudden discharge?
+ C-Rate - rate at which battery charges or discharges
+ Battery capacity decreases with increase in C-Rate
+ Avg I = Ah (battery capacity)/dT (number of hours of discharge)"""
def c_rate(dataFrame, end):
    # Convert 'created_at' to datetime if it's not already and convert to UTC timezone
    dataFrame['created_at'] = pd.to_datetime(dataFrame['created_at']).dt.tz_convert('UTC')

    # Convert end date to datetime and localize to UTC
    end_date = pd.to_datetime(end).tz_localize('UTC')

    # Filter data for the last 2 weeks up to the end date
    start_date = end_date - pd.DateOffset(weeks=2)
    filtered_df = dataFrame[(dataFrame['created_at'] >= start_date) & (dataFrame['created_at'] <= end_date)]

    # Extract unique device numbers from filtered data
    deviceNumbers = filtered_df['Device Number'].unique()

    num_devices = len(deviceNumbers)
    num_cols = 3  # Number of columns in the subplot grid
    num_rows = (num_devices + num_cols - 1) // num_cols  # Number of rows in the subplot grid, rounding up

    fig = make_subplots(rows=num_rows, cols=num_cols, subplot_titles=deviceNumbers)

    for i, deviceNumber in enumerate(deviceNumbers):
        device_df = filtered_df[filtered_df['Device Number'] == deviceNumber].sort_values('created_at')

        # Ensure 'created_at' is the index before resampling
        device_df = device_df.set_index('created_at')
        device_df = device_df.resample('H').mean(numeric_only=True).reset_index()

        # Calculate the rate of change of battery voltage per hour
        device_df['rate'] = device_df['Battery Voltage'].diff()

        row = i // num_cols + 1
        col = i % num_cols + 1

        fig.add_trace(go.Scatter(x=device_df['created_at'], y=device_df['rate'],
                                 mode='lines', name='Charge/Discharge Rate', marker=dict(color='red', size=5)), row=row, col=col)

        # Update axes labels
        fig.update_xaxes(title_text='Date', row=row, col=col)
        fig.update_yaxes(title_text='Rate (V/hour)', row=row, col=col)

    fig.update_layout(height=400 * num_rows, width=1200, showlegend=False)
    fig.show(renderer="colab")
# c_rate(final_df, end)


"""### Dunial device
+ This provides insight into the avaerage data points per hour for the hours of the day both before and after maintenance
"""
def duinal_device_data(dataFrame):
    # Extract unique device numbers from the data
    deviceNumbers = dataFrame['Device Number'].unique()

    num_devices = len(deviceNumbers)
    num_cols = 3  # Number of columns in the subplot grid
    num_rows = (num_devices + num_cols - 1) // num_cols  # Number of rows in the subplot grid, rounding up

    fig = make_subplots(rows=num_rows, cols=num_cols, subplot_titles=deviceNumbers)

    for i, deviceNumber in enumerate(deviceNumbers):
        # Filter the dataframe for the current device number
        device_df = dataFrame[dataFrame['Device Number'] == deviceNumber]
        row = i // num_cols + 1
        col = i % num_cols + 1

        # Convert 'created_at' column to datetime format
        device_df['created_at'] = pd.to_datetime(device_df['created_at'])

        # Extract the hour of the day for each data point
        device_df['hour'] = device_df['created_at'].dt.hour

        # Calculate the average number of data points for each hour
        device_df_hourly_avg = device_df.groupby('hour').size().reindex(np.arange(24), fill_value=0) / device_df['created_at'].dt.date.nunique()

        # Create a bar plot for the average number of data points per hour
        fig.add_trace(go.Bar(x=device_df_hourly_avg.index, y=device_df_hourly_avg.values, name=deviceNumber, marker=dict(color='blue')), row=row, col=col)

        # Update axes labels
        fig.update_xaxes(title_text='Hour of the Day', row=row, col=col)
        fig.update_yaxes(title_text='Avg Data Points per Hour', row=row, col=col)

    fig.update_layout(height=300 * num_rows, width=1200, showlegend=False, title='Average Data Points per Hour')
    fig.show(renderer='colab')
# duinal_device_data(final_df)


"""## Device State/Uptime
### Daily State/ Entries
* This plots the number of entries for each device per day with different color coding
* entires <=9  --> crimson
* 10 <= entries <= 15 --> orange
* 16 <= entries <= 20 --> yellow
* entries > 20 --> green"""
def get_color_uptime(uptime):
    if uptime <= 9:
        return 'crimson'
    elif 10 <= uptime <= 15:
        return 'orange'
    elif 16 <= uptime <= 20:
        return 'yellow'
    else:
        return 'green'
# get_color_uptime(9)

def plot_uptime(dataFrame):
    # Convert 'created_at' to datetime if it's not already and convert to UTC timezone
    dataFrame['created_at'] = pd.to_datetime(dataFrame['created_at']).dt.tz_convert('UTC')

    # Extract unique device numbers
    deviceNumbers = dataFrame['Device Number'].unique()

    # Calculate uptime for each device by date
    uptime_list = []
    for deviceNumber in deviceNumbers:
        device_df = dataFrame[dataFrame['Device Number'] == deviceNumber]
        device_df['date'] = device_df['created_at'].dt.date
        device_df['hour'] = device_df['created_at'].dt.hour
        uptime_df = device_df.groupby('date')['hour'].nunique().reset_index()
        uptime_df.columns = ['date', 'uptime']
        uptime_list.append(uptime_df)

    num_devices = len(deviceNumbers)
    num_cols = 3  # Number of columns in the subplot grid
    num_rows = (num_devices + num_cols - 1) // num_cols  # Number of rows in the subplot grid, rounding up

    fig = make_subplots(rows=num_rows, cols=num_cols, subplot_titles=deviceNumbers)

    for i, (deviceNumber, uptime_df) in enumerate(zip(deviceNumbers, uptime_list)):
        row = i // num_cols + 1
        col = i % num_cols + 1

        colors = [get_color_uptime(uptime) for uptime in uptime_df['uptime']]

        trace = go.Bar(x=uptime_df['date'], y=uptime_df['uptime'],
                       marker=dict(color=colors),
                       name=f'Device {deviceNumber}')

        fig.add_trace(trace, row=row, col=col)

        fig.update_xaxes(title_text='Date', row=row, col=col, tickangle=45)
        fig.update_yaxes(title_text='Uptime (Hours)', row=row, col=col)

    fig.update_layout(height=300*num_rows, width=1200, showlegend=False)

    fig.show(renderer="colab")
# plot_uptime(final_df)


"""### Daily Uptime/SOH/ Performance/ Quality [descriptive uptime]
#### Description:
Qualitative daily state of health quantified based on hourly entries i.e:
* Hourly entries > 17 - Optimal
* 15 <= * Hourly entries  <= 17 - Good
* 10 <= * Hourly entries  <= 14 - Fair
* Hourly entries < 10 - Poor"""
def descriptive_uptime_color(data_entry):
    if data_entry >= 18:
        return 'green'
    elif 15 <= data_entry <= 17:
        return 'yellow'
    elif 10 <= data_entry <= 14:
        return 'orange'
    else:
        return 'crimson'
# descriptive_uptime_color(18)

def descriptive_uptime_plot(dataFrame):
    # Convert 'created_at' to datetime and extract date
    dataFrame['created_at'] = pd.to_datetime(dataFrame['created_at'], utc=True) # Convert to datetime with UTC timezone
    dataFrame['date'] = dataFrame['created_at'].dt.date
    dataFrame['hour'] = dataFrame['created_at'].dt.hour

    # Extract unique device numbers
    deviceNumbers = dataFrame['Device Number'].unique()

    device_dict = defaultdict(lambda: {'date': [], 'optimal': [], 'good': [], 'fair': [], 'poor': []})

    # Calculate uptime per hour and categorize
    for deviceNumber in deviceNumbers:
        device_df = dataFrame[dataFrame['Device Number'] == deviceNumber]
        # Count occurrences per hour and date
        hourly_counts = device_df.groupby(['date', 'hour']).size().reset_index(name='data_entries')

        # Group by date and calculate number of entries categorized
        grouped = hourly_counts.groupby('date')['data_entries'].apply(list).reset_index()
        for _, row in grouped.iterrows():
            date = row['date']
            entries = row['data_entries']
            optimal_count = sum(1 for entry in entries if descriptive_uptime_color(entry) == 'green')
            good_count = sum(1 for entry in entries if descriptive_uptime_color(entry) == 'yellow')
            fair_count = sum(1 for entry in entries if descriptive_uptime_color(entry) == 'orange')
            poor_count = sum(1 for entry in entries if descriptive_uptime_color(entry) == 'crimson')

            device_dict[deviceNumber]['date'].append(date)
            device_dict[deviceNumber]['optimal'].append(optimal_count)
            device_dict[deviceNumber]['good'].append(good_count)
            device_dict[deviceNumber]['fair'].append(fair_count)
            device_dict[deviceNumber]['poor'].append(poor_count)

    # Define number of columns and rows for plotting
    num_devices = len(deviceNumbers)
    num_cols = 3  # Number of columns in the subplot grid
    num_rows = (num_devices + num_cols - 1) // num_cols  # Number of rows in the subplot grid, rounding up

    fig = make_subplots(rows=num_rows, cols=num_cols, subplot_titles=deviceNumbers)

    for i, deviceNumber in enumerate(device_dict.keys()):
        row = i // num_cols + 1
        col = i % num_cols + 1

        trace_optimal = go.Bar(x=device_dict[deviceNumber]['date'], y=device_dict[deviceNumber]['optimal'], name='Optimal', marker=dict(color='green'))
        trace_good = go.Bar(x=device_dict[deviceNumber]['date'], y=device_dict[deviceNumber]['good'], name='Good', marker=dict(color='yellow'))
        trace_fair = go.Bar(x=device_dict[deviceNumber]['date'], y=device_dict[deviceNumber]['fair'], name='Fair', marker=dict(color='orange'))
        trace_poor = go.Bar(x=device_dict[deviceNumber]['date'], y=device_dict[deviceNumber]['poor'], name='Poor', marker=dict(color='crimson'))

        fig.add_trace(trace_optimal, row=row, col=col)
        fig.add_trace(trace_good, row=row, col=col)
        fig.add_trace(trace_fair, row=row, col=col)
        fig.add_trace(trace_poor, row=row, col=col)

    # Update layout
    fig.update_layout(height=400*num_rows, width=1200, showlegend=False, barmode='stack')
    fig.show(renderer="colab")
# descriptive_uptime_plot(final_df)


"""### Data Completeness
* This plots the number of entries for each device per hour with different color coding
* entires <=9  --> crimson
* 10 <= entries <= 15 --> orange
* 16 <= entries <= 20 --> yellow
* entries > 20 --> green
To do:
Try to only show last 48 hours or 3 days"""
def get_color(uptime):
    if uptime <= 9:
        return 'crimson'
    elif 10 <= uptime <= 15:
        return 'orange'
    elif 16 <= uptime <= 20:
        return 'yellow'
    else:
        return 'green'
# get_color(9)

def plot_data_completeness(dataFrame, end_date):
    # Convert 'created_at' to datetime if it's not already and convert to UTC timezone
    dataFrame['created_at'] = pd.to_datetime(dataFrame['created_at']).dt.tz_convert('UTC')

    # Convert end_date to datetime with UTC timezone
    end_date = pd.to_datetime(end_date, utc=True)

    # Calculate start date as 14 days before the end date
    start_date = end_date - timedelta(days=14)

    # Filter data for the last two weeks
    dataFrame = dataFrame[(dataFrame['created_at'] >= start_date) & (dataFrame['created_at'] <= end_date)]

    # Extract unique device numbers
    deviceNumbers = dataFrame['Device Number'].unique()

    # device_df['timestamp'] = device_df['created_at'].dt.strftime('%Y-%m-%d %H')
    # Calculate uptime for each device by date
    uptime_list = []
    for deviceNumber in deviceNumbers:
        device_df = dataFrame[dataFrame['Device Number'] == deviceNumber]
        device_df['date'] = device_df['created_at'].dt.date
        device_df['hour'] = device_df['created_at'].dt.hour
        device_df['timestamp'] = device_df['created_at'].dt.strftime('%Y-%m-%d %H')
        # Apply count aggregation after groupby
        uptime_df = device_df.groupby('timestamp')['created_at'].count().reset_index(name='uptime')
        uptime_list.append(uptime_df)

    num_devices = len(deviceNumbers)
    num_cols = 3  # Number of columns in the subplot grid
    num_rows = (num_devices + num_cols - 1) // num_cols  # Number of rows in the subplot grid, rounding up

    fig = make_subplots(rows=num_rows, cols=num_cols, subplot_titles=deviceNumbers)

    for i, (deviceNumber, uptime_df) in enumerate(zip(deviceNumbers, uptime_list)):
        row = i // num_cols + 1
        col = i % num_cols + 1

        colors = [get_color(uptime) for uptime in uptime_df['uptime']]

        trace = go.Bar(x=uptime_df['timestamp'], y=uptime_df['uptime'],
                       marker=dict(color=colors),
                       name=f'Device {deviceNumber}')

        fig.add_trace(trace, row=row, col=col)

        fig.update_xaxes(title_text='timestamp', row=row, col=col, tickangle=45)
        fig.update_yaxes(title_text='Hourly Count', row=row, col=col)

    fig.update_layout(height=300*num_rows, width=1200, showlegend=False)

    fig.show(renderer="colab")
# plot_data_completeness(final_df, end)


"""## AirQloud Health
### This is divided into the three main components of device health
* Sensor correlation
* Battery performance
* Data completeness and uptime

### Sensor health
#### Color coding
* Green -> optimal sensor quality with error <= 5
* Yellow -> good sensor quality with 6 <= error <= 10
* Orange -> Fair sensor quality with 11 <= error <= 12
* Crimson -> Poor sensor quality with error > 12"""
def get_sensor_health_counts(df):
    # Calculate error margin between Sensor1 and Sensor2
    error_margin = np.abs(df['Sensor1 PM2.5_CF_1_ug/m3'] - df['Sensor2 PM2.5_CF_1_ug/m3'])

    # Count occurrences of different error margin ranges
    green_count = np.sum(error_margin <= 5)
    yellow_count = np.sum((error_margin >= 6) & (error_margin <= 10))
    orange_count = np.sum((error_margin >= 11) & (error_margin <= 12))
    poor_count = np.sum(error_margin >= 12)

    return green_count, yellow_count, orange_count, poor_count
# get_sensor_health_counts(final_df)

def sensor_health(df, airQlouds, deviceNames):
    # Check if both lists are empty
    if len(airQlouds) > 0 and len(deviceNames) > 0:
      return "airQlouds and deviceNames  can not both have data"
    if len(airQlouds) > 0:
      airqlouds = df['AirQloud'].unique()
      num_airqlouds = len(airqlouds)

      num_cols = 2  # Two pie charts per row
      num_rows = (num_airqlouds + 1) // 2  # Number of rows required

      fig = make_subplots(rows=num_rows, cols=num_cols, subplot_titles=airqlouds, specs=[[{'type':'pie'}, {'type':'pie'}]] * num_rows)

      for i, airqloud in enumerate(airqlouds):
        airqloud_df = df[df['AirQloud'] == airqloud]
        green_count, yellow_count, orange_count, poor_count = get_sensor_health_counts(airqloud_df)

        labels = ['Optimal', 'Good', 'Fair', 'Poor']
        values = [green_count, yellow_count, orange_count, poor_count]
        colors = ['green', 'yellow', 'orange', 'crimson']

        row = i // num_cols + 1
        col = i % num_cols + 1

        fig.add_trace(go.Pie(labels=labels, values=values, hole=0.3, marker=dict(colors=colors)), row=row, col=col)

      fig.update_layout(title="AirQloud Sensor Health", title_font_size=20, height=400*num_rows, width=600*num_cols)

      fig.show(renderer="colab")

    else:
      return "No AirQlouds selected"
# sensor_health(final_df, airQlouds, deviceNames)


"""### Battery Performance
#### Color coding
* Green -> Device is on and posted with in the hour
* Grey -> Device is off and didn't post with in the hour"""
# Function to calculate the average uptime of the devices
def airQloud_battery(df,start , end, AQData, airQlouds, deviceNames):
    # Check if both lists are empty
    if len(airQlouds) > 0 and len(deviceNames) > 0:
      return "airQlouds and deviceNames  can not both have data"
    if len(airQlouds) > 0:
      # time span
      weekly_df, analysis_duration_days, first_date_in_df, last_date_in_df = create_dates(start, end)
      analysis_duration_hours = analysis_duration_days * 24

      # Initialize lists to store results
      device_list = []
      online_completeness_lst = []
      offline_completeness_lst = []
      airQloud_lst = []

      # Iterate over unique device numbers
      for deviceNumber in df['Device Number'].unique():
        # Filter data for the current device
        device_df = df[df['Device Number'] == deviceNumber]

        # Convert 'created_at' column to datetime
        device_df['created_at'] = pd.to_datetime(device_df['created_at'])

        # Extract date and hour
        device_df['date'] = device_df['created_at'].dt.date
        device_df['hour'] = device_df['created_at'].dt.hour
        device_df['timestamp'] = device_df['created_at'].dt.strftime('%Y-%m-%d %H')

        # Group by date and count unique hours for uptime
        uptime_df = device_df.groupby('date')['hour'].nunique().reset_index(name='uptime')
        completeness_df = device_df.groupby(['timestamp']).size().reset_index(name='data_entries')

        # Calculate online completeness
        online_count = completeness_df[(completeness_df['data_entries'] > 0)].shape[0]

        # Append results to lists
        device_list.append(deviceNumber)
        online_completeness_lst.append(online_count)
        airQloud_lst.append(device_df['AirQloud'].unique()[0])

      # Create final DataFrame to return
      result_df = pd.DataFrame({
        'Device Number': device_list,
        'Online Completeness': online_completeness_lst,
        'AirQloud': airQloud_lst
      })

      # merged_df = daily_completeness.merge(df[['Device Number', 'AirQloud']].drop_duplicates(), on='Device Number')
      result_df = AQData.merge(result_df[['Device Number', 'Online Completeness']].drop_duplicates(), on='Device Number', how='outer')
      result_df.fillna(0, inplace=True)
      result_df['Downtime'] = analysis_duration_hours - result_df['Online Completeness']
      result_df.drop(columns=['Read Key', 'Device ID' ], inplace=True)

      airqlouds = df['AirQloud'].unique()
      num_airqlouds = len(airqlouds)

      num_cols = 2  # Two pie charts per row
      num_rows = (num_airqlouds + 1) // 2  # Number of rows required
      fig = make_subplots(rows=num_rows, cols=num_cols, subplot_titles=airqlouds, specs=[[{'type':'pie'}, {'type':'pie'}]] * num_rows)

      for i, airqloud in enumerate(airqlouds):
        airqloud_df = result_df[result_df['AirQloud'] == airqloud]

        labels = ['Online','Downtime']
        values = [airqloud_df['Online Completeness'].sum(), airqloud_df['Downtime'].sum()]
        colors = ['green', 'grey']

        row = i // num_cols + 1
        col = i % num_cols + 1
        fig.add_trace(go.Pie(labels=labels, values=values, hole=0.3, marker=dict(colors=colors)), row=row, col=col)

      fig.update_layout(title="AirQloud Battery Performance", title_font_size=20, height=400*num_rows, width=600*num_cols)

      fig.show(renderer="colab")
    else:
      return "No AirQlouds selected"
# airQloud_battery(final_df, start, end, AQData, airQlouds, deviceNames)


"""### Data completeness
#### Color coding
* Green -> optimal device performance
* Yellow -> good device performance
* Orange -> Fair device performance
* Crimson -> Poor device performance
* Grey -> Device downtime"""
# Function to calculate the average uptime of the devices
def airQloud_completeness(df,start , end, AQData, airQlouds, deviceNames):
    # Check if both lists are empty
    if len(airQlouds) > 0 and len(deviceNames) > 0:
      return "airQlouds and deviceNames  can not both have data"
    if len(airQlouds) > 0:
      # time span
      weekly_df, analysis_duration_days, first_date_in_df, last_date_in_df = create_dates(start, end)
      analysis_duration_hours = analysis_duration_days * 24

      # Initialize lists to store results
      device_list = []
      optimal_completeness_lst = []
      good_completeness_lst = []
      fair_completeness_lst = []
      poor_completeness_lst = []
      offline_completeness_lst = []
      airQloud_lst = []



      # Iterate over unique device numbers
      for deviceNumber in df['Device Number'].unique():
        # Filter data for the current device
        device_df = df[df['Device Number'] == deviceNumber]

        # Convert 'created_at' column to datetime
        device_df['created_at'] = pd.to_datetime(device_df['created_at'])

        # Extract date and hour
        device_df['date'] = device_df['created_at'].dt.date
        device_df['hour'] = device_df['created_at'].dt.hour
        device_df['timestamp'] = device_df['created_at'].dt.strftime('%Y-%m-%d %H')
        device_df['Error margin'] = np.abs(device_df['Sensor1 PM2.5_CF_1_ug/m3'] - device_df['Sensor2 PM2.5_CF_1_ug/m3'])

        # Group by date and count unique hours for uptime
        uptime_df = device_df.groupby('date')['hour'].nunique().reset_index(name='uptime')
        completeness_df = device_df.groupby(['timestamp']).size().reset_index(name='data_entries')
        # error = magnitude('Sensor1 PM2.5_CF_1_ug/m3' - 'Sensor2 PM2.5_CF_1_ug/m3')
        error_df = device_df.groupby(['timestamp'])['Error margin'].mean().reset_index(name='error')


        # Calculate average uptime
        average_uptime = round(uptime_df['uptime'].mean(), 2)
        average_completeness = round(completeness_df['data_entries'].mean(), 2)
        average_error = round(error_df['error'].mean(), 2)

        # Calculate completeness categories
        optimal_count = completeness_df[completeness_df['data_entries'] > 18].shape[0]
        good_count = completeness_df[(completeness_df['data_entries'] >= 15) & (completeness_df['data_entries'] <= 18)].shape[0]
        fair_count = completeness_df[(completeness_df['data_entries'] >= 10) & (completeness_df['data_entries'] <= 14)].shape[0]
        poor_count = completeness_df[(completeness_df['data_entries'] >= 1) & (completeness_df['data_entries'] <= 9)].shape[0]

        # Append results to lists
        device_list.append(deviceNumber)
        optimal_completeness_lst.append(optimal_count)
        good_completeness_lst.append(good_count)
        fair_completeness_lst.append(fair_count)
        poor_completeness_lst.append(poor_count)
        airQloud_lst.append(device_df['AirQloud'].unique()[0])

      # Create final DataFrame to return
      result_df = pd.DataFrame({
        'Device Number': device_list,
        'Optimal Completeness': optimal_completeness_lst,
        'Good Completeness': good_completeness_lst,
        'Fair Completeness': fair_completeness_lst,
        'Poor Completeness': poor_completeness_lst,
        'AirQloud': airQloud_lst
      })

      # merged_df = daily_completeness.merge(df[['Device Number', 'AirQloud']].drop_duplicates(), on='Device Number')
      result_df = AQData.merge(result_df[['Device Number', 'Optimal Completeness', 'Good Completeness', 'Fair Completeness', 'Poor Completeness']].drop_duplicates(), on='Device Number', how='outer')
      result_df.fillna(0, inplace=True)
      result_df['Downtime'] = analysis_duration_hours - (result_df['Optimal Completeness'] + result_df['Good Completeness'] + result_df['Fair Completeness'] + result_df['Poor Completeness'])
      result_df.drop(columns=['Read Key', 'Device ID' ], inplace=True)

      # summary_df = result_df.groupby('AirQloud').agg(
      #   optimal_completeness=('Optimal Completeness', 'sum'),
      #   good_completeness=('Good Completeness', 'sum'),
      #   fair_completeness=('Fair Completeness', 'sum'),
      #   poor_completeness=('Poor Completeness', 'sum'),
      #   downtime=('Downtime', 'sum')
      # ).reset_index()

      airqlouds = df['AirQloud'].unique()
      num_airqlouds = len(airqlouds)

      num_cols = 2  # Two pie charts per row
      num_rows = (num_airqlouds + 1) // 2  # Number of rows required
      fig = make_subplots(rows=num_rows, cols=num_cols, subplot_titles=airqlouds, specs=[[{'type':'pie'}, {'type':'pie'}]] * num_rows)

      for i, airqloud in enumerate(airqlouds):
        airqloud_df = result_df[result_df['AirQloud'] == airqloud]

        labels = ['Optimal', 'Good', 'Fair', 'Poor', 'Downtime']
        values = [airqloud_df['Optimal Completeness'].sum(), airqloud_df['Good Completeness'].sum(), airqloud_df['Fair Completeness'].sum(), airqloud_df['Poor Completeness'].sum(), airqloud_df['Downtime'].sum()]
        colors = ['green', 'yellow', 'orange', 'crimson', 'grey']

        row = i // num_cols + 1
        col = i % num_cols + 1
        fig.add_trace(go.Pie(labels=labels, values=values, hole=0.3, marker=dict(colors=colors)), row=row, col=col)

      fig.update_layout(title="AirQloud Completeness Performance", title_font_size=20, height=400*num_rows, width=600*num_cols)

      fig.show(renderer="colab")

    else:
      return "No AirQlouds selected"
# airQloud_completeness(final_df, start, end, AQData, airQlouds, deviceNames)


"""# Done"""
print("Powered by: AirQo")
# print("Made by Gibson")