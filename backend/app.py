import os
import datetime
import scipy
import numpy as np
from PIL import Image

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from db_models import Diary, db

from models import ControlNet, Text2Audio, Summarizer, stemmer
from models import IMAGE_PROMPT, IMAGE_NEGATIVE_PROMPT, AUDIO_PROMPT, AUDIO_NEGATIVE_PROMPT


app = Flask(__name__, static_folder="../frontend/build")
CORS(app)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react_app(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")


@app.route("/GET/image/<date>", methods=["GET"])
def get_sketch(date):
    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    diary = Diary.query.filter_by(date=date).first()
    if diary:
        return send_from_directory(diary.sketch)
    else:
        return send_from_directory("data/sketches/white.png")


@app.route("/GET/image/<date>", methods=["GET"])
def get_image(date):
    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    diary = Diary.query.filter_by(date=date).first()
    if diary:
        return send_from_directory(diary.image)
    else:
        return jsonify({"message": "Invalid Data"})


@app.route("/GET/audio/<date>", methods=["GET"])
def get_audio(date):
    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    diary = Diary.query.filter_by(date=date).first()
    if diary:
        return send_from_directory(diary.audio)
    else:
        return jsonify({"message": "Invalid Data"})


@app.route("/GET/text/<date>", methods=["GET"])
def get_text(date):
    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    diary = Diary.query.filter_by(date=date).first()
    if diary:
        return jsonify({"raw_text": diary.raw_text, "summarized_text": diary.summarized_text})
    else:
        return jsonify({"raw_text": "", "summarized_text": ""})


@app.route("/GET/all", methods=["GET"])
def get_all():
    diaries = Diary.query.all()
    return jsonify({"all": sorted([diary.to_dict() for diary in diaries], key=lambda x: x["date"])})


@app.route("/POST/image/<date>", methods=["POST"])
def post_image(date):
    sketch = request.files["file"]
    image = Image.fromarray(np.zeros((512,512,3), dtype=np.uint8))

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
    audio = None
    audio_path = os.path.join("data/audios", f"{date}.wav")

    scipy.io.wavfile.write(audio_path, rate=16000, data=audio)

    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    diary = Diary.query.filter_by(date=date).first()
    diary.audio = audio_path
    db.session.commit()
    return jsonify({"message": "success"})


@app.route("/POST/text/<date>", methods=["POST"])
def post_text(date):
    data = request.get_json()
    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    raw_text = data.get("raw_text")
    summarized_text = summarize_model.summarize(raw_text)

    diary = Diary.query.filter_by(date=date).first()
    if diary:
        if diary.raw_text != raw_text:
            diary.raw_text = raw_text
            diary.summarized_text = summarized_text
    else:
        diary = Diary(date=date, raw_text=raw_text, summarized_text=summarized_text)
        db.session.add(diary)
    db.session.commit()
    return jsonify({"message": "success"})


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

summarize_model = Summarizer()

if __name__ == '__main__':
    app.run(debug=True)