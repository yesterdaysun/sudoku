import itertools
import time
from copy import deepcopy
from functools import reduce

import numpy as np


class SudokuPoint(object):
    def __init__(self, index, candidates):
        self.index = index
        self.value = None
        self.candidates = candidates

    def get_key(self):
        return "".join(map(str, self.candidates))


class Sudoku(object):
    def __init__(self, text):
        self.grid = None
        self.count = 0

        self.init_grid(text)

    def init_grid(self, text):
        num = np.reshape(np.array(list(map(lambda n: 0 if n == "." else int(n), text))), (9, 9))
        self.grid = np.empty((9, 9), dtype=SudokuPoint)
        for index, value in np.ndenumerate(self.grid):
            self.grid[index] = SudokuPoint(index, {1, 2, 3, 4, 5, 6, 7, 8, 9})
        for index, value in np.ndenumerate(num):
            if value != 0:
                if not self.set_point_value(index, value):
                    raise Exception("Invalid Sudoku!")

    def set_point_value(self, index, value):
        self.count += 1
        point = self.grid[index]
        point.value = value
        point.candidates = None
        valid = True
        for region in self.get_regions_by_index(index):
            valid_state = self.discard_candidates(region, {value}, {index})
            valid = valid and valid_state
        return valid

    def get_row(self, index):
        return self.grid[index[0]]

    def get_col(self, index):
        return self.grid[:, index[1]]

    def get_block(self, index):
        row, col = map(lambda x: int(x / 3) * 3, index)
        return self.grid[row:row + 3, col:col + 3].flat

    def get_regions(self):
        for i in range(0, 9):
            yield self.grid[i]
            yield self.grid[:, i]
            row, col = int(i / 3) * 3, (i % 3) * 3
            yield self.grid[row:row + 3, col:col + 3].flat

    def get_rows_and_cols(self):
        for i in range(0, 9):
            yield self.grid[i]
            yield self.grid[:, i]

    def get_blocks(self):
        for i in range(0, 9):
            row, col = int(i / 3) * 3, (i % 3) * 3
            yield self.grid[row:row + 3, col:col + 3].flat

    def get_regions_by_index(self, index):
        yield self.get_row(index)
        yield self.get_col(index)
        yield self.get_block(index)

    def get_regions_by_points(self, points):
        index = points[0].index
        if self.is_same_row(points):
            yield self.get_row(index)
        if self.is_same_col(points):
            yield self.get_col(index)
        if self.is_same_block(points):
            yield self.get_block(index)

    def discard_candidates(self, region, candidates, exclude_indexes):
        valid = True
        for point in region:
            if point.candidates and point.index not in exclude_indexes:
                point.candidates = point.candidates - candidates
                if len(point.candidates) == 0:
                    valid = False
        return valid

    def is_region_solved(self, region):
        return len(reduce(lambda m, p: m.remove(p.value) or m, region, {1, 2, 3, 4, 5, 6, 7, 8, 9})) == 0

    def is_all_set(self):
        return all(map(lambda p: p.value, self.grid.flat))

    def is_solved(self):
        return all(map(lambda r: self.is_region_solved(r), self.get_regions()))

    def is_same_row(self, points):
        if len(points) <= 1:
            return True
        row = points[0].index[0]
        return all(map(lambda h: h.index[0] == row, points))

    def is_same_col(self, points):
        if len(points) <= 1:
            return True
        col = points[0].index[1]
        return all(map(lambda h: h.index[1] == col, points))

    def get_block_num(self, index):
        row, col = index
        return int(row / 3) * 3 + int(col / 3)

    def is_same_block(self, points):
        if len(points) <= 1:
            return True
        block_num = self.get_block_num(points[0].index)
        return all(map(lambda p: self.get_block_num(p.index) == block_num, points))

    def to_plain_text(self):
        return "".join(list(map(lambda p: str(p.value) if p.value else '.', self.grid.flat)))

    def print_grid_simple(self):
        print(np.reshape(np.array(list(map(lambda p: p.value or 0, self.grid.flat))), (9, 9)))

    def print_step(self, debug, name, index, value):
        if not debug:
            return
        print(name)
        y, x = index
        print(f"{chr(y + 65)}{x + 1}\t{value}")

    def print_rollback(self, debug, index, value):
        if not debug:
            return
        print("Rollback")
        y, x = index
        print(f"{chr(y + 65)}{x + 1}\t{value}")
        self.print_grid(debug)

    def print_grid(self, debug):
        if not debug:
            return
        result = np.full((27, 27), None, dtype=object)
        for index, point in np.ndenumerate(self.grid):
            y, x = index
            if point.value:
                result[y * 3:y * 3 + 3, x * 3:x * 3 + 3] = [
                    ['+', '-', '+'],
                    ['|', point.value, '|'],
                    ['+', '-', '+'],
                ]
            else:
                candidates = list(point.candidates)
                block = result[y * 3:y * 3 + 3, x * 3:x * 3 + 3].flat
                block[0:len(candidates)] = candidates

        print("     [1] [2] [3]   [4] [5] [6]   [7] [8] [9]   ")
        print("   + --- --- --- + --- --- --- + --- --- --- + ")
        for y in range(0, 27):
            if (y - 1) % 3 == 0:
                c = chr(int((y - 1) / 3) + 65)
                print(f"[{c}]", end="")
            else:
                print("   ", end="")
            for x in range(0, 27):
                if x == 0:
                    print("| ", end="")
                print(result[y, x] or ' ', end="")
                if (x + 1) % 3 == 0:
                    print(" ", end="")
                if (x + 1) % 9 == 0:
                    print("| ", end="")
            print()
            if (y + 1) % 9 == 0:
                print("   + --- --- --- + --- --- --- + --- --- --- + ")
            if (y + 1) % 3 == 0 and y != 26:
                print("   |             |             |             | ")


# 唯一候选数法
class UniqueCandidateFinder(object):
    def __init__(self, sudoku, debug=False):
        self.sudoku = sudoku
        self.name = "UniqueCandidateFinder"
        self.debug = debug

    # 1. 顺利解完, 不管有几个唯一解, 都返回True
    # 2. 发现空候选集, 说明无解, 返回False
    def solve(self):
        has_unique_solution = True
        while has_unique_solution:
            has_unique_solution = False
            for index, point in np.ndenumerate(self.sudoku.grid):
                if point.candidates:
                    if len(point.candidates) == 0:
                        return False
                    if len(point.candidates) == 1:
                        has_unique_solution = True
                        self.sudoku.print_step(self.debug, self.name, index, point.candidates)
                        self.sudoku.print_grid(self.debug)
                        if not self.sudoku.set_point_value(index, list(point.candidates)[0]):
                            return False
        return True


# 隐性唯一候选数法
class ImplicitUniqueCandidateFinder(object):
    def __init__(self, sudoku, debug=False):
        self.sudoku = sudoku
        self.name = "OnlyCandidateFinder"
        self.debug = debug

    def filter_only_candidate(self, current_point):
        for block in self.sudoku.get_regions_by_index(current_point.index):
            current_candidates = current_point.candidates.copy()
            for point in block:
                if point.candidates and point.index != current_point.index:
                    for n in point.candidates:
                        current_candidates.discard(n)
            if len(current_candidates) == 1:
                return list(current_candidates)[0]
        return None

    def solve(self):
        has_unique_solution = True
        while has_unique_solution:
            has_unique_solution = False
            for index, point in np.ndenumerate(self.sudoku.grid):
                if point.candidates:
                    candidate = self.filter_only_candidate(point)
                    if candidate:
                        has_unique_solution = True
                        self.sudoku.print_step(self.debug, self.name, index, candidate)
                        self.sudoku.print_grid(self.debug)
                        if not self.sudoku.set_point_value(index, candidate):
                            return False
        return True


# 候选数区块删减法
class BlockCandidateFinder(object):
    def __init__(self, sudoku, debug=False):
        self.sudoku = sudoku
        self.name = "BlockCandidateFinder"
        self.debug = debug

    def solve(self):
        for block in self.sudoku.get_blocks():
            processed = {}
            for point in block:
                if point.candidates:
                    for n in point.candidates:
                        if n not in processed:
                            processed[n] = []
                        processed[n].append(point)
            for n, points in filter(lambda e: 2 <= len(e[1]) <= 3, processed.items()):
                if self.sudoku.is_same_row(points):
                    indexes = set(map(lambda p: p.index, points))
                    self.sudoku.print_step(self.debug, self.name, points[0].index, n)
                    if not self.sudoku.discard_candidates(self.sudoku.get_row(points[0].index), {n}, indexes):
                        return False
                    self.sudoku.print_grid(self.debug)
                elif self.sudoku.is_same_col(points):
                    indexes = set(map(lambda p: p.index, points))
                    if not self.sudoku.discard_candidates(self.sudoku.get_col(points[0].index), {n}, indexes):
                        return False
        return True


# 隐性候选数对删减法
class ImplicitDoubleCandidateFinder(object):
    def __init__(self, sudoku, debug=False):
        self.sudoku = sudoku
        self.name = "ImplicitDoubleCandidateFinder"
        self.debug = debug

    def solve(self):
        for region in self.sudoku.get_regions():
            processed = {}
            for point in region:
                if point.candidates:
                    for n in point.candidates:
                        if n not in processed:
                            processed[n] = set()
                        processed[n].add(point.index)
            entries = list(filter(lambda e: len(e[1]) == 2, processed.items()))
            for i in range(0, len(entries) - 1):
                for j in range(i + 1, len(entries)):
                    if entries[i][1] == entries[j][1]:
                        candidates = {entries[i][0], entries[j][0]}
                        for index in entries[i][1]:
                            point = self.sudoku.grid[index]
                            if len(point.candidates) > 2:
                                point.candidates = candidates
        return True


# 候选数对删减法
class DoubleCandidateFinder(object):
    def __init__(self, sudoku, debug=False):
        self.sudoku = sudoku
        self.name = "DoubleCandidateFinder"
        self.debug = debug

    def find_pair_candidates(self, region):
        points = list(filter(lambda p: p.candidates and len(p.candidates) == 2, region))
        if len(points) <= 1:
            return None
        processed = {}
        for point in points:
            key = point.get_key()
            if key not in processed:
                processed[key] = []
            processed[key].append(point)

        for values in processed.values():
            if len(values) == 2:
                return values
        return None

    def solve(self):
        for region in self.sudoku.get_regions():
            pair = self.find_pair_candidates(region)
            if pair is not None:
                indexes = set(map(lambda p: p.index, pair))
                for r in self.sudoku.get_regions_by_points(pair):
                    if not self.sudoku.discard_candidates(r, pair[0].candidates, indexes):
                        return False
        return True


# 三候选数对删减法
class TripleCandidateFinder(object):
    def __init__(self, sudoku, debug=False):
        self.sudoku = sudoku
        self.name = "TripleCandidateFinder"
        self.debug = debug

    def find_triple_candidates(self, region):
        if len(list((filter(lambda p: p.candidates, region)))) < 4:
            return None
        points = list(filter(lambda p: p.candidates and len(p.candidates) == 3, region))
        if len(points) < 3:
            return None
        processed = {}
        for point in points:
            key = point.get_key()
            if key not in processed:
                processed[key] = []
            processed[key].append(point)

        for values in processed.values():
            if len(values) == 3:
                return values
        return None

    def solve(self):
        for region in self.sudoku.get_rows_and_cols():
            points = self.find_triple_candidates(region)
            if points is not None:
                indexes = set(map(lambda p: p.index, points))
                for r in self.sudoku.get_regions_by_points(points):
                    self.sudoku.print_step(self.debug, self.name, points[0].index, indexes)
                    self.sudoku.print_grid(self.debug)
                    if not self.sudoku.discard_candidates(r, points[0].candidates, indexes):
                        return False
                    self.sudoku.print_grid(self.debug)

        return True


# 三数集删减法
class TripleCandidateFinder2(object):
    def __init__(self, sudoku, debug=False):
        self.sudoku = sudoku
        self.name = "TripleCandidateFinder2"
        self.debug = debug

    def find_triple_candidates(self, region):
        if len(list((filter(lambda p: p.candidates, region)))) < 4:
            return None
        points = list(filter(lambda p: p.candidates and 2 <= len(p.candidates) == 3, region))
        if len(points) < 3:
            return None
        for combination in itertools.combinations(points, 3):
            candidates = set()
            for point in combination:
                candidates.update(point.candidates)
            if len(candidates) != 3:
                continue
            processed = {}
            for point in combination:
                for n in point.candidates:
                    if n not in processed:
                        processed[n] = 0
                    processed[n] += 1
            if all(map(lambda x: x >= 2, processed.values())):
                return combination
        return None

    def solve(self):
        for region in self.sudoku.get_regions():
            points = self.find_triple_candidates(region)
            if points is not None:
                indexes = set(map(lambda p: p.index, points))
                for r in self.sudoku.get_regions_by_points(points):
                    self.sudoku.print_step(self.debug, self.name, points[0].index, indexes)
                    self.sudoku.print_grid(self.debug)
                    if not self.sudoku.discard_candidates(r, points[0].candidates, indexes):
                        return False
                    self.sudoku.print_grid(self.debug)

        return True


# 候选数矩形删减法
class RectangleCandidateFinder(object):
    def __init__(self, sudoku, debug=False):
        self.sudoku = sudoku
        self.name = "RectangleCandidateFinder"
        self.debug = False

    def is_rectangle(self, points):
        p1, p2, p3, p4 = points
        return p1[0] == p2[0] and p3[0] == p4[0] and p1[1] == p3[1] and p2[1] == p4[1]

    def find_vertex(self, row):
        points = list(filter(lambda p: p.candidates, row))
        if len(points) < 2:
            return None, None
        processed = {}
        for point in points:
            for n in point.candidates:
                if n not in processed:
                    processed[n] = []
                processed[n].append(point)
        for n, points in processed.items():
            if len(points) == 2:
                yield n, points
        return None, None

    def find_other_vertex(self, target, vertex, row):
        points = list(filter(lambda p: p.candidates, row))
        if len(points) < 2:
            return None
        result = []
        for point in points:
            for n in point.candidates:
                if n == target:
                    result.append(point)
        if len(result) != 2:
            return None
        result = [vertex[0].index, vertex[1].index, result[0].index, result[1].index]
        result = sorted(result)
        if self.is_rectangle(result):
            return result

    def find_rectangle_candidates(self):
        for i in range(0, 8):
            row = self.sudoku.get_row((i, 0))
            for n, points in self.find_vertex(row):
                if n is None:
                    continue
                for j in range(i + 1, 9):
                    row2 = self.sudoku.get_row((j, 0))
                    vertex = self.find_other_vertex(n, points, row2)
                    if vertex:
                        return n, vertex
        return None, None

    def solve(self):
        n, vertex = self.find_rectangle_candidates()
        if n is not None:
            p1, p2, p3, p4 = vertex
            indexes = {p1, p2, p3, p4}
            self.sudoku.print_step(self.debug, self.name, p1, indexes)
            self.sudoku.print_grid(self.debug)
            if not self.sudoku.discard_candidates(self.sudoku.get_col(p1), {n}, indexes):
                return False
            if not self.sudoku.discard_candidates(self.sudoku.get_col(p2), {n}, indexes):
                return False
            self.sudoku.print_grid(self.debug)

        return True


FINDERS = [
    UniqueCandidateFinder,
    ImplicitUniqueCandidateFinder,
    BlockCandidateFinder,
    ImplicitDoubleCandidateFinder,
    DoubleCandidateFinder,
    TripleCandidateFinder,
    TripleCandidateFinder2,
    RectangleCandidateFinder,
    UniqueCandidateFinder,
    ImplicitUniqueCandidateFinder,
]


class BestPointFinder(object):
    def __init__(self, sudoku):
        self.sudoku = sudoku
        self.name = "BestPointFinder"

    def find(self):
        best_index = None
        best_candidates = np.zeros(10)
        for index, point in np.ndenumerate(self.sudoku.grid):
            if point.candidates:
                if len(point.candidates) == 0:
                    return index, []
                if len(point.candidates) == 1:
                    return index, point.candidates
                if len(point.candidates) < len(best_candidates):
                    best_index = index
                    best_candidates = point.candidates
        return best_index, best_candidates


class SudokuSolver(object):
    def __init__(self, text):
        self.sudoku = Sudoku(text)
        self.guess_count = 0
        self.debug = False

    def solve_unique_solutions(self):
        if self.sudoku.is_all_set():
            return True
        for finder_ctor in FINDERS:
            finder = finder_ctor(self.sudoku, self.debug)
            if not finder.solve():
                return None
            if self.sudoku.is_all_set():
                return True
        return False

    def dfs(self):
        state = self.solve_unique_solutions()
        if state is None:
            return False
        if state:
            return self.sudoku.is_solved()
        index, candidates = BestPointFinder(self.sudoku).find()
        if self.debug:
            self.sudoku.print_step(self.debug, "BestPointFinder", index, candidates)
            self.sudoku.print_grid(self.debug)

        if len(candidates) == 0:
            return False

        self.guess_count += 1
        for n in candidates:
            old = deepcopy(self.sudoku.grid)
            valid = self.sudoku.set_point_value(index, n)
            if not valid:
                self.sudoku.print_rollback(self.debug, index, n)
                self.sudoku.grid = old
                continue
            if self.dfs():
                return True
            self.sudoku.print_rollback(self.debug, index, n)
            self.sudoku.grid = old
        return False

    def solve(self):
        self.sudoku.print_grid_simple()
        start = time.time()

        if not self.dfs():
            raise Exception("Sudoku is wrong")

        print("\nAnswer:")
        self.sudoku.print_grid_simple()
        end = time.time()
        print(f"Guess Count: {self.guess_count}")
        print(f"Point Count: {self.sudoku.count}")
        print(f"Elapsed Time: {round(end - start, 2)}s")
        return self.sudoku.to_plain_text()


if __name__ == '__main__':
    # test(SudokuSolver)
    SudokuSolver("..53.....8......2..7..1.5..4....53...1..7...6..32...8..6.5....9..4....3......97..").solve()
    # SudokuSolver(".......59.1...4....8.1...........4.75.3.6....9........6......3......1....7.8..2..").solve()
    SudokuSolver("8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..").solve()
    # SudokuSolver("......8....2.7..4....3..6.16..1....5..9.4........57.....7..5.9.3.....1.8.8.......").solve()
    SudokuSolver("98.7..6..5...9..7...43.....3....7.9..6....4.....5....82..9...1.....23........1..9").solve()
    # SudokuSolver("....1.6..1.4695.23.6..84.....5.4...8.1..3..9.7...5.2....1869.5295.4231....2571...").solve()
    SudokuSolver("..1.....2.3...4.5.6...2.7.......5.....8.7.1...9.3.......7.6...8.4.....9.8.....2..").solve()
