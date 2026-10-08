import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime

# -----------------------------
# File Path
# -----------------------------
DATA_PATH = Path("data/predictions.csv")

# -----------------------------
# Create CSV if not exists
# -----------------------------
def create_csv():
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

    if not DATA_PATH.exists():
        df = pd.DataFrame(columns=[
            "date",
            "student_name",
            "marks",
            "accuracy",
            "time_taken",
            "attempts",
            "difficulty_level",
            "topic_coverage",
            "consistency_score",
            "predicted_skill"
        ])
        df.to_csv(DATA_PATH, index=False)

# -----------------------------
# Simple Rule Based Predictor
# -----------------------------
def predict_skill(marks, accuracy, time_taken, attempts, difficulty_level, topic_coverage, consistency_score):
    score = 0

    if marks >= 80:
        score += 3
    elif marks >= 60:
        score += 2
    else:
        score += 1

    if accuracy >= 80:
        score += 3
    elif accuracy >= 60:
        score += 2
    else:
        score += 1

    if topic_coverage >= 80:
        score += 2
    elif topic_coverage >= 50:
        score += 1

    if consistency_score >= 80:
        score += 2
    elif consistency_score >= 50:
        score += 1

    if time_taken <= 30:
        score += 1

    if attempts <= 2:
        score += 1

    if difficulty_level == "Hard":
        score += 2
    elif difficulty_level == "Medium":
        score += 1

    if score >= 12:
        return "Advanced"
    elif score >= 8:
        return "Intermediate"
    else:
        return "Beginner"

# -----------------------------
# Save Prediction
# -----------------------------
def save_prediction(row):
    df = pd.read_csv(DATA_PATH)
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df.to_csv(DATA_PATH, index=False)

# -----------------------------
# Streamlit App
# -----------------------------
st.set_page_config(
    page_title="AI Skill Predictor",
    page_icon="🤖",
    layout="centered"
)

create_csv()

st.title("🤖 AI Skill Predictor")
st.write("Student performance ke basis par skill level predict karein.")

st.sidebar.title("Menu")
page = st.sidebar.radio("Select Page", ["Predict Skill", "Prediction History"])

if page == "Predict Skill":
    st.subheader("Student Details")

    student_name = st.text_input("Student Name")

    marks = st.number_input("Marks", min_value=0, max_value=100, value=70)
    accuracy = st.number_input("Accuracy (%)", min_value=0, max_value=100, value=75)
    time_taken = st.number_input("Time Taken (minutes)", min_value=1, max_value=300, value=30)
    attempts = st.number_input("Attempts", min_value=1, max_value=20, value=2)

    difficulty_level = st.selectbox("Difficulty Level", ["Easy", "Medium", "Hard"])

    topic_coverage = st.number_input("Topic Coverage (%)", min_value=0, max_value=100, value=70)
    consistency_score = st.number_input("Consistency Score (%)", min_value=0, max_value=100, value=70)

    if st.button("Predict"):
        if student_name.strip() == "":
            st.warning("Please student name enter karein.")
        else:
            prediction = predict_skill(
                marks,
                accuracy,
                time_taken,
                attempts,
                difficulty_level,
                topic_coverage,
                consistency_score
            )

            st.success(f"{student_name} ka predicted skill level: {prediction}")

            row = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "student_name": student_name,
                "marks": marks,
                "accuracy": accuracy,
                "time_taken": time_taken,
                "attempts": attempts,
                "difficulty_level": difficulty_level,
                "topic_coverage": topic_coverage,
                "consistency_score": consistency_score,
                "predicted_skill": prediction
            }

            save_prediction(row)
            st.info("Prediction CSV file me save ho gayi.")

elif page == "Prediction History":
    st.subheader("Prediction History")

    df = pd.read_csv(DATA_PATH)

    if df.empty:
        st.warning("Abhi koi prediction saved nahi hai.")
    else:
        st.dataframe(df, use_container_width=True)

        st.subheader("Skill Level Count")
        skill_count = df["predicted_skill"].value_counts()
        st.bar_chart(skill_count)

        csv_data = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name="predictions.csv",
            mime="text/csv"
        )
