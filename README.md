# TopologyCubicalComplexes

Topological Data Analysis Project

# References

<http://www2.im.uj.edu.pl/mpd/publications/Wagner_persistence.pdf>
<https://eurocg11.inf.ethz.ch/abstracts/22.pdf>
<http://www.diva-portal.org/smash/get/diva2:1019117/FULLTEXT01.pdf>


# Abstarct/Intro
(Illustrer l'intro avec des images, parler aussi des applications dans les differents fields)

A cubical complex is a mathematical structure used in topology to study spaces. It provides a combinatorial description of spaces by using cubes as building blocks. The basic building blocks of a cubical complex are cubes of various dimensions. A 0-dimensional cube is a vertex, an 1-dimensional cube is an edge, a 2-dimensional cube is a square and so on. This structure is diffenrent from the simplicial complex. In algebraic topology, simplicial complexes and cubical complexes are two fundamental structures employed to represent and study topological spaces. Each approach utilizes distinct geometric elements as its building blocks.
At the heart of a simplicial complex are simplices, which are generalizations of the notion of triangles to higher dimensions- a triangle is a 2-dimensional simplex. A simplicial complex is described by specifying a set of vertices and detailing a collection of simplices, where each simplex is an ordered set of vertices. The relationships between simplices are determined by their shared faces.
In contrast, a cubical complex employs cubes as its basic constituents. The complex takes shape by gathering cubes in a manner such that the intersection of any two cubes is either void or a common face. The representation of a cubical complex often evokes a grid-like structure, where each cell corresponds to a cube in the complex ; two adjacent cubes share a face.

Simplicial and cubical complexes are like two different tools in math that help us understand shapes and spaces. Simplicial complexes use simple shapes called simplices, while cubical complexes use squares and cubes. People choose between these tools based on the kind of problem they're trying to solve. Some prefer the elegance of simplicial complexes, like using triangles to represent shapes. Others like the structured simplicity of cubical complexes, where shapes are more like grids. In the world of math, these tools are used to explore and understand how different spaces are connected. They each have their own strengths and can tell us interesting things about the shapes we're studying. 

# Method 

The method we use for computing homology follows the general principles of persistent homology. 
First we define the 'CubicalComplex' class which is initialized with a list of tuples, where each tuple corresponds to the vertices of a cube within the complex. 

Within this class we implemented a few functionalities for analysing the cubical complex. It is possible to traverse the complex and to obtain the amount of cubes within the complex, as well as its dimension (i.e. the maximum dimension of the cubes contained within the complex). Additionally, we are able to return the list of all vertices present in the complex (which enables easy access to the individual building blocks) ; it is also possible to find all cubes that are adjacent to a given vertex.

