import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

n = 5000

restaurants = {
    "Spice Garden":    "North Indian",
    "Dragon Palace":   "Chinese",
    "Pizza Hub":       "Italian",
    "Burger Barn":     "Fast Food",
    "Curry House":     "South Indian",
    "Sushi World":     "Japanese",
    "Biryani Bros":    "Biryani",
    "Wrap & Roll":     "Continental",
    "Tandoor Nights":  "Mughlai",
    "Green Bowl":      "Healthy/Salads",
}

restaurant_names = list(restaurants.keys())
cuisines        = list(restaurants.values())

# Peak hours weighted distribution
hour_weights = [0.5,0.3,0.2,0.1,0.1,0.2,0.4,0.8,1.2,1.0,
                0.9,1.5,3.0,2.5,1.8,1.2,1.0,1.5,3.5,3.8,
                3.2,2.0,1.2,0.7]
hour_weights = np.array(hour_weights) / sum(hour_weights)

hours       = np.random.choice(range(24), size=n, p=hour_weights)
days        = np.random.choice(['Mon','Tue','Wed','Thu','Fri','Sat','Sun'], size=n,
                               p=[0.12,0.11,0.12,0.13,0.16,0.20,0.16])
rest_idx    = np.random.choice(len(restaurant_names), size=n)
rest_col    = [restaurant_names[i] for i in rest_idx]
cuisine_col = [cuisines[i] for i in rest_idx]

# Delivery time: peaks during lunch/dinner
base_delivery = 25
delivery_noise = np.random.normal(0, 8, n)
peak_penalty   = np.where((hours>=12)&(hours<=14), 10,
                 np.where((hours>=19)&(hours<=21), 12, 0))
delivery_times = np.clip(base_delivery + delivery_noise + peak_penalty, 10, 90).astype(int)

# Ratings: higher when delivery is faster
base_rating = 4.0
rating_penalty = (delivery_times - 25) * 0.012 + np.random.normal(0, 0.3, n)
ratings = np.clip(base_rating - rating_penalty, 1.0, 5.0).round(1)

# Order value
cuisine_price = {"North Indian":350,"Chinese":300,"Italian":400,"Fast Food":200,
                 "South Indian":250,"Japanese":500,"Biryani":280,"Continental":380,
                 "Mughlai":320,"Healthy/Salads":260}
order_values = [cuisine_price[c] + np.random.normal(0,60) for c in cuisine_col]
order_values = np.clip(order_values, 100, 1200).astype(int)

start_date = datetime(2024, 1, 1)
dates = [start_date + timedelta(days=random.randint(0, 364)) for _ in range(n)]

df = pd.DataFrame({
    'order_id':       range(1, n+1),
    'date':           dates,
    'day_of_week':    days,
    'hour':           hours,
    'restaurant':     rest_col,
    'cuisine':        cuisine_col,
    'order_value':    order_values,
    'delivery_time':  delivery_times,
    'rating':         ratings,
    'discount_pct':   np.random.choice([0,10,20,30], size=n, p=[0.5,0.25,0.15,0.10]),
})

df['month'] = pd.to_datetime(df['date']).dt.month_name()
df.to_csv(r'C:\Users\Abhay\Documents\Zomato_analysis\zomato_orders.csv', index=False)
print(f"Generated {len(df)} records")
print(df.head())
