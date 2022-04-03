from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


class SeleniumComm:

    def __init__(self) -> None:
        self.__url = "https://www.nytimes.com/games/wordle/index.html"
        self.__driver = webdriver.Chrome("./chromedriver")

    def solve_wordle(self, solver):

        self.__driver.get(self.__url)
        time.sleep(2)

        # click body to elimintate wordl menu explanation
        body = self.__driver.find_element_by_tag_name("body")
        body.click()
    
        time.sleep(2)  # wait for page to load

        attempt = 1  # keeps track of current attempt number
        guess = solver.choose_random_word()  # first guess is always random
        while attempt <= 6:
            time.sleep(5)  # doesn't work without this
            body.send_keys(guess)  # enter guess
            time.sleep(2)  # let guess load
            body.send_keys(Keys.ENTER)  # click enter

            parsed_result = self.__parse_result(attempt)

            if solver.is_solution(parsed_result):
                break
            else:
                solver.save_new_info(guess, parsed_result)
                guess = solver.choose_next_guess()
                attempt += 1

        time.sleep(15)  # sleep to see the results
        self.__driver.quit()


    def __parse_result(self, attempt_number):
        
        # find letter boxes of last attempt
        game_app = self.__driver.find_element_by_tag_name('game-app')
        shadow_root1 = self.__driver.execute_script('return arguments[0].shadowRoot', game_app)
        board = shadow_root1.find_element_by_id("board")
        game_rows = board.find_elements_by_tag_name("game-row")  # find rows
        game_row = game_rows[attempt_number - 1]  # choose appropiate row for last attempt
        shadow_root2 = self.__driver.execute_script('return arguments[0].shadowRoot', game_row)
        row = shadow_root2.find_element_by_class_name("row")
        game_tiles = row.find_elements_by_xpath(".//*")

        # parse the evaluation of the last attempt
        result = []
        for tile in game_tiles:
            evaluation = tile.get_attribute("evaluation")
            if evaluation == "absent":
                result.append('b')
            elif evaluation == "present":
                result.append('y')
            else:
                result.append('g')

        return result
