from time import sleep

from Business.Hosts.Host import Host
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

URL= "https://semantle.com/"

class OnlineHost(Host):
        ## check if the guess word is match
    def __init__(self):
        self.browser= None
    def check_word(self, word):
        #sleep(2)
        print('start!')
        guess = self.browser.find_element(By.ID, "guess")
        guess.send_keys(word)
        guess_btn = self.browser.find_element(By.ID, value='guess-btn')
        guess_btn.click()
        print('guessed!')
        sleep(2)
        table=  self.browser.find_element(By.XPATH, value='//*[@id="guesses"]/tbody')
        print(table.text)
        return 0.5
    ## select word and start game
    def select_word_and_start_game(self):
        self.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.browser.get(URL)
        sleep(2)
        rules_btn = self.browser.find_element(By.ID, value='rules-close')
        rules_btn.click()

    def quitGame(self):
        self.browser.quit()
