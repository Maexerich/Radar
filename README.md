# Content
This repo contains results collected during my period as HiWi at the ASL Lab under Michael Pantic work on Radar sensors.

Related repositories are;
- [radar_rig_sensor_fusion](https://github.com/Maexerich/radar_rig_sensor_fusion/tree/main): Contains information on the developed radar rig
- [web-app](https://github.com/Maexerich/radar_web_app_control): Nifty web-app installed on the radar rig to record data easily
- [zadarlabs ROS driver](https://github.com/Maexerich/zadarlabs_arm_ros1): Wrapper for provided ROS driver
- [zadarlabs_implementation branch](https://github.com/ethz-asl/rio/tree/zadarlabs_implementation): Branch of rio repository containing the integration of the zadarlabs sensor. _(Here, simply look at the changes between the two last commits to find changes made.)_


RadarLiteratureReview.pdf: File in this repo, containing literature review done on radar odometry and highlights some potential areas.

Data can be downloaded from [GoogleDrive](https://drive.google.com/drive/folders/1XC0jialyL-7lJlex4hl4icKFQRRlaGvo?usp=drive_link).

# Results
Different 'tests'/evaluations were made;
- **RIO_RH_LH_Analysis** compares RIO estimates using the TI sensor and determining, what effect a flipped z-axis has on the estimate. This evaluation is done because the TI sensor outputs data in a left-handed (LH) coordinate frame, and it was not apparent, _if_ and _where_ RIO considers this.
- **ZadarlabsPointCloud** aggregates the datapoints from the ZadarLabs radar sensor to determine, whether structures become visible.
- **RIO_Comparison** compares the RIO estimates using TI or ZadarLabs sensor.

# Data
Data can be found on [GoogleDrive](https://drive.google.com/drive/folders/1XC0jialyL-7lJlex4hl4icKFQRRlaGvo?usp=drive_link).
Data should be downloaded and placed in the `data` folder.

Here is an overview of the different data collected and some comments:
|Directory   |Explanation   |Comment   |
|---|---|---|
|`data/AllSensors_noRIO/`   |Data was collected specifically for ZadarLabs point-cloud aggregation. <br>Used in the `ZadarlabsPointCloud` evaluation.  |Data was initially collected with incorrect tf for ZadarLabs sensor and was post-processed to have correct transformations.   |
|`data/RH_LH_raw/`   |Raw data collected to make the Right-Hand vs Left-Hand coordinate frame comparison for TI radar sensor, <br> found in `RIO_RH_LH_Analysis`.   |Does not contain ZadarLabs data.   |
|`data/RH_LH/`  |Contains the output of the RIO estimate made on the `RH_LH_raw` datasets. <br>**defaultRIO** refers to default implementation where the **modRIO** is with the z-axis flipped (in the RIO ROS package). |The RIO estimate was made in post after recording the bag files.   |
|`data/RIO_Comp_raw/`  |Data where TI & Zadar data was collected in order to compare RIO estimates side-by-side. <br>For TI and Zadar there is each one dataset, where only one of the radar sensors was recorded. <br>This could maybe be used to see whether cross-interference is relevant. | |
|`data/RIO_Comp` |In `raw/` we find the unprocessed recordings made with the `master.launch` file from the [radar rig](https://github.com/Maexerich/radar_rig_sensor_fusion/tree/main). <br>Using the scripts `rio_ti.launch` and `rio_zadar.launch` the estimates are made and the datasets with respective names were generated. |<br>The first few (~5) seconds are cut from the respective bag files (hence '...cutfromfront.bag' naming).|


# Zadarlabs Documents
[Software Guide](https://drive.google.com/file/d/1ylitqvMUCAnIMQ8hhzlgK2hkPvUzB6Z4/view) and [driver](https://drive.usercontent.google.com/download?id=1t71f4Y-6SmnaBKJxd4yMAqJjq1MNMCqC&export=download&authuser=0) can be found on GoogleDrive.

# Radar Rig
CAD files can be found on [GoogleDrive](https://drive.google.com/drive/folders/1LmM_rV13pX58VYUtpY1OkgPbWoKuzgi0?usp=drive_link) and more details on the radar-rig at the [repository](https://github.com/Maexerich/radar_rig_sensor_fusion/tree/main).