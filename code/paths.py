




from pathlib import Path
import os





source = Path().resolve().parent




for dir_ in ["videodrop_app_results"]:
    if not os.path.exists(Path(source, dir_)):
        print("No " + dir_ + " directory in the nanosight-videodrop-data-analysis directory." \
                        " Creating one.")
    
        os.mkdir(Path(source, dir_))


datapath = Path(source, "data")
codepath = Path(source, "code")
videodrop_app_path_results = Path(source, "videodrop_app_results")
