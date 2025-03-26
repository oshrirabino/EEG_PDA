import os
import pandas as pd
from Subjects import EegRecordSubject
from Subjects import Participant


def get_amp_diff_data(path: str, channels, events_to_check, tmin: float, tmax: float, max_files=0):
    """
    Processes EEG data for a visual oddball task, extracts amplitude differences, and associates them 
    with participant metadata.

    This function scans a given dataset directory, identifies EEG recordings corresponding to the 
    "visual oddball" task, and processes them using the `EegRecordSubject` class. The extracted 
    amplitude differences are then linked to participant demographic data stored in an Excel file.

    Parameters:
        path (str): The root directory containing the EEG data.
        channels (list[str]): List of EEG channel names to analyze.
        events_to_check (list[str]): List of event markers to extract epochs from.
        tmin (float): Start time (in seconds) of the epoch relative to the event.
        tmax (float): End time (in seconds) of the epoch relative to the event.
        max_files (int, optional): The maximum number of participants to process. 
                                   If 0, processes all available participants.

    Returns:
        list[Participant]: A list of `Participant` objects, each containing demographic data 
                           and the extracted amplitude difference.

    Notes:
        - The function reads participant demographic data from "src/participants.xlsx".
        - The EEG recordings are expected to be in `sub-XXX/eeg/sub-XXX_task-visualoddball_eeg.vhdr` format.
        - If a participant’s EEG file is missing or processing fails, an error is printed, and they are skipped.
    """
    df = pd.read_excel(r"src\participants.xlsx")
    
    # If max_files is not specified, use the number of participants in the dataset
    if max_files == 0:
        max_files = len(df)

    participants = []

    for i in range(1, max_files + 1):
        file_path = os.path.join(path, f"sub-{i:03}\eeg\sub-{i:03}_task-visualoddball_eeg.vhdr")
        
        if os.path.exists(file_path):
            try:
                # Create an EEG record object and extract amplitude differences
                eeg_r = EegRecordSubject(file_path)
                amp_diff = eeg_r.find_amp_diff_2(channels, events_to_check, tmin, tmax)

                # Retrieve participant metadata from the Excel file
                row = df.iloc[i]  # Assuming row i corresponds to participant i
                
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


def get_amp_diff_data_VS(path: str, channels, events_to_check, tmin: int, tmax: int, max_files=0):
    """
    Similar to `get_amp_diff_data`, but processes EEG data for a visual search task.

    The function follows the same workflow as `get_amp_diff_data`, except it looks for EEG files 
    associated with the "visual search" task.

    Due to lack of time the function is not generic for task, but should added another argument called
    'task' that can specify the task we checking to make the tools more generic and flexable

    """
    df = pd.read_excel(r"src\participants.xlsx")
    
    if max_files == 0:
        max_files = len(df)

    participants = []

    for i in range(1, max_files + 1):
        file_path = os.path.join(path, f"sub-{i:03}\eeg\sub-{i:03}_task-visualsearch_eeg.vhdr")

        if os.path.exists(file_path):
            try:
                eeg_r = EegRecordSubject(file_path)
                amp_diff = eeg_r.find_amp_diff_2(channels, events_to_check, tmin, tmax)
                
                row = df.iloc[i]  

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


def some_samples_p3b(path: str, channels, events_to_check, tmin: int, tmax: int, max_files=30):
    """
    Extracts amplitude differences from a subset of EEG recordings for a quick review.

    This function is useful for checking a small sample of EEG records before running a full analysis.
    It reads up to `max_files` EEG recordings, extracts amplitude differences, and prints the results.

    Parameters:
        path (str): The root directory containing the EEG data.
        channels (list[str]): List of EEG channel names to analyze.
        events_to_check (list[str]): List of event markers to extract epochs from.
        tmin (int): Start time (in seconds) of the epoch relative to the event.
        tmax (int): End time (in seconds) of the epoch relative to the event.
        max_files (int, optional): The number of EEG records to process. Default is 30.

    Notes:
        - This function does not return values; it prints the extracted amplitude differences.
        - Skips missing or unprocessable EEG records.
    """
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
