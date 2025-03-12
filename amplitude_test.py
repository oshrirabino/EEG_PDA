from Subjects import EegRecordSubject
import numpy as np
#creat the events to check, the channels to check and the eeg instance
vor = EegRecordSubject("rodata\Records\subject.1\sub-1_task-visualoddball_eeg.vhdr")
events_to_check = ["S201", "S202"]
channels = ["Pz", "P3", "P4"]
tmin = 0.3
tmax = 0.6
print(vor.find_amp_diff(channels, events_to_check, tmin, tmax))
s200_events = []
other_events = []

#store every avarge amplitude
for channel in channels:
    s200_pz = np.mean(vor.get_Amplitudes_array(channel, tmin, tmax, events_to_check))
    s200_events.append(s200_pz)
    all_event_types = set(vor.event_id.keys())  # Get all event names
    other_event_types = list(all_event_types - set(events_to_check))  # Remove unwanted events
    other_pz = np.mean(vor.get_Amplitudes_array(channel, tmin, tmax, other_event_types))
    other_events.append(other_pz)
#print the diff
print(f"the diff is: {np.mean(s200_events) - np.mean(other_events)}")