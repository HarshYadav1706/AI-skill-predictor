# AI Skill Predictor

Ye ek simple **Streamlit + Pandas** project hai.

Is project me student ke marks, accuracy, time taken, attempts, difficulty level, topic coverage aur consistency score ke basis par skill level predict hota hai.

## Folder Structure

```text
AI-Skill-Predictor/
│
├── app.py
│
├── data/
│   └── predictions.csv
│
├── requirements.txt
│
└── README.md
```

## Features

- Student skill prediction
- Beginner / Intermediate / Advanced output
- Prediction CSV file me save hoti hai
- Prediction history table
- Bar chart
- CSV download option

## Install

```bash
pip install -r requirements.txt
```

## Run Project

```bash
streamlit run app.py
```

## Input Columns

- Student Name
- Marks
- Accuracy
- Time Taken
- Attempts
- Difficulty Level
- Topic Coverage
- Consistency Score

## Output

- Predicted Skill Level:
  - Beginner
  - Intermediate
  - Advanced
