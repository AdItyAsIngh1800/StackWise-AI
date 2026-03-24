
# **🚀 StackWise AI**

  

### **Explainable + ML-Powered Tech Stack Decision System**

```
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white"/>
  <img src="https://img.shields.io/badge/React-Frontend-61DAFB?logo=react&logoColor=black"/>
  <img src="https://img.shields.io/badge/TypeScript-UI-3178C6?logo=typescript&logoColor=white"/>
  <img src="https://img.shields.io/badge/PostgreSQL-Database-4169E1?logo=postgresql&logoColor=white"/>
  <img src="https://img.shields.io/badge/LightGBM-ML%20Ranking-orange"/>
  <img src="https://img.shields.io/badge/Semantic%20Search-Embeddings-purple"/>
  <img src="https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white"/>
  <img src="https://img.shields.io/badge/License-MIT-yellow"/>
  <img src="https://img.shields.io/badge/Status-Production--Ready-success"/>
</p>

```

----------

# **📌 Overview**

  

**StackWise AI**  is an  **intelligent, explainable decision-support system**  that helps developers choose the optimal tech stack for their projects.

  

Unlike typical recommendation tools, it combines:

-   rule-based reasoning
    
-   ML-based ranking (LightGBM LambdaRank)
    
-   semantic search (embeddings)
    
-   explainability + trade-off analysis
    

  

👉 Result: **transparent, data-driven stack decisions instead of guesswork**

----------

# **🔥 Key Highlights**

-   🧠 **ML-powered ranking (LightGBM LambdaRank)**
    
-   🔎 **Semantic search using embeddings**
    
-   📊 **Explainable recommendations**
    
-   🔁 **Feedback-driven learning loop**
    
-   📈 **Analytics dashboard (NDCG, trends)**
    
-   ⚖️ **Pareto trade-off optimization**
    
-   🐳 **Fully Dockerized system**
    

----------

# **🎯 Problem Statement**

  

Choosing a tech stack is often:

-   intuition-based
    
-   trend-driven
    
-   inconsistent across teams
    

  

This leads to:

-   scalability issues
    
-   unnecessary complexity
    
-   poor architectural decisions
    

  

👉 **StackWise AI converts stack selection into a structured, explainable, and learnable system.**

----------

# **🧠 Core Features**

  

## **🔹 ML-Based Recommendation Engine**

-   LightGBM ranking model
    
-   Learns from feedback
    
-   Optimized using  **NDCG**
    

  

## **🔹 Explainable Decisions**

-   confidence score
    
-   reasoning
    
-   alternatives
    
-   trade-offs
    

  

## **🔹 Constraint-Based Filtering**

-   scalability constraints
    
-   operational complexity
    
-   team expertise
    

  

## **🔹 Semantic Search**

```
"fast backend for scalable systems"
```

Returns similar stacks using embeddings.

  

## **🔹 Sensitivity Analysis**

  

Evaluates decision stability under changing conditions.

  

## **🔹 Pareto Frontier**

  

Identifies optimal trade-offs between:

-   performance
    
-   ecosystem
    
-   simplicity
    

  

## **🔹 Feedback Learning Loop**

-   feedback stored in PostgreSQL
    
-   dataset generation
    
-   model retraining
    

  

## **🔹 Analytics Dashboard**

-   recommendation trends
    
-   confidence metrics
    
-   ML evaluation (NDCG)
    

----------

# **🏗️ System Architecture**

```mermaid
flowchart TD

    A[User<br>React UI] --> B[FastAPI Backend]

    B --> C[Recommendation Engine]

    C --> C1[Rule-based Candidate Generation]
    C --> C2[ML Ranking (LightGBM)]
    C --> C3[Confidence Calculation]
    C --> C4[Sensitivity Analysis]
    C --> C5[Pareto Optimization]

    C --> D[Semantic Search<br>(Embeddings)]

    C --> E[Evidence Layer]
    E --> E1[Language Signals]
    E --> E2[Catalog Config]

    B --> F[(PostgreSQL<br>Feedback + Runs)]

    F --> G[Training Data Pipeline]
    G --> H[Model Training]
```
----------

# **📂 Project Structure**

```
stackwise-ai/
├── backend/         # FastAPI API layer
├── frontend/        # React + TypeScript UI
├── engine/          # Core logic + ML
│   ├── ml/          # Training + prediction
│   ├── confidence.py
│   └── ...
├── evidence/        # Dataset signals
├── database/        # PostgreSQL operations
├── pipelines/       # Data + ML pipelines
├── data/            # Processed datasets
├── tests/           # API tests
├── docker-compose.yml
```

----------

# **🖼️ Screenshots**

  


### **🏠 Home Page**

  

![Home](./screenshots/home.png)

  

### **📊 Results Page**

![Results](./screenshots/results.png)

  

### **📈 Analytics Dashboard**

![Analytics](./screenshots/analytics.png)
----------

# **⚙️ Tech Stack**

  

## **Backend**

-   FastAPI
    
-   Pydantic
    
-   Uvicorn
    

  

## **Frontend**

-   React
    
-   TypeScript
    
-   Vite
    
-   Tailwind CSS
    
-   Recharts
    

  

## **ML & Data**

-   LightGBM (ranking)
    
-   Pandas
    
-   Polars
    
-   DuckDB
    
-   Sentence Transformers
    

  

## **Database**

-   PostgreSQL
    

----------

# **🚀 Getting Started**

  

## **1️⃣ Clone**

```
git clone https://github.com/your-username/StackWise-AI.git
cd StackWise-AI
```

----------

## **2️⃣ Run with Docker (Recommended)**

```
docker compose up --build
```

### **Access**

-   Frontend → http://localhost:5173
    
-   Backend → http://localhost:8000/docs
    

----------

## **3️⃣ Local Setup (Optional)**

  

### **Backend**

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

### **Database**

```
CREATE DATABASE stackwise_ai;
psql -d stackwise_ai -f database/schema.sql
```

### **Frontend**

```
cd frontend
npm install
npm run dev
```

----------

# **🔌 API Endpoints**

**Endpoint**

**Description**

/recommend

Stack recommendation

/recommend/natural-language

NL-based recommendation

/semantic-search

Embedding-based search

/analytics/*

Metrics & trends

/ml/evaluation

Model performance

----------

# **🧪 Example Request**

```
{
  "project_type": "api",
  "team_languages": ["python"],
  "low_ops": true,
  "expected_scale": "medium"
}
```

----------

# **📤 Example Output**

```
{
  "winner": {
    "language": "python",
    "backend_framework": "fastapi",
    "database": "postgresql",
    "deployment": "render",
    "score": 0.83
  },
  "confidence": 0.81,
  "ranking_source": "ml_model"
}
```

----------

# **📊 ML Evaluation**

```
GET /ml/evaluation
```

```
{
  "ndcg": 0.82,
  "num_samples": 906,
  "num_features": 16
}
```

----------

# **📉 Limitations**

-   synthetic feedback data
    
-   limited stack catalog
    
-   basic embedding model
    

----------

# **🚀 Future Improvements**

-   real user feedback loop
    
-   advanced embeddings
    
-   hybrid ranking (rules + ML)
    
-   cloud deployment
    
-   authentication + saved stacks
    

----------

# **👨‍💻 Author**

  

**Aditya Singh**

----------

# **📜 License**

  

MIT License

----------

# **⭐ Final Note**

  

This project demonstrates:

-   ML system design (ranking + evaluation)
    
-   full-stack engineering
    
-   containerized architecture
    
-   explainable AI principles
    

---------- 
