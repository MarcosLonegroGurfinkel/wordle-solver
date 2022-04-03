import random

class WordListComm:
    
    def __init__(self) -> None:
        self.file_path = "words.txt"

    def get_list_of_words(self):
        list_of_words = []
        with open(self.file_path,'r') as f:
            for line in f:
                list_of_words.append(line.strip())
        random.shuffle(list_of_words)
        return list_of_words