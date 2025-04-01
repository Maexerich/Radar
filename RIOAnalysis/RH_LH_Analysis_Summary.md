# Goal
We want to determine whether RIO as implemented [here](https://github.com/ethz-asl/rio/tree/demo/smooth_flight_tuned) uses a LH or RH radar coordinate frame as input, respectively the impact of feeding a RH vs LH coordinate frame to RIO.

From the current RIO implementation it is not clear whether the LH coordinate frame from the TI sensor is considered. To this day, no place was found where this is considered.

# Procedure
Run RIO twice; (a) no changes and (b) where we flip the z-axis-sign within the code of RIO.

We then compare the output of the two estimated trajectories to the ground truth vicon trajectory.

# Data `data/RH_LH`
For this we have recorded data using the [radar test rig](https://github.com/Maexerich/radar_rig_sensor_fusion) where the TI is in it's default configuration, e.g. outputting a LH coordinate frame.

We have run RIO in (a) default mode and (b) in modified mode, where;
- (a) no changes to RIO: `defaultRIO_     .bag`
- (b) flipped of z-axis behavior within the code of RIO `modRIO_     .bag`

`small`, `medium` refers to approximate length of recorded data.
`easy` refers to datasets containing only head-on motion, e.g. no translation (like a car moving) and staying for the most part in the same z-plane (more or less).

## Topics in question
- `/rio/odometry_navigation`: RIO estimated odometry
- `/radar/vrpn_client/estimated_odometry`: Vicon ground-truth (GT) odometry

> **Naming convention**  
> <span style="color: red;"> **defaultRIO:** implementation of RIO using a Left-Hand (LH) coordinate frame from the TI sensor
> **modRIO:** implementation of RIO using a Right-Hand (RH) coordinate frame (flipping z-axis of TI sensor frame) _(modRIO because it modifies RIO code)_

# Plots

Command used for respective plots, where only the filename was changed.
```bash
evo_traj bag RIOAnalysis/data/RH_LH/modRIO_small_2025-03-19-15-58-07.bag /rio/odometry_navigation --ref /radar/vrpn_client/estimated_odometry --align --plot
```
## *_small_2025-03-09-15-58-07.bag
Command for the 'modRIO', else replace bag-name with 'defaultRIO'.
```bash
evo_traj bag RIOAnalysis/data/RH_LH/modRIO_small_2025-03-19-15-58-07.bag /rio/odometry_navigation --ref /radar/vrpn_client/estimated_odometry --align --plot
```
<p>
    <img src="/RIOAnalysis/Default_small_2025-03-19-15-58-07.png" alt="Default RIO" hspace="10" width="45%">
    <img src="/RIOAnalysis/Mod_small_2025-03-19-15-58-07.png" alt="Modified RIO" hspace="10" width="45%">
    <br>
    <em>Left: Default RIO, Right: Modified RIO</em>
</p>

## *_small_2025-03-19-15-59-50.bag
Here we also visualize the orientation because this dataset by coincidence has well behaved orientations (do not go over the periodicity boundary).
### Position
<p>
    <img src="/RIOAnalysis/Default_small_2025-03-19-15-59-50.png" alt="Default RIO" hspace="10" width="45%">
    <img src="/RIOAnalysis/Mod_small_2025-03-19-15-59-50.png" alt="Modified RIO" hspace="10" width="45%">
    <br>
    <em>Left: Default RIO, Right: Modified RIO</em>
</p>

### Orientation
<p>
    <img src="/RIOAnalysis/Default_orientation_small_2025-03-19-15-59-50.png" alt="Default RIO" hspace="10" width="45%">
    <img src="/RIOAnalysis/Mod_orientation_small_2025-03-19-15-59-50.png" alt="Modified RIO" hspace="10" width="45%">
    <br>
    <em>Left: Default RIO, Right: Modified RIO</em>
</p>

## *_medium_easy_2025-03-19-16-02-39.bag
<p>
    <img src="/RIOAnalysis/Default_medium_easy_2025-03-19-16-02-39.png" alt="Default RIO" hspace="10" width="45%">
    <img src="/RIOAnalysis/Mod_medium_easy_2025-03-19-16-02-39.png" alt="Modified RIO" hspace="10" width="45%">
    <br>
    <em>Left: Default RIO, Right: Modified RIO</em>
</p>

## *_medium_2025-03-19-16-00-45.bag
<p>
    <img src="/RIOAnalysis/Default_medium_2025-03-19-16-00-45.png" alt="Default RIO" hspace="10" width="45%">
    <img src="/RIOAnalysis/Mod_medium_2025-03-19-16-00-45.png" alt="Modified RIO" hspace="10" width="45%">
    <br>
    <em>Left: Default RIO, Right: Modified RIO</em>
</p>

# Statistics: Relative Pose Error (RPE)
Statistics on relative-pose-error (rpe) across all datasets.
Replace specific bag file name in the following code;
```bash
evo_rpe bag RIOAnalysis/data/RH_LH/defaultRIO_small_2025-03-19-15-58-07.bag /radar/vrpn_client/estimated_odometry /rio/odometry_navigation --align --plot --delta 1 --delta_unit m --all_pairs
```

<p>
    <img src="/RIOAnalysis/stats.png" alt="RPE Statistics" hspace="10" width="60%">
    <br>
    <em>RPE statistics for all datasets, using delta of 1m</em>
</p>


# Conclusion

Without looking at all numbers or plots too precisely, I find it obvious that the current RIO implementation has mistakenly neglected the fact of the LH coordinate frame and does not consider it.

Considering that the coordinate frame of the TI is LH by default and flipping the z_axis to make it a RH coordinate frame clearly and in my opinion undoubtedly improves the RIO estimate.