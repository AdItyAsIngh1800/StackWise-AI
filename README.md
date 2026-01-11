# **Referee: Decision Comparison Tool (Week 6 Project)**

  

**Author:**  Aditya Singh

**Project Type:**  Rule-based decision support tool

**Tech Stack:**  Python, Streamlit, Pandas

----------

## **📌 Overview**

  

**Referee**  is a decision-support web application that helps users  **compare multiple technical options side-by-side**  instead of giving a single generic recommendation.

  

Users:

-   Select two or more options (e.g., ECS vs EKS vs Lambda)
    
-   Define  **hard requirements**  (e.g., “Need Kubernetes”)
    
-   Assign  **weights**  to decision criteria (cost, scalability, portability, etc.)
    

  

The tool then:

-   Filters out invalid options
    
-   Calculates weighted scores
    
-   Displays comparisons in tables
    
-   Explains  _why_  one option wins over others
    

  

This project demonstrates  **structured decision-making**, not AI guessing.

----------

## **🎯 Problem Statement**

  

When choosing between technical options, users often face:

-   Conflicting trade-offs
    
-   One-size-fits-all recommendations
    
-   No explanation of  _why_  one choice is better
    

  

Most tools give  **answers**, not  **decisions**.

----------

## **✅ Solution**

  

Referee acts as a  **neutral referee**:

-   Applies **hard constraints**
    
-   Uses **weighted scoring**
    
-   Clearly explains  **trade-offs**
    

  

The result is a transparent, user-controlled decision process.

----------

## **🧠 How It Works**

  

### **1. Option Catalog**

  

Each option (ECS, EKS, Lambda) is defined in a JSON catalog with:

-   Description
    
-   Strengths & weaknesses
    
-   Scores (1–10) for key criteria
    
-   Hard constraints (e.g., Kubernetes requirement)
    

  

### **2. Hard Constraints Check**

  

If a user requires Kubernetes:

-   Options that do not support Kubernetes are automatically rejected
    

  

### **3. Weighted Scoring**

  

Each criterion is multiplied by its user-defined weight.

  

**Example:**

```
Total Score = Σ (criterion score × weight) / total weights
```

### **4. Trade-off Explanation**

  

The tool explains the winner in simple English based on:

-   The user’s most important criteria
    
-   Score differences
    

----------

## **🧪 Example Use Case**

-   Compare **ECS vs EKS**
    
-   Set  **portability**  weight very high →  **EKS wins**
    
-   Set  **ops simplicity**  weight very high →  **ECS wins**
    
-   Enable “Need Kubernetes” →  **Only EKS remains valid**
    

  

This “flip” proves the tool supports real decision-making.

----------

## **🖥️ Tech Stack**

-   **Streamlit**  – Web UI
    
-   **Pandas**  – Tables & structured output
    
-   **Python**  – Core logic
    
-   **JSON**  – Knowledge catalog
    

  

❌ No databases

❌ No ML models

❌ No cloud SDKs

----------

## **📁 Project Structure**

```
referee-tool/
├── .kiro/
│   └── README.md
├── catalog/
│   └── options.json
├── evaluator/
│   ├── constraints.py
│   ├── scoring.py
│   └── explain.py
├── tests/
│   └── test_scoring.py
├── app.py
├── requirements.txt
└── README.md
```

----------

## **⚙️ Installation**

  

### **1. Clone the repository**

```
git clone <your-github-repo-url>
cd referee-tool
```

### **2. Install dependencies**

```
pip install -r requirements.txt
```

----------

## **▶️ Run the Application**

```
streamlit run app.py
```

The browser will open automatically.

----------

## **🧪 Run Tests (Optional)**

```
python -m pytest
```

Tests verify that score rankings flip correctly when weights change.

----------

## **📸 Screenshots & Demo**

  

Screenshots included in the repository:

-   Input form
    
-   Comparison results
    
-   Score flip based on weight changes
    

  

(Used for blog and project submission proof.)

----------

## **🚀 Future Improvements**

-   Add more comparison domains (databases, networking, APIs)
    
-   Export results as PDF
    
-   Persist user scenarios
    
-   Add radar charts for visual comparison
    

----------

## **👤 Author**

  

**Aditya Singh**

Week-6 Referee Project

Built as part of a structured decision-making exercise.