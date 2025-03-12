from Subjects import VORecord
import mne
import numpy as np

file_path = "rodata\Records\subject.1\sub-1_task-visualoddball_eeg.vhdr"
channel_name = 'Pz'
vor = VORecord(file_path)
#c = vor.get_Amplitudes_arrays("Pz", 0.3, 0.6, ["S202", "S201"])

channel_index = vor.raw.info["ch_names"].index(channel_name)

tmin, tmax = 0.3, 0.6        #300 to 600 ms after
epochs = mne.Epochs(vor.raw, vor.events, vor.event_id, tmin=tmin, tmax=tmax,baseline=None, preload=True)

special_epochs = epochs["S201"].get_data()
special_epochs = np.concatenate([special_epochs, epochs["S202"].get_data()])  # Concatenate S202

special_pz = special_epochs[:, channel_index, :]  # Shape: (num_special_trials, num_timepoints)
special_amplitudes = np.mean(np.abs(special_pz), axis=1)  # Shape: (num_special_trials,)

event_ids_to_drop = ["S201", "S202"]
# Get the indices of the events to drop
event_indices_to_drop = [i for i, event in enumerate(epochs.events[:, 2]) if event in event_ids_to_drop]

all_other_stimuli = epochs.drop(event_indices_to_drop)
other_epochs = all_other_stimuli.get_data()
other_pz = other_epochs[:, channel_index, :]
other_amplitude = np.mean(np.abs(other_pz), axis = 1)

mean_special = np.mean(special_amplitudes)
mean_other = np.mean(other_amplitude)
print(f"the regular mean amplitude is: {mean_other}, and the special mean amplitude is {mean_special}\n"
      f"So the diff is {mean_special - mean_other}")
