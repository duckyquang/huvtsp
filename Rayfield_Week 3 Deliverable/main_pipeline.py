import pandas as pd
from ai_module import train_model, predict
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("predictions.csv")
df["date"] = pd.to_datetime(df["date"])

# Train model
model = train_model(df[["output_kwh"]].fillna(0))

# Predict
df["anomaly"] = predict(model, df[["output_kwh"]].fillna(0)) == -1

# Generate summary
anomalies = df[df["anomaly"] == True]["date"].dt.strftime('%Y-%m-%d').tolist()
summary = f"Anomalies detected on: {', '.join(anomalies)}"

# Save updated CSV
df.to_csv("final_output.csv", index=False)

# Save summary
with open("weekly_summary.txt", "w") as f:
    f.write(summary)

# Plot
plt.figure(figsize=(10, 5))
plt.plot(df["date"], df["output_kwh"], label="Output (kWh)")
plt.scatter(
    df[df["anomaly"]]["date"],
    df[df["anomaly"]]["output_kwh"],
    color="red",
    label="Anomalies"
)
plt.title("Energy Output Over Time with Anomalies")
plt.xlabel("Date")
plt.ylabel("Output (kWh)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("anomaly_plot.png")
plt.close()
