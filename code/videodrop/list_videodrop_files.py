









import numpy as np
from paths import datapath
from pathlib import Path
import os






def list_videodrop_files_in_directory(directory_path, raw_suffix="_1"):
    
    # list_elements = os.listdir(directory_path)
    
    # list_elements = []
    # for (dirpath, dirnames, filenames) in os.walk(directory_path):
    #     list_elements += [os.path.join(dirpath, file) for file in filenames]


    # path_dic = {element: Path(directory_path, element) for element in list_elements 
    #             if os.path.isfile(Path(directory_path, element))}

    # list_dirs = [element for element in list_elements if os.path.isdir(Path(directory_path, element))]

    # for dir_ in list_dirs:
    #     list_elements = os.listdir(Path(directory_path, dir_))
    #     path_dic.update({element:Path(directory_path, dir_, element) for element in list_elements 
    #                      if os.path.isfile(Path(directory_path, dir_, element))})



    path_dic = {}
    list_dir = []
    for (dirpath, dirnames, filenames) in os.walk(directory_path):
        list_dir += dirnames
        for file in filenames:
            path_dic[file] = Path(dirpath, file)
            
            


    experiments = [file.replace("-Results.csv","") for file in path_dic 
                    if "-Results.csv" in file and "~lock" not in file]

    files_dic = {}

    for experiment in experiments:
        
        experiment_root = experiment

        result_file =  path_dic[experiment + "-Results.csv"]

        files_dic[experiment_root] = {"results_file":result_file}

    return files_dic






if __name__=="__main__":
    
    lea_data_path = Path(datapath, "Data Lea NTA Videodrop", "02022021 Vt=1,5ml/Videodrop 02022021 Vt=1,5ml")
    
    files_dic = list_videodrop_files_in_directory(lea_data_path)
