import requests
from bs4 import BeautifulSoup
from random import choice
from time import sleep

BASE_URL = "http://quotes.toscrape.com"  # Link to the website used for scraping


def scrape_quotes():  # Collects all quote elements
    next_page = "/page/1/"  # Link to the next page (will be changing every step of the loop)
    quotes = []  # List that will store quote elements
    while next_page:
        response = requests.get(BASE_URL + next_page)
        page = BeautifulSoup(response.text, "html.parser")  # Gets HTML code of the page
        quotes.extend(page.find_all(class_="quote"))  # Adds all quotes found on the page to the list
        next_btn = page.find(class_="next")  # Looks for next page
        next_page = f"{next_btn.find('a')['href']}" if next_btn else None  # Saves the link/sets it to None
        sleep(2)  # Pauses scraping for 2 seconds
    return quotes


# Extracts and returns a dictionary with a quote, an author and link to the author's bio
def get_quote_info(quote):
    text = quote.find(class_="text").get_text()
    author = quote.find(class_="author").get_text()
    author_bio = quote.find("a")["href"]
    return {"text": text, "author": author, "bio": author_bio}


# Counts how long author's last name is
def get_name_len(quote_info):
    return "Author's last name is " + str(len(quote_info["author"].split(" ")[-1])) + " characters long"


# Gets author's date of birth
def get_dob(quote_info):
    bio_response = requests.get(f"{BASE_URL}{quote_info['bio']}")
    bio_page = BeautifulSoup(bio_response.text, "html.parser")  # Gets HTML code of author's bio page
    dob = "The author was born on " + bio_page.find(class_="author-born-date").get_text() + \
          " " + bio_page.find(class_="author-born-location").get_text()
    return dob


# Gets author's initials
def get_initials(quote_info):
    names = quote_info["author"].split(" ")
    names = [name.split(".") for name in names]
    initials = [init[0] for name in names for init in name if init]
    return "Author's initials are " + ". ".join(initials)


# Prints a hint if player's guess was incorrect
def print_hint(remaining_guesses, info):
    if remaining_guesses == 3:
        print(f"Here's a hint: {get_dob(info)}.")
    elif remaining_guesses == 2:
        print(f"Here's a hint: {get_initials(info)}.")
    elif remaining_guesses == 1:
        print(f"Here's a hint: {get_name_len(info)}.")
    else:
        print(f"Sorry, you've run out of guesses. The answer is {info['author']}")


# Game logic
def start_game(quotes):
    rand_quote = choice(quotes)  # Chooses a random quote from the list
    info = get_quote_info(rand_quote)  # Extracts necessary information
    guesses = 4  # Player has 4 tries to guess the author
    print(f"Here's a quote:\n'{info['text']}'")
    while guesses > 0:
        answer = input(f"Who said this? Guesses remaining: {guesses}\n")
        if answer.lower() == info["author"].lower():
            print("You guessed correctly! Congratulations!")
            break
        guesses -= 1
        print_hint(guesses, info)
    play_again = ""
    while play_again not in ("y", "yes", "n", "no"):
        play_again = input("Would you like to play again(y/n)?\n")
    if play_again in ("y", "yes"):
        print("Great! Here we go again...")
        return start_game(quotes)
    else:
        print("See you next time!")


quotes_list = scrape_quotes()
start_game(quotes_list)
