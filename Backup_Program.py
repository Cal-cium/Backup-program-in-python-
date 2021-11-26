import shutil
from os import path, stat, walk, listdir
from os.path import exists

#notes on shutil
#This method is identical to shutil.copy() method but it also try to preserves the file’s metadata.
#Source must represent a file but destination can be a file or a directory.

def main():
    try:
        source_folder = "source-directory"
        destination_folder = "destination-directory"

        #copy any files in base directory first
        copy_files(source_folder, destination_folder)

        #now need to loop through the directories    
        folders = listdir(source_folder)
                        
        for folder in folders:            
            if path.isdir(path.join(source_folder, folder)):                      
                copy_directory(path.join(source_folder, folder), path.join(destination_folder, folder))            
            
        print("Finished")

    except Exception as ex:
         print(getattr(ex, 'message', repr(ex)))
    
def copy_files(source_folder, destination_folder ):
    """Copies all files in a directory to the destination folder"""
    
    file_names = next(walk(source_folder), (None, None, []))[2]  # [] if no file   

    for file_name in file_names:
        #create filename
        source = path.join(source_folder, file_name)
        destination = path.join(destination_folder, file_name)

        #copy file
        if (
            exists(destination)
            and stat(source).st_mtime - stat(destination).st_mtime <= 0
        ):               
            continue  #file does exist but is newer than the file in the source directory, so won't copy
              
        shutil.copy2(source, destination)
        print (f"{file_name} has been copied to {destination_folder}")                                          
     
def copy_directory(source_folder, destination_folder):
    """Copies directories and uses recursion to copy directories inside other directories"""
    
    if exists(destination_folder):
        #copy any files in current directory
        copy_files(source_folder, destination_folder)
    
        folders = listdir(source_folder)
        for folder in folders:
            if path.isdir(path.join(source_folder, folder)):
                copy_directory(path.join(source_folder, folder), path.join(destination_folder, folder))   
    else:            
        shutil.copytree(source_folder, destination_folder)
        
if __name__ == "__main__":
    main()