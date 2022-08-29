

from pathlib import Path
from paths import datapath
from app_videodrop import App

    
# """ Lea """

path = Path(datapath, "Data Lea NTA Videodrop")

data_app = App(data_dir=path,
                dilution_prefix="d",
                replicate_prefix="0", group_replicates=True)

data_app.run_manual()
# data_app.export_data()
# data_app.plot_videodrop()
data_app.run_clustering_normalized_videodrop_size_concentration_distributions_wasserstein()
# data_app.run_clustering_total_concentration_nanosight()


