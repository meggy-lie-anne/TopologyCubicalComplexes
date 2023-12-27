from typing import Callable
import numpy as np

class CubicalComplex:
    def __init__(self, cubes: list[tuple]) -> None:
        self.cubes = cubes

    def vertices(self):
        return [x for x in self.cubes if len(x) == 1]
    
    def adjacent_cubes(self, vertex: tuple[int]) -> list[tuple]:
        return [c for c in self.cubes if vertex[0] in c]
    
    def __iter__(self):
        return self.cubes.__iter__()
    
    def __len__(self):
        return self.cubes.__len__()

Vertex = tuple[int]
VertexFiltration = Callable[[Vertex], int]

def boundary(cube: tuple) -> list[tuple]:
    if len(cube) == 1:
        return []
    return [tuple(set(cube).difference({ x })) for x in cube]

def sorted_boundary_matrix(k: CubicalComplex, f: VertexFiltration):
    vertices = k.vertices()
    filtration: dict[tuple, int] = { v: f(v) for v in vertices }
    sorted_vertices = sorted(vertices, key=lambda x: filtration[x], reverse=True)
    filtration_index = len(k)
    findexes = dict()
    for v in sorted_vertices:
        print(v)
        for cube in k.adjacent_cubes(v) + [v]:
            if not cube in findexes:
                findexes[cube] = filtration_index - 1
                filtration_index = filtration_index - 1
    
    print(findexes)
    boundary_matrix = np.zeros((len(k), len(k)))
    for cube in k:
        col = findexes[cube]
        print("cube", cube, "is at column", col)
        for b in boundary(cube):
            row = findexes[b]
            print("    ", b, "is in its boundary, at row", row)
            boundary_matrix[row, col] = 1

    return boundary_matrix

cx = CubicalComplex([
    (1,),
    (2,),
    (3,),
    (4,),
    (1, 2),
    (2, 3),
    (3, 4),
    (4, 1),
])

print(sorted_boundary_matrix(cx, sum))