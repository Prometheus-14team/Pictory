import os
import unicodedata
import datetime
import scipy
import torch
import numpy as np
from PIL import Image
import base64
from io import BytesIO

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from db_models import Diary, db
from models import ControlNet, AudioLDM, LLM, FastText, stemmer, get_mapped_words

#인공지능 모델
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
llm = LLM(device=device)
fasttext = FastText()
controlnet = ControlNet(device=device)
audioldm = AudioLDM(device=device)

# Flask API
app = Flask(__name__, static_folder="../calendar-web/build")
CORS(app)

# 정적 파일 서빙 설정 (이미지 폴더 지정)
DRAWINGS_DIR = os.path.join(app.static_folder, "static", "tag")


# 화면
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react_app(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")

"""
# 스케치 보내기
@app.route("/GET/sketch/<date>", methods=["GET"])
def get_sketch(date):
    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    diary = Diary.query.filter_by(date=date).first()
    if diary:
        return send_from_directory(diary.sketch)
    else:
        return send_from_directory("data/sketches/white.png")
"""

# 그림일기의 채색된 그림 보내기
@app.route("/GET/image/<date>", methods=["GET"])
def get_image(date):
    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    diary = Diary.query.filter_by(date=date).first()
    if diary:
        return jsonify({"image": diary.image})
    else:
        return jsonify({"message": "Invalid Data"})


# 그림일기의 배경음악 보내기
@app.route("/GET/audio/<date>", methods=["GET"])
def get_audio(date):
    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    diary = Diary.query.filter_by(date=date).first()
    if diary:
        return jsonify({"audio": diary.audio})
    else:
        return jsonify({"message": "Invalid Data"})


# 그림일기 finalpost에 내용 보내기
@app.route("/GET/text/<date>", methods=["GET"])
def get_text(date):
    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    diary = Diary.query.filter_by(date=date).first()
    if diary:
        return jsonify({"raw_text": diary.raw_text, "summarized_text_kr": diary.summarized_text_kr})
    else:
        return jsonify({"raw_text": "", "summarized_text_kr": ""})


# 날짜별 감정 보내기
@app.route("/GET/expression/<date>", methods=["GET"])
def get_expression(date):
    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    diary = Diary.query.filter_by(date=date).first()
    if diary:
        return jsonify({"expression": diary.expression})
    else:
        return jsonify({"message": "Invalid Data"})


# 날짜별 날씨 보내기
@app.route("/GET/weather/<date>", methods=["GET"])
def get_weather(date):
    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    diary = Diary.query.filter_by(date=date).first()
    if diary:
        return jsonify({"weather": diary.weather})
    else:
        return jsonify({"message": "Invalid Data"})


@app.route("/data/drawings/<noun>/<filename>")
def get_drawing(noun, filename):
    try:
        return send_from_directory(os.path.join(DRAWINGS_DIR, noun), filename)
    except FileNotFoundError:
        return {"error": "파일을 찾을 수 없습니다."}, 404
    

# 그림일기 드로잉 요소 보내기
@app.route("/GET/tag/<date>", methods=["GET"])
def get_drawing_tag(date):
    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    diary = Diary.query.filter_by(date=date).first()
    if diary:
        diary_objects = stemmer(diary.raw_text)
        mapped_objects = get_mapped_words(diary_objects)
        similar_objects = fasttext.get_similar_words(diary_objects)

        if len(mapped_objects) >= 12:
            objects = mapped_objects[:12]
        else:
            objects = set(mapped_objects)
            for obj in similar_objects:
                if len(objects) < 12:
                    objects.add(obj)
                else:
                    objects = list(objects)
                    break
        pngs = [[f"/static/tag/{obj}/{i:02}.png" for i in range(80)] for obj in objects]
        tag = [[obj, *png]for obj, png in zip(objects, pngs)] 
        return jsonify({"tag": tag})
    else:
        print(f"No diary found for {date}") 
        return jsonify({"tag": []})


# 그림일기 모든 요소 보내기
@app.route("/GET/all", methods=["GET"])
def get_all():
    diaries = Diary.query.all()
    if not diaries:  
        return jsonify({"message": "No data found"}), 404
        
    print(sorted([diary.to_dict() for diary in diaries], key=lambda x: x["date"]))
    return jsonify({"all": sorted([diary.to_dict() for diary in diaries], key=lambda x: x["date"])})


# 유저가 만든 canvas이미지 보내기
@app.route("/POST/image/<date>", methods=["POST"])
def post_image(date):
        
    data = request.get_json()  
    image_data = data["image"]  # Base64로 인코딩된 이미지 데이터
    
    # Base64 데이터에서 'data:image/png;base64,' 부분을 제거하고 디코딩
    image_data = image_data.split(",")[1]  # 'data:image/png;base64,' 부분 제거
    sketch = Image.open(BytesIO(base64.b64decode(image_data)))  # Base64 디코딩하여 이미지로 변환
    
    sketch_arr = np.array(sketch)
    mask = (sketch_arr[:,:,-1] == 0)
    sketch_arr[mask] = 255
    sketch = Image.fromarray(sketch_arr).convert("RGB")

    sketch_path = os.path.join("/static/sketches", f"{date}.png")
    sketch.save(f"{app.static_folder}{sketch_path}")

    image_path = os.path.join("/static/images", f"{date}.png")
    image = controlnet.generate(sketch)
    image.save(f"{app.static_folder}{image_path}")

    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    diary = Diary.query.filter_by(date=date).first()
    diary.sketch = sketch_path
    diary.image = image_path
    db.session.commit()
    
    return jsonify({"message": "success"})


@app.route("/POST/audio/<date>", methods=["POST"])
def post_audio(date):
    datetime_date = datetime.datetime.strptime(date, "%Y-%m-%d")
    diary = Diary.query.filter_by(date=datetime_date).first()
    audio = audioldm.generate(diary.summarized_text_en)

    audio_path = os.path.join("/static/audios", f"{date}.wav")
    scipy.io.wavfile.write(f"{app.static_folder}{audio_path}", rate=16000, data=audio)
    
    diary.audio = audio_path
    db.session.commit()
    return jsonify({"message": "success"})


@app.route("/POST/text/<date>", methods=["POST"])
def post_text(date):
    data = request.get_json()
    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    raw_text = data.get("raw_text")
    expression = data.get("expression")
    weather = data.get("weather")

    diary = Diary.query.filter_by(date=date).first()
    if diary:
        if diary.raw_text != raw_text:
            summarized_text_kr = llm.summarize(raw_text)
            summarized_text_en = llm.translate(summarized_text_kr)
            
            diary.raw_text = raw_text
            diary.summarized_text_kr = summarized_text_kr
            diary.summarized_text_en = summarized_text_en
            diary.expression = expression
            diary.weather = weather
    else:
        summarized_text_kr = llm.summarize(raw_text)
        summarized_text_en = llm.translate(summarized_text_kr)
        
        diary = Diary(
            date=date, 
            raw_text=raw_text, 
            summarized_text_kr=summarized_text_kr,
            summarized_text_en=summarized_text_en,
            expression=expression,
            weather=weather
        )
        db.session.add(diary)
    db.session.commit()
    return jsonify({"message": "success"})


@app.route("/POST/expression/<date>", methods=["POST"])
def post_expression(date):
    data = request.get_json()
    expression = data.get("expression")

    diary = Diary.query.filter_by(date=date).first()
    diary.expression = expression
    db.session.commit()
    return jsonify({"message": "success"})


@app.route("/POST/weather/<date>", methods=["POST"])
def post_weather(date):
    data = request.get_json()
    weather = data.get("weather")

    diary = Diary.query.filter_by(date=date).first()
    diary.weather = weather
    db.session.commit()
    return jsonify({"message": "success"})


# 그림일기 드로잉 검색
@app.route("/POST/tag/search", methods=["POST"])
def search_tag():
    data = request.get_json()
    text = data.get("text")

    text_objects = stemmer(text)
    mapped_objects = get_mapped_words(text_objects)
    similar_objects = fasttext.get_similar_words(text_objects)
    print(mapped_objects)

    if len(mapped_objects) >= 12:
        objects = mapped_objects[:12]
    else:
        objects = set(mapped_objects)
        for obj in similar_objects:
            if len(objects) < 12:
                objects.add(obj)
            else:
                objects = list(objects)
                break
    print(objects)
    pngs = [[f"/static/tag/{obj}/{i:02}.png" for i in range(80)] for obj in objects]
    tag = [[obj, *png] for obj, png in zip(objects, pngs)]
    print(tag[0])
    return jsonify({"tag": tag})


# 데이터베이스
basdir = os.path.abspath(os.path.dirname(__file__))
dbfile = os.path.join(basdir, "db.sqlite")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + dbfile
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "pictory"

db.init_app(app)
db.app = app
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)