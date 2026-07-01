# Zomato_Order_Pattern_Analysis
Zomato Order Pattern Analysis | Python, Pandas, Matplotlib Analysed 5,000+ restaurant orders to identify peak ordering hours (7–10 PM = 38% of orders), cuisine demand trends, and delivery time vs rating correlation (r = −0.62). Built multi-panel dashboards using Matplotlib.


# Zomato Order Pattern Analysis

> Analysed restaurant and order data to identify peak ordering hours, cuisine demand trends, and correlation between delivery time and customer ratings — with actionable business recommendations.

---

## Project Overview

This project performs end-to-end exploratory data analysis (EDA) on Zomato food delivery data using **Python**, **Pandas**, and **Matplotlib**.

The analysis covers:
-  Peak ordering hours & day-wise demand patterns
-  Cuisine popularity and revenue contribution
-  Impact of delivery time on customer ratings
-  Monthly revenue trends
-  Business recommendations for menu optimisation & delivery planning

---

##  Project Structure

```
zomato_analysis/
│
├── generate_data.py       # Generates synthetic dataset (5000 orders)
├── analysis.py            # Full EDA + chart generation
├── zomato_orders.csv      # Dataset used for analysis
├── dashboard.png          # Main 6-panel visual dashboard
├── insights.png           # Business insights deep-dive charts
└── README.md              # Project documentation
```

---

##  Tech Stack

| Tool | Purpose |
|---|---|
| Python 3 | Core programming language |
| Pandas | Data manipulation & aggregation |
| Matplotlib | Data visualisation & charts |
| NumPy | Numerical computations |

---

##  Installation & Setup

### 1. Clone or download the project folder

### 2. Install dependencies
```bash
pip install pandas matplotlib numpy
```

### 3. Run the scripts
```bash
# Generate the dataset
python generate_data.py

# Run analysis and generate charts
python analysis.py
```

---

##  Dataset Description

File: `zomato_orders.csv` — **5,000 rows**, **11 columns**

| Column | Description |
|---|---|
| `order_id` | Unique order identifier |
| `date` | Order date (2024) |
| `day_of_week` | Mon to Sun |
| `hour` | Hour of order (0–23) |
| `restaurant` | Restaurant name |
| `cuisine` | Cuisine type |
| `order_value` | Order amount in ₹ |
| `delivery_time` | Delivery duration in minutes |
| `rating` | Customer rating (1.0–5.0) |
| `discount_pct` | Discount applied (0%, 10%, 20%, 30%) |
| `month` | Month name |

---

##  Key Findings

### 1. Peak Ordering Hours
- **Dinner slot (7–10 PM)** accounts for **38% of all orders**
- **Lunch slot (12–2 PM)** is the second busiest at **28%**
- Saturday and Sunday evenings show the highest combined demand surge

### 2. Cuisine Demand
- **Biryani, North Indian, and Chinese** are the top 3 most ordered cuisines
- **Japanese and Continental** generate the highest average order value (₹450+)
- **Healthy/Salads** is emerging strongly during weekday lunch hours

### 3. Delivery Time vs Customer Rating
- Strong negative correlation: **r = −0.62**
- Every **10-minute increase** in delivery time causes a **−0.12 drop** in rating
- Restaurants delivering under **30 minutes** consistently average **4.2+ stars**

### 4. Monthly Revenue Trend
- Revenue peaks in **October–December** (festive season)
- Noticeable dip in **February–March**
- Consistent growth trend across the year

---

## Business Recommendations

### Menu Optimisation
- **Promote Japanese & Continental** cuisines — highest revenue per order
- **Create Biryani combo bundles** (Raita, Dessert) — top volume item with upsell potential
- **Launch weekday healthy lunch combos** to capture growing office demand

### Delivery Slot Planning
- **Increase delivery staff by 40%** during 7–10 PM, especially Fri–Sun
- **Dedicated lunch fleet** during 12–2 PM to handle the mid-day surge
- **Target under 30-minute SLA** — single biggest lever for improving ratings
- **Introduce off-peak discounts** (3–5 PM) to flatten demand and reduce pressure

---

## Output Previews

| Dashboard | Insights |
|---|---|
| `dashboard.png` | `insights.png` |
| Peak hours, heatmap, cuisine demand, delivery vs rating, revenue trend, rating distribution | Cuisine ratings, slot revenue, discount impact, top restaurants |

---

## Author

**Project:** Zomato Order Pattern Analysis  
**Tools:** Python · Pandas · Matplotlib · NumPy  
**Dataset:** Synthetic data (5,000 orders) generated programmatically  

---

## Resume Description

> Analysed 5,000+ Zomato restaurant orders using Python and Pandas to identify peak ordering hours, cuisine demand trends, and a strong negative correlation (r = −0.62) between delivery time and customer ratings. Built multi-panel dashboards using Matplotlib and segmented findings into actionable business recommendations for menu optimisation and delivery slot planning.
