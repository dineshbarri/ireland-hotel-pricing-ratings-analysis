
#  Ireland Hotels Data Analysis  

<div align="center">

![POWERBI](https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=Power%2520BI&logoColor=white)
![MICROSOFT SQL SERVER](https://img.shields.io/badge/Microsoft_SQL_Server-CC2927?style=for-the-badge&logo=microsoft-sql-server&logoColor=white)
![PYTHON](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

</div>

This end-to-end data analytics project focuses on analyzing **hotels in Ireland** using real-world data scraped from *Booking.com*.  
The project covers the full lifecycle of a modern data analytics workflow:

✔ Data Collection through Web Scraping  
✔ Data Cleaning & Preprocessing using Python  
✔ Exploratory Data Analysis using SQL (SSMS)  
✔ Visual Analytics with Power BI  
✔ Final Insights & Business Value Summary  

---

## 📌 Project Overview

Understanding hotel pricing, ratings, availability, and review patterns is crucial for tourism insights and hospitality decision-making.  
This project analyzes hotels across major Irish cities to uncover trends in:

- Hotel pricing for weekend stays  
- Rating distributions  
- Review behavior vs. hotel scores  
- Room availability  
- Free cancellation impact  
- City-wise pricing & rating patterns  

The analysis provides actionable insights useful for:

- Tourism boards  
- Hospitality businesses  
- Travelers  
- Market researchers  

---


## 📁 **Repository Structure**
```text
Ireland-Hotels-Data-Analysis/
│
├── data/
│   ├── raw/
│   │   └── hotels.csv                 # Original scraped data
│   └── processed/
│       └── hotels_cleaned.csv          # Cleaned dataset
│
├── notebooks/
│   └── ireland-hotels.ipynb           # Data cleaning & preprocessing
│
├── sql/
│   └── Hotels_Ireland.sql             # All SQL queries for analysis
│
├── powerbi/
│   └── Ireland_Hotels_Dashboard.pbix  # Power BI dashboard file
│
├── docs/
│   └── README.md                      # Project documentation
│
└── requirements.txt                   # Python dependencies
```


---

## 🏨 1. Data Collection (Web Scraping)

### ✔ Source  
Data was collected from **Booking.com**, focusing on:

- Hotels located in **Ireland**  
- **One-night weekend stay**  
- Extracted using **Instant Data Scraper (Chrome Extension)**  

### ✔ Fields Extracted (Raw Data)
The scraper collected attributes including:

- Hotel Name  
- City  
- Price per Night  
- Score / Rating  
- Number of Reviews  
- Review Category  
- Free Cancellation (Yes/No)  
- Rooms Left  
- Description Snippets  
- Link to Hotel Page  

The scraped dataset was stored as: **hotels_raw.csv**

---


---

# 🧹 2. Data Cleaning using Python

Cleaning and preprocessing were performed in the Jupyter notebook:


### ✔ Key Cleaning Steps:

- Removed duplicates  
- Cleaned price formatting (`€`, commas, text)  
- Standardized rating and review count fields  
- Extracted numeric values from text fields  
- Cleaned boolean fields (e.g., Free Cancellation)  
- Filled or removed missing values  
- City extraction from hotel location text  
- Exported final cleaned dataset  

#### ✔ Final Cleaned Output:  **hotels_cleaned.csv**


---

# 🗄️ 3. SQL Analysis (SSMS)

The cleaned dataset was imported into SQL Server Management Studio (SSMS).

All SQL queries, CTEs, and table creation scripts are included in:


### 🔍 **Key Business Questions Solved (Using SQL + CTEs)**

---

### **1️⃣ Top Rated Hotels**
Identify the highest-scoring hotels across Ireland.

### **2️⃣ Average Rating by City**
Which cities have the best overall hotel ratings?

### **3️⃣ Top 5 Hotels by Rating & Review Count**
Ranking hotels using a combined metric:

- High rating  
- High review count  

### **4️⃣ Hotels Offering Free Cancellation with High Scores**
Helps identify flexible, yet top-performing stays.

### **5️⃣ Price Range Analysis by City**
Understand pricing patterns across major cities.

### **6️⃣ Room Availability by City**
Which cities have higher average rooms left?

### **7️⃣ Review Rate Distribution**
Distribution of hotels across review categories.

### **8️⃣ Impact of Review Count on Rating**
A correlation study using SQL aggregations.

---

# 📊 4. Power BI Dashboard

The cleaned dataset was imported into Power BI to develop a dynamic hotel insights dashboard.

### **Dashboard Features**

✔ **City-wise hotel distribution**  
✔ **Top-rated hotels visualized**  
✔ **Price range visuals (boxplots, bar charts)**  
✔ **Scatter plot for Review Count vs Score (correlation)**  
✔ **Map visual of hotels across Ireland**  
✔ **Filters & Slicers** for:  
- City  
- Price  
- Review category  
- Free cancellation  



---

# 📈 5. Insights & Findings

### **🏆 Top Cities by Rating**
Some Irish cities consistently show higher average hotel scores.

### **💶 Price Trends**
Hotels in cities like Dublin show higher weekend pricing.

### **🛏️ Room Availability**
Certain tourist-heavy locations show low room availability.

### **✔ Free Cancellation Impact**
Hotels offering flexible cancellation often maintain higher ratings.

### **⭐ Review Count vs Rating**
A moderate relationship observed — hotels with high review counts often maintain stable score averages.

---

# 🧩 6. Tools & Technologies Used

| Category | Technology |
|---------|-------------|
| **Web Scraping** | Instant Data Scraper |
| **Data Cleaning** | Python, Pandas, NumPy |
| **Database** | SQL Server (SSMS) |
| **Querying** | SQL, CTEs, Aggregations |
| **Visualization** | Microsoft Power BI |
| **Project Management** | GitHub |

---

# 🚀 7. How to Use This Repo

### **1. Clone the repository**
```bash
git clone https://github.com/dineshbarri/Ireland-Hotel-Pricing-Ratings-Analysis-Python-SQL-Power-BI.git
cd Ireland-Hotel-Pricing-Ratings-Analysis-Python-SQL-Power-BI
```








