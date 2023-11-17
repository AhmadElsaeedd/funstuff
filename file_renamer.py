import os

# The path to the directory containing subfolders with files to be renamed
base_directory = 'stories'

# Iterate over all items in the base directory
for folder_name in os.listdir(base_directory):
    folder_path = os.path.join(base_directory, folder_name)
    
    # Check if this is a directory
    if os.path.isdir(folder_path):
        # Initialize a counter to name files starting from 0 for each subfolder
        file_counter = 0
        
        # Iterate over all files in the subdirectory
        for file_name in os.listdir(folder_path):
            old_file_path = os.path.join(folder_path, file_name)
            
            # Make sure it's a file and not a directory
            if os.path.isfile(old_file_path):
                # Construct the new file name
                new_file_name = f"{file_counter}{os.path.splitext(file_name)[1]}"
                new_file_path = os.path.join(folder_path, new_file_name)
                
                # Rename the file
                os.rename(old_file_path, new_file_path)
                
                # Increment the counter for the next file
                file_counter += 1

print("Files in all subfolders have been renamed.")
