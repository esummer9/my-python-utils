import json
import os

from slugify import slugify
import csv

import logging
import time
import random
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

from zoneinfo import ZoneInfo
import unicodedata, re, webbrowser
from bs4 import BeautifulSoup


def create_mark_down(file_name, df, title, _logger):
    ## 마크다운 파일 생성 정의
    group_size = 5
    mark_down_desc = '''#인터넷 #서점 #종이책 #ebook #도서 #독서 #중고 #신간도서
#자기계발 #에세이 #인문학 #한국소설 #경제경영 #만화 #여행 #건강 #취미 #저자랭킹 #랭킹
#알라딘 #교보문고 #예스24 #leeda'''

    yt_iframe = '''
  ```html
<iframe width="360" height="640" src="https://www.youtube.com/embed/YouTube ID" title="YouTube video player"  frameborder="0"  
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen> 
</iframe>
  ``` '''

    df['출판일'] = df['출판일'].fillna('').astype(str)
    df['출판사'] = df['출판사'].fillna('').astype(str)
    df['출판사_출판일'] = df['출판사'].str.cat(df['출판일'].str[:4], sep=' ')

    df['작가명_출판사'] = df['작가명'] + ' | ' + df['출판사']

    with open(file_name, "w", encoding="utf-8") as f:

        f.write(f"\n\n# 제목\n\n")
        f.write(f" - {title}\n\n")

        f.write(f" > https://www.youtube.com/shorts/YouTube ID\n\n")
        f.write(f"{yt_iframe}\n\n")

        f.write(f"\n\n## 유튜브 설명\n\n")
        f.write(f" - {mark_down_desc}\n\n")

        for i in range(0, len(df), group_size):
            title_chunk = df['markdown_제목'].iloc[i:i+group_size]
            f.write(f"\n### {i+1}~{i+1+len(title_chunk)-1} 위:\n")
            f.write(" > "+ " <br>".join(title_chunk.tolist()))

        f.write(f"\n\n## 작가명\n\n")

        for i in range(0, len(df), group_size):
            title_chunk = df['작가명'].iloc[i:i+group_size]
            f.write(f"\n### {i+1}~{i+1+len(title_chunk)-1} 위\n")
            f.write(" > " + " <br>".join(title_chunk.tolist()))

        f.write(f"\n\n## 출판사_출판일\n\n")

        for i in range(0, len(df), group_size):
            title_chunk = df['출판사_출판일'].iloc[i:i+group_size]
            f.write(f"\n### {i+1}~{i+1+len(title_chunk)-1} 위\n")
            f.write(" > " + " <br>".join(title_chunk.tolist()))

        f.write(f"\n\n## 작가명_출판사\n\n")

        for i in range(0, len(df), group_size):
            title_chunk = df['작가명_출판사'].iloc[i:i+group_size]
            f.write(f"\n### {i+1}~{i+1+len(title_chunk)-1} 위\n")
            f.write(" > " + " <br>".join(title_chunk.tolist()))

        f.write(f"\n## 도서 목록\n")
        f.write(f"\n|순번| 제목 | 부제 | 출판사 | 출판일 | 판매가 | 포인트 | 연결 | 편집장 |")
        f.write(f"\n|-|-|-|-|-|-|-|-|-|")

        for i, x in df.iterrows():
            editors = '-'
            try:
                if x['편집장의 선택']:
                    editors = f"[{i+1:03d} - {x['title']}](#{i+1:03d})"
            except Exception as e:
                _logger.error( e)

            try :
                f.write(f"\n|{i+1:03d} | {x['markdown_제목']} | {x['부제']} | {x['출판사']} | {x['출판일']} | {x['판매가']} | {x['sales_point']} | {editors} |")
            except Exception as e:
                _logger.error( e)
            finally:
                # f.write(f"| {x['book_url']}\n")
                pass


