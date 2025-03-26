import amp_funcs as af
import pandas as pd
from Subjects import Participant
import matplotlib.pyplot as plt
"""
Script that create data for specific task and store it in excel file.
 It get all participants objects using "get_amp_diff_data_VS" and store the data
"""

path = r"src\rodata"

participants = af.get_amp_diff_data_VS(path, ["Fz", "F3", "F4", "FC1", "FC2", "C3", "C4"], [201, 202], 0.125, 0.225)

data = {
    'Gender': [p.gender for p in participants],
    'Age': [p.age for p in participants],
    'Highest_Edu': [p.highest_edu for p in participants],
    'Highest_Adult_Edu': [p.highest_adult_edu for p in participants],
    'Income_Household': [p.income_household for p in participants],
    'amp_diff': [p.amp_diff for p in participants],
}
df = pd.DataFrame(data)
df.to_excel("output_fz.xlsx", index=False)

