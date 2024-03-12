# Ball-Pivoting-Algorithm


Python implementation of the ball-pivoting algorithm (BPA), which was published in 1999 by Bernardini  [[1]](#1). The code implements are inspired by Lotemn102 (2021). Ball-Pivoting-Algorithm [GitHub repository](https://github.com/Lotemn102/Ball-Pivoting-Algorithm.git)

## Algorithm Overview

<p align="center">
  <img src="images/figure1.png" width="250">
</p>

This algorithm solves the problem of reconstructing mesh surface from a 3D point cloud. The main assumption this algorithm is
based on is the following: Given three vertices, and a ball of radius `r`, the three vertices form a triangle if the ball is getting "caught" and settle 
between the points, without containing any other point.

The algorithm stimulates a virtual ball of radius `r`. Each iteration consists of two steps:
- **Seed triangle** - The ball rolls over the point cloud until it gets "caught" between three vertices and settles between in them. 
Choosing the right `r` promises no other point is contained in the formed triangle. This triangle is called "Seed triangle".
- **Expanding triangle** - The ball pivots from each edge in the seed triangle, looking for a third point. It pivots until it gets
"caught" in the triangle formed by the edge and the third point. A new triangle is formed, and the algorithm
tries to expand from it. This process continues until the ball can't find any point to expand to.

At this point, the algorithm looks for a new seed triangle, and the process described above starts all over.

The following figures demonstrates those two steps. 

<p align="center">
  <img src="images/figure2.png" width="250">
</p>

<p align="center">2D view of the finding seed triangle step</p>

<p align="center">
  <img src="images/figure1.png" width="250">
</p>

<p align="center">2D view of the expanding triangle step</p>

Two vague assumptions that are necessary for the algorithm are that the point cloud is "dense enough", and that the
chosen `r` size is "slightly" larger than the average space between points. I couldn't find a metric method to evaluate
those two variables at the moment, and more work needs to be done on this.
  

## Data Structures
### Grid
I used a virtual 3D grid in which in each cell of the grid, all points are at distance of maximum `2r` from all 
other points. With this method, i am able to limit the number of points i need to search. Since we are looking to fit a
ball of radius `r` between three points, we can be assured that if the distance be two points is larger than `2r`, the ball
won't get caught between them. Therefore, while checking all possible points to pivot from a point `p` when generating 
seed triangle or expanding triangle, i need to check `p`'s cell, and all 8 cells that touches this cell. Note that there
might get points that are `4r` apart, and i have to check that when iterating through these neighbor points. Example for that
is shown in the following figure. 

<p align="center">
  <img src="images/figure3.png" width="250">
</p>

<p align="center">2D view on part of the grid. The orange cells are the neighbors of the green cell</p>

Each cell is represented by a single point. For example, all cells are represented by the point marked by `p`:
<p align="center">
  <img src="images/figure5.png" width="200">
</p>

Each cells saves the entire points contained in it, but i also needed each point to save which cell it belongs to, to avoid 
iterating all the grid when searching for a point. I decided that each point will save the cell in belongs to. In order to 
decrease the memory required for this cyclic-design, each point save encoded unique version of the cell it belongs to. The encoding
was done by shifting and concatenating the coordinates of the point that defines the cell.

<p align="center">
  <img src="images/figure6.png" width="250">
</p>

<p align="center">Encodeing the cell define by (1, 2, 3) to 197121</p>


### Point
Consists of 3 coordinates, the normal in this point, the cell node it's sitting in, according to the grid's initiation.

### Edge
Consists of 2 Point objects.


## Complexity
Finding a seed costs <img src="https://latex.codecogs.com/gif.latex?O(n^2logn)" width="6%"/> time. We iterate through all points.
For each point `p1`, i check in <img src="https://latex.codecogs.com/gif.latex?O(1)" width="3%"/> time it's neighbor cells
in order to find all points that are at maximum  distance of `2r` from `p1`. I sort all neighbor points by distance from 
`p1` in <img src="https://latex.codecogs.com/gif.latex?O(nlogn)" width="5%"/>  to make sure the formed triangles will be as small as possible to reduce the number of cases where a
point in contained inside the formed triangle. For each point `p2` in `p1`'s neighbors, the same sorting process occurs. 
In order to check if a ball with radius of `r` can fit into the triangle defined by `p1`, `p2` and `p3`, i calculate the
radius of the inner-circle of that triangle. This calculation is in <img src="https://latex.codecogs.com/gif.latex?O(1)" width="3%"/> 
. If the normal of this triangle is in the same direction as the point's normal, the triangle is added to the mesh.
This check is also in <img src="https://latex.codecogs.com/gif.latex?O(1)" width="3%"/> . 

Expanding a single triangle costs <img src="https://latex.codecogs.com/gif.latex?O(nlogn)" width="5%"/> . 
For each of the triangle's edges `e=(p1,p2)`, i check in <img src="https://latex.codecogs.com/gif.latex?O(1)" width="3%"/> 
time the neighbor cells of `p1` and `p2` in order to find all points that are at maximum distance of `2r` from `p1` and `p2`.
I sort the points as before, in <img src="https://latex.codecogs.com/gif.latex?O(nlogn)" width="5%"/> .
I then check if the ball can fit into the formed triangle, and that it's normal vector is in the same
direction as the points.

At the worst case, the algorithm fails to expand the triangle everytime and has to find a new seed, making the total
run time complexity <img src="https://latex.codecogs.com/gif.latex?O(n^3logn)" width="6%"/> . This scenario is unlikely.

## Input format
This algorithm expects to get as input `.txt` file in the following pattern:
> x y z nx ny nz
> 
Where `x`, `y` and `z` are the point's coordinates, and `nx`, `ny` and `nz` are the point's normal vector's coordinates.
In order to generate the data to test the algorithm, i've downloaded 3D objects in .obj format [[4]](#4), extracted the points, and 
extracted each point's normal based on one of the facets it belongs to. Examples of the data are in the `data` folder. Code for generating new data is in `data_generator.py`.

## How to run the code

### Requirements
- Python>=3.7
- numpy>=1.20.1

### Running the main.py

```bash
python main.py -i data/bunny.txt -r 0.1
```

### utils

- `data_generator.py` - Generates data from .obj files.
- `bpa.py` - The main implementation of the algorithm, including the grid and the data structures and save the mesh to a .obj file.

## Reconstruction Results



## References
<a id="1">[1]</a>  [The Ball-Pivoting Algorithm for Surface Reconstruction](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=817351), by F. Bernardini, J. Mittleman and H. Rushmeier, 1999.

<a id="2">[2]</a>  [An Analysis and Implementation of a Parallel Ball Pivoting
Algorithm](https://www.ipol.im/pub/art/2014/81/article.pdf), by J. Digne, 2014.

<a id="3">[3]</a>  [Open3D offical website](http://www.open3d.org/).

<a id="4">[4]</a>  [Collection of .obj files](https://github.com/alecjacobson/common-3d-test-models).
