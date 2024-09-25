import os
import shutil
from datetime import datetime


def organize_files(folder_path):
    """
    Organizes files in a Windows folder based on file type and creation date.
    """

    for filename in os.listdir(folder_path):
        # Ignore folders
        if os.path.isdir(os.path.join(folder_path, filename)):
            continue

        # Get file extension and creation date
        file_extension = os.path.splitext(filename)[1][1:].lower()
        file_creation_time = os.path.getctime(os.path.join(folder_path, filename))
        file_creation_date = datetime.fromtimestamp(file_creation_time).strftime(
            "%Y-%m-%d"
        )

        # Create destination folders if they don't exist
        destination_folder = os.path.join(folder_path, file_extension)
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        destination_subfolder = os.path.join(destination_folder, file_creation_date)
        if not os.path.exists(destination_subfolder):
            os.makedirs(destination_subfolder)

        # Move file to destination
        source_path = os.path.join(folder_path, filename)
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


if __name__ == "__main__":
    folder_to_organize = input(
        "Enter the full path of the folder you want to organize: "
    )
    organize_files(folder_to_organize)
    print("Files organized successfully!")
