import streamlit as st
import pandas as pd
import datetime
import os
import barcode
from barcode.writer import ImageWriter
from PIL import Image
import io
import uuid

# 定数
DB_FILE = os.path.join(os.path.expanduser("~"), "Desktop", "responses.csv")

# セッション状態初期化
for key in ["started", "submitted", "uuid"]:
    if key not in st.session_state:
        st.session_state[key] = False if key != "uuid" else uuid.uuid4().hex[:16].upper()

# バーコード生成関数
def generate_barcode(code: str) -> Image.Image:
    CODE128 = barcode.get_barcode_class('code128')
    barcode_obj = CODE128(code, writer=ImageWriter())
    buffer = io.BytesIO()
    barcode_obj.write(buffer)
    buffer.seek(0)
    return Image.open(buffer)

#同意画面
def show_consent():
    st.header("【研究参加に関するご案内とご同意のお願い】")
    st.write("この事前アンケートは、『眼底写真による疾患スクリーニングに関する研究』を目的として実施しております。ご記入いただいた情報は、研究目的のみに使用し個人が特定されることはありません。また、眼底写真の情報を研究機関に提供する可能性があります。ご協力は任意であり、同意をいただけない場合でも不利益は一切ありません。ご同意いただける場合は、下記の「同意して記入を始める」ボタンを押してください。")
    if st.button("同意して記入を始める"):
        st.session_state.started = True
        st.rerun()

# 送信後バーコード表示
def show_barcode():
    unique_id = st.session_state.uuid
    st.success("ご回答ありがとうございました！")
    st.write(f"このバーコード（ID: {unique_id}）をカメラに読み取らせてください：")
    st.image(generate_barcode(unique_id))

# メインUI（アンケート部分）
def show_survey():
    st.subheader("事前アンケート")

# user_ID
    # ランダムなID（数字＋英字でもOK）
    unique_id = st.session_state.uuid  # 例: A1B2C3D4E5

    # Code128でバーコード生成
    CODE_TYPE = barcode.get_barcode_class('code128')
    barcode_obj = CODE_TYPE(unique_id, writer=ImageWriter())

    # メモリ上に保存
    buffer = io.BytesIO()
    barcode_obj.write(buffer)
    buffer.seek(0)


#   age
    age = st.slider("年齢を選択してください", 0,100,40)
    gender = st.radio("性別", ["男性", "女性", "その他"])
    height_dict = {
        "140cm未満": 135,
        "140-144cm": 142,
        "145-149cm": 147,
        "150-154cm": 152,
        "155-159cm": 157,
        "160-164cm": 162,
        "165-169cm": 167,
        "170-174cm": 172,
        "175-179cm": 177,
        "180-184cm": 182,
        "185-189cm": 187,
        "190-194cm": 192,
        "195-199cm": 197,
        "200cm以上": 205
    }
    height = st.select_slider("身長", options = height_dict)
    weight_dict = {
        "40kg未満": 35,
        "40-44kg": 42,
        "45-49kg": 47,
        "50-54kg": 52,
        "55-59kg": 57,
        "60-64kg": 62,
        "65-69kg": 67,
        "70-74kg": 72,
        "75-79kg": 77,
        "80-84kg": 82,
        "85-89kg": 87,
        "90-94kg": 92,
        "95-99kg": 97,
        "100-104kg": 102,
        "105-105kg": 107,
        "110-105kg": 112,
        "115-105kg": 117,
        "120kg以上": 130
    }
    weight = st.select_slider("体重", options = weight_dict)
    health = st.selectbox("今日の健康状態をどう感じますか？", ["とても良い", "良い", "普通", "悪い", "とても悪い"])
    history = st.multiselect("今までにかかったことのある病気（複数選択可）",
    ["高血圧", "糖尿病", "心疾患", "脳卒中", "がん", "緑内障", "脂質異常", "その他"],
    max_selections=5,
    accept_new_options=True,
    key = "self_history")
    history_other = st.text_input("その他を選択された方はよろしければご記入ください。")
    st.write("ご家族の既往歴について教えてください（わからなければわからないでOKです）")
    family_history_fgf = st.multiselect("父方の祖父",
    ["高血圧", "糖尿病", "心疾患", "脳卒中", "がん", "緑内障", "脂質異常", "わからない"],
    max_selections = 5,
    accept_new_options = False,
    key = "fgf_history")
    family_history_fgm = st.multiselect("父方の祖母",
    ["高血圧", "糖尿病", "心疾患", "脳卒中", "がん", "緑内障", "脂質異常", "わからない"],
    max_selections = 5,
    accept_new_options = False,
    key = "fgm_history")
    family_history_mgf = st.multiselect("母方の祖父",
    ["高血圧", "糖尿病", "心疾患", "脳卒中", "がん", "緑内障", "脂質異常", "わからない"],
    max_selections = 5,
    accept_new_options = False,
    key = "mgf_history")
    family_history_mgm = st.multiselect("母方の祖母",
    ["高血圧", "糖尿病", "心疾患", "脳卒中", "がん", "緑内障", "脂質異常", "わからない"],
    max_selections = 5,
    accept_new_options = False,
    key = "mgm_history")
    family_history_f = st.multiselect("父親",
    ["高血圧", "糖尿病", "心疾患", "脳卒中", "がん", "緑内障", "脂質異常", "わからない"],
    max_selections = 5,
    accept_new_options = False,
    key = "father_history")
    family_history_m = st.multiselect("母親",
    ["高血圧", "糖尿病", "心疾患", "脳卒中", "がん", "緑内障", "脂質異常", "わからない"],
    max_selections = 5,
    accept_new_options = False,
    key = "mother_history")
    smoking = st.selectbox("喫煙習慣",["いいえ", "はい（紙巻き）", "はい（加熱式）", "過去に喫煙していた"])
    # 合数ベースで定義（後で純アルコールgに換算も可能）
    alcohol_amount_dict = {
    "飲まない": 0,
    "1合未満": 0.5,
    "1〜2合": 1.5,
    "2〜3合": 2.5,
    "3〜4合": 3.5,
    "4〜5合": 4.5,
    "5合以上": 5.5,
    }
    # 頻度ベース（週あたり）
    alcohol_freq_dict = {
    "飲まない": 0,
    "月に1〜3回": 0.5,   # 週換算で0.5回
    "週に1〜2回": 1.5,
    "週に3〜4回": 3.5,
    "ほぼ毎日": 6.5,
    }
    freq = st.selectbox("飲酒の頻度", list(alcohol_freq_dict.keys()))
    amount = st.selectbox("1回あたりの飲酒量", list(alcohol_amount_dict.keys()))

    # 数値に変換
    freq_val = alcohol_freq_dict[freq]
    amount_val = alcohol_amount_dict[amount]

    # 週あたり飲酒量（合）*20g(純アルコール)
    pure_alcohol_weekly_total = freq_val * amount_val * 20

    # 睡眠時間の選択肢と対応する数値
    sleep_options = ["4時間未満", "4〜5時間","5〜6時間", "6〜7時間", "7〜8時間", "8〜9時間", "9〜10時間", "10時間以上"]
    sleep_dict = {
    "4時間未満": 3.5,
    "4〜5時間": 4.5,
    "5〜6時間": 5.5,
    "6〜7時間": 6.5,
    "7〜8時間": 7.5,
    "8〜9時間": 8.5,
    "9〜10時間": 9.5,
    "10時間以上": 10.5
    }
    sleep_hours = st.select_slider("平日の平均睡眠時間は？", options=sleep_options)
    numeric_sleep = sleep_dict[sleep_hours]

    # 睡眠の質
    sleep_quality = st.radio("睡眠の質について、どう感じていますか？", ["とても良い", "まあまあ", "あまり良くない", "悪い"])
    sleep_quality_score = {"とても良い": 4, "まあまあ": 3, "あまり良くない": 2, "悪い": 1}[sleep_quality]

    # 運動頻度
    exercise_freq_options = ["0日", "1〜2日", "2〜3日", "3〜4日", "4〜5日", "5日以上"]
    exercise_freq_dict = {
        "0日": 0,
        "1〜2日": 1.5,
        "2〜3日": 2.5,
        "3〜4日": 3.5,
        "4〜5日": 4.5,
        "5日以上": 5
    }
    exercise_freq = st.select_slider("1週間のうち運動する日数は？", options=exercise_freq_options)
    numeric_exercise_days = exercise_freq_dict[exercise_freq]

    # 運動強度
    exercise_intensity = st.radio("普段の運動の強度は？", ["軽い（ウォーキング程度）", "中程度（軽いジョギング）", "強め（ランニングや筋トレなど）"])
    exercise_intensity_score = {
        "軽い（ウォーキング程度）": 1,
        "中程度（軽いジョギング）": 2,
        "強め（ランニングや筋トレなど）": 3
    }[exercise_intensity]

# データベース保存 or JSON化して送るなどもこの形なら簡単です
    if not st.session_state.submitted:
        if st.button("送信して撮影に進む"):
            new_data = pd.DataFrame([{
                "uuid" : unique_id,
                "timestamp": datetime.datetime.now().isoformat(),
                "age": age,
                "gender": gender,
                "height": height,
                "weight": weight,
                "health": health,
                "medical_history": history,
                "other_disease": history_other,
                "fgf_history": family_history_fgf,
                "fgm_history": family_history_fgm,
                "mgf_history": family_history_mgf,
                "mgm_history": family_history_mgm,
                "f_history": family_history_f,
                "m_history": family_history_m,
                "smoking": smoking,
                "weekly_alcohol_intake": pure_alcohol_weekly_total,
                "sleep_hours": numeric_sleep,
                "sleep_quality": sleep_quality_score,
                "weekly_exercise_days": numeric_exercise_days,
                "exercise_intensity": exercise_intensity_score
            }])

            try:
                existing = pd.read_csv(DB_FILE)
                df = pd.concat([existing, new_data], ignore_index=True)
            except FileNotFoundError:
                df = new_data

            df.to_csv(DB_FILE, index=False)
            st.session_state.submitted = True
            st.rerun()

# アプリ起動ロジック
if not st.session_state.started:
    show_consent()
elif not st.session_state.submitted:
    show_survey()
else:
    show_barcode()
