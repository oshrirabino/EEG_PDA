import sys
import os
sys.path.insert(0, os.path.abspath("C:\PyhtonDAP\src"))  # Add src/ to Python's module search path

from Subjects import EegRecordSubject

file_path = r"src\rodata\sub-001\eeg\sub-001_task-visualoddball_eeg.vhdr"

eeg_r = EegRecordSubject(file_path)
eeg_r.display()