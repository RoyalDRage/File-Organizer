import os
import shutil
import logging
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.simpledialog import askstring
import threading

# Configure logging
user_home = os.path.expanduser('~')
# Configure logging to the user's download folder
# Note that you can also configure the logging file location using
#log_file_path = os.path.join(user_home, 'Desktop', 'organize_downloads.log') This will be the desktop
#Use the following if you want to have a different location
# logging.basicConfig(filename='E:/Test/tested/organize_downloads.log', level=logging.INFO,
#                        format='%(asctime)s - %(levelname)s - %(message)s')

log_file_path = os.path.join(user_home, 'Downloads','Desktop','organize_downloads.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Start logging
logging.info("Starting to organize downloads...")


def ask_user_confirmation(files_to_move, root):
    """
    Displays a confirmation message in a Tkinter window and prompts the user to confirm the file movement.

    Args:
        files_to_move (list): List of file names to be moved.
        root (tk.Tk): The main Tkinter window.

    Returns:
        bool: True if the user confirms ('yes'), False otherwise.
    """
    # Prepare the confirmation message
    confirmation_message = "The following files will be moved:\n\n" + "\n".join(files_to_move)

    # Use messagebox for user confirmation
    user_response = messagebox.askyesno("Confirmation", confirmation_message + "\n\nDo you want to proceed?")

    # Return True if the user confirms by clicking 'yes', False otherwise
    return user_response


def organize_downloads(downloads_folder, destination_folder, folder_mapping):
    # Create the destination folder if it doesn't exist.
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
        logging.info(f"Created destination folder: {destination_folder}")

    # Gather a list of files to be moved (for user confirmation)
    moved_files = []

    all_files = [f for f in os.listdir(downloads_folder) if os.path.isfile(os.path.join(downloads_folder, f))]
    files_to_move = [f for f in all_files if os.path.splitext(f)[1] in folder_mapping]

    if not ask_user_confirmation(files_to_move, root):
        print("Operation cancelled by the user.")
        logging.info("Operation cancelled by the user.")
        return

    # Scan the Downloads folder for new files.
    moved_files = []  # Initialize the moved_files list to keep track of what you move

    for filename in files_to_move:  # Iterate only through the files confirmed for moving
        file_path = os.path.join(downloads_folder, filename)  # Full path of the file
        file_extension = os.path.splitext(filename)[1]  # Get the file extension

        if file_extension in folder_mapping:  # Check if the extension is one we're organizing
            extension_folder = os.path.join(destination_folder, folder_mapping[file_extension])

            # Create the folder for this extension if it doesn't exist
            if not os.path.exists(extension_folder):
                os.makedirs(extension_folder)
                logging.info(f"Created extension folder: {extension_folder}")

            destination_path = os.path.join(extension_folder, filename)  # Destination path for the file

            # Now try to move the file
            try:
                shutil.move(file_path, destination_path)
                moved_files.append(filename)  # Add the file to the moved files list
                logging.info(f"Moved {filename} to {extension_folder}")
            except Exception as e:
                logging.error(f"Error moving {filename}: {str(e)}")

    # After moving the files, print and log the moved files
    if moved_files:
        print("Moved the following files:")
        for f in moved_files:
            print(f)
        logging.info(f"Moved the following files: {', '.join(moved_files)}")
    else:
        print("No files were moved.")

event = threading.Event()
def start_organizing(root):
    if messagebox.askyesno("Confirmation", "Do you want to proceed with file organization?"):
        organize_button.state(['disabled'])
        event.clear()

        # Start the organize_downloads function in a new thread
        # Example: To change the location, update the first argument of the 'args' tuple to the desired Downloads folder.
        # For instance, to use the user's Downloads folder: os.path.join(os.path.expanduser('~'), 'Downloads')
        #For specif locations you can simply type the location of the desired folder : 'E:/Randomfiles', 'E:/Sortedfolder/recent/',{
        #Files from E:/Randomfiles would be sorted into E:/Sortedfolder/recent/
        thread = threading.Thread(target=organize_downloads,
                                  args=(os.path.join(os.path.expanduser('~'), 'Downloads'), os.path.join(user_home, 'Downloads'), {
                                      '.pdf': 'PDFs',
                                      '.jpg': 'Images',
                                      '.jpeg': 'Images',
                                      '.png': 'Images',
                                      '.gif': 'Images',
                                      '.bmp': 'Images',
                                      '.mp3': 'Music',
                                      '.mp4': 'Videos',
                                      '.avi': 'Videos',
                                      '.mkv': 'Videos',
                                      '.mov': 'Videos',
                                      '.wmv': 'Videos',
                                      '.m4v': 'Videos',
                                      '.txt': 'Text Files',
                                      # Add more file extensions and folders as needed.
                                  }))
        thread.start()

        # Check the thread's status after some time and re-enable the button if the thread is no longer active
        def check_thread():
            if thread.is_alive():
                # If the thread is still alive, check again after some time
                root.after(100, check_thread)
            else:
                # If the thread is finished, re-enable the button
                organize_button.state(['!disabled'])
                root.destroy()

        # Start checking the thread status
        check_thread()

# Initialize the Tkinter window
root = tk.Tk()
root.title("File Organizer")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Add a button to start the file organization
organize_button = ttk.Button(frame, text="Organize Downloads", command=lambda: start_organizing(root))
organize_button.grid(row=0, column=0, sticky=tk.W)

root.mainloop()
