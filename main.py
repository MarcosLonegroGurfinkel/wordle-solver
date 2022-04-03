from SeleniumComm import SeleniumComm
from SolverLogic import SolverLogic
from WordListComm import WordListComm



def main():
    wc = WordListComm()
    list_of_words = wc.get_list_of_words()

    solver_logic = SolverLogic(list_of_words)

    sc = SeleniumComm()
    sc.solve_wordle(solver_logic)

# run from command line
if __name__ == "__main__":
    main()