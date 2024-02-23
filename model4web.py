import pandas as pd
from Preprocessing import text_preprocess
import joblib

mj = joblib.load('pipeline_model')

def predict_cmt (corpus):
    processed = text_preprocess(corpus)
    pre = mj.predict([processed])
    dense_array = pre.toarray()
    label_names = ['vận chuyển', 'giá', 'đóng gói', 'dịch vụ', 'mùi hương', 'kết cấu', 'độ bền', 'Màu sắc']
    df = pd.DataFrame(columns=label_names, data = dense_array)
    labels = df.columns[df.eq(1).any()]
    return labels 
