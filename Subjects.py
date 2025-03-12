import numpy as np
import mne
import pandas as pd

class EegRecordSubject:
    def __init__(self, file_path: str):
        """
        Initializes the EEG record subject by loading the BrainVision EEG data.

        :param file_path: Path to the .vhdr file (the header file).
        """

        self.file_path = file_path
        try:
            self.raw = mne.io.read_raw_brainvision(self.file_path, preload=True)
            print("EEG data successefully uploaded")
        except FileNotFoundError:
            print("File did not found")
            self.raw = None
        except Exception as e:
            print(f"Exception {e} occured")
            self.raw = None
        
        if self.raw:
            self.channels = self.raw.ch_names
            self.events, self.event_id = mne.events_from_annotations(self.raw)
        else:
            self.channels = None

    def display(self, n_channels = 31, picks = None, scalings = 'auto', events = None):
        # Get the sampling rate (Hz)
        sampling_rate = self.raw.info['sfreq']

        # Get the total number of samples
        num_samples = self.raw.n_times

        # Calculate the total duration of the recording in seconds
        
        self.raw.plot(events = None, scalings = scalings, n_channels = n_channels,
                       picks = picks, block = True)
        

    def get_Amplitudes_array(self, channel_name: str, tmin: int, tmax: int, signs):
        """
        This method calculates the average amplitude for the specified channel around the epochs marked 
        with the special event names provided in the `signs` list. It returns the amplitude values of 
        the selected epochs in a numpy array.
    
        Args:
            channel_name (str): The name of the channel (e.g., 'Pz') from which the amplitudes are calculated.
            tmin (int): The start time (in seconds) for the epoch window.
            tmax (int): The end time (in seconds) for the epoch window.
            signs (list, tuple, or set): A collection of event names (e.g., ['S201', 'S202']) that represent the 
                                          special stimuli. The function checks if the collection contains valid 
                                          event names.
    
        Returns:
        numpy.ndarray: A numpy array containing the average absolute amplitudes for the specified channel 
                        across the special epochs defined by `signs`.
    
        Raises:
        ValueError: If the `signs` argument is not a valid collection of strings representing event names.
        KeyError: If the `channel_name` is not found in the available channels.
        """
    
        # Find the index of the specified channel in the raw data
        channel_index = self.raw.info["ch_names"].index(channel_name)
    
        # Create epochs based on the raw data, events, and event IDs
        epochs = mne.Epochs(self.raw, self.events, self.event_id, tmin=tmin, tmax=tmax,
                            baseline=None, preload=True)
    
        # Validate that 'signs' is a collection of strings
        if isinstance(signs, (list, tuple, set)) and all(isinstance(sign, str) for sign in signs):
            # Concatenate epochs for all special event names in 'signs'
            special_epochs = np.concatenate([epochs[sign].get_data() for sign in signs])
        else:
            print("SIGNS IS NOT VALID")
            raise ValueError("The 'signs' argument must be a collection of strings representing valid event names.")
    
        # Extract the data for the specified channel and compute the amplitudes
        chosen_epochs = special_epochs[:, channel_index, :]
        chosen_amplitudes = np.mean(np.abs(chosen_epochs), axis=1)
    
        return chosen_amplitudes
    
    def find_amp_diff(self, channels, events_to_check, tmin: int, tmax: int):
        #check for valid channels and events
        if not (isinstance(channels, (list, tuple, set)) and
                 all(isinstance(channel, str) for channel in channels)):
            raise ValueError("channels not valid")
        if not (isinstance(events_to_check, (list, tuple, set)) and 
                all(isinstance(event, str) for event in events_to_check)):
            raise ValueError("events not valid")
        
        special_events = []
        other_events = []
        #store every avarge amplitude
        for channel in channels:
            spacial_ch = np.mean(self.get_Amplitudes_array(channel, tmin, tmax, events_to_check))
            special_events.append(spacial_ch)
            all_event_types = set(self.event_id.keys())  # Get all event names
            other_event_types = list(all_event_types - set(events_to_check))  # Remove unwanted events
            other_pz = np.mean(self.get_Amplitudes_array(channel, tmin, tmax, other_event_types))
            other_events.append(other_pz)
        return np.mean(special_events) - np.mean(other_events)
         





class VORecord(EegRecordSubject):
    def __init__(self, file_path):
        super().__init__(file_path)

    def display(events = None):
        super().display(n_channels = 1, picks = 'Pz', events = events)       