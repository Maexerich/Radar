# Content
This repo contains results collected during my period as HiWi at the ASL Lab under Michael Pantic work on Radar sensors.

# Results

# Data
Data can be found on [GoogleDrive]().
Data should be downloaded and placed in the `data` folder.

Here is an overview of the different data collected and some comments:
|Directory   |Explanation   |Comment   |
|---|---|---|
|`data/AllSensors_noRIO/`   |Data was collected specifically for ZadarLabs point-cloud aggregation. <br>Used in the `ZadarlabsPointCloud` evaluation.  |Data was initially collected with incorrect tf for ZadarLabs sensor and was post-processed to have correct transformations.   |
|`data/RH_LH_raw/`   |Raw data collected to make the Right-Hand vs Left-Hand coordinate frame comparison for TI radar sensor, <br> found in `RIO_RH_LH_Analysis`.   |Does not contain ZadarLabs data.   |
|`data/RH_LH/`  |Contains the output of the RIO estimate made on the `RH_LH_raw` datasets. <br>**defaultRIO** refers to default implementation where the **modRIO** is with the z-axis flipped (in the RIO ROS package). |The RIO estimate was made in post after recording the bag files.   |
|`data/RIO_Comp_raw/`  |Data where TI & Zadar data was collected in order to compare RIO estimates side-by-side. <br>For TI and Zadar there is each one dataset, where only one of the radar sensors was recorded. <br>This could maybe be used to see whether cross-interference is relevant. | |


# Zadarlabs Documentation
Software Guide at: https://drive.google.com/file/d/1ylitqvMUCAnIMQ8hhzlgK2hkPvUzB6Z4/view

Zadarlabs driver: https://drive.usercontent.google.com/download?id=1t71f4Y-6SmnaBKJxd4yMAqJjq1MNMCqC&export=download&authuser=0