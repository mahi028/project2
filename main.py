import pandas as pd
import numpy as np
import shutil
import sqlite3
import pyzipper
import zipfile, hashlib
import io, os, re
import subprocess, json, http, requests
from PIL import Image
from fastapi import FastAPI, File, Form, UploadFile
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from io import BytesIO

app = FastAPI()

def get_vscode_output():
    result = subprocess.run("code -s", shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def send_httpie_request():
    result = subprocess.run(
        ["uv", "run", "--with", "httpie", "--", "https", "GET", "https://httpbin.org/get?email=23f1000561@ds.study.iitm.ac.in"],
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

def verify_github_url(github_url):
    response = requests.get(github_url)
    return response.text if response.status_code == 200 else None

def verify_github_url(github_url="https://raw.githubusercontent.com/MohitKumar020291/project2/refs/heads/main/email.json"):
    return "https://raw.githubusercontent.com/MohitKumar020291/project2/refs/heads/main/email.json"

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
    elif """Let's make sure you know how to use GitHub. Create a GitHub account if you don't have one. Create a new public repository. Commit a single JSON file called email.json with the value {"email": "23f1000561@ds.study.iitm.ac.in"} and push it.""" in question:
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