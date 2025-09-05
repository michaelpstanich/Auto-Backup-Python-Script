# Requires Python 3.8+
import os
import glob
import win32com.client # pip install pywin32
import shutil
import filecmp
import datetime

# # # # # # # # # # # #
# # # Develped by Michael "Spirit Shard" Stanich - michaelpstanich.com
# # # Auto-Backup-Python-Script v0.1
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
# # # Below are a few parameters you should modify to fit your needs, currently they are filled out to my own personal set-up!
# # # 

# script_dir : Current working directory of the python script, so we can grab the relative folder for backup shortcuts.
script_dir = os.path.dirname(__file__)

# shortcutes_dir : Relative folder for the 'to backup' shortcuts folder
shortcuts_dir = os.path.join(script_dir, "Backup_Shortcuts")

# backup_dir : Where to copy the files to for backup. Should set this to either your backup drive or a virtual drive for cloud syncing.
backup_dir = "./backup_dir" # Example "Q:/My Drive/Auto-Backups"

# discard_dir : Where 'discarded' files should go. Discarded files should include files removed from source but are still found in the backup, and any files from backup that are out-dated.
discard_dir = "./discard_dir" # Example "Q:/My Drive/Auto-Backups/_Discarded_"

# followsymlink : Whether the backup process should follow symlinks and backup those as well, set to false by default since symlinks can be used to reference files under multiple direcotries (I use this often enough in my workflow, just remember to also backup your symlink source folders if you do as well! May also want to change to True if you are creating backups for a team so that the backup for the project contains all the needed files.)
followsymlink = False

# report_files : Whether we should print out reports on files backed up or discarded
report_files = True

# report_dir : Whether we should report on prepared directories and what directories are being scanned
report_dir = False

linebreak = " - - - - - - - - - - - - - - - - - - - - " # Style of line-break used in report print
minbreak = " - " # Style of small line-break used in report print

# # #
# # # !!! Do not modify below this line unless you know what you're doing !!!
# # # # # # # # # # # #

# Get shell so we can use it for shortcut targets
shell = win32com.client.Dispatch("WScript.shell")


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
    return (str(time_now.year) + "-" + str(time_now.month) + "-" + str(time_now.day) + "_" + str(time_now.hour) + "_" + str(time_now.minute) + "_" + str(time_now.second))
#end

def BackupDirectory(root_path="", source_path="", backup_path="."):
    
    printrep_dir(minbreak)
    printrep_dir("Backing up source folder " + source_path + " into " + backup_path)
    #printrep("root_path = "+ root_path)
    #printrep("source_path = " + source_path)
    #printrep("backup_path = " + backup_path)
    #discard_path = os.path.join(discard_dir, (backup_path.replace(backup_dir, "").removeprefix("\\") + "/" + timestamp))
    discard_path = (os.path.join(os.path.join(discard_dir, timestamp), backup_path.replace(backup_dir, "").removeprefix("\\")))
    #printrep("discard_path = " + discard_path)

    if root_path == "" or not os.path.exists(root_path):
        print("Provided root path is invalid = " + root_path)
        return
    #end

    if source_path == "" or not os.path.exists(source_path):
        print("Provided source path is invalid = " + source_path)
        return
    #end

    if not os.path.exists(backup_path):
        print("Backup path did not exist, creating backup path = " + backup_path)
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
            printrep_files("> > > > > Discarding " + file_path + " -> " + discard_path)
            shutil.move(file_path, discard_path)
        #end
    #end

    # Backup any files that are only in the source directory
    for file in dir_compare.left_only:
        file_path = os.path.join(source_path, file)
        if os.path.isfile(file_path):
            printrep_files("> > > > > Backing " + file_path + " -> " + backup_path)
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
                printrep_files("> > > > > Backing " + file_path + " -> " + backup_path + " (" + old_backup_path + " -> " + discard_path + ")")
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
                BackupDirectory(root_path=root_path, source_path=entry.path, backup_path=subdir_path)
            #end
        #end
    #end
#end

# Startup Code
printrep_files(linebreak)
print("Preparing Auto-Backup process!")
print("Running from " + script_dir)
print("Backup links folder = " + shortcuts_dir)
print("Copy folder = " + backup_dir)
print("Discard folder = " + discard_dir)
print(linebreak)
#os.system("pause")
print("Begining Auto-backup process!")


timestamp = GetCurrentTimeString()

for x in glob.glob(shortcuts_dir + "\\*.lnk", recursive=True):
    x_backuplinkname = os.path.basename(x)
    x_shortcut = shell.CreateShortcut(x)
    printrep_dir('Scanning and Backing up = ' + x_shortcut.Targetpath)
    print("Following backup link and processing " + x_backuplinkname)
    BackupDirectory(root_path=x_shortcut.Targetpath, source_path=x_shortcut.Targetpath, backup_path=os.path.join(backup_dir, x_backuplinkname.removesuffix(".lnk")))
    printrep_files(linebreak)
#end
print("Backup script complete (assuming no errors), please allow time for any cloud sync to take place before modifying backup.")
os.system("pause")