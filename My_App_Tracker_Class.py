import os
import re
import shutil
import schedule
import time
from datetime import datetime

class application_tracker(object):
    def __init__(self, source_directory, destination_directory):
        self.source_directory = source_directory
        self.destination_directory = destination_directory

    def return_file_names(self, source_directory):
        f_name = []
        if os.path.isdir(source_directory):
            try:   
                for dirpath, dirname, filenames in os.walk(source_directory):
                    for filename in filenames:
                        f_name.append(filename)
            except Exception:
                print("Folder is empty")
        return f_name
            
    def get_indexes(self, string):
        count = []
        for index, val in enumerate(string):
            if '.' in val:
                count.append(index)
        return count[-1]
    
    def if_file_exists(self, pattern, source_directory):
        file_names = self.return_file_names(source_directory)
        for files in file_names:
            if re.search(pattern, files):
                os.chdir(source_directory)
                splitted_name = files.split('_') # pull out underscores from file name 
                return splitted_name

    def organize_folder_names(self, source_directory):
        folder_names = {}
        list_of_names = self.if_file_exists(r'CV', source_directory)
       # creation_time = str(Time).replace(":", ".")
        if list_of_names[-1].endswith(".pdf"):
            end_index = self.get_indexes(list_of_names[-1])
            folder_names['Company Folder'] = list_of_names[-1][:end_index]
        job_title = list_of_names[-2]
        folder_names['Job Folder'] = job_title + str(' ')# + creation_time
        return folder_names

    def make_dirs(self, destination_directory, source_directory):
        folder_dict = self.organize_folder_names(source_directory)
        to_there = str(folder_dict['Company Folder'])+r'/'+str(folder_dict['Job Folder'])
        changeDirectory = os.chdir(destination_directory)
        try:
            make_directories = os.makedirs(to_there)
        except FileExistsError:
            print("Couldn't create because folder with name " + str(folder_dict['Job Folder']) + "already exists")

    def transfer_files(self, source_directory, destination_directory):
        try: 
            application_files = os.listdir(source_directory)
            folders = self.organize_folder_names(source_directory)
            destination_dir = destination_directory + r'/' + str(folders['Company Folder'])+r'/'+str(folders['Job Folder'])
            print('url is: ' + destination_dir)
            for files in application_files:
                if os.path.isdir(source_directory): 
                    shutil.move(source_directory+files, destination_dir)
        except FileExistsError:
            print("No files were found")
        

########################## MAIN PROGRAM ##########################################################################################

source = '/Users/jayan/Documents/PythonProjects/My_Application_Tracker/Origin/'

destination = '/Users/jayan/Documents/Jobs_Applied'

app_object = application_tracker(source, destination)

app_object.organize_folder_names(source)   
        
app_object.make_dirs(destination, source)

app_object.transfer_files(source, destination)
