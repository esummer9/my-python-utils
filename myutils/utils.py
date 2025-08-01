# myutils/utils.py
import os
import pandas as pd
import re  # 정규 표현식 사용을 위한 임포트 모듈
import requests
from bs4 import BeautifulSoup
import logging
import time
from datetime import datetime
from zoneinfo import ZoneInfo    
import random    

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile      

import unicodedata

from slugify import slugify


def my_function():
    print("This is a placeholder function in myutils/utils.py")


def my_function2():
    print("*" * 2, "This is a placeholder function in myutils/utils.py", "*" * 2)


def slugify_korean(text):
    # 파일명 slugify
    # 1. 문자열을 NFC 정규화
    text = unicodedata.normalize('NFC', text)

    # 2. 소문자로 변환
    text = text.lower()

    # 3. 특수 문자 제거 (한글, 영문, 숫자, 공백, 하이픈만 허용)
    text = re.sub(r'[^가-힣a-z0-9\s-]', '', text)

    # 4. 공백 및 하이픈을 하나의 하이픈으로 변환
    text = re.sub(r'[\s\-]+', '-', text)

    # 5. 앞뒤 하이픈 제거
    text = text.strip('-')

    return text


def check_and_create_directory(directory_path):
    # 다운로드 디렉토리 검사 및 생성
    if not os.path.exists(directory_path):
        # 디렉토리가 존재하지 않으면 생성
        os.makedirs(directory_path)
        print(f"디렉토리 '{directory_path}'를 생성했습니다.")
    else:
        pass


def download_image(seq=None, title=None, image_url=None, save_directory="images"):
    # 이미지 다운로드
    # 1. 저장 디렉토리 생성 (없으면)
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
        print(f"디렉토리 '{save_directory}'를 생성했습니다.")

    # 2. 파일 이름 및 확장자 추출
    # URL에서 마지막 부분(파일 이름)을 가져옵니다.
    # 예: https://example.com/path/to/image.jpg -> image.jpg

    file_name = image_url.split('/')[-1]

    if title :
        file_name = slugify_korean(title) + f"_{file_name}"

    # URL에 쿼리 파라미터가 있을 경우 제거 (예: image.jpg?v=123 -> image.jpg)
    if '?' in file_name:
        file_name = file_name.split('?')[0]

    # 파일 확장자 확인 (소문자로 변환)
    file_extension = os.path.splitext(file_name)[1].lower()

    # 지원하는 이미지 확장자인지 확인
    if file_extension not in ['.jpg', '.jpeg', '.png']:
        print(f"경고: 지원하지 않는 이미지 확장자 '{file_extension}' 입니다. URL: {image_url}")
        # 필요하다면 기본 확장자를 지정하거나, 다운로드를 건너뛸 수 있습니다.
        # 이 예시에서는 일단 다운로드를 시도합니다.
        # file_name = file_name + ".jpg" # 또는 .png 등으로 강제 지정 가능

    save_path = os.path.join(save_directory, f'{seq}-{file_name}')

    try:
        # 3. HTTP GET 요청 보내기
        # stream=True를 사용하여 큰 파일을 효율적으로 처리합니다.
        response = requests.get(image_url, stream=True)
        response.raise_for_status()  # HTTP 오류가 발생하면 예외 발생

        # 4. 이미지 데이터 저장
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192): # 8KB씩 읽어서 쓰기
                f.write(chunk)

        # print(f"'{file_name}' 다운로드 완료!")
        return save_path

    except requests.exceptions.RequestException as e:
        print(f"이미지 다운로드 중 오류 발생: {image_url} - {e}")
        return None
    except Exception as e:
        print(f"파일 저장 중 알 수 없는 오류 발생: {e}")
        return None


def parse_korean_number(s):
    if pd.isna(s):
        return None

    # 공백 제거 및 쉼표 제거
    s = s.strip().replace(',', '')

    # 숫자 추출 + 단위 확인
    match = re.match(r'([0-9.]+)([^\d]*)', s)
    if not match:
        return None

    num_str, unit = match.groups()
    try:
        num = float(num_str)
    except:
        return None

    # 단위에 따라 변환
    if '천만' in unit:
        return int(num * 10_000_000)
    elif '억' in unit:
        return int(num * 100_000_000)
    elif '만' in unit:
        return int(num * 10_000)
    elif '천' in unit:
        return int(num * 1_000)
    else:
        return int(num)


def parse_number_korean(s):
    if pd.isna(s):
        return None

    # 공백 제거 및 쉼표 제거
    s = f"{s}"
    # 숫자 추출 + 단위 확인
    match = re.match(r'([0-9.]+)([^\d]*)', s)
    if not match:
        return None

    num_str, unit = match.groups()
    try:
        num = float(num_str)
    except:
        return None

    # 단위에 따라 변환
    if num > 100_000_000:
        return f"{int(num / 100_000_000)} 억+"
    elif num > 10_000_000:
        return f"{int(num / 10_000_000)} 천만+"
    elif num > 1_000_000:
        return f"{int(num / 1_000_000)} 백만+"
    elif num > 100_000:
        return f"{int(num / 100_000)} 십만+"
    elif num > 10_000:
        return f"{int(num / 10_000)} 만+"
    else:
        return f"{int(num)}"


def clean_and_convert(_df, _column, count, is_sort):
    # _df['new_rank'] = pd.to_numeric(_df[_column].str.replace(',', ''), errors='coerce')
    _df['new_rank'] = _df[_column]

    # 2. Filter for records where the conversion was successful (not NaN)
    numeric_records = _df.dropna(subset=['new_rank'])

    # 3. Randomly select 13 records
    random_13_records = numeric_records.sample(n=count, random_state=42) # random_state for reproducibility

    # 4. Sort the selected records by 'column_a_numeric' in descending order
    if is_sort:
        return random_13_records.sort_values(by='new_rank', ascending=False)
    else:
        return random_13_records
