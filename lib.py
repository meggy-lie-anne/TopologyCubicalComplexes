from typing import Callable, Optional
import numpy as np

def is_degenerate(coord: int) -> bool:
    return coord % 2 == 0

class Cube:
    def __init__(self, coords: tuple) -> None:
        self.coords = coords
    
    def dimension(self) -> int:
        return len([c for c in self.coords if not is_degenerate(c)])

    def boundary(self) -> list["Cube"]:
        b = []
        for (i, c) in enumerate(self.coords):
            if not is_degenerate(c):
                left = list(self.coords)
                right = list(self.coords)
                left[i] = c - 1
                right[i] = c + 1
                b.append(Cube(tuple(left)))
                b.append(Cube(tuple(right)))
        return b
    
    def __iter__(self):
        return self.coords.__iter__()
    
    def __getitem__(self, i):
        return self.coords[i]
    
    def __len__(self):
        return self.coords.__len__()
    
    def __eq__(self, other):
        return self.coords == other.coords
    
    def __hash__(self) -> int:
        return tuple(self.coords).__hash__()
    
    def __repr__(self) -> str:
        return f'[{", ".join([str(c) for c in self.coords])}]'

class CubicalComplex:
    def __init__(self, cubes: list[Cube]) -> None:
        dim = len(cubes[0])
        for c in cubes:
            if len(c) != dim:
                raise Exception("All cubes in the same complex should have the same dimension")
        self.cubes = cubes

    def vertices(self):
        return [x for x in self.cubes if x.dimension() == 0]
    
    def adjacent_cubes(self, vertex: Cube) -> list[Cube]:
        def is_adjacent(cube: Cube) -> bool:
            adj_in_all_dimensions = True
            for (i, coord) in enumerate(vertex):
                adj_in_all_dimensions = adj_in_all_dimensions and (coord - 1 <= cube[i] and cube[i] <= coord + 1)
            return adj_in_all_dimensions
        
        return [c for c in self.cubes if is_adjacent(c) and c != vertex]
    
    def __iter__(self):
        return self.cubes.__iter__()
    
    def __len__(self):
        return self.cubes.__len__()
    
    def dimension(self):
        return len(self.cubes[0]) - 1

    def __repr__(self) -> str:
        return '{\n' + '\n'.join([ f'  {c},' for c in self.cubes ]) + '\n}'

VertexFiltration = Callable[[Cube], int]

def sorted_boundary_matrix(k: CubicalComplex, f: VertexFiltration) -> tuple[np.ndarray, list[Cube]]:
    vertices = k.vertices()
    sorted_vertices = sorted(vertices, key=f, reverse=True)
    print(sorted_vertices)
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
        for b in cube.boundary():
            row = findexes[b]
            boundary_matrix[row, col] = 1

    sorted_cubes = sorted(k.cubes, key=lambda c: findexes[c])
    return (boundary_matrix, sorted_cubes)

def low(row: np.ndarray) -> Optional[int]:
    for i in range(len(row) - 1, -1, -1):
        coeff = row[i]
        if coeff == 1:
            return i

def reduce(mat: np.ndarray, k: CubicalComplex, filtration: list[Cube]):
    pivot_idx = [0 for _ in range(len(mat))]
    for d in range(k.dimension(), 0, -1):
        for j in range(0, len(mat)):
            sx_dim = filtration[j].dimension()
            if sx_dim == d:
                l = low(mat[:, j])
                while l != None:
                    if pivot_idx[l] != 0:
                        mat[:, j] = (mat[:, j] + mat[:, pivot_idx[l]]) % 2
                    else:
                        break
                    l = low(mat[:, j])
                l = low(mat[:, j])
                if l != None:
                    pivot_idx[l] = j
                    mat[:, l] = 0

INF = float('inf')
Pair = tuple[int, int | float]

def pairs(mat: np.ndarray) -> list[Pair]:
    p = []
    for (j, col) in enumerate(mat.T):
        l = low(col)
        if l == None:
            if all([low(c) != j for c in mat.T]):
                p.append((j, INF))
        else:
            p.append((l, j))
    return p

def pairs_for_dimension(dimension: int, pairs: list[Pair], sorted_cubes: list[Cube]) -> list[Pair]:
    return [p for p in pairs if sorted_cubes[p[0]].dimension() == dimension]

def plot_pairs(pairs: list[Pair], sorted_cubes: list[Cube]):
    import matplotlib.pyplot as plt
    end = len(sorted_cubes)
    to_num = lambda x: end if x == INF else x
    plt.barh(
        [i for (i, _) in enumerate(pairs)],
        [to_num(p[1]) - p[0] for p in pairs],
        0.5,
        [p[0] for p in pairs],
        color=[(0.2, 0.2, 0.8) if p[1] == INF else (0.5, 0.5, 1) for p in pairs],
        tick_label=[f'{sorted_cubes[p[0]]} (dim {sorted_cubes[p[0]].dimension()})' for p in pairs]
    )
    plt.show()

def complex_from_sage(cubes: list[tuple]) -> CubicalComplex:
    def full_boundary(c: Cube) -> list[Cube]:
        res = [c]
        last_boundary = [c]
        for _ in range(0, c.dimension()):
            b = []
            for x in last_boundary:
                boundary = x.boundary()
                for y in boundary:
                    b = b + [y]
            res = res + b
            last_boundary = b
        return res

    def cube_from_sage(cube: tuple) -> list[Cube]:
        c = Cube(tuple([
            x[0] * 2 + len(set(x)) - 1
            for x in cube
        ]))
        return full_boundary(c)

    return CubicalComplex(list(set([
        x
        for c in cubes
        for x in cube_from_sage(c)
    ])))

def main(cx: CubicalComplex):
    print(len(cx), cx)
    mat, f = sorted_boundary_matrix(cx, cx.cubes.index)
    print([(x, x.dimension()) for x in f])
    print(mat)
    reduce(mat, cx, f)
    print(mat)
    print(pairs(mat))
    print([f[p[0]].dimension() for p in pairs(mat)])
    plot_pairs(pairs(mat), f)

cx = CubicalComplex([
    Cube((0, 0)),
    Cube((0, 2)),
    Cube((2, 2)),
    Cube((2, 0)),
    Cube((1, 0)),
    Cube((2, 1)),
    Cube((1, 2)),
    Cube((0, 1)),
])

projective_plane = complex_from_sage([
    ([0, 1], [0], [0], [0, 1], [0]),
    ([0, 1], [0], [0], [0], [0, 1]),
    ([0], [0, 1], [0, 1], [0], [0]),
    ([0], [0, 1], [0], [0, 1], [0]),
    ([0], [0], [0, 1], [0], [0, 1]),
    ([0, 1], [0, 1], [1], [0], [0]),
    ([0, 1], [1], [0, 1], [0], [0]),
    ([1], [0, 1], [0, 1], [0], [0]),
    ([0, 1], [0, 1], [0], [0], [1]),
    ([0, 1], [1], [0], [0], [0, 1]),
    ([1], [0, 1], [0], [0], [0, 1]),
    ([0, 1], [0], [0, 1], [1], [0]),
    ([0, 1], [0], [1], [0, 1], [0]),
    ([1], [0], [0, 1], [0, 1], [0]),
    ([0], [0, 1], [0], [0, 1], [1]),
    ([0], [0, 1], [0], [1], [0, 1]),
    ([0], [1], [0], [0, 1], [0, 1]),
    ([0], [0], [0, 1], [0, 1], [1]),
    ([0], [0], [0, 1], [1], [0, 1]),
    ([0], [0], [1], [0, 1], [0, 1])]
)

torus = complex_from_sage([
    ([1,1], [0,1], [1,1], [0,1]),
    ([0,1], [0,0], [0,0], [0,1]),
    ([0,0], [0,1], [0,1], [0,0]),
    ([0,1], [1,1], [0,1], [1,1]),
    ([0,0], [0,1], [0,0], [0,1]),
    ([0,0], [0,1], [1,1], [0,1]),
    ([0,1], [1,1], [0,1], [0,0]),
    ([0,1], [0,0], [1,1], [0,1]),
    ([0,1], [1,1], [0,0], [0,1]),
    ([0,1], [1,1], [1,1], [0,1]),
    ([1,1], [0,1], [0,0], [0,1]),
    ([1,1], [0,1], [0,1], [1,1]),
    ([0,1], [0,0], [0,1], [1,1]),
    ([1,1], [0,1], [0,1], [0,0]),
    ([0,1], [0,0], [0,1], [0,0]),
    ([0,0], [0,1], [0,1], [1,1])
])

klein_bottle = complex_from_sage([
    ([0,1], [0,0], [0,0], [0,0], [0,1], [1,1]),
    ([1,1], [0,0], [0,1], [0,1], [0,0], [0,0]),
    ([0,0], [0,0], [0,1], [0,0], [0,1], [1,1]),
    ([0,1], [0,0], [0,1], [1,1], [0,0], [1,1]),
    ([0,1], [0,0], [1,1], [0,1], [0,0], [0,0]),
    ([0,1], [0,1], [0,0], [0,0], [1,1], [0,0]),
    ([0,1], [0,0], [0,0], [0,0], [0,1], [0,0]),
    ([0,0], [0,1], [0,0], [1,1], [0,1], [1,1]),
    ([0,1], [1,1], [0,0], [0,0], [0,0], [0,1]),
    ([0,0], [0,0], [0,1], [1,1], [0,1], [1,1]),
    ([0,1], [0,0], [0,1], [1,1], [0,0], [0,0]),
    ([0,0], [0,1], [0,0], [0,1], [1,1], [1,1]),
    ([0,0], [0,1], [0,0], [1,1], [0,1], [0,0]),
    ([0,0], [0,0], [0,1], [0,0], [0,1], [0,0]),
    ([0,0], [0,1], [0,0], [0,1], [1,1], [0,0]),
    ([0,0], [0,0], [0,1], [1,1], [0,1], [0,0]),
    ([0,0], [0,1], [0,1], [0,0], [0,0], [1,1]),
    ([1,1], [1,1], [0,0], [0,0], [0,1], [0,1]),
    ([0,0], [1,1], [0,0], [0,1], [0,1], [1,1]),
    ([0,0], [0,0], [1,1], [0,1], [0,1], [1,1]),
    ([0,0], [0,1], [0,1], [0,0], [0,0], [0,0]),
    ([0,0], [0,0], [0,1], [0,1], [1,1], [1,1]),
    ([0,0], [1,1], [0,0], [0,1], [0,1], [0,0]),
    ([0,0], [0,0], [0,1], [0,1], [1,1], [0,0]),
    ([0,0], [0,0], [1,1], [0,1], [0,1], [0,0]),
    ([0,0], [1,1], [0,0], [0,0], [0,1], [0,1]),
    ([0,0], [0,1], [0,0], [0,1], [0,0], [1,1]),
    ([0,1], [1,1], [0,1], [0,0], [0,0], [1,1]),
    ([0,1], [0,1], [1,1], [0,0], [0,0], [1,1]),
    ([0,0], [0,1], [0,0], [0,1], [0,0], [0,0]),
    ([1,1], [0,1], [0,1], [0,0], [0,0], [1,1]),
    ([0,1], [1,1], [0,1], [0,0], [0,0], [0,0]),
    ([0,1], [0,0], [0,0], [0,1], [0,0], [1,1]),
    ([0,1], [0,1], [1,1], [0,0], [0,0], [0,0]),
    ([0,1], [1,1], [0,0], [0,0], [1,1], [0,1]),
    ([1,1], [0,1], [0,1], [0,0], [0,0], [0,0]),
    ([0,1], [0,0], [0,0], [0,1], [0,0], [0,0]),
    ([1,1], [0,1], [0,0], [0,0], [0,1], [1,1]),
    ([0,1], [0,0], [1,1], [0,1], [0,0], [1,1]),
    ([0,1], [0,1], [0,0], [0,0], [1,1], [1,1]),
    ([1,1], [0,0], [0,1], [0,1], [0,0], [1,1]),
    ([1,1], [0,1], [0,0], [0,0], [0,1], [0,0])
])

main(klein_bottle)