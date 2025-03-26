import sys
import os
sys.path.insert(0, os.path.abspath("C:\PyhtonDAP\src"))  # Add src/ to Python's module search path

import amp_funcs as af
import pandas as pd
import matplotlib.pyplot as plt


path = r"src\rodata"

participants = af.get_amp_diff_data(path, ["Pz", "P3", "P4"], [201, 202], 0.3, 0.6, max_files=10)

data = {
    'Gender': [p.gender for p in participants],
    'Age': [p.age for p in participants],
    'Highest_Edu': [p.highest_edu for p in participants],
    'Highest_Adult_Edu': [p.highest_adult_edu for p in participants],
    'Income_Household': [p.income_household for p in participants],
    'amp_diff': [p.amp_diff for p in participants],
}
df = pd.DataFrame(data)

# Group by education_level and calculate the mean amp_diff
grouped_df = df.groupby("Highest_Adult_Edu", as_index=False)["amp_diff"].mean()

# Plot the grouped data
grouped_df.plot(x='Highest_Adult_Edu', y='amp_diff', alpha=0.7, color='red', figsize=(10, 6))

# Labels and title
plt.xlabel("Parent Education Level")
plt.ylabel("Mean Amplitude Difference (amp_diff)")
plt.title("Mean Amplitude Difference vs Parent Education Level")

# Show the plot
plt.show()