import amp_funcs as af
import pandas as pd
from Subjects import Participant
import matplotlib.pyplot as plt

path = "rodata"

participants = af.get_amp_diff_data(path, ["Pz", "P3", "P4"], [201, 202], 0.3, 0.6)

data = {
    'Gender': [p.gender for p in participants],
    'Age': [p.age for p in participants],
    'Highest_Edu': [p.highest_edu for p in participants],
    'Highest_Adult_Edu': [p.highest_adult_edu for p in participants],
    'Income_Household': [p.income_household for p in participants],
    'amp_diff': [p.amp_diff for p in participants],
}
df = pd.DataFrame(data)
df.to_excel("output_p3b.xlsx", index=False)

df.plot(kind="scatter", x = "Highest_Adult_Edu", y = "amp_diff", alpha = 0.5, color = 'blue',
        figsize=(10,6))

plt.xlabel('Parent Education Level')
plt.ylabel('Amplitude Difference')
plt.title('Amplitude Difference vs Parent Education Level')

plt.show()
