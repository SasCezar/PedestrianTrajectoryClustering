# PedestrianTrajectoryClustering

![Image 1](https://github.com/SasCezar/PedestrianTrajectoryClustering/blob/master/images/gorrini_lanes.png "Pedestrian Configurations Lines")
![Image 2](https://github.com/SasCezar/PedestrianTrajectoryClustering/blob/master/images/3_3_A.png "Results")
![Image 3](https://github.com/SasCezar/PedestrianTrajectoryClustering/blob/master/images/boa-300-055-095_combined_MB.png "Results")


Pedestrian flow analysis aims to provide insight into human movement patterns in buildings or outdoor areas. These analyses provide valuable information to building designers and other decision makers. A substantial bodyof research is based on pedestrian behavior and the interaction of pedestrian swith their environment and other pedestrians.In order to help this analysis we propose a pedestrian trajectories clustering system for lane discovery. Our solution uses the work of [Atev et al.](http://hanj.cs.illinois.edu/pdf/sigmod07_jglee.pdf) on clustering of vehicular trajectories applied to our domain. We evaluate our solution on multiple dataset.

## Conclusions
We presented a system for pedestrian lane recognition based on spectral clustering and  Hausdorff distance. We performed  analysis on two different dataset. The results, even if the quantitative measures were promising, showed us that a system based on whole trajectories does not give enough information on a lane. This type of analysis does not give us information onhow much a lane stays alive, how many times a lane is reformed, and so on. Our type of analysis is more suitable for static analyses such as urban and architectural planning. As future work, we aim to perform a time based clustering, and try different distance measures. Another improvement could be performed to theclustering algorithm, which actually does not make use of the direction andof the speed of a pedestrian.


Check the [report.pdf](report.pdf) file for the full description of the project
