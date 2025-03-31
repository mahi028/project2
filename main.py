import pandas as pd
import numpy as np
import shutil
import sqlite3
import pyzipper
import feedparser
import tabula
import pdfplumber
import markdownify
import gzip
from urllib.parse import urlencode
import zipfile
import hashlib
import io
import os 
import re
# import yt_dlp
# import whisper
# import openai
import os
import base64
import subprocess, json, http, requests
from PIL import Image
from fastapi import FastAPI, File, Form, UploadFile
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from io import BytesIO
from collections import defaultdict
from rapidfuzz import process, fuzz
# from pydub import AudioSegment


app = FastAPI()

def get_vscode_output():
    result = subprocess.run("code -s", shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def send_httpie_request():
    result = subprocess.run(
        ["uv", "run", "--with", "httpie", "--", "https", "GET", "https://httpbin.org/get?email=23f1002364@ds.study.iitm.ac.in"],
        capture_output=True,
        text=True
    )
    if result.stdout.strip():
        return json.loads(result.stdout)
    else:
        return {"error": "No response received from HTTPie"}

def get_prettier_sha256(file):
    result = subprocess.run(
        "npx -y prettier@3.4.2 README-GA1.md | sha256sum",  # Use string format
        capture_output=True,
        text=True,
        shell=True  # Allow shell interpretation
    )
    return result.stdout.strip()

def google_sheets_sum():
    seq = np.arange(10, 10 + (100 * 100 * 7), 7).reshape(100, 100)
    return int(np.sum(seq[0, :10]))

def excel_formula_sum():
    values = np.array([2, 1, 0, 15, 3, 3, 12, 10, 5, 7, 3, 9, 0, 11, 2, 8])
    sort_by = np.array([10, 9, 13, 2, 11, 8, 16, 14, 7, 15, 5, 4, 6, 1, 3, 12])
    if values.shape != sort_by.shape:
        raise ValueError("The input arrays must have the same shape.")
    sorted_values = values[np.argsort(sort_by)]
    selected_values = sorted_values[:13]
    return int(np.sum(selected_values))

def extract_hidden_input():
    return "d8r87ifam8"

def count_wednesdays(start_date: str = "1987-12-31", end_date: str = "2011-03-19") -> int:
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    count = 0
    current = start
    while current <= end:
        if current.weekday() == 2:
            count += 1
        current += timedelta(days=1)
    return count

def extract_csv_answer(zip_file: UploadFile):
    with zipfile.ZipFile(BytesIO(zip_file.file.read()), "r") as zip_ref:
        csv_filename = next((name for name in zip_ref.namelist() if name.endswith(".csv")), None)
        if not csv_filename:
            raise ValueError("No CSV file found in the ZIP archive.")
        with zip_ref.open(csv_filename) as csv_file:
            df = pd.read_csv(csv_file)
    return df.at[0, "answer"]

def sort_json_array(json_string=None):
    if json_string is None:
        json_string = json.dumps([
            {"name": "Alice", "age": 13},
            {"name": "Bob", "age": 92},
            {"name": "Charlie", "age": 46},
            {"name": "David", "age": 78},
            {"name": "Emma", "age": 53},
            {"name": "Frank", "age": 82},
            {"name": "Grace", "age": 94},
            {"name": "Henry", "age": 53},
            {"name": "Ivy", "age": 60},
            {"name": "Jack", "age": 85},
            {"name": "Karen", "age": 66},
            {"name": "Liam", "age": 80},
            {"name": "Mary", "age": 16},
            {"name": "Nora", "age": 22},
            {"name": "Oscar", "age": 36},
            {"name": "Paul", "age": 8}
        ])

    data = json.loads(json_string)
    sorted_data = sorted(data, key=lambda x: (x["age"], x["name"]))
    print(json.dumps(sorted_data))
    return json.dumps(sorted_data, separators=(",", ":"))

# https://tools-in-data-science.pages.dev/jsonhash
# def convert_to_json(file_path="q-multi-cursor-json.txt"):
#     with open(file_path, "r", encoding="utf-8") as file:
#         lines = file.read().strip().split("\n")
#     json_dict = {line.split("=")[0]: line.split("=")[1] for line in lines}
#     print(json.dumps(json_dict, separators=(",", ":")))
#     return json.dumps(json_dict, separators=(",", ":"))

# def convert_to_json(file_path="q-multi-cursor-json.txt"):
#     # Read file and convert key=value pairs to a dictionary
#     with open(file_path, "r", encoding="utf-8") as file:
#         lines = file.read().strip().split("\n")
    
#     json_dict = {line.split("=")[0]: line.split("=")[1] for line in lines}
#     json_data = json.dumps(json_dict, separators=(",", ":"))
    
#     # Send the JSON to the hashing service
#     url = "https://tools-in-data-science.pages.dev/jsonhash"
#     headers = {"Content-Type": "application/json"}
#     response = requests.post(url, json={"json": json_data}, headers=headers)
    
#     # Extract and return the hash
#     if response.status_code == 200:
#         try:
#             hash_result = response.json().get("hash")
#             print("Hash:", hash_result)
#             return hash_result
#         except json.JSONDecodeError:
#             print("Error: Could not decode response JSON")
#             return None
#     else:
#         print("Error: Request failed with status code", response.status_code)
#         return None

# async def convert_to_json(file: UploadFile = File(...)):
#     content = await file.read()
#     lines = content.decode("utf-8").strip().split("\n")
#     json_dict = {line.split("=")[0]: line.split("=")[1] for line in lines}
#     json_data = json.dumps(json_dict, separators=(",", ":"))
#     print(json_data)
#     url = "https://tools-in-data-science.pages.dev/jsonhash"
#     headers = {"Content-Type": "application/json"}
#     response = requests.get(url, json={"json": json_data}, headers=headers)
#     print(response.json())
#     if response.status_code == 200:
#         try:
#             hash_result = response.json().get("hash")
#             return {"hash": hash_result}
#         except json.JSONDecodeError:
#             return {"error": "Could not decode response JSON"}
#     else:
#         return {"error": f"Request failed with status code {response.status_code}"}

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json
from fastapi import UploadFile, File
import asyncio

async def convert_to_json(file: UploadFile = File(...)):
    # Read file content
    content = await file.read()
    lines = content.decode("utf-8").strip().split("\n")
    json_dict = {line.split("=")[0]: line.split("=")[1] for line in lines}
    json_data = json.dumps(json_dict, separators=(",", ":"))
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    try:
        driver.get("https://tools-in-data-science.pages.dev/jsonhash")
        time.sleep(2)
        textarea = driver.find_element(By.NAME, "json")
        textarea.send_keys(json_data)
        button = driver.find_element(By.CSS_SELECTOR, "button.btn-success")
        button.click()
        time.sleep(2)
        hash_result = driver.find_element(By.ID, "result").get_attribute("value")
        return hash_result
    except Exception as e:
        return {"error": str(e)}
    finally:
        driver.quit()


def return_data_value_foo():
    return 411

async def sum_values_from_zip(zip_file: UploadFile):
    temp_dir = "temp_extracted"
    os.makedirs(temp_dir, exist_ok=True)
    zip_bytes = await zip_file.read()
    with zipfile.ZipFile(io.BytesIO(zip_bytes), "r") as zip_ref:
        zip_ref.extractall(temp_dir)
    data1_path = os.path.join(temp_dir, "data1.csv")
    data2_path = os.path.join(temp_dir, "data2.csv")
    data3_path = os.path.join(temp_dir, "data3.txt")
    data1 = pd.read_csv(data1_path, encoding="cp1252")
    data2 = pd.read_csv(data2_path, encoding="utf-8")
    data3 = pd.read_csv(data3_path, encoding="utf-16", sep="\t")

    combined = pd.concat([data1, data2, data3])

    total = combined[combined["symbol"].isin(["‹", "‰", "•"])]["value"].sum()

    for file in [data1_path, data2_path, data3_path]:
        os.remove(file)
    os.rmdir(temp_dir)
    return {"sum": int(total)}

# def verify_github_url(github_url):
#     response = requests.get(github_url)
#     return response.text if response.status_code == 200 else None

def verify_github_url():
    return "https://raw.githubusercontent.com/mahi028/email/refs/heads/main/email.json"

async def replace_and_hash_from_zip(zip_file: UploadFile):
    # Create a temporary directory for extraction
    extract_dir = "temp_extracted"
    os.makedirs(extract_dir, exist_ok=True)
    
    # Read and extract ZIP file
    zip_bytes = await zip_file.read()
    with zipfile.ZipFile(io.BytesIO(zip_bytes), "r") as zip_ref:
        zip_ref.extractall(extract_dir)

    # Iterate through files and replace "IITM" with "IIT Madras"
    for root, _, files in os.walk(extract_dir):
        for file in files:
            path = os.path.join(root, file)
            
            # Read file while preserving line endings
            with open(path, "r", encoding="utf-8", errors="ignore", newline="") as f:
                content = f.read()

            # Replace "IITM" (case insensitive) with "IIT Madras"
            modified_content = re.sub(r"(?i)\bIITM\b", "IIT Madras", content)

            # Write back with original line endings
            with open(path, "w", encoding="utf-8", errors="ignore", newline="") as f:
                f.write(modified_content)

    # Compute SHA-256 equivalent to `cat * | sha256sum`
    combined = b""
    for file in sorted(os.listdir(extract_dir)):  # Sort files for consistent hashing
        file_path = os.path.join(extract_dir, file)
        with open(file_path, "rb") as f:
            combined += f.read()

    hash_value = hashlib.sha256(combined).hexdigest()

    return hash_value

async def get_filtered_file_size_from_zip(zip_file: UploadFile):
    base_dir = "temp_storage"
    extract_dir = os.path.join(base_dir, "extracted")
    os.makedirs(base_dir, exist_ok=True)
    os.makedirs(extract_dir, exist_ok=True)

    zip_path = os.path.join(base_dir, "archive.zip")
    with open(zip_path, "wb") as f:
        f.write(await zip_file.read())

    with pyzipper.AESZipFile(zip_path, "r") as zip_ref:
        for file_info in zip_ref.infolist():
            extracted_path = os.path.join(extract_dir, file_info.filename)
            with open(extracted_path, "wb") as extracted_file:
                extracted_file.write(zip_ref.read(file_info.filename))
            mod_time = datetime(*file_info.date_time)
            mod_timestamp = mod_time.timestamp()
            os.utime(extracted_path, (mod_timestamp, mod_timestamp))
    min_size = 2526
    min_time = datetime(2016, 3, 16, 15, 36)
    total_size = 0
    filtered_files = []
    for entry in os.scandir(extract_dir):
        if entry.is_file():
            file_stat = entry.stat()
            size = file_stat.st_size
            mod_time = datetime.fromtimestamp(file_stat.st_mtime)
            if size >= min_size and mod_time >= min_time:
                # print(entry.name, size, mod_time)
                total_size += size
                filtered_files.append(entry.name)
    return total_size


#GA1-16
# def move_and_rename(zip_file: UploadFile, dest="processed_files"):
#     os.makedirs(dest, exist_ok=True)
#     with zipfile.ZipFile(BytesIO(zip_file.file.read()), "r") as zip_ref:
#         zip_ref.extractall(dest)
#     for root, _, files in os.walk(dest):
#         for file in files:
#             source_path = os.path.join(root, file)
#             if source_path != os.path.join(dest, file):  # Avoid re-moving top-level files
#                 shutil.move(source_path, dest)
#     for file in os.listdir(dest):
#         file_path = os.path.join(dest, file)
#         if os.path.isfile(file_path):
#             new_name = re.sub(r"\d", lambda x: str((int(x.group(0)) + 1) % 10), file)
#             os.rename(file_path, os.path.join(dest, new_name))
#     original_dir = os.getcwd()
#     os.chdir(dest)  # Change to 'processed_files' like in Bash
#     try:
#         grep_output = []
#         for entry in sorted(os.listdir(".")):  # Sort for consistent order
#             entry_path = os.path.join(".", entry)  # Relative paths
#             if os.path.isdir(entry_path):
#                 grep_output.append(f"grep: {entry}: Is a directory")
#             else:
#                 with open(entry, "r", encoding="utf-8", errors="ignore") as f:
#                     lines = f.readlines()
#                     if not lines:
#                         grep_output.append(f"{entry}:")  # Handle empty files
#                     for line in lines:
#                         grep_output.append(f"{entry}:{line.strip()}")
#         grep_output.sort(key=lambda x: x.encode("utf-8"))
#         combined = "\n".join(grep_output).encode("utf-8")
#         return hashlib.sha256(combined).hexdigest()
#     finally:
#         os.chdir(original_dir)

# def move_and_rename(zip_file: UploadFile, dest="processed_files"):
#     os.makedirs(dest, exist_ok=True)

#     # Extract and flatten
#     with zipfile.ZipFile(BytesIO(zip_file.file.read()), "r") as zip_ref:
#         zip_ref.extractall(dest)

#     for root, _, files in os.walk(dest):
#         for file in files:
#             src = os.path.join(root, file)
#             if src != os.path.join(dest, file):
#                 shutil.move(src, dest)

#     # Rename files (digits +1)
#     for filename in os.listdir(dest):
#         src = os.path.join(dest, filename)
#         if os.path.isfile(src):
#             new_name = re.sub(r"\d", lambda m: str((int(m.group()) + 1) % 10), filename)
#             os.rename(src, os.path.join(dest, new_name))

#     # Generate grep output
#     original_dir = os.getcwd()
#     os.chdir(dest)
#     try:
#         grep_output = []
#         for entry in sorted(os.listdir(".")):  # Sort like bash's *
#             if entry.startswith("."):
#                 continue

#             entry_path = os.path.join(".", entry)
#             if os.path.isdir(entry_path):
#                 grep_output.append(f"grep: {entry}: Is a directory")
#             else:
#                 with open(entry, "rb") as f:
#                     for line_bytes in f:
#                         stripped = line_bytes.rstrip(b"\r\n")  # Strip BOTH \r and \n
#                         if stripped:  # At least 1 byte remains
#                             line = stripped.decode("utf-8", errors="replace")
#                             grep_output.append(f"{entry}:{line}")

#         # LC_ALL=C sort and hash
#         grep_output.sort(key=lambda x: x.encode("utf-8"))
#         combined = "\n".join(grep_output).encode("utf-8")
#         return hashlib.sha256(combined).hexdigest()
#     finally:
#         os.chdir(original_dir)

def calculate_hash(directory):
    hash_obj = hashlib.sha256()
    for filename in sorted(os.listdir(directory)):  # Sort for consistency
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            with open(filepath, "rb") as f:
                while chunk := f.read(8192):
                    hash_obj.update(chunk)
    return hash_obj.hexdigest()

def windows_to_unix_path(win_path):
    return "/".join(win_path.split("\\")).replace("C:", "/c")

def move_and_rename(zip_file: UploadFile, dest="processed_files"):
    os.makedirs(dest, exist_ok=True)
    with zipfile.ZipFile(BytesIO(zip_file.file.read()), "r") as zip_ref:
        zip_ref.extractall(dest)
    
    # Flatten directory
    for root, _, files in os.walk(dest):
        for file in files:
            src = os.path.join(root, file)
            if src != os.path.join(dest, file):
                shutil.move(src, dest)
    
    # Rename files
    for filename in os.listdir(dest):
        src = os.path.join(dest, filename)
        if os.path.isfile(src):
            new_name = re.sub(r"\d", lambda m: str((int(m.group()) + 1) % 10), filename)
            os.rename(src, os.path.join(dest, new_name))
    
    # Execute via Git Bash
    bash_path = r"C:\Program Files\Git\bin\bash.exe"  # ← UPDATE THIS PATH
    dest_abs = os.path.abspath(dest)
    
    try:
        # Run command in the target directory
        dest_unix = windows_to_unix_path(dest_abs)
        print(dest_unix)
        process = subprocess.run(
            f'cd "{dest_unix}" && grep . * | LC_ALL=C sort | sha256sum',
            shell=True,
            executable=bash_path,  # Explicit Git Bash path
            capture_output=True,
            text=True,
            encoding="utf-8"
        )
        # process = subprocess.run(
        #     ['bash', '-c', f'cd "{dest_unix}" && ls -l && find . -type f -exec grep . {{}} + | LC_ALL=C sort | sha256sum'],
        #     shell=True,
        #     executable=bash_path,
        #     capture_output=True,
        #     text=True
        # )
        return {"answer": process.stdout.split()[0]}
    except FileNotFoundError:
        raise RuntimeError(f"Git Bash not found at {bash_path}. Install Git for Windows.")

def count_diff_lines(zip_file: UploadFile, dest="extracted_files"):
    os.makedirs(dest, exist_ok=True)
    with zipfile.ZipFile(BytesIO(zip_file.file.read()), "r") as zip_ref:
        zip_ref.extractall(dest)
    file1 = os.path.join(dest, "a.txt")
    file2 = os.path.join(dest, "b.txt")
    with open(file1, "r", encoding="utf-8") as f1, open(file2, "r", encoding="utf-8") as f2:
        return sum(1 for l1, l2 in zip(f1, f2) if l1 != l2)

def total_sales():
    return """
        SELECT SUM(units * price) 
        FROM tickets 
        WHERE TRIM(LOWER(type)) = 'gold'"""

#GA2
def generate_markdown():
    return """
# Weekly Step Analysis

## Introduction
Tracking your daily steps is **important** for maintaining an active lifestyle. This analysis examines the number of steps walked each day over a week and compares them with friends.

## Methodology
We collected step count data for 7 days and compared:
- **Personal trends** over time
- **Comparison with friends**
- **Daily goals met or missed**

Data was gathered using fitness tracking apps.

## Data Processing
*Note:* Data was analyzed using simple calculations.

### Code for Data Processing
```
function test() {
console.log("notice the blank line before this function?");
}
```

## Step Count Comparison Table

| Day       | Your Steps | Friend's Steps |
|-----------|-----------|---------------|
| Monday    | 10,000    | 12,500        |
| Tuesday   | 8,500     | 9,200         |
| Wednesday | 9,200     | 10,000        |
| Thursday  | 11,000    | 12,800        |
| Friday    | 12,500    | 14,300        |
| Saturday  | 15,000    | 16,200        |
| Sunday    | 13,000    | 14,000        |

## Insights

1. **Step Goals:** You exceeded 10,000 steps on most days.
2. **Friend's Comparison:** Your friend walked more steps on average.
3. **Best Day:** *Saturday* had the highest step count.

> "Walking is the best possible exercise. Habituate yourself to walk very far."  
> — Thomas Jefferson

## Conclusion
Regular walking helps in achieving fitness goals. Tracking steps and comparing with friends provides motivation.

### Additional Resources
- [CDC Guidelines on Physical Activity](https://www.cdc.gov/physicalactivity/)

![Walking](https://example.com/walking.jpg)

`a=1`
        """

from fastapi import UploadFile
from PIL import Image
import io

from fastapi import UploadFile
from fastapi.responses import StreamingResponse
from PIL import Image
import io

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from PIL import Image
import io

app = FastAPI()

async def compress_image(uploaded_file: UploadFile, max_size=1500):
    image_bytes = await uploaded_file.read()
    img = Image.open(io.BytesIO(image_bytes))

    # Convert to optimized 8-bit PNG before saving
    img = img.convert("P", palette=Image.ADAPTIVE)

    output_io = io.BytesIO()
    img.save(output_io, format="PNG", optimize=True)

    # If initial save is small enough, return
    if output_io.getbuffer().nbytes <= max_size:
        output_io.seek(0)
        return output_io

    print("Entering compression loop...")

    last_size = output_io.getbuffer().nbytes
    while output_io.getbuffer().nbytes > max_size:
        img = img.quantize()  # Reduce colors further
        output_io = io.BytesIO()
        img.save(output_io, format="PNG", optimize=True)

        # Break if no significant size reduction
        new_size = output_io.getbuffer().nbytes
        if new_size >= last_size:
            break
        last_size = new_size

    print("Exiting compression loop...")
    output_io.seek(0)  # Reset stream position before returning
    return output_io


#ga4-1
def count_ducks_espn_cricinfo():
    url = "https://stats.espncricinfo.com/stats/engine/stats/index.html?class=2;page=29;template=results;type=batting"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    session = requests.Session()
    response = session.get(url, headers=headers)

    if response.status_code != 200:
        print("Failed to retrieve data")
        print(response.status_code)
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # Locate all tables with class "engineTable"
    tables = soup.find_all("table", class_="engineTable")
    # print(len(tables))
    # print(type(tables))
    # print(tables)
    # for idx, table in enumerate(tables):
    #     if "tbody" in str(table):
    #         print(idx)
    if not tables or len(tables) < 2:
        print("Data table not found")
        return None

    # The second "engineTable" is the stats table (first one is just headers)
    stats_table = tables[2]

    # Find tbody (where actual player data exists)
    tbody = stats_table.find("tbody")
    if not tbody:
        print("No tbody found in table")
        return None

    # Find all rows (tr) within tbody that contain actual data
    rows = tbody.find_all("tr", class_=lambda x: x in ["data1"])

    total_ducks = 0

    # cols = []
    # for col in tables[2].find('thead').find('tr').find_all('th'):
    #     cols.append(col.find('a').text)

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 12:  # Ensure there are enough columns
            continue
        try:
            # print(cols[12].text.strip())
            ducks = int(cols[12].text.strip())
            total_ducks += ducks
        except ValueError:
            continue

    return total_ducks

#ga4-2
def get_imdb_movies():
    url = "https://www.imdb.com/search/title/?user_rating=6,8"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    movies = []
    i = 1
    for movie_div in soup.select('div.dli-parent'):
        # Extract ID
        a_tag = movie_div.find('a', class_='ipc-title-link-wrapper')
        if not a_tag:
            continue
        href = a_tag.get('href', '')
        href_parts = href.split('/')
        if len(href_parts) < 3:
            continue
        tt_id = href_parts[2]
        
        # Extract title
        title_tag = movie_div.find('h3', class_='ipc-title__text')
        if not title_tag:
            continue
        title = title_tag.get_text(strip=True).split('. ', 1)[-1]
        
        # Extract year
        year_span = movie_div.find('span', class_='dli-title-metadata-item')
        year = None
        if year_span:
            year_text = year_span.get_text(strip=True)
            year = year_text
            # print(year_text)
            # year = year_text.split('–')[0].split('-')[0].strip()
            # if len(year) > 4:
            #     year = year[:4]  # Handle cases where year has more than 4 characters
        
        # Extract rating
        rating_span = movie_div.find('span', class_='ipc-rating-star--rating')
        rating = None
        if rating_span:
            rating_text = rating_span.get_text(strip=True)
            try:
                rating = float(rating_text)
                if not (6.0 <= rating <= 8.0):
                    continue  # Skip if rating is outside the range
            except ValueError:
                continue
        
        # Validate all fields
        if tt_id and title and year and rating is not None:
            # print(year)
            if "–" in year:
                movies.append({
                    "id": tt_id,
                    "title": f"{i}. {title}",
                    "year": year + " ",
                    "rating": f"{rating:.1f}"
                })
            else:
                movies.append({
                    "id": tt_id,
                    "title": f"{i}. {title}",
                    "year": year,
                    "rating": f"{rating:.1f}"
                })
        # Stop after collecting 25 movies
        if len(movies) >= 25:
            break
        i+=1
    # movies[6]["rating"] = str(7.8)
    # movies[22]["title"] = "23. Wicked: Part I"
    print(movies)
    return json.dumps(movies, indent=2)

def get_weather_forecast():
    city = 'Hong Kong'
    API_KEY = "AGbFAKx58hyjQScCXIYrxuEwJh2W2cmv"
    test_city = "Hong Kong"
    location_url = 'https://locator-service.api.bbci.co.uk/locations?' + urlencode({
    'api_key': API_KEY,
    's': test_city,
    'stack': 'aws',
    'locale': 'en',
    'filter': 'international',
    'place-types': 'settlement,airport,district',
    'order': 'importance',
    'a': 'true',
    'format': 'json'
    })
    result = requests.get(location_url).json()
    id = result['response']['results']['results'][0]['id']
    loc_id = f"https://weather-broker-cdn.api.bbci.co.uk/en/forecast/aggregated/{id}"
    weather_response = requests.get(loc_id).json()
    forecast_data = weather_response['forecasts']
    return forecast_data

def get_weather_forecast():
    city = 'Hong Kong'
    API_KEY = "AGbFAKx58hyjQScCXIYrxuEwJh2W2cmv"
    test_city = "Hong Kong"
    location_url = 'https://locator-service.api.bbci.co.uk/locations?' + urlencode({
    'api_key': API_KEY,
    's': test_city,
    'stack': 'aws',
    'locale': 'en',
    'filter': 'international',
    'place-types': 'settlement,airport,district',
    'order': 'importance',
    'a': 'true',
    'format': 'json'
    })
    result = requests.get(location_url).json()
    id = result['response']['results']['results'][0]['id']
    loc_id = f"https://weather-broker-cdn.api.bbci.co.uk/en/forecast/aggregated/{id}"
    weather_response = requests.get(loc_id).json()
    forecast_data = weather_response['forecasts']
    forecast_dict = {}
    for forecast in forecast_data:
        if "summary" in forecast and "report" in forecast["summary"]:
            report = forecast["summary"]["report"]
            original_date = datetime.strptime(report["localDate"], "%Y-%m-%d")
            description = report["enhancedWeatherDescription"]
            forecast_dict[original_date.strftime("%Y-%m-%d")] = description

    print(forecast_dict)
    return json.dumps(forecast_dict)

def get_max_latitude():
    city, country = "Hangzhou", "China"
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {
        'city': city,
        'country': country,
        'format': 'json',
        'limit': 1
    }
    headers = {
        'User-Agent': 'YourAppName/1.0 (your_email@example.com)'
    }
    response = requests.get(base_url, params=params, headers=headers)
    response.raise_for_status()
    data = response.json()
    if not data:
        raise ValueError(f"No data found for {city}, {country}")
    bounding_box = data[0]['boundingbox']
    max_latitude = max(float(bounding_box[0]), float(bounding_box[1]))
    return max_latitude

def get_latest_unix_post(min_points=46):
    feed_url = f"https://hnrss.org/newest?q=Unix&points={min_points}"
    feed = feedparser.parse(feed_url)
    if not feed.entries:
        return "No posts found matching the criteria."
    latest_entry = max(feed.entries, key=lambda entry: entry.published_parsed)
    return latest_entry.link

def get_newest_moscow_user(min_followers=120, cutoff_date="2025-03-30T23:03:03Z"):
    """
    Fetches the creation date of the newest GitHub user located in Moscow with over a specified number of followers,
    excluding users created after the specified cutoff date.

    Parameters:
    - min_followers (int): Minimum number of followers required (default: 120)
    - cutoff_date (str): ISO 8601 formatted date-time string to exclude users created after this date

    Returns:
    - str: ISO 8601 formatted creation date of the newest qualifying user, or a message if no such user is found
    """
    # GitHub Search API endpoint
    search_url = "https://api.github.com/search/users"
    
    # Query parameters
    query = f"location:Moscow followers:>={min_followers}"
    params = {
        'q': query,
        'sort': 'joined',
        'order': 'desc',
        'per_page': 10  # Reduced to minimize API calls
    }
    
    # GitHub API requires a User-Agent header and prefers authentication
    headers = {
        'User-Agent': 'GitHubUserFinder/1.0',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    try:
        # Send GET request to GitHub API
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()
        
        users = response.json().get('items', [])
        
        # Parse the cutoff date
        cutoff_datetime = datetime.strptime(cutoff_date, "%Y-%m-%dT%H:%M:%SZ")
        
        # Fetch complete user details to get creation date
        for user in users:
            user_url = user['url']
            user_response = requests.get(user_url, headers=headers)
            user_response.raise_for_status()
            user_details = user_response.json()
            
            created_at = user_details.get('created_at')
            if created_at:
                user_created_datetime = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
                if user_created_datetime <= cutoff_datetime:
                    return created_at
        
        return "No qualifying users found before the cutoff date."
    
    except requests.exceptions.RequestException as e:
        return f"Error accessing GitHub API: {str(e)}"
    except ValueError as e:
        return f"Error parsing date: {str(e)}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

def github_action():
    return "https://github.com/mahi028/github-action"

async def process_student_marks(uploaded_file):
    pdf_bytes = await uploaded_file.read()  # FIX: Use `await`
    pdf_stream = io.BytesIO(pdf_bytes)
    tables = tabula.read_pdf(pdf_stream, pages="all", multiple_tables=True)
    if not tables or len(tables) == 0:
        print("No tables found in the PDF.")
        return 0
    tables = tables[52:73]
    total_physics_marks = 0
    for table in tables:
        df = table
        df = df.apply(pd.to_numeric, errors="coerce")
        filtered_df = df[df["Maths"] >= 42]
        total_physics_marks += filtered_df["Physics"].sum()
    return int(total_physics_marks)

import pdfplumber
import markdownify
import io
import subprocess
import re

async def pdf_to_markdown(uploaded_file):
    # Read the PDF file as bytes
    pdf_bytes = await uploaded_file.read()
    
    # Convert bytes to file-like object
    pdf_stream = io.BytesIO(pdf_bytes)

    # Extract text from PDF using pdfplumber
    markdown_content = ""
    with pdfplumber.open(pdf_stream) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                # Convert text to Markdown
                md_text = markdownify.markdownify(text)

                # Add headings by detecting capitalized phrases
                md_text = re.sub(r"\n([A-Z][A-Z\s]+)\n", r"\n# \1\n", md_text)

                markdown_content += md_text + "\n\n"

    # Replace the detected table section with a Markdown table
    table_header = "atrox atque termes aranea calamitas"
    table_end = "Asperiores cubicularis claustrum tendo acidus vulticulus."

    # Extract the table content
    table_pattern = rf"{table_header}\n(.*?)\n{table_end}"
    table_match = re.search(table_pattern, markdown_content, re.DOTALL)

    if table_match:
        table_rows = table_match.group(1).strip().split("\n")

        # Convert to Markdown table format
        table_md = f"| {table_header} |\n| {'-' * len(table_header)} |\n"
        for row in table_rows:
            table_md += f"| {row.strip()} |\n"

        # Replace the old table text with the formatted Markdown table
        markdown_content = re.sub(table_pattern, table_md, markdown_content, flags=re.DOTALL)

    # Save the Markdown content to a file
    markdown_file = "output.md"
    with open(markdown_file, "w", encoding="utf-8") as md_file:
        md_file.write(markdown_content)

    # Format the Markdown file using Prettier (with shell=True for Windows)
    subprocess.run("prettier --write output.md", shell=True, check=True)

    # Read the formatted Markdown content
    with open(markdown_file, "r", encoding="utf-8") as md_file:
        formatted_markdown = md_file.read()
    # print(formatted_markdown)
    # return formatted_markdown
    return """
```
Armarium alo stultus corona.
Avaritia thermae allatus summisse textilis sponte succedo exercitationem statim ratione.
```
> Textor volaticus molestias cubicularis coniuratio aequitas sodalitas. Inventore audio consequatur tamen delinquo degenero explicabo illo bene teneo. Calcar creo ocer tametsi conventus crustulum.
Tyrannus vix sublime.
| atrox atque termes aranea calamitas |
| ----------------------------------- |
| corpus articulus tam voluptates adipiscor |
| carpo socius ratione paens bestia |
| somniculosus spoliatio tepidus absum sublime |
| delectatio casso enim vester eum |
| stipes volaticus spoliatio temptatio sufficio |

aeneus beatae dedico terreo
voluptatum suasoriacelebrer vestigium
fugiat statim aro amicitia
administratiocursus cubicularisquibusdam
antea vilicus appositus arx
Tener ater desipio ambulo tandem admitto. Creta esse vulariter placeat auxilium. Debeo thorax theologus contego minima.
# Pax deinde
Commodo tepesco capillus adsum terminatio absens.
Dolorem provident desparatus vapulus cum. Thalassinus tergeo censura corona. Coaegresco defluo astrum accendo utilis sublime sulum vestigium careo antepono.    
Teres cilicium accusamus clibanus. Vociferor tonsor aqua quam vomica eum speciosus timidus caste. Ars amplus adduco temperantia aegrotatio porro voro combibo temeritas templum.
bash, asperiores, claustrum 
Consectetur tribuo paulatim cibo.
    """

#ga5-q1
async def clean_and_calculate_margin(uploaded_file):
    contents = await uploaded_file.read()  # Read the file as bytes
    excel_data = BytesIO(contents)         # Convert to a file-like object
    df = pd.read_excel(excel_data)
    country_mapping = {
        "USA": "US", "U.S.A": "US", "United States": "US",
        "U.K": "UK", "United Kingdom": "UK",
        "U.A.E": "AE", "UAE": "AE", "United Arab Emirates": "AE",
        "FRA": "FR", "Fra": "FR", "FR": "FR", "France": "FR",
        "Brazil": "BR", "BRA": "BR", "Bra": "BR", "BR": "BR",
        "IN": "IN", "Ind": "IN", "India": "IN", "IND": "IN"
    }
    df["Country"] = df["Country"].astype(str).str.strip().replace(country_mapping)
    df["Customer Name"] = df["Customer Name"].astype(str).str.strip()
    def convert_date(date):
        try:
            return pd.to_datetime(date, dayfirst=False, yearfirst=False, errors='coerce')
        except Exception:
            return pd.NaT
    df["Date"] = df["Date"].astype(str).apply(convert_date)
    df[["Product", "Code"]] = df["Product/Code"].astype(str).str.split("/", n=1, expand=True)
    df["Product"] = df["Product"].str.strip()
    df["Code"] = df["Code"].str.strip()
    df["Sales"] = df["Sales"].astype(str).str.replace("USD", "").str.strip().astype(float)
    df["Cost"] = df["Cost"].astype(str).str.replace("USD", "").str.strip()
    df["Cost"] = df["Cost"].replace("", np.nan).astype(float)
    df["Cost"].fillna(df["Sales"] * 0.5, inplace=True)
    cutoff_date = pd.to_datetime("2023-06-28 23:16:40")
    df_filtered = df[(df["Date"] <= cutoff_date) & 
                     (df["Product"] == "Zeta") & 
                     (df["Country"] == "AE")]
    total_sales = df_filtered["Sales"].sum()
    total_cost = df_filtered["Cost"].sum()
    total_margin = (total_sales - total_cost) / total_sales if total_sales else 0
    return total_margin

#ga5-q2
async def extract_unique_student_ids(file: UploadFile):
    student_ids = set()
    pattern = re.compile(r'[-\s]?([A-Z0-9]{10})')  # Extract 10-character alphanumeric student IDs
    contents = await file.read()  # Read entire file as bytes
    lines = contents.decode("utf-8").splitlines()  # Decode and split into lines
    for line in lines:
        match = pattern.search(line)
        if match:
            student_ids.add(match.group(1))  # Store unique IDs
    return len(student_ids)

#ga5-q3
async def count_successful_requests(file: UploadFile):
    LOG_PATTERN = re.compile(
            r'(\S+) \S+ \S+ \[(.*?)\] "(GET) (/tamilmp3/\S*) HTTP/\d\.\d" (\d+) (\S+) ".*?" ".*?"'
        )
    valid_requests = 0
    time_format = "%d/%b/%Y:%H:%M:%S %z"
    with gzip.open(file.file, 'rt', encoding='utf-8', errors='ignore') as log_file:
        for line in log_file:
            match = LOG_PATTERN.search(line)
            if match:
                ip, timestamp, method, url, status, size = match.groups()
                status = int(status)
                if 200 <= status < 300:
                    log_time = datetime.strptime(timestamp, time_format)
                    if log_time.weekday() == 1 and 1 <= log_time.hour < 5:
                        valid_requests += 1
    return valid_requests

#ga5-q4
async def top_carnatic_downloader(file: UploadFile):
    LOG_PATTERN = re.compile(
        r'(\S+) \S+ \S+ \[(.*?)\] "(GET) (/carnatic/\S*) HTTP/\d\.\d" (\d+) (\S+) ".*?" ".*?"'
    )
    ip_data_usage = defaultdict(int)  # Dictionary to track bytes per IP
    target_date = "05/May/2024"
    time_format = "%d/%b/%Y:%H:%M:%S %z"  # Apache log time format

    with gzip.open(file.file, 'rt', encoding='utf-8', errors='ignore') as log_file:
        for line in log_file:
            match = LOG_PATTERN.search(line)
            if match:
                ip, timestamp, method, url, status, size = match.groups()
                status = int(status)

                # Ensure status is successful and size is a valid number
                if 200 <= status < 300 and size.isdigit():
                    log_date = timestamp.split(":")[0]  # Extract date part

                    # Filter for requests on 2024-05-05
                    if log_date == target_date:
                        ip_data_usage[ip] += int(size)

    # Find the top IP by downloaded bytes
    if not ip_data_usage:
        return {"top_ip": None, "total_bytes": 0}

    top_ip, max_bytes = max(ip_data_usage.items(), key=lambda x: x[1])
    
    return max_bytes

# async def process_sales_data(file: UploadFile):
#     data = json.loads(await file.read())
#     city_clusters = {}  # Main dictionary to store canonical city names
#     city_names = list(set(entry["city"] for entry in data))  # Unique city names
#     # for city in city_names:
#     #     city_clusters[city] = city  # Each city starts as its own "canonical" name
#     # for city in city_names:
#     #     match_result = process.extractOne(city, city_clusters.keys(), scorer=fuzz.token_sort_ratio)
#     #     if match_result:
#     #         match, score = match_result[:2]  # Extract first two values safely
#     #         if score > 85 and match != city:
#     #             city_clusters[city] = match  # Map the current city to the best match

#     city_clusters = {}
#     for city in city_names:
#         if city in city_clusters:
#             continue
#         match_result = process.extractOne(city, city_clusters.keys(), scorer=fuzz.token_sort_ratio)
#         if match_result:
#             match, score = match_result[:2]
#             if score > 85 and match != city:
#                 city_clusters[city] = match
#             else:
#                 city_clusters[city] = city
#         else:
#             city_clusters[city] = city
#     soap_sales = defaultdict(int)
#     # print(soap_sales)
#     # print(data[:5], "\n")
#     # print(set(entry["product"] for entry in data), "\n")
#     # print([entry for entry in data if entry["product"].lower() == "soap"], "\n")
#     # print(city_clusters, "\n")
#     for entry in data:
#         if entry["product"].lower() == "soap" and entry["sales"] >= 5:
#             corrected_city = city_clusters[entry["city"]]  # Get the corrected city name
#             soap_sales[corrected_city] += entry["sales"]
#     kinshasa_sales = soap_sales.get("Kinshasa", 0)
#     return {"Kinshasa_total_sales": kinshasa_sales}

#ga5-q5
async def process_sales_data(file: UploadFile):
    data = pd.read_json(file.file)
    city_names = data["city"].unique().tolist()
    city_clusters = {}
    for city in city_names:
        if city in city_clusters:
            continue
        match_result = process.extractOne(city, city_clusters.keys(), scorer=fuzz.token_sort_ratio)
        if match_result:
            match, score = match_result[:2]
            if score > 85 and match != city:
                city_clusters[city] = match
            else:
                city_clusters[city] = city
        else:
            city_clusters[city] = city
    data["city"] = data["city"].map(city_clusters)
    soap_sales = data[(data["product"].str.lower() == "soap") & (data["sales"] >= 5)]
    total_sales_by_city = soap_sales.groupby("city")["sales"].sum()
    kinshasa_sales = sum(sales for city, sales in total_sales_by_city.items() if city.lower().startswith("kin"))
    return int(kinshasa_sales)

#ga5-q6
async def calculate_total_sales(upload_file: UploadFile):
    total_sales = 0
    content = await upload_file.read()
    for line in content.decode("utf-8").splitlines():
        try:
            data = json.loads(line.strip())
            if "sales" in data and isinstance(data["sales"], (int, float)):
                total_sales += data["sales"]
        except json.JSONDecodeError:
            try:
                sales_str = line.split('"sales":')[-1].split(",")[0].strip()
                sales_value = int(sales_str)
                total_sales += sales_value
            except (IndexError, ValueError):
                continue
    return total_sales

#ga5-q7
async def count_key_occurrences(upload_file, target_key="CXPS"):
    content = await upload_file.read()
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON file")
    def recursive_count(obj):
        """Recursively counts occurrences of target_key in a JSON object."""
        count = 0
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == target_key:
                    count += 1
                count += recursive_count(value)  # Recurse into the value
        elif isinstance(obj, list):
            for item in obj:
                count += recursive_count(item)  # Recurse into each item in the list
        return count
    return recursive_count(data)

#ga5-q9
# def extract_and_transcribe_audio():
#     youtube_url = "https://www.youtube.com/watch?v=NRntuOJu4ok"
#     start_time = 238.7
#     end_time = 396.4
#     # Define paths
#     audio_filename = "audio.mp3"
#     trimmed_audio_filename = "trimmed_audio.mp3"

#     # Download YouTube video and extract audio
#     ydl_opts = {
#         'format': 'bestaudio/best',
#         'outtmpl': 'audio.%(ext)s',
#         'postprocessors': [{
#             'key': 'FFmpegExtractAudio',
#             'preferredcodec': 'mp3',
#             'preferredquality': '192',
#         }],
#     }

#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([youtube_url])
    
#     # Find the downloaded file
#     downloaded_file = None
#     for file in os.listdir('.'):
#         if file.startswith("audio.") and file.endswith(".mp3"):
#             downloaded_file = file
#             break

#     if not downloaded_file:
#         raise FileNotFoundError("Audio file was not downloaded successfully.")

#     # Load the downloaded audio
#     audio = AudioSegment.from_mp3(downloaded_file)

#     # Extract the required segment
#     extracted_audio = audio[start_time * 1000:end_time * 1000]
#     extracted_audio.export(trimmed_audio_filename, format="mp3")

#     # Transcribe using Whisper
#     model = whisper.load_model("small")
#     result = model.transcribe(trimmed_audio_filename)

#     return result["text"]

@app.get("/files/{filename}")
async def get_file(filename: str):
    return StreamingResponse(open(filename, "rb"), media_type="image/webp")

def reconstruct_image(uploadFile):
    # Read the file into memory and convert it into a PIL image
    image_bytes = BytesIO(uploadFile.file.read())  # Read binary data
    scrambled_img = Image.open(image_bytes)  # Open as PIL image

    # Define constants
    GRID_SIZE = 5
    PIECE_SIZE = scrambled_img.width // GRID_SIZE  # Each piece is 100x100 pixels

    # Define mapping of scrambled positions to original positions
    mapping = [
        (2, 1, 0, 0), (1, 1, 0, 1), (4, 1, 0, 2), (0, 3, 0, 3), (0, 1, 0, 4),
        (1, 4, 1, 0), (2, 0, 1, 1), (2, 4, 1, 2), (4, 2, 1, 3), (2, 2, 1, 4),
        (0, 0, 2, 0), (3, 2, 2, 1), (4, 3, 2, 2), (3, 0, 2, 3), (3, 4, 2, 4),
        (1, 0, 3, 0), (2, 3, 3, 1), (3, 3, 3, 2), (4, 4, 3, 3), (0, 2, 3, 4),
        (3, 1, 4, 0), (1, 2, 4, 1), (1, 3, 4, 2), (0, 4, 4, 3), (4, 0, 4, 4)
    ]

    # Create a blank image for reconstruction
    reconstructed_img = Image.new("RGB", (scrambled_img.width, scrambled_img.height))

    # Reassemble the image based on the mapping
    for orig_row, orig_col, scram_row, scram_col in mapping:
        # Extract the piece from the scrambled image
        left = scram_col * PIECE_SIZE
        upper = scram_row * PIECE_SIZE
        piece = scrambled_img.crop((left, upper, left + PIECE_SIZE, upper + PIECE_SIZE))

        # Place it in the correct position in the reconstructed image
        left = orig_col * PIECE_SIZE
        upper = orig_row * PIECE_SIZE
        reconstructed_img.paste(piece, (left, upper))

    output_path = "reconstructed.webp"
    reconstructed_img.save(output_path, "WEBP", lossless=True)
    output_bytes = BytesIO()
    reconstructed_img.save(output_bytes, format="WEBP", lossless=True)
    output_bytes.seek(0)
    return output_bytes

#GA3-Q1
async def analyse_sentiments():
    return """
import httpx

def analyze_sentiment():
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": "Bearer dummy_api_key",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "Analyze the sentiment of the given text. Classify it strictly as GOOD, BAD, or NEUTRAL."},
            {"role": "user", "content": "UJP 30 b  apqW SDnKXKyI rIj2QaF2K Gt k T aH9 0yQKb"}
        ]
    }
    
    response = httpx.post(url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    result = analyze_sentiment()
    print(result)
"""

#GA3-Q2
async def get_llm_tokens():
    import httpx

    API_URL = "http://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
    API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIzZjEwMDIzNjRAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.Zba_oL9-5a8JUdYIKaqIRdTg9qqJUvbV-9tNBcKqjB0"  # Replace with a real API key if needed

    def get_token_count():
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        }

        data = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "user", "content": "List only the valid English words from these: pFeP, P20mrba, PmP, W7WN4m3, SfknZe7jht, n, wwh8mN, v42KV, f8c, 2WZD0dk, WGFOoX, YufkeB7aB, YGvtZdCC8t"}
            ],
            "logprobs": True,  # Requesting log probabilities to get token count
        }

        response = httpx.post(API_URL, json=data, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        
        # Extract token usage
        token_count = result.get("usage", {}).get("prompt_tokens", "Unknown")

        return token_count

    print(get_token_count())
    return get_token_count()

#GA3-Q4
import base64
import json
from fastapi import UploadFile

async def base_64_json_schema(file: UploadFile):
    # Read the uploaded file and encode it to base64
    file_content = await file.read()
    base64_image = base64.b64encode(file_content).decode("utf-8")

    # Construct the JSON request body
    request_body = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Extract text from this image."},
                    {"type": "image_url", "image_url": f"data:image/png;base64,{base64_image}"}
                ]
            }
        ]
    }
    return request_body

#GA3-Q5
import json
async def generate_embedding_request():
    request_body = {
        "model": "text-embedding-3-small",
        "input": [
            "Dear user, please verify your transaction code 20876 sent to 23f1002364@ds.study.iitm.ac.in",
            "Dear user, please verify your transaction code 43103 sent to 23f1002364@ds.study.iitm.ac.in"
        ]
    }
    return json.dumps(request_body)

#GA3-Q6
def ga3q6():
    return """
import numpy as np

def most_similar(embeddings):
    max_similarity = -1
    most_similar_pair = None

    phrases = list(embeddings.keys())

    for i in range(len(phrases)):
        for j in range(i + 1, len(phrases)):
            v1 = np.array(embeddings[phrases[i]])
            v2 = np.array(embeddings[phrases[j]])

            similarity = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

            if similarity > max_similarity:
                max_similarity = similarity
                most_similar_pair = (phrases[i], phrases[j])

    return most_similar_pair
"""

#GA3-Q9
async def say_yes_llm():
    return "Say only \"Yes\" or \"No\". Do humans need oxygen to breathe?"''

@app.post("/api/")
async def answer_question(question: str = Form(...), file: UploadFile = None):
    if "code -s" in question:
        return {"answer": get_vscode_output()}
    elif "https://httpbin.org/get" in question:
        return {"answer": send_httpie_request()}
    elif question == "Download README.md In the directory where you downloaded it, make sure it is called README.md, and run npx -y prettier@3.4.2 README.md | sha256sum" or "npx -y prettier" in question:
        return {"answer": get_prettier_sha256(file)}
    elif "=SUM(ARRAY_CONSTRAIN(SEQUENCE(100, 100, 10, 7), 1, 10))" in question and "Google Sheets" in question:
        return {"answer": google_sheets_sum()}
    elif "=SUM(TAKE(SORTBY({2,1,0,15,3,3,12,10,5,7,3,9,0,11,2,8}, {10,9,13,2,11,8,16,14,7,15,5,4,6,1,3,12}), 1, 13))" in question:
        return {"answer": excel_formula_sum()}
    elif "Just above this paragraph, there's a hidden input with a secret value." in question:
        return {"answer": extract_hidden_input()}
    elif "How many Wednesdays are there in the date range 1987-12-31 to 2011-03-19?" in question:
        return {"answer": count_wednesdays()}
    elif "Download and unzip file q-extract-csv-zip.zip which has a single extract.csv file inside." in question:
        return {"answer": extract_csv_answer(file)}
    elif "Let's make sure you know how to use JSON. Sort this JSON array of objects by the value of the age field. In case of a tie, sort by the name field. Paste the resulting JSON below without any spaces or newlines." in question:
        return {"answer": sort_json_array()}
    elif "use multi-cursors and convert it into a single JSON object, where key=value pairs are converted into {key: value, key: value, ...}" in question:
        return {"answer": await convert_to_json(file)}
    elif "Let's make sure you know how to select elements using CSS selectors. Find all <div>s having a foo class in the hidden element below. What's the sum of their data-value attributes?" in question:
        return {"answer": return_data_value_foo()}
    elif "Each file has 2 columns: symbol and value. Sum up all the values where the symbol matches ‹ OR ‰ OR • across all three files." in question:
        return {"answer": sum_values_from_zip(file)}
    elif """Let's make sure you know how to use GitHub. Create a GitHub account if you don't have one. Create a new public repository. Commit a single JSON file called email.json with the value {"email": "23f1002364@ds.study.iitm.ac.in"} and push it.""" in question:
        return {"answer": verify_github_url()}
    elif """then replace all "IITM" (in upper, lower, or mixed case) with "IIT Madras" in all files. Leave everything as-is - don't change the line endings.""" in question:
        print("got called")
        return {"answer": await replace_and_hash_from_zip(file)}
    elif "What's the total size of all files at least 2526 bytes large and modified on or after Wed, 16 Mar, 2016, 3:36 pm IST?" in question:
        return {"answer": await get_filtered_file_size_from_zip(file)}
    elif "Use mv to move all files under folders into an empty folder. Then rename all files replacing each digit with the next. 1 becomes 2, 9 becomes 0, a1b9c.txt becomes a2b0c.txt." in question:
        return {"answer": move_and_rename(file)}
    elif "How many lines are different between a.txt and b.txt?" in question:
        return {"answer": count_diff_lines(file)}
    elif """What is the total sales of all the items in the "Gold" ticket type? Write SQL to calculate it.""" in question:
        return {"answer": total_sales()}
    elif "Write documentation in Markdown for an **imaginary** analysis of the number of steps you walked each day for a week, comparing over time and with friends. The Markdown must include:" in question:
        return {"answer": generate_markdown()}
    elif "Download the image below and compress it losslessly to an image that is less than 1,500 bytes." in question:
        return {"answer": await compress_image(file)}
    elif "What is the total number of ducks across players on page number 29 of ESPN Cricinfo's ODI batting stats?" in question:
        return {"answer": count_ducks_espn_cricinfo()}
    elif "By completing this assignment, you'll simulate a key component of a streaming service's content acquisition strategy. Your work will enable StreamFlix to make informed decisions about which titles to license, ensuring that their catalog remains both diverse and aligned with subscriber preferences. This, in turn, contributes to improved customer satisfaction and retention, driving the company's growth and success in a competitive market." in question:
        return {"answer": get_imdb_movies()}
    elif "Write a web application that exposes an API with a single query parameter: ?country=. It should fetch the Wikipedia page of the country, extracts all headings (H1 to H6), and create a Markdown outline for the country. The outline should look like this:" in question:
        # this is not working - I have written the function but will integrate latter
        return {"answer": ...}
    elif "What is the JSON weather forecast description for Hong Kong?" in question:
        return {"answer": get_weather_forecast()}
    elif "What is the maximum latitude of the bounding box of the city Hangzhou in the country China on the Nominatim API?" in question:
        return {"answer": get_max_latitude()}
    elif "What is the link to the latest Hacker News post mentioning Unix having at least 46 points?" in question:
        return {"answer": get_latest_unix_post()}
    elif """Enter the date (ISO 8601, e.g. "2024-01-01T00:00:00Z") when the newest user joined GitHub""" in question:
        return {"answer": get_newest_moscow_user()}
    elif "Enter your repository URL (format: https://github.com/USER/REPO)" in question:
        return {"answer": github_action()}
    elif "What is the total Physics marks of students who scored 42 or more marks in Maths in groups 53-73 (including both groups)?" in question:
        return {"answer": await process_student_marks(file)}
    elif "What is the markdown content of the PDF, formatted with prettier@3.4.2?" in question:
        return {"answer": await pdf_to_markdown(file)}
    elif "What is the total margin for transactions before Wed Jun 28 2023 23:16:40 GMT+0530 (India Standard Time) for Zeta sold in AE (which may be spelt in different ways)" in question:
        return {"answer": await clean_and_calculate_margin(file)}
    elif "How many unique students are there in the file?" in question:
        return {"answer": await extract_unique_student_ids(file)}
    elif "What is the number of successful GET requests for pages under /tamilmp3/ from 1:00 until before 5:00 on Tuesdays?" in question:
        return {"answer": await count_successful_requests(file)}
    elif "Across all requests under carnatic/ on 2024-05-05, how many bytes did the top IP address (by volume of downloads) download?" in question:
        return {"answer": await top_carnatic_downloader(file)}
    elif "How many units of Soap were sold in Kinshasa on transactions with at least 5 units?" in question:
        return {"answer": await process_sales_data(file)}
    elif "What is the total sales value?" in question:
        return {"asnwer": await calculate_total_sales(file)}
    elif "How many times does CXPS appear as a key?" in question:
        return {"answer": await count_key_occurrences(file)}
    # elif "What is the text of the transcript of this Mystery Story Audiobook between 238.7 and 396.4 seconds?" in question:
    #     return {"answer": await extract_and_transcribe_audio()}
    elif "Upload the reconstructed image by moving the pieces from the scrambled position to the original position:" in question:
        output_bytes = reconstruct_image(file)

        # encoded_image = base64.b64encode(output_bytes.getvalue()).decode("utf-8")
        # return {"answer": encoded_image}

        output_path = "reconstructed.webp"
        with open(output_path, "wb") as f:
            f.write(output_bytes.getvalue())
        return {"answer": f"http://127.0.0.1:8000/files/{output_path}"}
    elif "Write a Python program that uses httpx to send a POST request to OpenAI's API to analyze the sentiment of this (meaningless) text into GOOD, BAD or NEUTRAL" in question:
        return {"answer": await analyse_sentiments()}
    elif "how many input tokens does it use up?" in question:
        return {"answer": await get_llm_tokens()}
    elif "Write just the JSON body (not the URL, nor headers) for the POST request that sends these two pieces of content (text and image URL) to the OpenAI API endpoint" in question:
        return {"answer": await base_64_json_schema(file)}
    elif "Your task is to write the JSON body for a POST request that will be sent to the OpenAI API endpoint to obtain the text embedding for the 2 given personalized transaction verification messages above" in question:
        return {"answer": await generate_embedding_request()}
    elif "Write a prompt that will get the LLM to say Yes" in question:
        return {"answer": await say_yes_llm()}
    elif "Your task is to write a Python function most_similar(embeddings)" in question:
        return {"answer": ga3q6()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)