# Auto-Backup-Python-Script

Created by Michael "Spirit Shard" Stanich

Website - https://michaelpstanich.com/  
Discord (The Broken Chatbox) - https://discord.gg/h3vB7S4FEw

**v-- Donations! =^.^= --v**  
Ko-Fi - https://ko-fi.com/michaelpstanich  
SubscribeStar - https://subscribestar.adult/michaelpstanich

***

## !!! WARNING !!!

This script moves and copies files around! Ensure you know what you're doing before deploying this script with anything important! I am not responsible for any damage caused by this script or any damage done by any modifications/configurations of the script!

This script should only be used as a secondary backup method, combine this with typical manual backups to ensure things are secured!

***

## Auto-Backup-Python-Script

This is a simple python script I made for myself which scans a source and backup directory for changes made in the source directory, then attempts to backup files by moving conflicting files out of the backup folder and copying over the source files. The primary goal of this script is to create a quick and simple back-up system to run between work sessions. This script follows an 'only back-up what's changed' methodology where conflicting alterations in the backup folder is moved into a time-stamped discard folder before copying source (saving space when compared to backing up the entire directory as a unit or storing a database of changes), making it easy to manage manually should you wish to do so, or create automatic scripts to assist.

### Requirements :

- Windows 10+ (Currently designed for Win11, not coded for other platforms)
- Python 3.8+ on PATH (if using the included .bat files)
- pywin32 optional package

### Features :

- Scan a source directory and copy files to a backup directory to 'sync' the directories
- Backup files that would be deleted or overwrite are instead moved into a time-stamped 'discard' directory for loose versioning and saving space (only stores files changed, not the entire directory)
- Configurable directories and some parameters within the user.ini configuration file
- Print-out (terminal) for file/directory changes to manually track changes or report to a log when ran through another script
- Easy to use (shortcut).lnk method for designating directories to update (a simpole alt+ drag into the backup_shortcuts folder and it's already set-up to backup!)
- When using .lnk files to designate source directories, rename the shortcut to rename the name of the backup folder
- Define folders to backup in a .txt file with a simple to read and edit format, with comments supported

### Limitations :

- Has no 'undo/backtrack' functionality or any versioning, changes are one-shot and can't be undone (files should be moved into the designated discard directory before any overwrites would take place, but still take pre-cautions!)
- Script will fail and stop if there are any issues scanning/moving/copying files (this is to prevent undefined behavior and data loss)
- No logging files, so changes must be tracked with an external script or manually
- No sanity checks on configured directories, meaning common mistakes are possible, ensure paths are valid before running
- Does not lock files from editing, so anything changed while the script is running but hasn't been backed up yet will reflect active changes, usually best to run when not working on files to ensure everything is backed up properly.

### My Use-Case :  

The reason I made this script is because auto-backup tools would run into issues with file permissions and constantly cause certain tools to break if they tried to sync while I was working. This script works around these issues by moving on a per-file basis and only ever 'reads' files in the source directory without ever trying to 'lock' them, as well as only runs when I specifically set it to. As I often forget manual backups, this is quite easy to set-up and modify as needed. My personal use case is to have this script (optionally) backup to my local backup, then also set the backup to sync to Google Drive via the virtual drive using the desktop app.

### Configuration Options

Config settings are located inside the default.ini provided with the script, you can create your overwrites inside the user.ini file.

\[Pathing\]  
**shortcuts_dir**  
Relative folder for the 'to backup' shortcuts folder  

**textlist_dir**  
Relative folder for the 'to backup' text file lists  

**backup_dir**  
Where to copy the files to for backup. Should set this to either your backup drive or a virtual drive for cloud syncing  

**discard_dir**  
Where to copy the files to for backup. Should set this to either your backup drive or a virtual drive for cloud syncing

\[Behavior\]  
**follow_shortcut**  
Follow .lnk files in the shortcuts directory to backup

**follow_textlist**  
Follow paths found in the txt file directory to backup

**followsymlink**  
Whether the backup process should follow symlinks and backup those as well, set to false by default since symlinks can be used to reference files under multiple direcotries (I use this often enough in my workflow, just remember to also backup your symlink source folders if you do as well! May also want to change to True if you are creating backups for a team so that the backup for the project contains all the needed files.)

**folderslashreplace**  
Replaces lines of the path when auto-generating folder names from paths

\[Printout\]  
**report_files**  
Whether we should print out reports on files backed up or discarded

**report_dir**  
Whether we should report on prepared directories and what directories are being scanned

**linebreak**  
Style of line-break used in report print

**minbreak**  
Style of small line-break used in report print

### How To Use :

- First open the "user.ini" file inside any text editor and configure the paths and parameters as you see fit. (Look inside the "Auto-Backup-Python-Script.py" script to see the configuration comments if required)
- Inside the backup_links folder (unless changed from default), create a .txt file with the paths to backup and/or create .lnk shortcuts of folders to backup
- Double check and manually validate all paths are valid
- Afterward you can double click the provided "RunBackup.bat" to initiate the backup via terminal (cmd.exe or powershell depending on system configuration), this will copy files to the configured backup directory and move non-existing or overwrite files to the configured Discard folder.
- Wait until the script finishes, if enabled any files moved/copied will print out their source and destination
- Once complete you can close the terminal window, if backing up to the cloud via virtual drive, please allow time for the files to properly sync before messing with files to prevent issues.

### Notes :
- Remember to review the directories the script shows after initializing to ensure things are moving in the correct direction and into the correct place
- The backup can be aborted at any point by closing the terminal, terminating the program. Changes already made will still apply.
- Script has a pause function at the end, meaning if you run this automatically it will still remain open for review if need be.

***

Licensed and Distributed under MIT License