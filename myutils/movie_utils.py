import pandas as pd
import re  # 정규 표현식 사용을 위한 임포트 모듈 


def create_movie_mark_down(file_name, df, title, _logger, df_rank):
    ## 마크다운 파일 생성 정의
    group_size = 5
    mark_down_desc = '''#영화 #movie #한국 #문화 #K-컬처 #롯데시네마 #CGV #MEGABOX #주말 #여가시간 #휴식 #힐링 #나들이  
    #leeda'''

    df['감독'] = df['감독'].fillna('').astype(str)
    df['출연자'] = df['출연자'].fillna('').astype(str)

    with open(file_name, "w", encoding="utf-8") as f:

        f.write(f"\n\n# 제목\n\n")
        f.write(f" - {title}\n\n")

        f.write(f"\n\n## 유튜브 설명\n\n")
        f.write(f" - {mark_down_desc}\n\n")

        f.write(f"\n\n## 제목 - 랜덤10개 \n\n")

        for i in range(0, len(df_rank), 10):
            rank_chunk = df_rank['title'].iloc[i:i + 10]
            f.write(" > " + " <br>".join(rank_chunk.tolist()))

        f.write(f"\n\n## 영화제목\n\n")

        for i in range(0, len(df), group_size):
            title_chunk = df['title'].iloc[i:i + group_size]
            f.write(f"\n### {i + 1}~{i + 1 + len(title_chunk) - 1} 위\n")
            f.write(" > " + " <br>".join(title_chunk.tolist()))

        f.write(f"\n\n## 감독명\n\n")

        for i in range(0, len(df), group_size):
            title_chunk = df['감독'].iloc[i:i + group_size]
            f.write(f"\n### {i + 1}~{i + 1 + len(title_chunk) - 1} 위\n")
            f.write(" > " + " <br>".join(title_chunk.tolist()))

        f.write(f"\n\n## markdown_설명줄\n\n")

        for i in range(0, len(df), group_size):
            title_chunk = df['markdown_설명줄'].iloc[i:i + group_size]
            f.write(f"\n### {i + 1}~{i + 1 + len(title_chunk) - 1}\n")
            f.write(" > " + " <br>".join(title_chunk.tolist()))

        f.write(f"\n## 영화 목록\n")

        for i, x in df.sort_values(by='new_rank', ascending=False).iterrows():
            try:
                view_desc = '관람자수:'
                f.write(f"\n - {x['markdown_제목']} | {x['감독']} | {x['개봉일']} | {x['장르_시간']} | {x['등급']} | {view_desc} {x['관람자수_int']} | {x['url']} |")

                summary = x['SUMMARY']
                summary = summary.replace('더보기', '_')
                f.write(f"\n```\n{summary}\n```\n\n")
            except Exception as e:
                _logger.error(e)
                print("create_movie_mark_down", e)
            finally:
                # f.write(f"| {x['book_url']}\n")
                pass

        yt_iframe = '''
      ```html
    <iframe width="360" height="640" src="https://www.youtube.com/embed/YouTube ID" title="YouTube video player"  frameborder="0"  
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen> 
    </iframe>
      ``` '''

        f.write(f"\n\n## Youtube iframe \n\n")
        f.write(f" > https://www.youtube.com/shorts/YouTube ID\n\n")
        f.write(f"{yt_iframe}\n\n")
