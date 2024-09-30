import os
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


def organize_files():
    """
    Organizes files in the selected folder based on file type.
    """

    folder_to_organize = folder_path_var.get()

    if not folder_to_organize:
        result_label.config(text="Please select a folder first!", foreground="red")
        return

    for filename in os.listdir(folder_to_organize):
        file_path = os.path.join(folder_to_organize, filename)

        # Ignore folders, symlinks, and Windows shortcuts (.lnk files)
        if (
            os.path.isdir(file_path)
            or os.path.islink(file_path)
            or filename.lower().endswith(".lnk")
        ):
            continue

        # Get file extension
        file_extension = os.path.splitext(filename)[1][1:].lower()

        # Create destination folder for the file extension if it doesn't exist
        destination_folder = os.path.join(folder_to_organize, file_extension)
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        # Move file to the destination folder
        destination_path = os.path.join(destination_folder, filename)

        # Handle potential filename conflicts
        if os.path.exists(destination_path):
            base_filename, ext = os.path.splitext(filename)
            i = 1
            while os.path.exists(
                os.path.join(destination_folder, f"{base_filename}_{i}{ext}")
            ):
                i += 1
            destination_path = os.path.join(
                destination_folder, f"{base_filename}_{i}{ext}"
            )

        shutil.move(file_path, destination_path)

    # Identify and optionally delete empty folders
    identify_empty_folders(folder_to_organize)

    result_label.config(text="Files organized successfully!", foreground="green")


def browse_folder():
    """
    Opens a file dialog to select a folder.
    """
    folder_selected = filedialog.askdirectory()
    folder_path_var.set(folder_selected)


def identify_empty_folders(folder_path):
    """
    Identifies empty folders and optionally deletes them.
    """
    empty_folders = []
    for dirpath, dirnames, filenames in os.walk(folder_path):
        if not dirnames and not filenames:
            empty_folders.append(dirpath)

    if empty_folders:
        # List empty folders in a message box
        folder_list = "\n".join(empty_folders)
        messagebox.showinfo(
            "Empty Folders Found",
            f"Found the following empty folders:\n\n{folder_list}",
        )

        # Ask the user if they want to delete the empty folders
        delete_empty = messagebox.askyesno(
            "Delete Empty Folders?",
            f"Do you want to delete these {len(empty_folders)} empty folders?",
        )

        if delete_empty:
            for folder in empty_folders:
                os.rmdir(folder)
            result_label.config(
                text=f"Files organized and {len(empty_folders)} empty folders deleted.",
                foreground="green",
            )
        else:
            result_label.config(
                text=f"Files organized, but empty folders were not deleted.",
                foreground="green",
            )
    else:
        result_label.config(
            text="Files organized. No empty folders found.", foreground="green"
        )


# Create the main window
window = tk.Tk()
window.title("File Organizer")
window.geometry("500x350")

# Configure the dark theme colors
dark_bg = "#2e2e2e"
dark_fg = "#ffffff"
dark_button_bg = "#444444"
dark_button_fg = "#ffffff"
highlight_color = "#8c8c8c"

# Set the window background color
window.configure(bg=dark_bg)

# Use ttk for modern styling
style = ttk.Style()
style.theme_use("clam")

# Custom dark theme styles
style.configure(
    "TLabel",
    background=dark_bg,
    foreground=dark_fg,
)

style.configure(
    "TFrame",
    background=dark_bg,
)

style.configure(
    "TButton",
    background=dark_button_bg,
    foreground=dark_button_fg,
    padding=6,
    relief="flat",
)
style.map("TButton", background=[("active", highlight_color)])

style.configure(
    "TEntry",
    fieldbackground=dark_bg,
    foreground=dark_fg,
)

# Folder selection
folder_path_var = tk.StringVar()

# Folder label with dark theme
folder_label = ttk.Label(window, text="Select Folder:")
folder_label.pack(pady=10)

folder_frame = ttk.Frame(window)
folder_frame.pack(pady=5)

# Folder entry with dark theme
folder_entry = ttk.Entry(folder_frame, textvariable=folder_path_var, width=40)
folder_entry.pack(side="left", padx=5)

# Browse button with dark theme
browse_button = ttk.Button(folder_frame, text="Browse", command=browse_folder)
browse_button.pack(side="left")

# Organize button with dark theme
organize_button = ttk.Button(window, text="Organize Files", command=organize_files)
organize_button.pack(pady=20)

# Result label with dark theme
result_label = ttk.Label(window, text="")
result_label.pack(pady=10)

window.mainloop()
