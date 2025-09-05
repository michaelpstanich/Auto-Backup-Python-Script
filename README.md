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

This is a simple python script I made for myself which scans a source and backup directory for changes made in the source directory, then attempts to backup files by moving conflicting files out of the backup folder and copying over the source files. The primary feature of this script is using windows .lnk (shortcuts) to designate folders to recursively backup, and an 'only back-up what's changed' methodology where conflicting alterations in the backup folder is moved into a time-stamped discard folder before copying source (saving space when compared to backing up the entire directory as a unit).

### Requirements :

- Windows 10+ (Currently designed for Win11, not coded for other platforms)
- Python 3.8+ on PATH (if using .bat files)
- pywin32 optional package

### Features :

- Scan a source directory and copy files to a backup directory to 'sync' the directories
- Backup files that would be deleted or overwrite are instead moved into a time-stamped 'discard' directory for loose versioning and saving space (only stores files changed, not the entire directory)
- Configurable directories and some parameters within the python script to edit yourself
- Print-out (terminal) for file/directory changes
- Easy to use (shortcut).lnk method for designating directories to update (a simpole alt+ drag into the backup_shortcuts folder and it's already set-up to backup!)
- When using .lnk files to designate source directories, rename the shortcut to rename the name of the backup folder

### Limitations :

- Has no 'undo/backtrack' functionality or any versioning, changes are one-shot and can't be undone (files should be moved into the designated discard directory before any overwrites would take place, but still take pre-cautions!)
- Script will fail and stop if there are any issues scanning/moving/copying files (this is to prevent undefined behavior and data loss)
- No logging or config files, everything is contained directly in the script at the moment
- No sanity checks on configured directories, meaning common mistakes are possible
- Does not lock files from editing, so anything changed while the script is running but hasn't been backed up yet will reflect active changes (or may even outright fail to sync with cloud virtual drives like Google Drive)

### My Use-Case :  

The reason I made this script is because auto-backup tools would run into issues with file permissions and constantly cause certain tools to break if they tried to sync while I was working. This script works around these issues by moving on a per-file basis and only ever 'reads' files in the source directory without ever tryign to 'lock' them, as well as only runs when I specifically set it to. Using .lnk files is also quick and easy to create and modify; as I often forget manual backups, this is quite easy to set-up and modify as needed. My personal use case is to have this script (optionally) backup to my local backup, then also set the backup to sync to Google Drive via the virtual drive using the desktop app.

### How To Use :

- First open the "Auto-Backup-Python-Script.py" file inside any text editor and configure the paths and parameters as you see fit.
- Now place any shortcuts to the folders you wish to backup into the provided "backup_shortcuts" folder and name them whatever you want the backup folder to be.
- Afterward you can double click the provided "RunBackup.bat" to initiate the backup via terminal. (Note : "_NoPause" versions are provided which comment out the pause function so the script runs without needing any user input after initialization. By default, the script will get the directories and print them to the console for the user to confirm before running the actual backup)
- Wait until the script finishes, if enabled any files moved/copied will print out their source and destination
- Once complete you can close the terminal window, if backing up to the cloud via virtual drive, please allow time for the files to properly sync before messing with files to prevent issues.

### Notes :
- Remember to review the directories the script shows after initializing to ensure things are moving in the correct direction and into the correct place
- The backup can be aborted at any point by closing the terminal, terminating the program. Changes already made will still apply.
- Script has a pause function at the end, meaning if you run this automatically it will still remain open for review if need be.

***

Licensed and Distributed under MIT License