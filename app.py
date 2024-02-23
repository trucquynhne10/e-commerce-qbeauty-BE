from flask import Flask, render_template, request, redirect, send_from_directory, send_file
import pandas as pd
from Preprocessing import text_preprocess
import joblib
from flask import jsonify
import sqlite3

mj = joblib.load('D:\Đồ án học máy\Web\BE\pipeline_model')

app = Flask(__name__)

def db_connection():
    conn = None
    try: 
        conn = sqlite3.connect("cmt.sqlite")
    except sqlite3.Error as e:
        print(e)
    return conn

@app.route("/predict", methods=["GET", "POST"])
def predict_comment():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == "GET":
        cursor = conn.execute("SELECT * FROM cmt")
        predictedCmt = [
            dict(id=row[0], cmt=row[1], predict=row[2])
            for row in cursor.fetchall()
        ]
        if predictedCmt is not None:
            return jsonify(predictedCmt)
        
    if request.method == "POST":
        corpus = request.json.get('cmt')
        processed = text_preprocess(corpus)
        pre = mj.predict([processed])
        dense_array = pre.toarray()
        label_names = ['vận chuyển', 'giá', 'đóng gói', 'dịch vụ', 'mùi hương', 'kết cấu', 'độ bền', 'Màu sắc']
        df = pd.DataFrame(columns=label_names, data=dense_array)
        labels = df.columns[df.eq(1).any()].tolist()
        labels_str = ', '.join(labels)
        sql = """INSERT INTO cmt(cmt, predict) VALUES (?, ?)"""
        cursor.execute(sql, (corpus, labels_str))
        conn.commit()
        return "Successfull"

@app.route("/filter/<tag>", methods = ["GET"])
def filterTag(tag):
    conn = db_connection()
    cursor = conn.cursor()
    sql = """SELECT * FROM cmt where predict LIKE ?"""
    cursor.execute(sql, ('%'+tag+'%',))
    rows = cursor.fetchall()
    cmts = []
    for r in rows:
        cmts.append(r)
    if cmts is not None:
        return jsonify(cmts), 200
    else:
        return "Something wrong", 404

if __name__ == '__main__':
    app.run(debug=True)