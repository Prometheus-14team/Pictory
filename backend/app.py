import numpy as np
from PIL import Image

from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)
diary_data = {}
image_data = {}
audio_data = {}


@app.route("/")
def calendar():
    return render_template("calendar.html")


@app.route("/diary/<date>")
def diary(date):
    content = diary_data.get(date, "")
    return render_template("diary.html", date=date, content=content)


@app.route("/diary/<date>/write", methods=["POST"])
def write_diary(date):
    content = request.form.get("content")
    diary_data[date] = content
    return redirect(url_for("calendar"))


@app.route("/diary/<date>/delete", methods=["POST"])
def delete_diary(date):
    if date in diary_data:
        del diary_data[date]
    return redirect(url_for("calendar"))


@app.route("/diary/<date>/create", methods=["GET", "POST"])
def create(date):
    image = image_data.get(date, "")
    audio = audio_data.get(date, "")
    image_url = url_for('static', filename=f'images/{date}_image.png')
    print(image_url)
    return render_template("create.html", date=date, image=image)


@app.route("/diary/<date>/create/image", methods=["POST"])
def create_image(date):
    color = np.random.randint(0,3)
    image = np.zeros((512,512,3), dtype=np.uint8)
    image[:,:,color] = 255
    image = Image.fromarray(image)
    image_data[date] = f"/static/images/{date}_image.png"
    image.save(f"./static/images/{date}_image.png")
    return redirect(url_for("create", date=date))


@app.route("/diary/<date>/create/audio", methods=["POST"])
def create_audio(date):
    content = diary_data.get(date)
    return redirect(url_for("create", date=date))


if __name__ == '__main__':
    app.run()
