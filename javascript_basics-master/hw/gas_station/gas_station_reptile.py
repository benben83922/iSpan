# 

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv
import pymysql
import requests

# === 設定 Chrome options ===
options = Options()
# options.add_argument("--headless")  # 不開視窗（可省略）
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# === 啟動瀏覽器 ===
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://www2.moeaea.gov.tw/oil111/Dealer/GasStations")

time.sleep(3)  # 等待頁面資料載入（可依網速調整）

try:
    test = driver.find_element(By.XPATH,"/html/body/main/div[5]/div/div/div/a/i")
    test.click()
except:
    pass
# === 抓取表格資料 ===
rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

data = []
for row in rows:
    cols = [td.text.strip() for td in row.find_elements(By.TAG_NAME, "td")]
    if cols:
        data.append(cols)

driver.quit()
# print(data)
# print(len(data))



# 建立連線
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="P@ssw0rd",
    database="my_database",
    charset="utf8mb4"  # 避免中文亂碼
)

cursor = conn.cursor()

item = data[0]
address = item[5]
url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
response = requests.get(url, verify=False)
print(response.text)
print("--------------------------------")
if response.status_code == 200:
        try:
            l_data = response.json()
        except requests.exceptions.JSONDecodeError:
            print("伺服器回傳非JSON內容",response.text)
        if l_data["status"] == "OK":
            lon = l_data["results"][0]["geometry"]["location"]["lng"]
            lat = l_data["results"][0]["geometry"]["location"]["lat"]
            print("緯度:", lat)
            print("經度:", lon)
            sql = "INSERT INTO gas_station_info(brand, address, service_time, station_name, longitude, latitude, phone) VALUES (%S, %S, %S, %S, %S, %S, %S )"
            cursor.execute(sql, (data[0][3], data[0][5], '', data[0][4], lon, lat, data[0][6]))
        else:
            print("查無結果")
else:
    print("HTTP錯誤", response.status_code)



# for item in data:
#     address = item[5]
#     url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
#     response = requests.get(url, verify=False)
#     # print(response.text)
#     if response.status_code == 200:
#         try:
#             l_data = response.json()
#         except requests.exceptions.JSONDecodeError:
#             print("伺服器回傳非JSON內容",response.text)
#         if "data" in l_data and l_data["data"]:
#             lon = l_data["data"][0]["lon"]
#             lat = l_data["data"][0]["lat"]
#             print("緯度:", lat)
#             print("經度:", lon)
#         else:
#             print("查無結果")
#     else:
#         print("HTTP錯誤", response.status_code)
    # sql = "INSERT INTO gas_station_info(brand, address, service_time, station_name, longitude, latitude, phone) VALUES (%S, %S, %S, %S, %S, %S, %S )"
    # cursor.execute(sql, (item[3], item[5], , item[4], item[0], item[0], item[6]))

conn.commit()

# # 執行 SQL
# cursor.execute("SELECT * FROM gas_station_info;")
# rows = cursor.fetchall()

cursor.close()
conn.close()
