#!/usr/bin/env python
# coding: utf-8

# In[7]:


import os
import json
import csv
import re
from datetime import datetime  

# === CONFIGURATION ===
folder_path = "/Users/User1/Desktop/conversation"  # Change this to your actual folder path
output_csv = "user_id_conversation.csv"  

target_user = "user_id"  # Replace with the user ID you're searching for

# Define the date range (YYYY-MM-DD)
start_date = datetime.strptime("2024-08-10", "%Y-%m-%d")
end_date = datetime.strptime("2025-03-10", "%Y-%m-%d")

# List to store extracted data
data_list = []

# Walk through all subdirectories and files
for root, _, files in os.walk(folder_path):
    for file in files:
        if file.endswith(".json"):  # Process only JSON files
            file_path = os.path.join(root, file)
            folder_name = os.path.basename(root)  # Extract the folder name

            # Extract date from file name (assuming format YYYY-MM-DD in the file name)
            date_match = re.search(r"\b(\d{4}-\d{2}-\d{2})\b", file)
            if not date_match:
                continue  # Skip files without a valid date format

            extracted_date = date_match.group(1)  # Extracted date as string
            file_date = datetime.strptime(extracted_date, "%Y-%m-%d")  # Convert to date object

            # Filter by date range
            if not (start_date <= file_date <= end_date):
                continue  # Skip files outside the date range

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    json_data = json.load(f)  # Load JSON file
                    contains_target_user = False  # Flag to check if user is present

                    messages = []

                    def process_entry(entry, contains_target_user_flag):
                        """Process a JSON entry and extract relevant fields."""
                        user_id = entry.get("user", "")
                        text = entry.get("text", "")
                        timestamp = entry.get("ts", "")
                        time_str = ""
                        time_obj = None

                        if timestamp:
                            try:
                                # Convert Slack timestamp (float or string) to HH:MM:SS
                                ts_int = int(float(timestamp))  # Convert to whole seconds
                                time_obj = datetime.utcfromtimestamp(ts_int)  # Convert to UTC
                                time_str = time_obj.strftime("%H:%M:%S")  # Format as HH:MM:SS
                            except (ValueError, TypeError):
                                pass  # Keep empty if conversion fails

                        if user_id == target_user:
                            contains_target_user_flag[0] = True  # Modify flag outside function

                        messages.append({
                            "Folder": folder_name,
                            "File": file,
                            "Date": extracted_date,
                            "Timestamp": timestamp,  # Original timestamp
                            "Time": time_str,  # Converted time in HH:MM:SS
                            "User": user_id,
                            "Text": text,
                            "Datetime": time_obj if time_obj else datetime.min  # Use for sorting
                        })

                    # Using a list as a mutable flag
                    contains_target_user_flag = [False]

                    # Handle JSON structure (dict or list)
                    if isinstance(json_data, dict):  
                        process_entry(json_data, contains_target_user_flag)
                    elif isinstance(json_data, list):  
                        for entry in json_data:
                            if isinstance(entry, dict):
                                process_entry(entry, contains_target_user_flag)

                    # Only add messages if the target user was in the file
                    if contains_target_user_flag[0]:
                        data_list.extend(messages)

            except Exception as e:
                print(f"Error processing {file_path}: {e}")

# === SORT DATA ===
# 1. Sort by Folder (A-Z)
# 2. Sort by Date (newest first)
# 3. Sort by Time (earliest first within each date)
data_list.sort(key=lambda x: (x["Folder"], datetime.strptime(x["Date"], "%Y-%m-%d"), x["Datetime"]))

# === SAVE TO CSV ===
with open(output_csv, "w", newline="", encoding="utf-8") as csv_file:
    fieldnames = ["Folder", "File", "Date", "Timestamp", "Time", "User", "Text"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    for row in data_list:
        del row["Datetime"]  # Remove sorting helper column
        writer.writerow(row)

print(f"Filtered messages saved as {output_csv}")


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




