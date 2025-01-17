from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Diary(db.Model):
    __tablename__ = "diary"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, unique=False, nullable=False)
    raw_text = db.Column(db.String(2048), unique=False, nullable=True)
    summarized_text = db.Column(db.String(512), unique=False, nullable=True)
    sketch = db.Column(db.String(512), unique=False, nullable=True)
    image = db.Column(db.String(512), unique=False, nullable=True)
    audio = db.Column(db.String(512), unique=False, nullable=True)

    def to_dict(self):
        return {"id": self.id, "date": self.date, "raw_text": self.raw_text, "summarized_text": self.summarized_text,
                "sketch": self.sketch, "image": self.image, "audio": self.audio}