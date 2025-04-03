# Goal
Aggregate point cloud of ZadarLabs over time to hopefully see structures of the environment.

# Data
Go to root directory at `/RIOAnalysis/data/AllSensors_noRIO` and look at subdirectories. Following sections should have dataset uniquely noted.
RVIZ file can be found in this directory, however some values might have been adjusted accordingly.

# Results
Coloration is according to 'range' channel.
The large coordinate frame denotes the VICON coordinate frame; e.g. x-axis (red) is parallel to the windows and y-axis (green) points parallel to the hallways.
## allSensors_noRIO_short_circle_2024-04-02-16-53-27.bag and ...-16-56-27.bag
Color denotes distance. Pink at 10m or further. Room is little speck in the middle. Aggregation time of 15s. Large coordinate frame in the center is for the VICON system.
<p>
    <img src="Circular_topdown_far.png" alt="Top-down view of panning motion" hspace="10" width="45%">
    <img src="Circular_topdown_near.png" alt="Top-down view of panning motion close-up" hspace="10" width="45%">
    <br>
    <em>Top down view of panning motion in VICON room while walking in 'circles'.</em>
</p>

In the right  image we can see in red the trace from the circular motion. The straigth edge which is approached closely is most likely the metal-laced-net. It is not obvious that the wall behind is detected.

## allSensors_noRIO_short_staticslowpan_2025-04-02-17-00-38.bag
In the figures we have a part of the dataset which is quasi-static (handheld) and aggregated for 20s.
<p>
    <img src="Static_topdown.png" alt="Top-down view of static motion" hspace="10" width="45%">
    <img src="Static_3D.png" alt="3D view of static motion" hspace="10" width="45%">
    <br>
    <em>Two different perspectives of static motion within the VICON room.</em>
</p>

# Conclusion
- Point cloud certainly has some structure
- Unclear whether we can look past the 'net'
- We clearly detect points too far away (pink), hinting at multipath-reflections. How about outdoors (static)?