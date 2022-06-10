package com.sudoku;

import java.util.*;
import java.util.stream.Collectors;

public class Sudoku {
    private static final Set<Integer> VALID_SET = new HashSet<>(Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9));
    private final List<List<Cell>> sudoku;
    private static int STEPS = 0;

    public Sudoku(String sudokuText) {
        sudoku = new ArrayList<>();
        for (int i = 0; i < 81; i += 9) {
            List<Cell> row = sudokuText.substring(i, i + 9).chars()
                    .mapToObj((c) -> new Cell(c == '.' ? 0 : c - '0'))
                    .collect(ArrayList::new, ArrayList::add, ArrayList::addAll);
            sudoku.add(row);
        }
    }

    public Sudoku(Sudoku other) {
        sudoku = new ArrayList<>();
        for (int i = 0; i < 9; i++) {
            List<Cell> row = new ArrayList<>();
            for (int j = 0; j < 9; j++) {
                row.add(new Cell(other.getCell(i, j).getValue()));
            }
            sudoku.add(row);
        }
    }

    public String getText() {
        StringBuilder sb = new StringBuilder();
        for (List<Cell> row : sudoku) {
            for (Cell i : row) {
                sb.append(i.getValue() == 0 ? "." : i);
            }
        }
        return sb.toString();
    }

    public void print() {
        for (List<Cell> row : sudoku) {
            System.out.println(row);
        }
        System.out.println(STEPS);
    }

    public boolean isComplete() {
        for (List<Cell> row : sudoku) {
            for (Cell i : row) {
                if (i.getValue() == 0) {
                    return false;
                }
            }
        }
        return true;
    }

    public boolean isSolved() {
        for (List<Cell> row : sudoku) {
            Set<Integer> rowSet = row.stream().map(Cell::getValue).collect(Collectors.toSet());
            if (isInvalid(rowSet)) {
                return false;
            }
        }
        for (int c = 0; c < 9; c++) {
            Set<Integer> col = new HashSet<>();
            for (int r = 0; r < 9; r++) {
                col.add(sudoku.get(r).get(c).getValue());
            }
            if (isInvalid(col)) {
                return false;
            }
        }
        for (int r = 0; r < 9; r += 3) {
            for (int c = 0; c < 9; c += 3) {
                Set<Integer> square = new HashSet<>();
                for (int i = 0; i < 3; i++) {
                    for (int j = 0; j < 3; j++) {
                        square.add(sudoku.get(r + i).get(c + j).getValue());
                    }
                }
                if (isInvalid(square)) {
                    return false;
                }
            }
        }
        return true;
    }

    private boolean isInvalid(Set<Integer> rowSet) {
        return !VALID_SET.equals(rowSet);
    }

    public Sudoku solve() {
        STEPS = 0;
        return solve(this);
    }

    private Sudoku solve(Sudoku sudoku) {
        if (sudoku.isComplete() && sudoku.isSolved()) {
            return this;
        }
        sudoku.calculateCandidates();
        int minCandidates = Integer.MAX_VALUE;
        int minRow = 0;
        int minCol = 0;
        for (int r = 0; r < 9; r++) {
            for (int c = 0; c < 9; c++) {
                Cell cell = sudoku.getCell(r, c);
                if (cell.getValue() == 0) {
                    if (cell.getCandidates().size() < minCandidates) {
                        minCandidates = cell.getCandidates().size();
                        minRow = r;
                        minCol = c;
                    }
                }
            }
        }
        if (minCandidates == Integer.MAX_VALUE) {
            return null;
        }
        for (int i : getCell(minRow, minCol).getCandidates()) {
            Sudoku newSudoku = new Sudoku(sudoku);
            newSudoku.getCell(minRow, minCol).setValue(i);
            Sudoku solved = newSudoku.solve(newSudoku);
            STEPS += 1;
            if (solved != null) {
                return solved;
            }
        }
        return null;
    }

    private void calculateCandidates() {
        for (int r = 0; r < 9; r++) {
            for (int c = 0; c < 9; c++) {
                Cell cell = sudoku.get(r).get(c);
                if (cell.getValue() == 0) {
                    HashSet<Integer> candidates = new HashSet<>(VALID_SET);
                    for (int i = 0; i < 9; i++) {
                        candidates.remove(sudoku.get(r).get(i).getValue());
                        candidates.remove(sudoku.get(i).get(c).getValue());
                    }
                    int rStart = (r / 3) * 3;
                    int cStart = (c / 3) * 3;
                    for (int i = 0; i < 3; i++) {
                        for (int j = 0; j < 3; j++) {
                            candidates.remove(sudoku.get(rStart + i).get(cStart + j).getValue());
                        }
                    }
                    cell.setCandidates(candidates);
                }
            }
        }
    }

    public Cell getCell(int r, int c) {
        return sudoku.get(r).get(c);
    }
}
