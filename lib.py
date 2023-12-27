from typing import Callable, Optional
import numpy as np

class CubicalComplex:
    def __init__(self, cubes: list[tuple]) -> None:
        self.cubes = cubes

    def vertices(self):
        return [x for x in self.cubes if len(x) == 1]
    
    def adjacent_cubes(self, vertex: tuple[int]) -> list[tuple]:
        return [c for c in self.cubes if vertex[0] in c and c != vertex]
    
    def __iter__(self):
        return self.cubes.__iter__()
    
    def __len__(self):
        return self.cubes.__len__()
    
    def dimension(self):
        return max([len(c) - 1 for c in self.cubes])

Vertex = tuple[int]
VertexFiltration = Callable[[Vertex], int]

def boundary(cube: tuple) -> list[tuple]:
    if len(cube) == 1:
        return []
    return [tuple(set(cube).difference({ x })) for x in cube]

def sorted_boundary_matrix(k: CubicalComplex, f: VertexFiltration) -> tuple[np.ndarray, list[tuple]]:
    vertices = k.vertices()
    sorted_vertices = sorted(vertices, key=f, reverse=True)
    filtration_index = len(k)
    findexes = dict()
    for v in sorted_vertices:
        for cube in k.adjacent_cubes(v) + [v]:
            if not cube in findexes:
                findexes[cube] = filtration_index - 1
                filtration_index = filtration_index - 1
    
    boundary_matrix = np.zeros((len(k), len(k)))
    for cube in k:
        col = findexes[cube]
        for b in boundary(cube):
            row = findexes[b]
            boundary_matrix[row, col] = 1

    sorted_cubes = sorted(k.cubes, key=lambda c: findexes[c])
    return (boundary_matrix, sorted_cubes)

def low(row: np.ndarray) -> Optional[int]:
    for i in range(len(row) - 1, -1, -1):
        coeff = row[i]
        if coeff == 1:
            return i

def reduce(mat: np.ndarray, k: CubicalComplex, filtration: list[tuple]):
    pivot_idx = [0 for _ in range(len(mat))]
    for d in range(k.dimension(), 0, -1):
        for j in range(0, len(mat)):
            sx_dim = len(filtration[j])
            if sx_dim == d:
                l = low(mat[:, j])
                while l != None:
                    if pivot_idx[l] != 0:
                        mat[:, j] = (mat[:, j] + mat[:, l]) % 2
                    else:
                        break
                    l = low(mat[:, j])
                l = low(mat[:, j])
                if l != None:
                    pivot_idx[l] = j
                    mat[:, l] = 0

INF = 'INF'
def pairs(mat: np.ndarray) -> list[tuple[int, int | str]]:
    p = []
    for (j, col) in enumerate(mat.T):
        l = low(col)
        if l == None:
            if all([low(c) != j for c in mat.T]):
                p.append((j, INF))
        else:
            p.append((l, j))
    return p

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

mat, f = sorted_boundary_matrix(cx, sum)
print(mat)
reduce(mat, cx, f)
print(mat)
print(pairs(mat))