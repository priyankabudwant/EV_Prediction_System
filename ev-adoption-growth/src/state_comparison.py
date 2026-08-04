import pandas as pd
import matplotlib.pyplot as plt

# Load maker dataset
df = pd.read_csv("data/EV Maker by Place.csv")

# Count makers per state
state_counts = df.groupby("State")["EV Maker"].count().reset_index()

state_counts = state_counts.sort_values(by="EV Maker", ascending=False)

print(state_counts)

plt.figure()
plt.bar(state_counts["State"], state_counts["EV Maker"])
plt.xticks(rotation=90)
plt.xlabel("State")
plt.ylabel("Number of EV Makers")
plt.title("State-wise EV Maker Distribution")
plt.show()
