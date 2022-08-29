



from paths import datapath
from pathlib import Path
import pandas
import numpy as np




def read_result_file(filepath):

    raw_table = pandas.read_csv(filepath, sep="\t")

    contains_tracking_title = raw_table.iloc[:,0].apply(lambda s: True if "TRACKING" in s else False)
    index_tracking = np.where(contains_tracking_title)[0][0]
    contains_results_title = raw_table.iloc[:,0].apply(lambda s: True if "RESULTS" in s else False)
    index_results = np.where(contains_results_title)[0][0]
    contains_settings_title = raw_table.iloc[:,0].apply(lambda s: True if "SETTINGS" in s else False)
    index_settings = np.where(contains_settings_title)[0][0]
        
    table = raw_table.iloc[index_tracking + 1:,0]  
    table = table.str.split(pat=";", expand=True)  
    table.columns = table.iloc[0]  
    table = table.iloc[1:]  
    
    try:
        table = table.apply(pandas.to_numeric)
    except:
        print(str(filepath), "Warning", "wrong decimal delimiter")
        table = table.applymap(lambda s: s.replace(",","."))
        table = table.apply(pandas.to_numeric)



    general_description_table = raw_table.iloc[index_results+1:index_settings]
            
    general_description_table = general_description_table.iloc[:,0].str.split(pat=";", expand=True).iloc[:,:2]
    general_description_table.index = general_description_table.iloc[:,0]
    general_description_table.drop(0, axis=1, inplace=True)
  
    concentration = float(general_description_table.loc["Concentration"].values[0].split(" ")[0].replace(",","."))
    median = float(general_description_table.loc["Median diameter"].values[0].split(" ")[0])
    mean = float(general_description_table.loc["Mean diameter"].values[0].split(" ")[0])
    mode = float(general_description_table.loc["Modal diameter"].values[0].split(" ")[0])
    D90 = float(general_description_table.loc["D90"].values[0].split(" ")[0])
    D10 = float(general_description_table.loc["D90"].values[0].split(" ")[0])
    particles_per_frame = float(general_description_table.loc["Average counted particles"].values[0].split(" ")[0])
    
    general_description_table.loc["Total concentration"] = concentration
    general_description_table.loc["Median size"] = median
    general_description_table.loc["Mode size"] = mode
    general_description_table.loc["Mean size"] = mean
    general_description_table.loc["D90 size"] = D90
    general_description_table.loc["D10 size"] = D10
    general_description_table.loc["Average particles per frame"] = particles_per_frame
    general_description_table.loc["Number of videos"] = int(general_description_table.loc["Number of videos"])
    general_description_table.loc["Tracked particles"] = int(general_description_table.loc["Tracked particles"])

    
    general_description_table = general_description_table.loc[["Total concentration", "Median size", "Mode size", "D90 size", "D10 size", "Mean size", "Tracked particles", "Average particles per frame", "Number of videos"]]

    general_description_table = general_description_table.astype(float)

    return table, general_description_table
    







if __name__=="__main__":
    
    filepath = Path(datapath, "data Lea 02022021 Vt=1,5ml", "20220221_165750_020221-EVs d200 01", "020221-EVs d200-Results.csv")

    table = read_result_file(filepath)
