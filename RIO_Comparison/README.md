# Purpose
Compare RIO estimates using the TI-AWR1843AOP with the ZadarLabs Zprime 2.0 radar sensor.

# Data
Data should be (placed) at `data/RIO_Comp/`, where:
- `/raw/` contains each file twice, once truly 'raw' and once where the first ~5 seconds were removed ('...cut-from-front.bag').
- `RIO_TI` and `RIO_ZADAR` respectively contain the RIO estimates made using the respective `rio_ti.launch` and `rio_zadar.launch` files from the [radar rig](https://github.com/Maexerich/radar_rig_sensor_fusion/tree/main) repository.
- `RIO_with_Zadar_alternative_configurations` contains Zadar RIO estimates with alternative configurations.


# Configurations and approach
Zadarlabs sensor publishes at ~20Hz and provides 3.5-4.5K datapoints per scan. Significantly higher than using the TI sensor (8Hz with ~15 points per scan).


Some sort of data-throughput limitation makes sense.

## ZadarLabs throttler
In the [`rio_zadar.launch`](https://github.com/Maexerich/radar_rig_sensor_fusion/blob/main/launch/rio_zadar.launch) a throttler has been implemented, throttling the 20Hz down to 5Hz.

This has not been tested and optimized rigorously, but seems to work fine and seems reasonable.


## Limiting datapoints
There would be many reasonable ways to limit the number of datapoints;
- use SNR ratio to keep reasonable points compared to noisy points
- use distance threshold, as we have seen from the ZadarLabs PointCloud aggregation (in `ZadarlabsPointCloud/`), points extremely far away are detected which surely do not exist
- randomly sample a subset

I have tried a quick approach on using SNR limiting, however this did funnily enough not work very well.
Limiting the number of points (some upper threshold) seemed to have a positive impact on the estimate.

The most promising configuration used was;
- limiting to 800 points, randomly sampled (common.cpp)
- limiting to a maximum of 400 tracked landmarks (landmark_tracker.cpp)


# Results
Used this or equivalent commands to create figures
```bash
evo_traj bag RIO_TI_circle_slow_cutfromfront.bag /rio/odometry_navigation --ref /radar/vrpn_client/estimated_odometry --align --plot
```

## circle-slow
This dataset is a slow circular walking pattern, hence the sinusoidal motion in x and y.


Impressive enough, Z-accuracy goes to TI for this dataset. However, using a more refined data-filtering method, I expect the ZadarLabs to perform better.
<p>
    <img src="/RIO_Comparison/TI_circle_slow.png" alt="TI" hspace="10" width="45%">
    <img src="/RIO_Comparison/Zadar_circle_slow.png" alt="Zadar" hspace="10" width="45%">
    <br>
    <em>Left: TI-RIO, Right: Zadar-RIO</em>
</p>

## rollercoaster_slow
This dataset is a rollercoaster motion, e.g. translation, rotation, odd orientations, done slowly. It can be considered a 'difficult' dataset.

<p>
    <img src="/RIO_Comparison/TI_rollercoaster_slow.png" alt="TI" hspace="10" width="45%">
    <img src="/RIO_Comparison/Zadar_rollercoaster_slow.png" alt="Zadar" hspace="10" width="45%">
    <br>
    <em>Left: TI-RIO, Right: Zadar-RIO</em>
</p>

## TI-only and Zadar Only
These two datasets were recorded with only one Radar sensor respectively. In case we expect to have cross-talk between different radar sensors (not obvious to this day), these datasets might provide insights.

Be cautious when comparing left and right side of these figures, as they **do not** share a ground-truth! (despite them looking extremely similar)

<p>
    <img src="/RIO_Comparison/TIonly_circle_slow.png" alt="TI" hspace="10" width="45%">
    <img src="/RIO_Comparison/Zadaronly_circle_slow.png" alt="Zadar" hspace="10" width="45%">
    <br>
    <em>Left: TI only, Right: Zadar only</em>
</p>

## Alternate ZadarLabs configurations
*using the ZadarOnly dataset for the comparison of different configurations*

### 800 vs 1500 random detections
Left we use the 800 random detections and to the right we use 1500 random detections - if anything, it looks less robust.
<p>
    <img src="/RIO_Comparison/Zadaronly_circle_slow.png" alt="TI" hspace="10" width="45%">
    <img src="/RIO_Comparison/Zadaronly_circle_slow_ALTERNATIVE_1500Detections.png" alt="Zadar" hspace="10" width="45%">
    <br>
    <em>Left: best Zadar config, Right: 1.5K detections</em>
</p>

### Limiting based on SNR
Limiting based on Signal-to-Noise-Ratio makes sense in theory, but in practice might need more investigation/tuning than just setting a simple threshold like I had implemented.

<p>
    <img src="/RIO_Comparison/Zadaronly_circle_slow.png" alt="TI" hspace="10" width="45%">
    <img src="/RIO_Comparison/Zadaronly_circle_slow_ALTERNATIVE_snr15limit.png" alt="Zadar" hspace="10" width="45%">
    <br>
    <em>Left: best Zadar config, Right: lower limit of snr set to 15</em>
</p>



# Code and reproducibility
Zadarlabs implementation has been done on [this branch]() from the rio repository. To see what has been modified from the `demo/smooth_flight_tuned` branch, compare the last two commits on the `zadarlabs_implementation` branch.

When re-running this system remember that `catkin build` must be called every time changes are made in the rio-source files. In particular, the datatypes of the PointClouds between TI and ZadarLabs differ, and are not compatible out of the box.