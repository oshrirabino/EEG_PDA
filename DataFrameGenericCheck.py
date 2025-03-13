import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel("output_p3b.xlsx")

# Group by education_level and calculate the mean amp_diff
grouped_df = df.groupby("Highest_Adult_Edu", as_index=False)["amp_diff"].mean()

# Plot the grouped data
grouped_df.plot(kind='scatter', x='Highest_Adult_Edu', y='amp_diff', alpha=0.7, color='red', figsize=(10, 6))

# Labels and title
plt.xlabel("Parent Education Level")
plt.ylabel("Mean Amplitude Difference (amp_diff)")
plt.title("Mean Amplitude Difference vs Parent Education Level")

# Show the plot
plt.show()