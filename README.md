# AFC_Tailgate_Lag
Underground longwall mining use AFC's to extract coal. The coal is sheared of the face which then falls into a conveyor. A pan is used along side the conveyor to hold cables,
of which must be in constant alignment with the coal face. If pan to face misalignment is allowed to go too far, the shearer will eventually not make straight cuts,  
and the tailgate end may either run into the rib away from the face or will not reach the edge of the block. When is occurs, additional ‘straightening cuts’ are required.

The scope of this project is to build a tailgate lag exception monitoring system using Python with SQL integration. The application will analyse AFC pan line tailgate images 
to infer a lag distance between the tailgate and the rest of the AFC pan line. The measurements and other metadata are stored in a MS SQL database. The outcome is for 
these tailgate distance measurements be used (by others), to report by exception when the tailgate distance to the remaining AFC pan line threshold is breached.


## Problem Statement

1. Track a part of the tailgate in each image.
2. Find the distance from conveyor to the tailgate.

## Assumptions

1. The conveyor is always parallel to the coal face
2. The camera takes the image at 0 degs, i.e., looking straight up the cut
