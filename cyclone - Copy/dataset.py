import pandas as pd
import random
from datetime import datetime, timedelta

# Tamil Nadu districts (38)
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

# Generate data every 3 days for 1 year
start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 12, 31)
date_list = []

current_date = start_date
while current_date <= end_date:
    date_list.append(current_date.strftime('%Y-%m-%d'))
    current_date += timedelta(days=3)

# Prepare dataset
rows = []
for district in districts:
    for date in date_list:
        wind_speed = random.randint(30, 160)
        pressure = random.randint(950, 1020)
        humidity = random.randint(55, 100)

        cyclone = 1 if (wind_speed > 100 and pressure < 980 and humidity > 85) else 0

        rows.append({
            'date': date,
            'district': district,
            'wind_speed': wind_speed,
            'pressure': pressure,
            'humidity': humidity,
            'cyclone': cyclone
        })

# Convert to DataFrame
df = pd.DataFrame(rows)

# Save to CSV
df.to_csv("cyclone_data.csv", index=False)

print(" Cyclone dataset (2025, 38 TN districts, 4636 rows) saved as 'cyclone_data.csv'")
print(df.head())
