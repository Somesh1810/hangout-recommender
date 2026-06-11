# 🍽️ Hangout Place Recommendation System — Bangalore

A data-driven recommendation engine to help users find the perfect hangout spot in Bangalore based on occasion, budget, cuisine, and location preferences.

## 📊 Dataset
- **Source:** Zomato Bangalore Restaurants (Kaggle)
- **Records:** ~51,000 restaurants across 93 Bangalore localities

## 🔧 Tech Stack
- Python (Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn)
- SQL (SQLite)
- Jupyter Notebook

## 📁 Project Structure
```
hangout-recommender/
├── data/
│   ├── zomato.csv           # Raw dataset
│   └── zomato_clean.csv     # Cleaned & engineered dataset
├── notebooks/
│   └── zomato_project.ipynb # Main project notebook
├── requirements.txt
└── README.md
```

## 🚀 Project Phases
| Phase | Description |
|-------|-------------|
| 1 | Data Cleaning & Preprocessing |
| 2 | Feature Engineering (budget buckets, occasion tags, ambience mapping) |
| 3 | Exploratory Data Analysis (9-panel EDA dashboard) |
| 4 | Content-Based Recommendation Engine (TF-IDF + Cosine Similarity) |
| 5 | SQL Filtering Layer (SQLite queries) |

## 💡 How the Recommender Works
The engine accepts user preferences:
- **Occasion** — Date Night, Friends Hangout, Family Outing, Night Out, Solo Meal
- **Budget** — Budget (≤₹300), Mid-Range (₹301–600), Premium (₹601–1000), Luxury (₹1000+)
- **Cuisine** — North Indian, Chinese, Italian, Continental, etc.
- **Location** — Any Bangalore area (Indiranagar, Koramangala, HSR, etc.)

It uses TF-IDF vectorization on combined restaurant features and ranks results using a hybrid score: **60% content similarity + 40% rating**.

## 📦 Installation
```bash
pip install -r requirements.txt
```

## ▶️ Run
Open `notebooks/zomato_project.ipynb` in Jupyter and run all cells.