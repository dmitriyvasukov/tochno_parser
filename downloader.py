import re
import requests
import os
import zipfile
import io
from bs4 import BeautifulSoup
from urllib.parse import unquote

#Конфиг
url = "https://tochno.st/datasets/pres_grants"
output_dir = "downloaded_data"


def download_and_extract_zip(url, output_dir):
    try:
        print(f"Скачять): {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        print(f"Размер архива: {len(response.content)/1024:.2f} KB")
        
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            csv_files = [f for f in zip_ref.namelist() if f.lower().endswith('.csv')]
            
            if not csv_files:
                print(f"В архиве нет CSV-файлов: {zip_ref.namelist()}")
                return
            
            zip_name = os.path.splitext(os.path.basename(url))[0]
            extract_path = os.path.join(output_dir, zip_name)
            os.makedirs(extract_path, exist_ok=True)
            
            for file in csv_files:
                zip_ref.extract(file, extract_path)
                print(f"Успешно извлечен: {os.path.join(extract_path, file)}")
                
    except Exception as e:
        print(f"Ошибка при обработке {url}: {type(e).__name__} - {str(e)}")



os.makedirs(output_dir, exist_ok=True)
print(f"Сохранение в: {os.path.abspath(output_dir)}")

try:
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    scripts = soup.find_all('script')
    
    for i, script in enumerate(scripts, 1):
        if not script.string or 'window.__NUXT__' not in script.string:
            continue
            
        file_matches = re.finditer(r'url:\s*"((https?:[^"]+\.zip)[^"]*)"', script.string)
        
        if not file_matches:
            print("Не найдены URL архивов в скрипте")
            continue
            
        for match in file_matches:
            file_url = match.group(1).replace('\\/', '/').replace('\\u002F', '/')
            file_url = unquote(file_url)
            print(f"Найден архив: {file_url}")
            download_and_extract_zip(file_url, output_dir)
            
except Exception as e:
    print(f"Ошибка: {type(e).__name__} - {str(e)}")
