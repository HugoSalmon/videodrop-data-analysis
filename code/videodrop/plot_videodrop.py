
import numpy as np
import matplotlib.pyplot as plt








def plot_videodrop_size_distribution(concatenated_table_size, name, save_path_fig):

    fig, ax = plt.subplots(2, 1, figsize=(20,10))

    bin_centers = concatenated_table_size["Bin centre (nm)"].values
    bin_diffs = np.array([bin_centers[0]*2] + list(bin_centers[1:] - bin_centers[:-1]))
    bins =  [0] + list(bin_centers + bin_diffs/2)
    
    values = concatenated_table_size["N particles (normalized) "+name].values
    ponderated_values = concatenated_table_size["N particles (ponderated & normalized) "+name].values



    ax[0].hist(bin_centers, weights=values, bins=bins)
    ax[0].set_title("Raw sizes normalized histogram")
    ax[1].hist(bin_centers, weights=ponderated_values, bins=bins)
    ax[1].set_title("Ponderated sizes normalized histogram")

#        ax[0].legend(fontsize=13)
    ax[0].tick_params(axis="both", labelsize=13)
#        ax[1].legend(fontsize=13)
    ax[1].tick_params(axis="both", labelsize=13)
    

    density_estimation = concatenated_table_size["Size density estimation "+name].values
    ax[0].plot(bin_centers, density_estimation)

    density_estimation_ponderated = concatenated_table_size["Size density estimation (ponderated) "+name].values
    ax[1].plot(bin_centers, density_estimation_ponderated)

           
    fig.suptitle(name, fontsize=15)

    fig.tight_layout()
    fig.savefig(save_path_fig)
    
    plt.close(fig)
    
    
    
    
    
def plot_videodrop_size_distribution_replicates(concatenated_results, global_name, replicate_names, save_path_fig):
    
    fig, ax = plt.subplots(2, len(replicate_names)+1, figsize=(30,10), sharex=True, sharey=True)

    bin_centers = concatenated_results["Bin centre (nm)"].values

    bin_diffs = np.array([bin_centers[0]*2] + list(bin_centers[1:] - bin_centers[:-1]))
    bins =  [0] + list(bin_centers + bin_diffs/2)
            
    start = 0
    stop = len(bin_centers)
  
    for k, name in enumerate(replicate_names):

        values = concatenated_results["N particles (normalized) "+name]
        ponderated_values = concatenated_results["N particles (ponderated & normalized) "+name]

        ax[0,k].hist(bin_centers, weights=values, bins=bins, label="Raw sizes normalized histogram")
        ax[1,k].hist(bin_centers, weights=ponderated_values, bins=bins, label="Ponderated sizes normalized histogram")

        density_estimation = concatenated_results["Size density estimation "+name].values
        ax[0,k].plot(bin_centers, density_estimation)

        density_estimation_ponderated = concatenated_results["Size density estimation (ponderated) "+name].values
        ax[1,k].plot(bin_centers, density_estimation_ponderated)
        

        ax[0,k].set_title(name, fontsize=13)

        ax[0, k].legend(fontsize=13)
        ax[0, k].tick_params(axis="both", labelsize=13)
        
        ax[1, k].legend(fontsize=13)
        ax[1, k].tick_params(axis="both", labelsize=13)
  
    average_values = concatenated_results["Average of N particles (normalized) "+global_name]
    average_ponderated_values = concatenated_results["Average of N particles (ponderated & normalized) "+global_name]

    ax[0,-1].hist(bin_centers, weights=average_values, bins=bins, label="Raw sizes normalized histogram")
    ax[1,-1].hist(bin_centers, weights=average_ponderated_values, bins=bins, label="Ponderated sizes normalized histogram")

    mean_density_estimation = concatenated_results["Average of Size density estimation "+global_name].values
    ax[0,-1].plot(bin_centers, density_estimation)

    mean_density_estimation_ponderated = concatenated_results["Average of Size density estimation (ponderated) "+global_name].values
    ax[1,-1].plot(bin_centers, density_estimation_ponderated)
    
    ax[0,-1].set_title("Average over replicates", fontsize=13)

    ax[0, -1].legend(fontsize=13)
    ax[0, -1].tick_params(axis="both", labelsize=13)
    
    ax[1, -1].legend(fontsize=13)
    ax[1, -1].tick_params(axis="both", labelsize=13)

    fig.suptitle(global_name, fontsize=15)

    fig.tight_layout()
    fig.savefig(save_path_fig)
    plt.close(fig)
    
    
    


def plot_all_conds_videodrop(results_table, dic_exp, list_conds, size_concentration_attributes,
                              colors_time=None, lim_left=None, 
                              lim_right=None, savepath=None):


    fig, axes = plt.subplots(len(list_conds),2, figsize=(25,15), sharex=True, sharey=False)
            
    if len(list_conds)==1:
        ax = axes.reshape(1,-1)
    else:
        ax = axes
        
    colors = ["cyan", "dodgerblue", "darkblue", "orange", "tomato", "darkred"]    + ["cyan", "dodgerblue", "darkblue", "orange", "tomato", "darkred"]  + ["cyan", "dodgerblue", "darkblue", "orange", "tomato", "darkred"]  + ["cyan", "dodgerblue", "darkblue", "orange", "tomato", "darkred"]  

    colors += 5*colors

    bin_centers = results_table["Bin centre (nm)"].values
    bin_diffs = np.array([bin_centers[0]*2] + list(bin_centers[1:] - bin_centers[:-1]))
    bins =  [0] + list(bin_centers + bin_diffs/2)
        
    for i, key in enumerate(list_conds):
        
        for n, name in enumerate(dic_exp[key]):

            normalized_concentration = results_table["N particles (normalized) "+name].values

            ponderated_normalized_concentration = results_table["N particles (ponderated & normalized) "+name].values
                        
            c_totale = size_concentration_attributes.loc[name]["Total concentration"]
            
            # reliable = reliable_results.loc[name]["Is reliable"]
            
            if colors_time is not None:
                color = colors_time[n]
                
            else:
                color=colors[n]


            ax[i,0].plot(bin_centers, normalized_concentration, color=color, label=name + " C=%.2e"%c_totale+", normalized")  
                        
            ax[i,1].plot(bin_centers, ponderated_normalized_concentration, color=color, label=name + " C=%.2e"%c_totale+", ponderated and normalized")  


    for i in range(len(list_conds)):
        
        if lim_left is not None:
            ax[i,0].set_xlim(left=lim_left)
        if lim_right is not None:
            ax[i,0].set_xlim(right=lim_right)

        ax[i,0].legend(fontsize=13, loc="upper right")
        ax[i,1].legend(fontsize=13, loc="upper right")

        ax[i,0].set_ylabel("Concentration (Particles/ml)", fontsize=13)
            
        ax[i,0].tick_params(labelsize=13)
        ax[i,1].tick_params(labelsize=13)

        
    lims = [ax[i,0].get_ylim()[1] for i in range(len(list_conds))]

    for i in range(len(list_conds)):
        ax[i,0].set_ylim([0,np.max(lims)])
    
    lims_normalized = [ax[i,1].get_ylim()[1] for i in range(len(list_conds))]

    for i in range(len(list_conds)):
        ax[i,1].set_ylim([0,np.max(lims_normalized)])
        
        
    ax[-1,0].set_xlabel("Diameter size (nm)", fontsize=13)
    ax[-1,1].set_xlabel("Diameter size (nm)", fontsize=13)
    
    ax[0,1].set_title("Normalized distributions", fontsize=15)

    fig.tight_layout()
    
    if savepath is not None:
        fig.savefig(savepath)  
        
    plt.close(fig)
        
    