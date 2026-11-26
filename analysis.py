import pandas as pd
import matplotlib.pyplot as plt

# ---------- Read CSV files ----------
house_profile_1 = pd.read_csv("inputs/house_profile_1.csv", comment='#', header=None)
water_draw = pd.read_csv("inputs/water_draw.csv", comment='#', header=None)
meter_data1 = pd.read_csv("outputs/meter_data1.csv", comment='#', header=None)
water_heater1 = pd.read_csv("outputs/water_heater1.csv", comment='#', header=None)

# ---------- Timestamps ----------
profile_time = pd.to_datetime(house_profile_1.iloc[:, 0])
draw_time = pd.to_datetime(water_draw.iloc[:, 0])
meter_time = pd.to_datetime(meter_data1.iloc[:, 0].str.replace(" PST", "", regex=False))
wh_time = pd.to_datetime(water_heater1.iloc[:, 0].str.replace(" PST", "", regex=False))

# ---------- GridLAB-D value parsing ----------
# Voltage is POLAR ("120.089+120d" = 120.089 V at 120 deg): magnitude is the first number.
voltage = pd.to_numeric(
    meter_data1.iloc[:, 1].str.extract(r'^\s*([+-]?[\d.]+(?:[eE][+-]?\d+)?)')[0]
)

# Current is RECTANGULAR ("-9.29749+16.2751j"): complex magnitude is correct.
current = meter_data1.iloc[:, 3].str.strip().apply(complex).abs()

real_power = pd.to_numeric(meter_data1.iloc[:, 5])      # W
wh_load = pd.to_numeric(water_heater1.iloc[:, 2])       # kW

# ---------- Plots ----------
fig, axes = plt.subplots(6, 1, figsize=(14, 16), sharex=True)

axes[0].plot(profile_time, house_profile_1.iloc[:, 1])
axes[0].set_title("House 1 Demand")
axes[0].set_ylabel("Power (W)")

axes[1].plot(draw_time, water_draw.iloc[:, 1])
axes[1].set_title("Water Draw")
axes[1].set_ylabel("Demand (GPM)")

axes[2].plot(meter_time, voltage)
axes[2].set_title("Meter Voltage")
axes[2].set_ylabel("Voltage (V)")
# axes[2].set_ylim(118, 122)   # uncomment to show the sag at true scale

axes[3].plot(meter_time, current)
axes[3].set_title("Meter Current")
axes[3].set_ylabel("Current (A)")

axes[4].plot(meter_time, real_power)
axes[4].set_title("Meter Real Power")
axes[4].set_ylabel("Power (W)")

axes[5].plot(wh_time, wh_load)
axes[5].set_title("Water Heater Actual Load")
axes[5].set_ylabel("Load (kW)")
axes[5].set_xlabel("Timestamp")

for ax in axes:
    ax.grid(True)

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()