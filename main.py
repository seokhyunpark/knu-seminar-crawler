import json
import time

from crawler import fetch_body_text
from gemini import generate_response
from seminar_database import SeminarDatabase

db = SeminarDatabase("config.json")

for i in range(350, 0, -1):
    try:
        url = f"https://cse.knu.ac.kr/bbs/board.php?bo_table=sub5_4&wr_id={i}"
        data = generate_response(fetch_body_text(url))
        if data is not None:
            data = data.replace("```", "").strip()
            data = data.strip('json').strip()
            data = data.strip('[').strip(']').strip()
            data = data.replace('""', "''")
            data = json.loads(data)

            title: str = data['title']
            postDate: str = data['postDate']
            startTime: str = data['startTime']
            endTime: str = data['endTime']
            days: list = data['day']
            place: str = data['place']
            category_texts: list = data['categoryText']
            tag_texts: list = data['tagText']

            print("제목: ", title)
            print("작성일: ", postDate)
            print("시작 시간: ", startTime)
            print("종료 시간: ", endTime)
            print("요일: ", days)
            print("장소: ", place)
            print("카테고리: ", category_texts)
            print("태그: ", tag_texts)
            print()

            db.start_transaction()
            columns = ['postID', 'url', 'title', 'postDate', 'startTime', 'endTime', 'day', 'place']
            for day in days:
                values = [i, url, title, postDate, startTime, endTime, day, place]
                db.insert('Post', columns, values)
            for category_text in category_texts:
                columns = ['postID', 'categoryText']
                values = [i, category_text]
                db.insert('Category', columns, values)
            for tag_text in tag_texts:
                columns = ['postID', 'tagText']
                values = [i, tag_text]
                db.insert('Tag', columns, values)
            db.commit_transaction()

        time.sleep(3)
    except:
        pass
db.disconnect()
