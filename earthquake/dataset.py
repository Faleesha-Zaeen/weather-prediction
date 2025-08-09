# dataset.py
import pandas as pd
import random
from datetime import datetime, timedelta

random.seed(42)

districts = [
    "Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem",
    "Erode", "Tirunelveli", "Vellore", "Thanjavur", "Dindigul",
    "Thoothukudi", "Cuddalore", "Nagapattinam", "Theni", "Virudhunagar",
    "Karur", "Krishnagiri", "Namakkal", "Pudukkottai", "Ramanathapuram",
    "Sivaganga", "Tirupur", "Villupuram", "Dharmapuri", "Ariyalur",
    "Tiruvarur", "Perambalur", "Nilgiris", "Kallakurichi", "Chengalpattu",
    "Tenkasi", "Ranipet", "Tirupathur", "Kanchipuram", "Thiruvallur",
    "Mayiladuthurai", "Thiruporur", "Thirumangalam"
]

start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 12, 31)

dates = []
current_date = start_date
while current_date <= end_date:
    dates.append(current_date.strftime('%Y-%m-%d'))
    current_date += timedelta(days=3)

rows = []
for district in districts:
    for date in dates:
        magnitude = round(random.uniform(2.0, 7.0), 1)
        depth_km = random.randint(5, 300)
        seismic_activity = random.randint(0, 100)
        earthquake = 1 if magnitude >= 5.0 and seismic_activity >= 60 else 0

        rows.append({
            "date": date,
            "district": district,
            "magnitude": magnitude,
            "depth_km": depth_km,
            "seismic_activity": seismic_activity,
            "earthquake": earthquake
        })

df = pd.DataFrame(rows)
df.to_csv("earthquake_data.csv", index=False)
print(f" earthquake_data.csv created with {len(df)} rows")
