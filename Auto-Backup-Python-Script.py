# Requires Python 3.8+
import os
import glob
import win32com.client # pip install pywin32
import shutil
import filecmp
import datetime
import configparser

#
# #
# # #
# # # # # # # # # # # #
# # # Develped by Michael "Spirit Shard" Stanich - michaelpstanich.com
# # # Auto-Backup-Python-Script v0.3
# # #
# # # - - - - - - - - - - - - - - - - - - - - - - - - - - -
# # # !!! PLEASE BE EXTREMELY CAREFUL USING THIS SCRIPT !!!
# # #
# # # This script moves and copies files!
# # # If mis-configured,
# # # files could move into folders in a destructive way
# # # or even overwrite existing files, causing data loss
# # # 
# # # Please be extremely careful and please vet this code before use!
# # # (please test the script and your configuration on a simple test set-up before real files)
# # # - - - - - - - - - - - - - - - - - - - - - - - - - - -
# # # 
# # #
# # # !!! Do not modify below this line unless you know what you're doing !!!
# # # # # # # # # # # #
# # #
# #
#

# # # Config Reading Section

# script_dir : Current working directory of the python script, so we can grab the relative folder for backup shortcuts
script_dir = os.path.dirname(__file__)

# Load the config files using config parser, start with default then user overwrite ini
config = configparser.ConfigParser()
config.read(os.path.join(script_dir, 'default.ini'))
config.read(os.path.join(script_dir, 'user.ini'))

# Follow .lnk files in the shortcuts directory to backup
follow_shortcut = config.getboolean('Behavior', 'follow_shortcut', fallback=True)

# shortcutes_dir : Relative folder for the 'to backup' shortcuts folder
shortcuts_dir = os.path.join(script_dir, config.get('Pathing', 'shortcuts_dir', fallback="backup_links"))

# textlist_dir : Relative folder for the 'to backup' text file lists
textlist_dir = os.path.join(script_dir, config.get('Pathing', 'textlist_dir', fallback="backup_links"))

# Follow paths found in the txt file directory to backup
follow_textlist = config.getboolean('Behavior', 'follow_textlist', fallback=True)

# backup_dir : Where to copy the files to for backup. Should set this to either your backup drive or a virtual drive for cloud syncing
backup_dir = config.get('Pathing', 'backup_dir', fallback="C:/Auto-Backups")

# discard_dir : Where 'discarded' files should go. Discarded files should include files removed from source but are still found in the backup, and any files from backup that are out-dated
discard_dir = config.get('Pathing', 'discard_dir', fallback="C:/Auto-Backups/_Discarded_")

# followsymlink : Whether the backup process should follow symlinks and backup those as well, set to false by default since symlinks can be used to reference files under multiple direcotries (I use this often enough in my workflow, just remember to also backup your symlink source folders if you do as well! May also want to change to True if you are creating backups for a team so that the backup for the project contains all the needed files.)
followsymlink = config.getboolean('Behavior', 'followsymlink', fallback=False)

# report_files : Whether we should print out reports on files backed up or discarded
report_files = config.getboolean('Printout', 'report_files', fallback=False)

# report_dir : Whether we should report on prepared directories and what directories are being scanned
report_dir = config.getboolean('Printout', 'report_dir', fallback=False)

# Replaces lines of the path when auto-generating folder names from paths
folderslashreplace = config.get('Printout', 'folderslashreplace', fallback="-")

# Style of line-break used in report print
linebreak = config.get('Printout', 'linebreak', fallback="- - - - - - - - - - - - - - - - - - - -")

# Style of small line-break used in report print
minbreak = config.get('Printout', 'minbreak', fallback="-")

# Get shell so we can use it for shortcut targets
shell = win32com.client.Dispatch("WScript.shell")


# # # Define Functions Section

def printrep_files(printout=""):
    if report_files:
        print(printout)
    #end
#end

def printrep_dir(printout=""):
    if report_dir:
        print(printout)
    #end
#end

def GetCurrentTimeString():
    time_now = datetime.datetime.now()
    #return ("Y"+ str(time_now.year) + "-M" + str(f"{time_now.month:02d}") + "-D" + str(f"{time_now.day:02d}") + "_h" + str(f"{time_now.hour:02d}") + "_m" + str(f"{time_now.minute:02d}") + "_s" + str(f"{time_now.second:02d}"))
    return (str(time_now.year) + "-" + str(f"{time_now.month:02d}") + "-" + str(f"{time_now.day:02d}") + "_" + str(f"{time_now.hour:02d}") + "_" + str(f"{time_now.minute:02d}") + "_" + str(f"{time_now.second:02d}"))
#end

def BackupDirectory(root_path="", source_path="", backup_path=".", backup_name=""):
    
    printrep_dir(minbreak)
    printrep_dir("Backing up source folder " + source_path + " into " + backup_path)
    # Different versions of discard path handling, you can un-comment to try them if you wish
    #discard_path = os.path.join(discard_dir, (backup_path.replace(backup_dir, "").removeprefix("\\") + "/" + timestamp))
    #discard_path = (os.path.join(os.path.join(discard_dir, timestamp), backup_path.replace(backup_dir, "").removeprefix("\\")))
    #discard_path = (os.path.join(os.path.join(discard_dir, backup_path.replace(backup_dir, "").removeprefix("\\")), timestamp))
    discard_path = os.path.join(discard_dir, backup_name, timestamp, backup_path.replace(os.path.join(backup_dir, backup_name), "").removeprefix("\\"))

    if root_path == "" or not os.path.exists(root_path):
        print("Provided root path is invalid = " + root_path)
        return
    #end

    if source_path == "" or not os.path.exists(source_path):
        print("Provided source path is invalid = " + source_path)
        return
    #end

    if not os.path.exists(backup_path):
        print("Backup path did not exist")
        print(">>> creating backup path and backing up files")
        print(">>> " + backup_path)
        os.makedirs(backup_path)
    #end
    
    dir_compare = filecmp.dircmp(source_path, backup_path)

    # Move discarded files no longer in source from backup into discarded time-stamped folder
    if len(dir_compare.right_only) > 0:
        if not os.path.exists(discard_path):
            os.makedirs(discard_path)
        #end
        for file in dir_compare.right_only:
            file_path = os.path.join(backup_path, file)
            printrep_files("Discarding File")
            printrep_files(">>> From : "+ file_path)
            printrep_files(">>> To   : "+ discard_path)
            shutil.move(file_path, discard_path)
        #end
    #end

    # Backup any files that are only in the source directory
    for file in dir_compare.left_only:
        file_path = os.path.join(source_path, file)
        if os.path.isfile(file_path):
            printrep_files("Backing-Up File")
            printrep_files(">>> From : " + file_path)
            printrep_files(">>> To   : " + backup_path)
            shutil.copy2(file_path, backup_path, follow_symlinks=followsymlink)
        #end
    #end

    # Backup any files that are different between the source and backup directory, moving backups files into discarded directory
    if len(dir_compare.diff_files) > 0:
        if not os.path.exists(discard_path):
            os.makedirs(discard_path)
        #end
        for file in dir_compare.diff_files:
            file_path = os.path.join(source_path, file)
            if os.path.isfile(file_path):
                old_backup_path = os.path.join(backup_path, file)
                printrep_files("Backing-Up File")
                printrep_files(">>> From : " + file_path)
                printrep_files(">>> To   : " + backup_path)
                printrep_files(">>> >>> Discarding old")
                printrep_files(">>> >>> From : " + old_backup_path)
                printrep_files(">>> >>> To   : " + discard_path)
                shutil.move(old_backup_path, discard_path)
                shutil.copy2(file_path, backup_path, follow_symlinks=followsymlink)
            #end
        #end
    #end

    printrep_dir("Done with " + source_path + "")
    with os.scandir(source_path) as entries:
        for entry in entries:
            if entry.is_dir():
                subdir_path = os.path.join(backup_path, os.path.basename(entry.path))
                printrep_dir("Moving to subdirectory " + subdir_path)
                BackupDirectory(root_path=root_path, source_path=entry.path, backup_path=subdir_path, backup_name=backup_name)
            #end
        #end
    #end
#end



# Startup Code
print(linebreak)
print("Preparing Auto-Backup process!")
print("Running from " + script_dir)
print("Backup links folder = " + shortcuts_dir)
print("Copy folder = " + backup_dir)
print("Discard folder = " + discard_dir)
print(linebreak)
os.system("pause")
print(linebreak)
print("Begining Auto-backup process!")


timestamp = GetCurrentTimeString()

if follow_shortcut:
    for x in glob.glob(shortcuts_dir + "/*.lnk", recursive=True):
        x_backuplinkname = os.path.basename(x)
        x_shortcut = shell.CreateShortcut(x)
        printrep_dir('Scanning and Backing up = ' + x_shortcut.Targetpath)
        print("Following backup link and processing " + x_backuplinkname)
        BackupDirectory(root_path=x_shortcut.Targetpath, source_path=x_shortcut.Targetpath, backup_path=os.path.join(backup_dir, x_backuplinkname.removesuffix(".lnk")), backup_name=x_backuplinkname.removesuffix(".lnk"))
        print(linebreak)
    #end
#end

if follow_textlist:
    for x in glob.glob(textlist_dir + "/*.txt", recursive=True):
        print("Following and processing paths defined in " + os.path.basename(x))
        print(linebreak)
        with open(x) as file:
            while line := file.readline():
                if not line.startswith("#"):
                    linesplit = line.split("|")
                    x_path = linesplit[0].replace("\n", "")
                    if not x_path == "" and os.path.exists(x_path):
                        x_name = ""
                        if len(linesplit) > 1:
                            x_name = linesplit[1].replace("\n", "")
                        #end
                        if x_name == "":
                            x_name = x_path.replace(":", "").replace("\\", folderslashreplace).replace("/", folderslashreplace) 
                        #end
                        printrep_dir("Processing path = " + x_path)
                        BackupDirectory(root_path=x_path, source_path=x_path, backup_path=os.path.join(backup_dir, x_name), backup_name=x_name)
                        print(linebreak)
                    #end
                #end
            #end
        #end
    #end
#end

print("Backup script complete (assuming no errors), please allow time for any cloud sync to take place before modifying backup.")
os.system("pause")