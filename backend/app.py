import os
import datetime
import scipy
import torch
import numpy as np
from PIL import Image

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from db_models import Diary, db
from models import ControlNet, AudioLDM, LLM, FastText, stemmer, get_mapped_words


# Flask API
app = Flask(__name__, static_folder="../frontend/build")
CORS(app)

# 화면
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react_app(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")


# 스케치 보내기
@app.route("/GET/sketch/<date>", methods=["GET"])
def get_sketch(date):
    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    diary = Diary.query.filter_by(date=date).first()
    if diary:
        return send_from_directory(diary.sketch)
    else:
        return send_from_directory("data/sketches/white.png")


# 그림일기의 그림 보내기
@app.route("/GET/image/<date>", methods=["GET"])
def get_image(date):
    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    diary = Diary.query.filter_by(date=date).first()
    if diary:
        return send_from_directory(diary.image)
    else:
        return jsonify({"message": "Invalid Data"})


# 그림일기의 배경음악 보내기
@app.route("/GET/audio/<date>", methods=["GET"])
def get_audio(date):
    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    diary = Diary.query.filter_by(date=date).first()
    if diary:
        return send_from_directory(diary.audio)
    else:
        return jsonify({"message": "Invalid Data"})


# 그림일기 내용 보내기
@app.route("/GET/text/<date>", methods=["GET"])
def get_text(date):
    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    diary = Diary.query.filter_by(date=date).first()
    if diary:
        return jsonify({"raw_text": diary.raw_text, "summarized_text": diary.summarized_text})
    else:
        return jsonify({"raw_text": "", "summarized_text": ""})


# 그림일기 드로잉 요소 보내기
@app.route("/GET/drawing/<data>", methods=["GET"])
def get_drawing(date):
    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    diary = Diary.query.filter_by(date=date).first()
    if diary:
        diary_objects = stemmer(diary.raw_text)
        mapped_objects = get_mapped_words(diary_objects)
        mapped_objects += fasttext.get_similar_words(mapped_objects)
        mapped_pngs = list(map(lambda x: f"./data/{x}.png"))
        return jsonify({"drawing": list(zip(mapped_objects, mapped_pngs))})
    else:
        return jsonify({"drawing": []})


# 그림일기 모든 요소 보내기
@app.route("/GET/all", methods=["GET"])
def get_all():
    diaries = Diary.query.all()
    return jsonify({"all": sorted([diary.to_dict() for diary in diaries], key=lambda x: x["date"])})


@app.route("/POST/image/<date>", methods=["POST"])
def post_image(date):
    sketch = request.files["file"]
    image = controlnet.generate(sketch)

    sketch_path = os.path.join("data/sketches", f"{date}.png")
    image_path = os.path.join("data/images", f"{date}.png")
    sketch.save(sketch_path)
    image.save(image_path)

    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    diary = Diary.query.filter_by(date=date).first()
    diary.sketch = sketch_path
    diary.image = image_path
    db.session.commit()
    return jsonify({"message": "success"})


@app.route("/POST/audio/<date>", methods=["POST"])
def post_audio(date):
    diary = Diary.query.filter_by(date=date).first()
    audio = audioldm.generate(diary.summarized_text_en)

    audio_path = os.path.join("data/audios", f"{date}.wav")
    scipy.io.wavfile.write(audio_path, rate=16000, data=audio)
    
    diary = Diary.query.filter_by(date=date).first()
    diary.audio = audio_path
    db.session.commit()
    return jsonify({"message": "success"})


@app.route("/POST/text/<date>", methods=["POST"])
def post_text(date):
    data = request.get_json()
    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    raw_text = data.get("raw_text")

    diary = Diary.query.filter_by(date=date).first()
    if diary:
        if diary.raw_text != raw_text:
            summarized_text_kr = llm.summarize(raw_text)
            summarized_text_en = llm.translate(summarized_text_kr)
            
            diary.raw_text = raw_text
            diary.summarized_text_kr = summarized_text_kr
            diary.summarized_text_en = summarized_text_en
    else:
        summarized_text_kr = llm.summarize(raw_text)
        summarized_text_en = llm.translate(summarized_text_kr)
        
        diary = Diary(
            date=date, 
            raw_text=raw_text, 
            summarized_text_kr=summarized_text_kr,
            summarized_text_en=summarized_text_en
        )
        db.session.add(diary)
    db.session.commit()
    return jsonify({"message": "success"})

"""
# 그림일기 드로잉 검색
@app.route("/GET/drawing/search", methods=["GET", "POST"])
def get_drawing(date):
    data = request.get_json()
    tag = data.get("tag")

    mapped_objects = fasttext.get_similar_words([tag])
    mapped_pngs = list(map(lambda x: f"./data/{x}.png"))
    return jsonify({"drawing": list(zip(mapped_objects, mapped_pngs))})
"""

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

# 인공지능 모델
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
llm = LLM(device=device)
fasttext = FastText()
controlnet = ControlNet(device=device)
audioldm = AudioLDM(device=device)

if __name__ == '__main__':
    app.run(debug=True)