from time import sleep

from Business.Hosts.Host import Host
from selenium import webdriver
from selenium.webdriver.common.by import By

URL= "https://semantle.com/"

class OnlineHost(Host):
        ## check if the guess word is match
    def __init__(self):
        self.browser= None
        self.guesses={}
        self.legal_guesses= 0
    def check_word(self, word):
        guess = self.browser.find_element(By.ID, "guess")
        guess.send_keys(word)
        guess_btn = self.browser.find_element(By.ID, value='guess-btn')
        guess_btn.click()
        sleep(2)
        table=  self.browser.find_element(By.XPATH, value='//*[@id="guesses"]/tbody')
        postTable = table.text.split("\n")[1:-1:2]
        if self.legal_guesses == len(postTable):
            if word not in self.guesses.keys():
                guess.clear()
                return "illegal word - try again"
        else:
            self.legal_guesses += 1
            guess_similarity = [tuple(row.split())[2] for row in postTable]
            self.guesses[word] = float(guess_similarity[0])
        sleep(2)
        return self.guesses[word]


    ## select word and start game
    def select_word_and_start_game(self,out):
        out("===========LOADING ONLINE SERVER============")
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument("disable-gpu")
        # OR options.add_argument("--disable-gpu")
        self.browser = webdriver.Chrome('chromedriver', chrome_options=options)
        self.browser.get(URL)
        sleep(2)
        rules_btn = self.browser.find_element(By.ID, value='rules-close')
        rules_btn.click()

    def quitGame(self):
        self.browser.quit()
