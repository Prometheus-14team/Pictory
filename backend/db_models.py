from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Diary(db.Model):
    __tablename__ = "diary"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, unique=False, nullable=False)
    raw_text = db.Column(db.String(2048), unique=False, nullable=True)
    summarized_text_kr = db.Column(db.String(512), unique=False, nullable=True)
    summarized_text_en = db.Column(db.String(512), unique=False, nullable=True)
    sketch = db.Column(db.String(512), unique=False, nullable=True)
    image = db.Column(db.String(512), unique=False, nullable=True)
    audio = db.Column(db.String(512), unique=False, nullable=True)
    expression = db.Column(db.String(32), unique=False, nullable=True)
    weather = db.Column(db.String(32), unique=False, nullable=True)

    def to_dict(self):
        return {"id": self.id, "date": self.date, "raw_text": self.raw_text, "summarized_text_kr": self.summarized_text_kr, "summarized_text_en": self.summarized_text_en,
                "sketch": self.sketch, "image": self.image, "audio": self.audio, "expression": self.expression, "weather": self.weather}