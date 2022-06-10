import com.sudoku.Sudoku;
import org.junit.jupiter.api.Test;

import java.util.Arrays;
import java.util.HashSet;

import static org.junit.jupiter.api.Assertions.*;

class SudokuTest {
    @Test
    public void test_create_sudoku() {
        String sudokuText = "..53.....8......2..7..1.5..4....53...1..7...6..32...8..6.5....9..4....3......97..";
        Sudoku sudoku = new Sudoku(sudokuText);
        String text = sudoku.getText();
        assertEquals(sudokuText, text);
        System.out.println();
    }

    @Test
    public void test_print_sudoku() {
        String sudokuText = "..53.....8......2..7..1.5..4....53...1..7...6..32...8..6.5....9..4....3......97..";
        new Sudoku(sudokuText).print();
    }

    @Test
    public void test_sudoku_is_complete() {
        String sudokuText = "145327698839654127672918543496185372218473956753296481367542819984761235521839764";
        assertTrue(new Sudoku(sudokuText).isComplete());

        sudokuText = "..53.....8......2..7..1.5..4....53...1..7...6..32...8..6.5....9..4....3......97..";
        assertFalse(new Sudoku(sudokuText).isComplete());
    }

    @Test
    public void test_sudoku_is_solved() {
        String sudokuText = "145327698839654127672918543496185372218473956753296481367542819984761235521839764";
        assertTrue(new Sudoku(sudokuText).isSolved());
    }

    @Test
    public void test_sudoku_is_solved_false() {
        String sudokuText = "115327698839654127672918543496185372218473956753296481367542819984761235521839764";
        assertFalse(new Sudoku(sudokuText).isSolved());

        sudokuText = "123456789123456789123456789123456789123456789123456789123456789123456789123456789";
        assertFalse(new Sudoku(sudokuText).isSolved());
    }

    @Test
    public void test_sudoku_solve_simple() {
        String sudokuText = "145327698839654127672918543496185372218473956753296481367542819984761235521839764";
        Sudoku sudoku = new Sudoku(sudokuText).solve();
        assertEquals("145327698839654127672918543496185372218473956753296481367542819984761235521839764", sudoku.getText());
    }

    @Test
    public void test_sudoku_solve_get_candidate() {
        String sudokuText = "..53.....8......2..7..1.5..4....53...1..7...6..32...8..6.5....9..4....3......97..";
        Sudoku sudoku = new Sudoku(sudokuText).solve();
        assertEquals(new HashSet<>(Arrays.asList(1, 2, 6, 9)), sudoku.getCell(0, 0).getCandidates());
        assertEquals(new HashSet<>(Arrays.asList(1, 2, 4, 5, 8)), sudoku.getCell(8, 8).getCandidates());
        assertEquals(new HashSet<>(Arrays.asList()), sudoku.getCell(0, 2).getCandidates());
    }

    @Test
    public void test_sudoku_solve_lack_1() {
        String sudokuText = ".45327698839654127672918543496185372218473956753296481367542819984761235521839764";
        Sudoku sudoku = new Sudoku(sudokuText).solve();
        assertEquals("145327698839654127672918543496185372218473956753296481367542819984761235521839764", sudoku.getText());
    }

    @Test
    public void test_sudoku_solve_lack_more() {
        String sudokuText = "..5327698..9654127672918543....85372218473956753296481....42819..476123552183976.";
        Sudoku sudoku = new Sudoku(sudokuText).solve();
        assertEquals("145327698839654127672918543496185372218473956753296481367542819984761235521839764", sudoku.getText());
    }

    @Test
    public void test_sudoku_solve_multi() {
        String sudokuText = "..53.....8......2..7..1.5..4....53...1..7...6..32...8..6.5....9..4....3......97..";
        Sudoku sudoku = new Sudoku(sudokuText).solve();
        assertEquals("145327698839654127672918543496185372218473956753296481367542819984761235521839764", sudoku.getText());
    }

    @Test
    public void test_others() {
        String sudokuText = "8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..";
        Sudoku sudoku = new Sudoku(sudokuText).solve();
        sudoku.print();

        System.out.println();
        sudokuText = "..53.....8......2..7..1.5..4....53...1..7...6..32...8..6.5....9..4....3......97..";
        sudoku = new Sudoku(sudokuText).solve();
        sudoku.print();

        System.out.println();
        sudokuText = "98.7..6..5...9..7...43.....3....7.9..6....4.....5....82..9...1.....23........1..9";
        sudoku = new Sudoku(sudokuText).solve();
        sudoku.print();
    }
}