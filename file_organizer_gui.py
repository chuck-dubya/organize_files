import os
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import filedialog


def organize_files():
    """
    Organizes files in the selected folder based on file type and creation date.
    """

    folder_to_organize = folder_path_var.get()

    if not folder_to_organize:
        result_label.config(text="Please select a folder first!")
        return

    for filename in os.listdir(folder_to_organize):
        # Ignore folders
        if os.path.isdir(os.path.join(folder_to_organize, filename)):
            continue

        # Get file extension and creation date
        file_extension = os.path.splitext(filename)[1][1:].lower()
        file_creation_time = os.path.getctime(
            os.path.join(folder_to_organize, filename)
        )
        file_creation_date = datetime.fromtimestamp(file_creation_time).strftime(
            "%Y-%m-%d"
        )

        # Create destination folders if they don't exist
        destination_folder = os.path.join(folder_to_organize, file_extension)
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        destination_subfolder = os.path.join(destination_folder, file_creation_date)
        if not os.path.exists(destination_subfolder):
            os.makedirs(destination_subfolder)

        # Move file to destination
        source_path = os.path.join(folder_to_organize, filename)
        destination_path = os.path.join(destination_subfolder, filename)

        # Handle potential filename conflicts
        if os.path.exists(destination_path):
            base_filename, ext = os.path.splitext(filename)
            i = 1
            while os.path.exists(
                os.path.join(destination_subfolder, f"{base_filename}_{i}{ext}")
            ):
                i += 1
            destination_path = os.path.join(
                destination_subfolder, f"{base_filename}_{i}{ext}"
            )

        shutil.move(source_path, destination_path)

    result_label.config(text="Files organized successfully!")


def browse_folder():
    """
    Opens a file dialog to select a folder.
    """

    folder_selected = filedialog.askdirectory()
    folder_path_var.set(folder_selected)


# Create the main window
window = tk.Tk()
window.title("File Organizer")

# Folder selection
folder_path_var = tk.StringVar()
folder_label = tk.Label(window, text="Select Folder:")
folder_label.pack()
folder_entry = tk.Entry(window, textvariable=folder_path_var, width=50)
folder_entry.pack()
browse_button = tk.Button(window, text="Browse", command=browse_folder)
browse_button.pack()

# Organize button
organize_button = tk.Button(window, text="Organize Files", command=organize_files)
organize_button.pack()

# Result label
result_label = tk.Label(window, text="")
result_label.pack()

window.mainloop()
