import random
from collections import Counter


class SolverLogic:
    def __init__(self, list_of_words) -> None:
        
        self.__list_of_words = list_of_words
        self.__yellow_letters = []
        self.__found = {}  # dictionary of index (0 to 4) to letter

        self.__min_number_appearances = {}  # dictionary of letter to min number of appearances
        self.__max_number_appearances = {}  # dictionary of letter to max number of appearances


    def choose_next_guess(self):
        for word in self.__list_of_words:
            if self.__passes_green(word) and self.__passes_yellow(word) and self.__passes_number_of_appearances(word):
                return word
        raise Exception()


    def choose_random_word(self):
        word = random.choice(self.__list_of_words)
        return word

    def __passes_number_of_appearances(self, word):
        # for each letter in word, count the number of times it appears
        # add the number of times that it appears in green and in yellow
        # if the numbers match return true, else return false
        c = Counter(word)
        for letter in c:
            if letter in self.__min_number_appearances and c[letter] < self.__min_number_appearances[letter]:
                return False

            if letter in self.__max_number_appearances and c[letter] > self.__max_number_appearances[letter]:
                return False
        
        return True

    def __passes_green(self, word):
        for index in self.__found:
            if word[index] != self.__found[index]:
                return False
        return True

    def __passes_yellow(self, word):
        for option in self.__yellow_letters:
            letter = option[0]
            positions_list = option[1]

            if letter not in word:
                return False
            
            for position in positions_list:
                if word[position] == letter:
                    return False

        return True

    def save_new_info(self, last_guess, result):
        
        for i in range(len(result)):
            color = result[i]
            letter = last_guess[i]

            if color == 'y':
                if self.__is_in_yellow_letters(letter):
                    index = self.__find_index_of_letter(letter)
                    self.__yellow_letters[index][1].append(i)
                else:
                    self.__yellow_letters.append([letter, [i]])

            elif color == 'g':
                self.__found[i] = letter

        # index of black letters
        word = str(last_guess)
        indexes_of_black = []
        for i in range(len(result) - 1, -1, -1):
            if result[i] == 'b':
                indexes_of_black.append(i)
        
        # remove all black letters from word
        for index in indexes_of_black:
            word = word[0:index] + word[index + 1:]
        
        # create counter of yellow and green letters
        c = Counter(word)

        # for each one found, if it is not in self.min_number_appearances, add it
        for letter in c:
            if letter not in self.__min_number_appearances:
                self.__min_number_appearances[letter] = c[letter]
            # if it is and the value is greater, replace it
            else:
                if c[letter] > self.__min_number_appearances[letter]:
                    self.__min_number_appearances[letter] = c[letter]


        # save max number of appearances
        for index in indexes_of_black:
            black_letter = last_guess[index]
            number_of_green_and_yellow_appearances = word.count(black_letter)
            self.__max_number_appearances[black_letter] = number_of_green_and_yellow_appearances


    @staticmethod
    def is_solution(result):
        return all(x == 'g' for x in result)

    def __is_in_yellow_letters(self, letter):
        for option in self.__yellow_letters:
            if letter == option[0]:
                return True
        return False

    def __find_index_of_letter(self, letter):
        for i in range(len(self.__yellow_letters)):
            option = self.__yellow_letters[i]
            if option[0] == letter:
                return i

        raise Exception()
