# File-Organizer
File Organizer Documentation
Introduction
This script is designed to organize files in a specified downloads folder based on their file extensions. It utilizes a graphical user interface (GUI) built with Tkinter to prompt the user for confirmation before moving files. The organization is defined by a mapping of file extensions to destination folders.
#Dependecies
pip install tk
Features
User Confirmation: Before moving any files, the script displays a confirmation window with a list of files to be moved, allowing the user to proceed or cancel the operation.

Logging: The script logs its activities, including the start of the organization process, any errors encountered during file movement, and the files that were successfully moved. The log file is located in the user's Downloads folder.

Threaded Execution: The file organization process runs in a separate thread, preventing the GUI from freezing during the operation. The user can monitor the progress and cancel the operation if needed.

Usage
Dependencies: The script requires the following dependencies:

os: Operating system module for file and directory operations.
shutil: High-level file operations.
logging: Logging module for tracking script activities.
tkinter: GUI library for creating the user interface.
threading: Module for managing threads.
Configuration:

Configure the logging file path according to your preference. By default, it logs to a file named organize_downloads.log in the user's Downloads folder.
Folder Mapping:

Customize the folder_mapping dictionary to define the destination folders for specific file extensions. For example:
python
Copy code
{
    '.pdf': 'PDFs',
    '.jpg': 'Images',
    # Add more extensions and corresponding folders as needed.
}
Run the Script:

Execute the script, and a GUI window titled "File Organizer" will appear.
Click the "Organize Downloads" button to start the file organization process.
Confirm the operation in the displayed window.
The script will move the specified files to their corresponding folders, and the user can monitor the progress in the console.
Example
python
Copy code
python file_organizer.py
Note
Ensure that the Tkinter library is installed in your Python environment.
Disclaimer
This script assumes that the user understands the potential consequences of moving files and has a backup of important data. The script's behavior is determined by the configuration of the folder_mapping dictionary, and it's essential to review and customize it according to your needs.

Author
This script was created by RoyalDRage. Feel free to provide feedback or contribute to its improvement.
