# 🧠 Solance AI: Student Mental Health Prediction System

## 📌 Overview

Solance AI is a machine learning-powered web application designed to predict the mental health status of university students based on academic, demographic, and psychological factors.

The system leverages supervised learning techniques along with explainable AI (XAI) to provide not only predictions but also meaningful insights into contributing factors.

---

## 🎯 Key Features

* 🔍 Predicts likelihood of depression (Binary Classification)
* 📊 Provides confidence score using probability estimates
* 🧠 Explainable AI insights using Permutation Importance
* 📈 Interactive and modern Streamlit dashboard
* 🕘 Tracks prediction history (session-based)
* 🎨 Premium UI with glassmorphism and circular progress visualization

---

## 📂 Dataset

**Student Mental Health Dataset**
Source: https://www.kaggle.com/datasets/shariful07/student-mental-health

### Dataset Details:

* ~101 samples
* 11 features including:

  * Gender
  * Age
  * Course
  * Year of Study
  * CGPA
  * Marital Status
  * Anxiety
  * Panic Attacks
  * Treatment History

---

## ⚙️ Machine Learning Pipeline

### 🔹 Preprocessing

* Removed irrelevant columns (Timestamp)
* Handled missing values
* Label Encoding for categorical variables
* Feature Scaling using StandardScaler

### 🔹 Models Used

* Logistic Regression
* Decision Tree
* Random Forest
* Support Vector Machine (SVM)
* XGBoost

### 🏆 Best Model

**Support Vector Machine (SVM)**

* Achieved highest accuracy (~90%)
* Handles non-linear relationships effectively using RBF kernel

---

## 🧠 Explainable AI (XAI)

### Method Used:

**Permutation Importance**

### Why not SHAP?

* SVM (RBF kernel) is not inherently interpretable
* Permutation Importance is model-agnostic and efficient

### Key Findings:

1. Specialist Treatment → Strongest indicator
2. Marital Status → Emotional stability factor
3. Course → Academic stress relevance
4. Other factors → Gender, CGPA, Anxiety, Panic
5. Least important → Age

---

## 🖥️ Application Interface

### Input Features:

* Gender
* Age
* Course
* Year of Study
* CGPA
* Marital Status
* Anxiety
* Panic Attack
* Treatment History

### Output:

* Prediction (Depressed / Low Risk)
* Confidence Score (Circular Visualization)
* Top Contributing Factors with explanations

---

## 🚀 Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/your-username/solance-ai.git
cd solance-ai
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Application

```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
solance-ai/
│
├── app.py                      # Streamlit frontend + ML inference
├── requirements.txt           # Dependencies
├── model.pkl                  # Trained SVM model
├── scaler.pkl                 # StandardScaler
├── encoders.pkl               # Label encoders
├── columns.pkl                # Feature order
│
├── notebooks/
│   └── Student_Mental_Health_XAI.ipynb
│
├── assets/                    # (optional - screenshots, UI images)
│
└── README.md
```

---

## 📊 Results Summary

* SVM achieved best performance among all models
* Model successfully captures academic + psychological patterns
* Explainability enhances trust and interpretability

---

## 🔮 Future Scope

* Integration with real-time counseling systems
* Deployment on cloud (Streamlit Cloud / Render)
* Use of SHAP/LIME for deeper explainability
* Larger dataset for improved generalization
* Mobile application interface

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork the repository and submit a pull request.

---

## 📜 License

This project is for academic and research purposes.

---

## 👨‍💻 Author

**Aviral Gupta**
B.Tech CSE
Manipal University Jaipur

---

## ⭐ Acknowledgements

* Kaggle dataset contributors
* Open-source ML libraries (Scikit-learn, XGBoost)
* Streamlit for UI framework

---
