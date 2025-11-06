import os
from flask import Flask, request, jsonify
import pandas as pd

from database import Base, engine, SessionLocal
from models import UploadedFile  # noqa: F401
from utils import clean_data, analyze_data  # noqa: F401

app = Flask(__name__)
Base.metadata.create_all(bind=engine)


@app.route("/")
def home():
    return "API работает!"


@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "Файл не найден"}), 400

    filename = file.filename
    filepath = os.path.join("uploads", filename)
    os.makedirs("uploads", exist_ok=True)
    file.save(filepath)

    db = SessionLocal()
    uploaded_file = UploadedFile(filename=filename, filepath=filepath)
    db.add(uploaded_file)
    db.commit()
    db.refresh(uploaded_file)
    db.close()

    return jsonify(
        {"message": "Файл загружен", "file_id": uploaded_file.id}
    )


@app.route("/data/clean", methods=["GET"])
def clean_endpoint():
    df = pd.read_csv("uploads/sample.csv")
    cleaned_df = clean_data(df)
    cleaned_df.to_csv("uploads/cleaned_sample.csv", index=False)

    return jsonify({"message": "Данные очищены"})


@app.route("/data/stats", methods=["GET"])
def stats_endpoint():
    df = pd.read_csv("uploads/sample.csv")
    stats = analyze_data(df)

    return jsonify(stats)


if __name__ == "__main__":
    app.run(debug=True)
