# NoStealer

NoStealer is an application based on Python designed to silently copy folders from Windows 7+ systems to a USB drive.

## Features:

1. **Silent Operation**: The application runs in the background and does not notify the user until a USB drive is
   inserted.
2. **Customizable Targets**: Specify which folders on the system you want to copy.
3. **Automatic USB Detection**: When a USB drive is plugged in, the program will automatically detect it, copy the
   targeted folders, and then notify the user.
4. **Notifications**: Provides optional Windows toast notifications for various actions, such as when a folder is added
   or if it's already on the target list.

### Emphasis:

- Files are synced in one direction. Even if the source folder is deleted, the data remains in local data storage. To
  completely remove it, delete the corresponding folder in local data storage.
- Modifications to the source file will overwrite the data file, but if the source file is deleted, the data file
  remains.
- The program operates silently and, when it detects a specified USB drive configuration, it automatically copies files.
  After copying, it notifies the user via a Windows desktop notification, displaying the copied files.
- For completely silent operation, please modify the configuration file `NoStealer\data\settings.json`.

## How to Use:

1. **Deployment**:
    - Download the latest release.
    - Extract the NoStealer application to a directory.

2. **Adding Folders**:
    - Use `add_path.py` with folder paths as arguments to add them to the target list. This script will notify you to
      confirm the addition or if the path already exists.

3. **Running NoStealer**:
    - Execute `launcher.bat`. The program will begin monitoring the specified target folders and copy them to a USB
      drive when detected.

4. **Customizing Settings**:
    - Customize your preferences in the configuration file `NoStealer\data\settings.json`:
        - `data_folder`: Location of the local data storage. Default is `D:\CodeProjects\PythonProjects\NoStealer\data`.
        - `usb_drive_folder_rel_path`: The relative path on the USB drive where the data will be stored. Default
          is `".\\NoStealerData"` (`.` represents the drive letter, e.g., `F:\`).
    - Manually specify target folders in `targets.txt` (one folder path per line).

## Important Paths:

- **Local Data Storage**: `D:\CodeProjects\PythonProjects\NoStealer\data`
- **USB Data Path**: `.\\NoStealerData`

## Note:

- Ensure that the user running the application has the necessary permissions to access the target folders.

## Credits:

- Developed by [Noob-0-GitHub](https://github.com/Noob-0-GitHub/NoStealer).
