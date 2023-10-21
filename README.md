# NoStealer

## Description:

NoStealer is a Python application designed to silently copy folders from Windows 7+ systems to a USB drive.

## Features:

1. **Silent Operation**: The application runs in the background without alerting the user.
2. **Customizable Targets**: Specify which folders on the system should be copied.
3. **Automatic USB Detection**: When a USB drive is inserted, the program will automatically detect it and copy the
   targeted folders.
4. **Notifications**: Provides optional Windows toast notifications for various actions (e.g., when a folder is added or
   already exists in the target list).

## How to Use:

1. **Setup**:
    - Download the re
    - Place the NoStealer application in a directory.
    - Customize your settings in `settings.json`:
        - `data_folder`: Where the copied data will be temporarily stored.
        - `usb_drive_folder_rel_path`: The relative path on the USB where the data will be stored.
    - Specify target folders in `targets.txt` (one folder path per line).

2. **Adding Folders**:
    - Use `add_path.py` with folder paths as arguments to add them to the target list. This script provides
      notifications to confirm the addition or if the path already exists.

3. **Running NoStealer**:
    - Execute `NoStealer.py`. The program will start monitoring the specified target folders and will copy them to a USB
      drive when detected.

## Important Paths:

- **Temporary Data Storage**: `D:\CodeProjects\PythonProjects\NoStealer\data`
- **USB Data Path**: `.\\NoStealerData`
- **Current Target Folders**:
    - `D:\Anthony-XKN\桌面\TargetFolder`

## Notes:

- Ensure that the user running the application has the necessary permissions to access the target folders.
- Always test on a non-critical system first to ensure desired behavior.

## Credits:

- Developed by [Noob-0-GitHub](https://github.com/Noob-0-GitHub/NoStealer)
