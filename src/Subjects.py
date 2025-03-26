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
            #filtring data
            self.raw.filter(0.1, 40, fir_design='firwin')
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
        
    #OUT DATED
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
        epochs = mne.Epochs(self.raw, self.events, self.event_id, tmin=-0.2, tmax=0.8,
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
        time_range = (tmin, tmax) 
        sfreq = chosen_epochs.info["sfreq"]

        tmin_idx = int((time_range[0] - chosen_epochs.times[0]) * sfreq)
        tmax_idx = int((time_range[1] - chosen_epochs.times[0]) * sfreq)

        chosen_amplitudes_2 = np.mean(chosen_epochs[:, :, tmin_idx:tmax_idx], axis=(0, 2))
        chosen_amplitudes = np.mean(np.abs(chosen_epochs), axis=1)
    
        return chosen_amplitudes_2
    
    #OUT DATED
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
    
    def find_amp_diff_2(self, channels, rare_events, tmin: float, tmax: float):
        """
        Computes the difference in mean amplitude between "rare" event epochs 
        and all other epochs within a specified time window.

        Parameters:
        -----------
        channels : list of str
            List of channel names to include in the analysis.
        rare_events : list of int
            List of event IDs that are considered "rare" events.
        tmin : int
            Start time (in seconds) for computing the mean amplitude.
        tmax : int
            End time (in seconds) for computing the mean amplitude.

        Returns:
        --------
        float
            The difference in mean amplitude (in original data units) 
            between rare event epochs and frequent event epochs.
    
        Notes:
        ------
        - The function first creates an MNE `Epochs` object using the provided channels and event IDs.
        - It splits the epochs into "rare" and "frequent" based on `rare_events`.
        - Mean amplitude is computed across all selected channels and time points.
        - The returned value is `mean_rare - mean_freq`, representing the difference in response.

        """
        # Extract event IDs for all epochs
        epochs = mne.Epochs(self.raw, events = self.events, event_id = self.event_id,
                          tmin = -0.2, tmax = 0.8, picks = channels, baseline = (None, 0))
        
        # Create masks to separate rare and frequent events
        epoch_event_ids = epochs.events[:, 2]
        mask_rare = np.isin(epoch_event_ids, rare_events)
        rare_epochs = epochs[mask_rare]   # Contains only rare event epochs
        freq_epochs = epochs[~mask_rare]  # Contains all other epochs

        # Convert time window to sample indices
        time_range = (tmin, tmax)
        sfreq = epochs.info["sfreq"]
        tmin_idx = int((time_range[0] - epochs.times[0]) * sfreq)
        tmax_idx = int((time_range[1] - epochs.times[0]) * sfreq)

        # Compute mean amplitude for rare and frequent epochs
        mean_rare = np.mean(rare_epochs.get_data()[:, :, tmin_idx:tmax_idx+1], axis=(0, 2))
        mean_rare = np.mean(mean_rare)
        mean_freq = np.mean(freq_epochs.get_data()[:, :, tmin_idx:tmax_idx+1], axis=(0, 2))
        mean_freq = np.mean(mean_freq)

        return mean_rare - mean_freq



        
         
class Participant:
    def __init__(self, gender: str, age: float, highest_edu: str, highest_adult_edu: float, income_household: str, amp_diff: float):
        self.gender = gender
        self.age = age
        self.highest_edu = highest_edu
        self.highest_adult_edu = highest_adult_edu
        self.income_household = income_household
        self.amp_diff = amp_diff  # Instance of EegRecordSubject

    def __repr__(self):
        return f"Participant(gender={self.gender}, age={self.age}, highest_edu={self.highest_edu}, income_household={self.income_household})"
     