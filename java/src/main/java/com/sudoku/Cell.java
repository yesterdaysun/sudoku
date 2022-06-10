package com.sudoku;

import lombok.Data;

import java.util.HashSet;
import java.util.Set;

@Data
public class Cell {
    private Integer value;
    private Set<Integer> candidates = new HashSet<>();

    public Cell(int i) {
        this.value = i;
    }

    @Override
    public String toString() {
        return value.toString();
    }
}
