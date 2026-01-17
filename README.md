# 🏔️ AI-Based Rockfall Risk Prediction System  
### Smart India Hackathon (SIH) – Mining Safety Innovation Project

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![LightGBM](https://img.shields.io/badge/LightGBM-ML-green)](https://lightgbm.readthedocs.io)
[![Flask](https://img.shields.io/badge/Flask-Web_App-orange)](https://flask.palletsprojects.com)
[![Status](https://img.shields.io/badge/Status-Production_Ready-brightgreen)](#)
[![License](https://img.shields.io/badge/License-SIH_2024-red)](LICENSE)

**An AI-driven rockfall risk prediction and monitoring system for open-pit and underground mines, combining machine learning, multisource geospatial data, and explainable risk insights to enhance mining safety.**

---

## 🌟 Project Overview

Rockfall incidents pose a serious threat to worker safety, equipment, and productivity in mining operations. This project delivers a **data-driven, scalable, and interpretable solution** for predicting rockfall risk using **machine learning** and **multisource environmental data**.

At its core, the system uses a **LightGBM multiclass classification model** to categorize rockfall risk into **LOW, MEDIUM, and HIGH** levels. The model is trained on a rich feature set derived from terrain, seismic activity, rainfall patterns, geotechnical sensors, drone-based surface analysis, and temporal factors. The final model was selected after evaluating multiple ML and DL models using **macro F1-score, cross-validation, and statistical testing**.

---

## 🤖 AI / ML Pipeline (Latest)

- **Final Model**: LightGBM (best macro F1-score)
- **Classes**: LOW / MEDIUM / HIGH risk
- **Preprocessing**:
  - Missing value handling  
  - StandardScaler normalization  
  - Statistical feature selection (ANOVA F-test)  
  - Recursive Feature Elimination with CV (RFECV)
- **Class Imbalance Handling**: SMOTE (applied only on training data)
- **Evaluation Metrics**: Accuracy, Precision, Recall, Macro F1, ROC-AUC
- **Model Selection Validation**: Friedman statistical test

The trained **LightGBM model**, **scaler**, and **selected feature list** are saved and reused during inference to ensure consistent and reliable predictions.

---

## 📊 Data Sources & Features

The system integrates **50+ engineered features**, including:

- **Terrain & Geospatial**: elevation, slope, aspect, latitude, longitude  
- **Seismic Indicators**: magnitude, depth, vibration, RMS, error metrics  
- **Rainfall**: monthly, seasonal, and annual precipitation  
- **Geotechnical Sensors**: displacement, strain, pore pressure  
- **Drone-Derived Indicators**: crack density, debris texture, vegetation ratio  
- **Remote Sensing (SAR-ready)**: displacement velocity, coherence, deformation rate  
- **Temporal Factors**: season, month, year  

---

## 🧠 Prediction & Interpretability

During inference, the system:
- Uses **LightGBM `predict_proba()`** for probabilistic risk scoring
- Outputs:
  - Risk level (LOW / MEDIUM / HIGH)
  - Risk probability score
  - Confidence value
  - Key contributing factors
  - Timestamp
- Supports **Explainable AI (XAI)** extensions (SHAP-ready) for feature-level interpretation

A **fallback geological risk logic** is included to ensure graceful degradation if the trained model is unavailable.





---

## 📈 Impact & Use Cases

- Early warning system for **rockfall-prone zones**
- Decision support for **mine safety officers**
- Risk-aware **operational planning**
- Research platform for **AI in mining safety**

---

## 📂 Dataset

Dataset used for training and evaluation:  
**https://drive.google.com/drive/folders/1rpohGmnZ4MsZd-Gxtwc3yrewVzRVGI87**

---

## 🏆 Smart India Hackathon 2024

This project was developed as part of **Smart India Hackathon 2024**, focusing on **AI-driven mining safety solutions** with emphasis on reliability, interpretability, and real-world deployment readiness.

---

## 📄 License

Developed under **Smart India Hackathon (SIH) 2024** guidelines for academic and innovation purposes.

---

**Built for safer mines using Machine Learning and Explainable AI**

## 📁 Project Structure
SIH_PROJECT/
│
├── README.md                         # Project overview and setup guide
├── LICENSE                           # Project license (SIH 2024)
├── .gitignore                        # Git ignored files
│
├── output/                           # Saved ML artifacts
│   ├── best_rockfall_model.joblib    # Trained LightGBM model
│   ├── scaler.joblib                 # Feature scaler
│   └── selected_features.pkl        # Final selected feature list
│
├── scripts/                          # Data analysis & model development
│   │
│   ├── notebooks/                   # Jupyter notebooks (EDA, experiments)
│   │   ├── eda_analysis.ipynb
│   │   ├── feature_selection.ipynb
│   │   └── model_comparison.ipynb
│   │
│   ├── datasets/                    # Training & evaluation datasets
│   │   └── dataset_balanced_risk_final.csv
│   │
│   └── model_training.py            # End-to-end ML training pipeline
│
├── web_app/                          # Flask web application
│   │
│   ├── app_with_auth.py             # Main Flask app with authentication
│   ├── prediction_service.py        # Rockfall prediction logic
│   ├── risk_explainer.py            # Explainable AI (XAI) module
│   ├── alert_service.py             # Risk alert handling
│   ├── data_service.py              # Mine & region data management
│   │
│   ├── templates/                   # HTML templates
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   └── results.html
│   │
│   ├── static/                      # Static assets
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   │
│   └── requirements.txt             # Web application dependencies
│
└── documentation/                   # Project documentation
    ├── FINAL_PROJECT_DOCUMENTATION.md
    ├── TECHNICAL_ARCHITECTURE.md
    ├── COMPREHENSIVE_USER_GUIDE.md
    └── PROJECT_OVERVIEW.md



