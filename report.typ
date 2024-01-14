#import "@preview/cetz:0.1.2"

#set text(font: "New Computer Modern")
#set par(justify: true, leading: 0.9em)
#show heading: it => {
  v(1em)
  it
  v(1em, weak: true)
}

#v(2em)

#align(center, [
  = Cubical complexes

  Meggy-Lie-Anne Chamand, Ana Gelez 
])

#v(4em)

*This research project focuses on the implementation of homology and persistent homology algorithms for cubical complexes - mathematical structures that provide a combinatorial description of spaces by using cubes as building blocks. Usually, those two concepts are computed for filtrations arising from simplicial complexes, but in certain cases (e.g. 3D models, bitmap pictures etc) the use of cubical decomposition is more appropriate. its applications on different surfaces (e.g. Klein bottle, torus, projective plane). We were able to build the boundary matrices and the persistent homology barcodes for complexes built in $ZZ_2$.*


== Introduction

When talking about homology and persistent homology, it is often assumed that we are studying simplicial complexes and their filtrations. However, in some areas, data is better represented with *cubical complexes*, in which simplices are replaced with cubes. For instance, it is the case when dealing with an image made of square pixels, or a video which can be seen as a three-dimensional image, where the third dimension is time.

For instance, they offer a useful framework for representing pixel-based data, such as bitmap images, where each pixel corresponds naturally to a cube. In this context, the grid-like structure of cubical complexes aligns smoothly with the structure of pixel grids. Moreover, the boundary definition in cubical complexes is particularly advantageous for tasks related to image processing. In a cubical complex, determining the boundary of a cube is straightforward, making it well-suited for identifying neighboring pixels in an image.

More formally, a cube can be defined as a product of elementary intervals. An elementary interval is either degenerate ([𝑖, 𝑖], 𝑖 ∈ N) or non-degenerate ([𝑖, 𝑖 + 1]). A 2-dimensional cube (square) spanning from (1, 3) to (2, 4) would then be represented as:

$ [1, 2] times [3, 4] $

Similarly to a simplicial complex, we can define a cubical complex as a set of cubes such that if a cube is part of the complex, then its boundary is part of it too.

#let pt = c => cetz.draw.rect(c, (c.at(0) + 0.1, c.at(1) + 0.1), fill: black)

#figure(
  cetz.canvas({
    import cetz.draw: *
    
    pt((0, 0))
    pt((2, 0))
    pt((2, 2))
    pt((0, 2))
    line((0.05, 0), (0.05, 2))
    line((2.05, 0.05), (0.05, 0.05))
  }),
  caption: "Example of a cubical complex"
) <ex1>

Using similar definitions as for simplicial complex, it is possible to define homology and persistent homology for this kind of complex.

== Method

=== Representing cubical complexes


We can improve the efficiency of the representation of cubical complexes by taking advantage of their structure. In a 𝑑-dimensional complex, each cube can be efficiently represented as an element of $NN^d$. Here, each element of this vector corresponds to a dimension. If the coordinate is even, the corresponding interval in the product is degenerate; if it is odd, it is non-degenerate. The interval corresponding to a coordinate $x$ starts at $x div 2$ (using Euclidean division).

The complex illustrated in @ex1 can be represented using this set (assuming the y-axis points down, and (0, 0) is in the upper-left corner):

$
{
  vec(0, 0), vec(0, 2), vec(2, 0), vec(2, 2), vec(0, 1), vec(1, 2)
}
$

Each element of this set corresponds to a cube in the complex. The first coordinate in each pair represents the x-coordinate, and the second coordinate represents the y-coordinate. For instance, $vec(0,2)$ gives us $[0,0] times [1,1]$, corresponding to the 0-dimensional cube (vertex) (0,1) ; $vec(1,2)$ gives us $[0,1] times [1,1]$, correponding to the 1-dimensional cube (edge) [0,1].

This representation is much more compact and less ambiguous than listing the vertices that are part of each cube.



=== Computing homology


It is then possible to compute homology, and more generaly, persistent homology. To do so, we implemented the algorithm described by Wagner _et al._ @Wagner2012.

Using a filtration, that is represented as a function that assigns to each vertex an index, we build a generalization of this filtration, that assigns an index to all cubes in the complex. Cubes can then be sorted according to their assigned index. The order of the vertices is preserved, and a non-vertex cube is guaranteed to be after all its vertices.

We use this ordering to build a boundary matrix: each column corresponds to a cube in the complex (the $i$-th column corresponds to the cube with filtration index $i$ to be exact). The $j$-th element in this column is $1$ if the cube with filtration index $j$ is part of the boundary of the $i$-th cube (otherwise, it is $0$).

Using the representation described above, it is easy to compute the boundary of any cube: for each coordinate $x$, if it is non-degenerate, the boundary includes two cubes that both share the same coordinates as the cube excepted for $x$ which is replaced with $x - 1$ and $x + 1$ respectively. 

Afterwards, the matrix is reduced, using the algorithm proposed by Chen _et al._ @Chen2011PersistentHC. We can then exploit the equations provided in this same article to build persistence pairs.

== Results

=== A simple example

We decided to test our code on a simple example, drawn below (the number below each step is the filtration index of the cube that is added at this step):

#align(center, table(
  columns: 8,
  rows: 2,
  stroke: gray,
  cetz.canvas({
    import cetz.draw: *
    scale(0.7)
    pt((0, 0))
    rect((2.1, 2.1), (2.1, 2.1))
  }),
  cetz.canvas({
    import cetz.draw: *
    scale(0.7)
    pt((0, 0))
    pt((2, 0))
    rect((2.1, 2.1), (2.1, 2.1))
  }),
  cetz.canvas({
    import cetz.draw: *
    scale(0.7)
    
    pt((0, 0))
    pt((2, 0))
    line((0, 0.05), (2, 0.05))
    rect((2.1, 2.1), (2.1, 2.1))
  }),
  cetz.canvas({
    import cetz.draw: *
    scale(0.7)
    
    pt((0, 0))
    pt((2, 0))
    line((0, 0.05), (2, 0.05))
    pt((2, 2))
  }),
  cetz.canvas({
    import cetz.draw: *
    scale(0.7)
    
    pt((0, 0))
    pt((2, 0))
    line((0, 0.05), (2, 0.05))
    pt((2, 2))
    line((2.05, 0.05), (2.05, 2.05))
  }),
  cetz.canvas({
    import cetz.draw: *
    scale(0.7)
    
    pt((0, 0))
    pt((2, 0))
    line((0, 0.05), (2, 0.05))
    pt((2, 2))
    line((2.05, 0.05), (2.05, 2.05))
    pt((0, 2))
  }),
  cetz.canvas({
    import cetz.draw: *
    scale(0.7)
    
    pt((0, 0))
    pt((2, 0))
    line((0, 0.05), (2, 0.05))
    pt((2, 2))
    line((2.05, 0.05), (2.05, 2.05))
    pt((0, 2))
    line((2.05, 2.05), (0.05, 2.05))
  }),
  cetz.canvas({
    import cetz.draw: *
    scale(0.7)
    
    pt((0, 0))
    pt((2, 0))
    line((0, 0.05), (2, 0.05))
    pt((2, 2))
    line((2.05, 0.05), (2.05, 2.05))
    pt((0, 2))
    line((2.05, 2.05), (0.05, 2.05))
    line((0.05, 2.05), (0.05, 0.05))
  }),
  "0",
  "1",
  "2",
  "3",
  "4",
  "5",
  "6",
  "7",
))

Our algorithm gives the following boundary matrix, which is then reduced:

#{
  show "0": text.with(fill: gray)

  $
  mat(
  0, 0, 1, 0, 1, 0, 0, 0;
  0, 0, 1, 0, 0, 0, 0, 1;
  0, 0, 0, 0, 0, 0, 0, 0;
  0, 0, 0, 0, 1, 0, 1, 0;
  0, 0, 0, 0, 0, 0, 0, 0;
  0, 0, 0, 0, 0, 0, 1, 1;
  0, 0, 0, 0, 0, 0, 0, 0;
  0, 0, 0, 0, 0, 0, 0, 0;
  )

  arrow

  mat(
  0, 0, 1, 0, 1, 0, 0, 0;
  0, 0, 1, 0, 0, 0, 0, 0;
  0, 0, 0, 0, 0, 0, 0, 0;
  0, 0, 0, 0, 1, 0, 1, 0;
  0, 0, 0, 0, 0, 0, 0, 0;
  0, 0, 0, 0, 0, 0, 1, 0;
  0, 0, 0, 0, 0, 0, 0, 0;
  0, 0, 0, 0, 0, 0, 0, 0;
  )
  $
}

If we build the homology pairs and plot them on a bar diagram, this is what we obtain. 

#figure(image("simple_bars.png"))

The dark blue bars are homology generators: the longest one is for the $0$-dimension generator (one connected component) and the short one is for the $1$-dimension generator (the loop that appears at the last step). The light blue bars correspond to the addition of a vertex followed by the addition of a line: a new connected component is created and then immediatly killed.

=== Some classic examples

For these complexes, we used data from SageMath that we converted to our own format. Here are the bar charts that we obtain:

#figure(image("plane_bars.png"), caption: "Projective plane bars")
#figure(image("klein_bars.png"), caption: "Klein bottle bars")
#figure(image("torus_bars.png"), caption: "Torus bars")

We can see that the number of generator is what we would expect. For instance, the torus has one generator in dimension 0, two in dimension one, and one in dimension two.

== Discussion

Our algorithm seems to correctly compute persistent homology for cubical complexes. Unfortunately, due to time constraints, we were unable to implement the persistent homology algorithm using various coefficients. As it is, our code only supports $ZZ_2$.

The choice of coefficients in persistent homology are important for the detail of the captured topological features. For instance, using $ZZ_2$ coefficients simplifies computations and is well-suited for applications in image processing and computer graphics.

Extending the model to support other coefficients would require we use a more general definition of boundaries (e.g. in $ZZ$, cubes in a boundary are oriented). However, this comes at the cost of increased computational complexity. The reduction algorithm should also be adapted to work in a different field, when summing columns together.

== Conclusion

In conclusion, this research project delved into the implementation of homology and persistent homology algorithms specifically applied to cubical complexes. While traditional approaches focus on simplicial complexes, cubical complexes provide a more suitable representation for certain types of data, such as pixel-based images or three-dimensional structures incorporating time.

The method presented efficiently represents cubical complexes, and allow for a more effective representation compared to listing individual vertices. The implemented algorithms for computing homology and persistent homology were based on the work of Wagner et al. [1], with an emphasis on using filtrations to assign indices to cubes and building boundary matrices. 

Results from testing the code on both a simple example and classic mathematical surfaces, such as the Klein bottle, torus, and projective plane, gave expected outcomes. The homology generators and their corresponding dimensions align with the theoretical expectations. However, our current implementation supports only $ZZ_2$ coefficients. It can be noted that $ZZ_2$ coefficients are suitable for applications in image processing and computer graphics. Also, extending the model to accommodate other coefficients would involve a more general definition of boundaries.

Further work could involve refining the model to support additional coefficients, adapting the reduction algorithm accordingly, and exploring applications in various fields where cubical complexes play a crucial role.



== Division of work 

Ana Gelez : researches on cubical complexes and persistent homology, implementation of the algorithm, tests, report
Meggy-Lie-Anne Chamand : researches on cubical complexes and persistent homology, report


== References

#bibliography("report.bib", title: none)