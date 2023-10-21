# NoStealer 使用说明

## 描述:

NoStealer 是一个Python应用程序，设计用于从Windows 7+系统静默地复制文件夹到USB驱动器

## 功能:

1. **静默操作**: 该应用程序在后台运行，在U盘插入前不会通知用户
2. **可自定义目标**: 指定系统上应复制的文件夹
3. **自动检测USB**: 当插入USB驱动器时，程序将自动检测并复制目标文件夹，并且通知用户
4. **通知**: 对于各种操作（例如，当文件夹被添加或已存在于目标列表中）提供可选的Windows弹窗通知

### 强调

- 文件单向同步，即使源文件夹删除，数据仍然保留在本地数据存储中，完全删除请删除本地数据存储中的对应文件夹
- 源文件修改会覆盖数据文件，但是源文件删除时数据文件保留
- 程序静默运行，并在检测到指定配置U盘时，自动复制文件，复制后使用Windows桌面通知通知用户并显示拷贝的文件
- 如需程序完全静默运行，请修改配置文件`NoStealer\data\settings.json`

## 使用方法:

1. **部署**:
    - 下载最新发行版
    - 将NoStealer应用程序解压到在一个目录中

2. **添加文件夹**:
    - 使用带有文件夹路径作为参数的`add_path.py`将它们添加到目标列表。此脚本提供通知以确认添加或路径已存在

3. **运行NoStealer**:
    - 执行`launcher.bat`。程序将开始监控指定的目标文件夹，并在检测到USB驱动器时将它们复制到其中

4. **自定义设置**
    - 在配置文件`NoStealer\data\settings.json`中自定义您的设置:
        - `data_folder`: 本地数据存储的位置，默认为`D:\CodeProjects\PythonProjects\NoStealer\data`
        - `usb_drive_folder_rel_path`: 在USB上存储数据的相对路径，默认为`".\\NoStealerData"`(`.`表示盘符，如`F:\`)
    - 在`targets.txt`中手动指定目标文件夹（每行一个文件夹路径）

## 重要路径:

- **本地数据存储**: `D:\CodeProjects\PythonProjects\NoStealer\data`
- **USB数据路径**: `.\\NoStealerData`

## 注意:

- 确保运行应用程序的用户具有访问目标文件夹所需的权限

## 贡献者:

- 由[Noob-0-GitHub](https://github.com/Noob-0-GitHub/NoStealer)开发
