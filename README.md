# 📊 Quiz Analysis

This project generates a detailed Excel report with statistics from Moodle quizzes. It groups quizzes by name, calculates global averages, question-level accuracy and penalties, and produces charts to support educational analysis.

---

## 🚀 Features

- Groups quizzes by shared name
- Calculates:
  - Global average grade
  - Accuracy and penalty percentages per question
  - Average failure rate per quiz
- Generates an Excel report with:
  - A summary sheet with average failure rates and bar chart
  - A detailed sheet with per-question stats, filters, and formatting
- Uses a `.env` file for secure database configuration

---

## 📂 Project Structure
project/
├── main.py # Entry point
├── db.py # Database connection and query logic
├── excel.py # Excel generation logic
├── utils.py # Utility functions
├── .env # Environment variables (DB credentials, output path)
├── requirements.txt # Python dependencies
└── README.md # This file

---

## ⚙️ Requirements

- Python 3.7+
- MySQL or MariaDB
- Access to Moodle's database with the following views already defined:
  - `vw_target_quizzes`
  - `vw_question_stats`
  - `vw_quiz_stats`

---

## 📦 Installation

1. Clone the repository:

```
git clone https://github.com/Danimarqz/quiz-analysis.git
cd quiz-analysis
```

2. Create a `.env` file with your database settings:
DB_HOST=localhost
DB_NAME=db
DB_USER=user
DB_PASS=your_password
EXPORTS_DIR=/path/to/output/excel

3. Install the required Python packages:
```
pip install -r requirements.txt
```

## 🧪 Usage

Run the script with:
```
python main.py
```
The file informe_quizzes.xlsx will be saved in the directory specified by EXPORTS_DIR.

## 📈 Output
The generated Excel file contains:

Summary per Quiz: Average failure percentage per quiz, with a column chart.

Detail per Question: Per-question data including attempts, correct answers, penalties, and percentages — with filters and formatting applied.

## 🎓 Use Cases
Perfect for:

Teachers analyzing student performance across quiz versions

Coordinators identifying problematic questions

Institutions generating automated Moodle reports

## 📝 License
This project is licensed under the MIT License. You are free to use, modify, and distribute it.

🙌 Author
Daniel Márquez — @Danimarqz
