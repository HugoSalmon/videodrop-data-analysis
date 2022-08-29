

from videodrop.list_videodrop_files import list_videodrop_files_in_directory
from videodrop.read_videodrop_files import read_result_file


from pathlib import Path
import numpy as np
import pandas
import statsmodels.api as sm



def extract_videodrop_experiment_measures(data_path, dilution_prefix="dilution"):

    files_dic = list_videodrop_files_in_directory(data_path)

    sorted_name_experiments = sorted(list(files_dic.keys()))

    if len(sorted_name_experiments)==0:
        return [], None, None
    
    general_informations_attributes = []
    list_tables_size_intensity = []
    
    dilutions = []
        
    for i, name_experiment in enumerate(sorted_name_experiments):
        
        try:
            splitted = name_experiment.split(" ")
            dilution_string = [s for s in splitted if dilution_prefix in s][0]
            dilution_factor = int(dilution_string.replace(dilution_prefix,""))
            print(name_experiment, dilution_factor)
            dilutions.append(dilution_factor)
        except:
            print("Warning, no dilution factor found, set to 1")
            dilution_factor = 1
            dilutions.append("Not found")


        results_file = files_dic[name_experiment]["results_file"]

        results_data, general_description_table = read_result_file(results_file)

        
        raw_sizes = []
        ponderated_sizes = []
        raw_intensities = []
        ponderated_intensities = []
        
        for k in range(len(results_data)):
            raw_sizes += [results_data["diameter"].iloc[k]]
            ponderated_sizes += [results_data["diameter"].iloc[k]] * (results_data["length"].iloc[k] + results_data["jumps"].iloc[k]) 
            # on pondère par le nombre de frames où la particule était là même si on ne l'a pas détectée

            raw_intensities += [results_data["intensity"].iloc[k]]            
            ponderated_intensities += [results_data["intensity"].iloc[k]] * (results_data["length"].iloc[k] + results_data["jumps"].iloc[k]) 


        step_videodrop = 10
        bins_size = np.arange(0,1000+step_videodrop,step_videodrop)

        step_videodrop_intensity = 1
        bins_intensity = np.arange(0,800+step_videodrop_intensity,1)

          
        bin_diffs_size = bins_size[1:] - bins_size[:-1]  
        bin_centers_size = bins_size[1:] - bin_diffs_size/2
         
        values_ponderated, _ = np.histogram(ponderated_sizes, bins=bins_size, density=True)
        values, _ = np.histogram(raw_sizes, bins=bins_size, density=True)
        
 
        bin_diffs_intensity = bins_intensity[1:] - bins_intensity[:-1]  
        bin_centers_intensity = bins_intensity[1:] - bin_diffs_intensity/2
                 

        density_estimator = sm.nonparametric.KDEMultivariate(data=raw_sizes, var_type='c', bw='cv_ls')
        estim_dens_raw_sizes = density_estimator.pdf(bin_centers_size)

        density_estimator = sm.nonparametric.KDEMultivariate(data=ponderated_sizes, var_type='c', bw='normal_reference')
        estim_dens_ponderated_sizes = density_estimator.pdf(bin_centers_size)

        
        intensities_ponderated_values, _ = np.histogram(ponderated_intensities, bins=bins_intensity)
        intensities_values, _ = np.histogram(raw_intensities, bins=bins_intensity, density=True)
        
        
        

        # normal_reference: normal reference rule of thumb (default)

        # cv_ml: cross validation maximum likelihood

        # cv_ls: cross validation least squares


        
        size_table = pandas.DataFrame(np.array([bin_centers_size, values, values_ponderated, estim_dens_raw_sizes, estim_dens_ponderated_sizes]).T, columns = ["Bin centre (nm)", "N particles (normalized)", "N particles (ponderated & normalized)", "Size density estimation", "Size density estimation (ponderated)"])
        size_table.columns = [col+" "+name_experiment if col!="Bin centre (nm)" else col for col in size_table.columns]
        
        intensity_table = pandas.DataFrame(np.array([bin_centers_intensity, intensities_values, intensities_ponderated_values]).T, columns = ["Bin centre (nm)", "N particles (normalized)", "N particles (ponderated & normalized)"])
        intensity_table.columns = [col+" "+name_experiment if col!="Bin centre (nm)" else col for col in intensity_table.columns]
        
        size_intensity_2D_histogram, _, _ = np.histogram2d(x=raw_sizes, y=raw_intensities, bins=[bins_size, bins_intensity], density=True)

        ponderated_size_intensity_2D_histogram, _, _ = np.histogram2d(x=ponderated_sizes, y=ponderated_intensities, bins=[bins_size, bins_intensity], density=True)


        size_intensity_table = pandas.DataFrame(np.array(size_intensity_2D_histogram), 
                                                columns = bin_centers_intensity,
                                                index=bin_centers_size)

        
        if i==0:
            concatenated_table_size = size_table
            concatenated_table_intensity = intensity_table

        else:
            size_table.drop("Bin centre (nm)", axis=1, inplace=True)
            concatenated_table_size = pandas.concat([concatenated_table_size, size_table], axis=1)
            intensity_table.drop("Bin centre (nm)", axis=1, inplace=True)

            concatenated_table_intensity = pandas.concat([concatenated_table_intensity, intensity_table], axis=1)

        list_tables_size_intensity.append(size_intensity_table)


        general_informations_attributes.append(general_description_table.values[:,0].tolist())

    general_informations_attributes = pandas.DataFrame(np.array(general_informations_attributes), columns=list(general_description_table.index))    
    
    general_informations_attributes.index = sorted_name_experiments
    
    size_concentration_attributes = general_informations_attributes[[col for col in general_informations_attributes if "particles" not in col and "videos" not in col]]
    n_particles = general_informations_attributes[[col for col in general_informations_attributes if "particles" in col or "videos" in col]]
    
    
    
    return sorted_name_experiments, dilutions, concatenated_table_size, concatenated_table_intensity, list_tables_size_intensity, size_concentration_attributes, n_particles


