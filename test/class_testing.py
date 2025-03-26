import sys
import os
sys.path.insert(0, os.path.abspath("C:\PyhtonDAP\src"))  # Add src/ to Python's module search path

from Subjects import EegRecordSubject
import pandas as pd
import numpy as np 
import mne

file_path = r"src\rodata\sub-001\eeg\sub-001_task-visualoddball_eeg.vhdr"

eeg_r = EegRecordSubject(file_path)
epochs = mne.Epochs(eeg_r.raw, events = eeg_r.events, event_id = eeg_r.event_id,
                            tmin = -0.2, tmax = 0.8, baseline = None, picks = ["Pz", "P3", "P4"])
epoch_event_ids = epochs.events[:, 2]
rare_event_ids = [201, 202]
mask_rare = np.isin(epoch_event_ids, rare_event_ids)
rare_epochs = epochs[mask_rare]   # Contains only rare event epochs
freq_epochs = epochs[~mask_rare]  # Contains all other epochs

print(rare_epochs.events[:5])
print(freq_epochs.events[:5])