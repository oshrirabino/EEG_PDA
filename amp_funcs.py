import os
import pandas as pd
from Subjects import EegRecordSubject
from Subjects import Participant

def get_amp_diff_data(path: str, channels, events_to_check, tmin: int, tmax: int, max_files = 0):
    df = pd.read_excel("participants.xlsx")
    if max_files == 0:
        max_files = len(df)
    participants = []
    for i in range(1, max_files + 1):
        file_path = os.path.join(path, f"sub-{i:03}\eeg\sub-{i:03}_task-visualoddball_eeg.vhdr")
        if os.path.exists(file_path):
            try:
                eeg_r = EegRecordSubject(file_path)
                amp_diff = eeg_r.find_amp_diff_2(channels, events_to_check, tmin, tmax)
                row = df.iloc[i]  # Get the i-th row (since row 0 is the header)
                participant = Participant(
                    gender=row["Gender"],
                    age=float(row["Age"]),
                    highest_edu=row["Highest_Edu"],
                    highest_adult_edu=float(row["Highest_Adult_Edu_Nb"]),
                    income_household=row["Income_Household"],
                    amp_diff=amp_diff
                )
                participants.append(participant)
            except Exception as e:
                print(f"Failed to load {file_path}: {e}")
    return participants

def some_sampels_p3b(path: str, channels, events_to_check, tmin: int, tmax: int, max_files = 30):
    records = []
    for i in range(1, max_files + 1):
        file_path = os.path.join(path, f"sub-{i:03}\eeg\sub-{i:03}_task-visualoddball_eeg.vhdr")
        if os.path.exists(file_path):
            try:
                eeg_r = EegRecordSubject(file_path)
                records.append(eeg_r.find_amp_diff(channels, events_to_check, tmin, tmax))
            except Exception as e:
                print(e)
    print(records)




