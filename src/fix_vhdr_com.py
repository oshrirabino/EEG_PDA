import os  # Import the 'os' module, which provides functions for interacting with the operating system, like working with files and directories.

def fix_eeg_filenames(base_dir):
    """
    This function iterates through the subject folders and calls the appropriate processing function
    for each .vhdr and .vmrk file found within the 'eeg' subfolder.

    Args:
        base_dir (str): The base directory where the subject folders ('sub-001' to 'sub-127') are located.
    """
    for sub_num in range(1, 128):  # Loop through the numbers 1 to 127 (inclusive) to generate the subject folder names.
        sub_folder = f"sub-{sub_num:03d}"  # Create the subject folder name (e.g., 'sub-001', 'sub-002', etc.). The ':03d' ensures the number is always three digits with leading zeros.
        eeg_folder = os.path.join(base_dir, sub_folder, "eeg")  # Construct the full path to the 'eeg' subfolder within the current subject folder.

        if not os.path.exists(eeg_folder):  # Check if the 'eeg' folder actually exists.
          print(f"eeg folder not found in {sub_folder}")  # If the folder doesn't exist, print a message.
          continue  # Skip to the next iteration of the loop (next subject folder).

        for filename in os.listdir(eeg_folder):  # Loop through all the files and folders within the 'eeg' folder.
            file_path = os.path.join(eeg_folder, filename)  # Construct the full path to the current file.
            if filename.endswith(".vhdr"):  # Check if the filename ends with '.vhdr'.
                process_vhdr(file_path, sub_folder)  # If it's a .vhdr file, call the 'process_vhdr' function to fix it.
            elif filename.endswith(".vmrk"):  # Check if the filename ends with '.vmrk'.
                process_vmrk(file_path, sub_folder)  # If it's a .vmrk file, call the 'process_vmrk' function to fix it.

def process_vhdr(vhdr_path, sub_folder):
    """
    This function processes a single .vhdr file to correct the 'DataFile=' and 'MarkerFile=' lines.

    Args:
        vhdr_path (str): The full path to the .vhdr file.
        sub_folder (str): The name of the parent subject folder (e.g., 'sub-001').
    """
    try:  # Start a 'try' block to handle potential errors during file processing.
        with open(vhdr_path, 'r', encoding='utf-8') as f:  # Open the .vhdr file in read mode ('r') with UTF-8 encoding to handle various characters. The 'with' statement ensures the file is automatically closed.
            lines = f.readlines()  # Read all lines from the file and store them in a list called 'lines'.

        vhdr_filename = os.path.basename(vhdr_path)  # Extract the filename from the full path (e.g., 'sub-011_task-visualoddball_eeg.vhdr').
        task_name = vhdr_filename.split('_task-')[1].split('_eeg')[0]  # Extract the task name from the filename. It splits the filename at '_task-', takes the part after that, and then splits that part at '_eeg' to get the task name in between.

        correct_eeg_filename = f"{sub_folder}_task-{task_name}_eeg.eeg"  # Construct the correct .eeg filename based on the subject folder and task name.
        correct_vmrk_filename = f"{sub_folder}_task-{task_name}_eeg.vmrk"  # Construct the correct .vmrk filename based on the subject folder and task name.

        for i, line in enumerate(lines):  # Loop through each line in the 'lines' list, keeping track of the line index 'i'.
            if line.startswith("DataFile="):  # Check if the current line starts with 'DataFile='.
                lines[i] = f"DataFile={correct_eeg_filename}\n"  # If it does, replace the line with the correct 'DataFile=' line, including a newline character at the end.
            elif line.startswith("MarkerFile="):  # Check if the current line starts with 'MarkerFile='.
                lines[i] = f"MarkerFile={correct_vmrk_filename}\n"  # If it does, replace the line with the correct 'MarkerFile=' line, including a newline character at the end.

        with open(vhdr_path, 'w', newline='\n', encoding='utf-8') as f:  # Open the same .vhdr file again, but this time in write mode ('w'). 'newline='\n'' ensures consistent newline characters, and 'encoding='utf-8'' handles encoding.
            f.writelines(lines)  # Write the modified 'lines' list back to the file, overwriting the original content.

        print(f"Fixed filenames in {vhdr_path}")  # Print a message indicating that the file has been processed.

    except Exception as e:  # If any error occurs within the 'try' block, this block will catch it.
        print(f"Error processing {vhdr_path}: {e}")  # Print an error message, including the specific error that occurred.

def process_vmrk(vmrk_path, sub_folder):
    """
    This function processes a single .vmrk file to correct the 'DataFile=' line.

    Args:
        vmrk_path (str): The full path to the .vmrk file.
        sub_folder (str): The name of the parent subject folder (e.g., 'sub-001').
    """
    try:  # Start a 'try' block to handle potential errors during file processing.
        with open(vmrk_path, 'r', encoding='utf-8') as f:  # Open the .vmrk file in read mode ('r') with UTF-8 encoding.
            lines = f.readlines()  # Read all lines from the file.

        vmrk_filename = os.path.basename(vmrk_path)  # Extract the filename from the full path.
        task_name = vmrk_filename.split('_task-')[1].split('_eeg')[0]  # Extract the task name from the filename.

        correct_eeg_filename = f"{sub_folder}_task-{task_name}_eeg.eeg"  # Construct the correct .eeg filename.

        for i, line in enumerate(lines):  # Loop through each line.
            if line.startswith("DataFile="):  # Check if the line starts with 'DataFile='.
                lines[i] = f"DataFile={correct_eeg_filename}\n"  # Replace the line with the correct 'DataFile=' line.

        with open(vmrk_path, 'w', newline='\n', encoding='utf-8') as f:  # Open the .vmrk file in write mode, ensuring consistent newline characters and UTF-8 encoding.
            f.writelines(lines)  # Write the modified lines back to the file.

        print(f"Fixed filenames in {vmrk_path}")  # Print a success message.

    except Exception as e:  # Catch any errors.
        print(f"Error processing {vmrk_path}: {e}")  # Print an error message.

base_directory = "."  # Set the base directory to the current directory. You can change this if your subject folders are located elsewhere.
fix_eeg_filenames(base_directory)  # Call the main function to start the process, using the specified base directory.
