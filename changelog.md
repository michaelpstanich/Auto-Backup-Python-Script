v0.3
- Added "folderslashreplace" config setting, sets what slashes in filepaths are replaced with when auto-generating names
- Changed default "/" replacement to "-", removing the spaces on both sides to prevent the path increasing length
- Added config parsing, configuration is now stored in default.ini and user.ini
- - default.ini stores the default configuration and will overwrite on pull
- - user.ini is for user overwrites, copy from default.ini and change your settings, is part of .gitignore
- - Config addition changed some settings, default locations start on C: now, please configure before use
- Vastly improved information print-out, now splits across multiple times and reads much more cleanly
- Changed so line breaks will show after every directy is checked even if reports are disabled, helping to show progress
- Changed discard path to now leads to the defined backup path name, then timestamp, then recursive backup files
- - Was {timestamp} / {BackupName} / {FoldersAndFiles}
- - Is now {BackupName} / {timestamp} / {FoldersAndFiles}
- - This makes it much easier to manage backups manually and makes automatic processes easier to parse
- Changed timestamp to display with Y/M/S/h/m/s prefixing thier values to make tiemstamp easier to read

v0.2
Added .txt support with name definitions (Path|Name)
	Scans each line to find a file path, use | after the file path to define the name of the backup folder
	Start a line with # to create a comment (Must be at the start of a line)
	Invalid characters for a folder will cause an error and should stop the script
	Will skip emtpy and comment lines
Changed default shortcut/text folder to "backup_links"
Removed "NoPause" variant, users can customize script to create this functionality

v0.1
Initial release