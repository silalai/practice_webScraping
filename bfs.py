import requests
from bs4 import BeautifulSoup
import csv
import re
from googletrans import Translator

translator = Translator()

# ฟังก์ชันสำหรับดึงข้อมูลจากเว็บ
def scrape_data(url):
    web_data = requests.get(url)
    soup = BeautifulSoup(web_data.text, 'html.parser')
    
    find_word = soup.find_all("p", {"class": "p-comparison-table__item-name p-comparison-table__item-name--underline external-ab__default-name"})
    find_description = soup.find_all("div", {"class": "css-z4d070"})
    find_price = soup.find_all("span", {"class": "css-62pds5"})
    find_download = soup.find_all("div", {"class": "l-stack l-stack--row l-stack--spacing-4 l-stack--ai-normal l-stack--jc-normal l-stack--nowrap"})
    
    data = []
    rating = 1  # เพิ่มตัวแปร rating
    
    for name, description, price, download in zip(find_word[:5], find_description[3:8], find_price[:5], find_download[:5]):
        span_element = name.find("span")
        if span_element:
            text = span_element.text.strip().replace("เกม Simulator น่าเล่น", "").replace("เกมแนว Visual Novel", "")
            paragraph = description.find("p")
            if paragraph:
                description_text_th = paragraph.text.strip()
                description_text_en = translator.translate(description_text_th, src='th', dest='en').text
            else:
                description_text_en = ""
            price_text = price.text.strip()
            price_th = re.sub(r'[^\dบาท]', '', price_text)
            price_en = translator.translate(price_th, src='th', dest='en').text
            
            download_text = download.find("span", {"class": "css-9qvt39"})
            if download_text:
                download_text = download_text.text.strip()
            else:
                download_text = ""
            
            link_download = download.find("a")['href'] if download.find("a") else ""
            
            # เพิ่มข้อมูลในรูปแบบที่ถูกต้อง
            data.append([rating, text, description_text_en, price_en, download_text, link_download])
            rating += 1
    
    return data

# เปิดไฟล์ CSV เพื่อเขียนข้อมูล
with open('simulation_games.csv', mode='w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    
    # เขียนหัวข้อคอลัมน์
    writer.writerow(['Rating', 'Simulation', 'Description', 'Price', 'Download', 'Link Download'])
    
    # เขียนข้อมูล Simulation games ในแต่ละแถว
    rating = 1
    simulation_data = scrape_data("https://th.my-best.com/49548")
    for row in simulation_data:
        writer.writerow(row)
        rating += 1

# เพิ่ม sheet ใหม่ "Visual novel" ลงในแผ่นงานที่สอง
with open('simulation_games.csv', mode='a', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    
    # เขียนหัวข้อคอลัมน์
    writer.writerow(['Rating', 'Visual Novel', 'Description', 'Price', 'Download', 'Link Download'])
    
    # เขียนข้อมูล Visual Novel ในแต่ละแถว
    rating = 1
    visual_novel_data = scrape_data("https://th.my-best.com/50144")
    for row in visual_novel_data:
        writer.writerow(row)
        rating += 1

# เพิ่ม sheet ใหม่ "MOBA" ลงในแผ่นงานที่สาม
with open('simulation_games.csv', mode='a', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    
    # เขียนหัวข้อคอลัมน์
    writer.writerow(['Rating', 'MOBA', 'Description', 'Price', 'Download', 'Link Download'])
    
    # เขียนข้อมูล MOBA ในแต่ละแถว
    rating = 1
    moba_data = scrape_data("https://th.my-best.com/49479")
    for row in moba_data:
        writer.writerow(row)
        rating += 1
