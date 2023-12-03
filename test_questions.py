import requests
import json
import random
import time
import zmq

another_count = 0
new_count = 0
user_welcome = "Welcome to Quizzical Trivia"
user_difficulty_easy = "Easy"
user_difficulty_medium = "Medium"
user_difficulty_hard = "Hard"
categories = ["music", "sport_and_leisure", "film_and_tv", "arts_and_literature", "history", "society_and_culture",
              "science", "geography", "food_and_drink", "general_knowledge"]

print("""
           .--.                   .---.
       .---|__|           .-.     |~~~|
    .--|===|--|_          |_|     |~~~|--.
    |  |===|  |'\     .---!~|  .--|   |--|
    |%%|   |  |.'\    |===| |--|%%|   |  |
    |%%|   |  |\.'\   |   | |__|  |   |  |
    |  |   |  | \  \  |===| |==|  |   |  |
    |  |   |__|  \.'\ |   |_|__|  |~~~|__|
    |  |===|--|   \.'\|===|~|--|%%|~~~|--|
    ^--^---'--^    `-'`---^-^--^--^---'--'

    """)


# Lists of spanish, english, swedish, french, and polish words
one_list = ["uno: Spanish", "one: English", "ett: Swedish", "un: French", "jeden: Polish"]
two_list = ["dos: Spanish", "two: English", "två: Swedish", "deux: French", "dwa: Polish"]
three_list = ["tres: Spanish", "three: English", "tre: Swedish", "trois: French", "trzy: Polish"]


def introduction():
    """Introduces user to the program and counts down until program begins"""
    user_name = input("What is your name?")
    print(user_welcome + ", " + user_name)
    print("")
    time.sleep(1)
    print(random.choice(one_list))
    time.sleep(1)
    print(random.choice(two_list))
    time.sleep(1)
    print(random.choice(three_list))
    time.sleep(1)
    print("")
    print("")


introduction()

def ask_cat_diff():
    """Asks user to select which category and difficulty for specific question"""
    print('\n'.join([", ".join([category for category in categories[i:i + 3]]) for i in range(0, len(categories), 3)]))
    cat = input("Which category would you like to try?")
    print("")
    print("Easy, Medium, or Hard?")
    diff = input("Select a difficulty")


def check_cat_diff(cat, diff):
    """Validates user input for category and difficulty"""
    if cat not in categories:
        print("")
        print("Please select a valid category")
        print("")
        complete()
    if diff.lower() != "easy" and diff.lower() != "medium" and diff.lower() != "hard":
        print("")
        print("Please select Easy, Medium or Hard")
        print("")
        complete()


def random_category(new_category):
    random_cat_user_input = input("Would you like to choose a random category? Y/N")

    if random_cat_user_input.lower() == "y":
         new_category = random.choice(categories)






def complete():
    """Uses microservice to retrieve data from API call"""

    print('\n'.join([", ".join([category for category in categories[i:i + 3]]) for i in range(0, len(categories), 3)]))
    get_category = input("Which category would you like to try?")
    print("")
    print("Easy, Medium, or Hard?")
    print("Points distribution: Easy = 1, Medium = 2, Hard = 3")
    get_diff = input("Select a difficulty")
    check_cat_diff(get_category, get_diff)

    random_cat_user_input = input("Or would you like to choose a random category? Y/N")

    if random_cat_user_input.lower() == "y":
        get_category = random.choice(categories)


    context = zmq.Context()
    #  Socket to talk to server
    print("Connecting to trivia app server…")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")
    request = {"request": "getQuestion", "category": f"{get_category}", "difficulty": f"{get_diff}"}
    string_request = json.dumps(request)
    encoded_request = string_request.encode('UTF-8')
    socket.send(encoded_request)
    #  Get the reply.
    message = socket.recv()
    message_str = message.decode('UTF-8')
    received = json.loads(message_str)

    def display_all():
        """Asks user if they want to view the question and correct answer"""
        category_check = input("Would you like to see the question and correct answer? Y/N")

        if category_check.lower() == "y":
            print("")
            print(received["question"]["text"])
            print("Correct answer:", received["correctAnswer"])
            print("")
            complete()

        elif category_check.lower() == "n":
            print("")


        elif category_check.lower() != "y" and category_check.lower() != "n":
            print("Please select either Y/N")
            display_all()

    def display_questions_answers():
        """If user selects N, display questions and possible answers"""
        count = 0
        print(received["question"]["text"])
        new_list = [received["correctAnswer"]]
        for index in received["incorrectAnswers"]:
            new_list.append(index)
            random.shuffle(new_list)
        for index in new_list:
            count += 1
            answers_nums = (str(count) + "." + index)
            print(answers_nums)
        answer()

    def answer():
        """Keeps score based on given answer"""
        score_count = 0
        user_input = input("Choose an answer:")
        if user_input == received["correctAnswer"]:
            print("Correct!")
            score_keeping_plus()

        if user_input != received["correctAnswer"]:
            print("Incorrect")
            # print("Correct answer:", received["correctAnswer"])
            score_keeping_minus()


    def start_over():
        """Start over gives the user the ability to keep running the program"""
        user_input_over = input("Would you like to choose a new category and difficulty or Review? Y/N/Review")
        if user_input_over.lower() == "y":
            complete()
        if user_input_over.lower() == "review":
            display_all()

        if user_input_over.lower() == "n":
            user_input_complete = input("Would you like to exit program? Y/N")
            if user_input_complete.lower() == "y":
                global new_count
                print("")
                print("Your final score is:", new_count)
                exit()
            if user_input_complete.lower() == "n":
                start_over()

    def score_keeping_plus():
        """Keeps track of score based on difficulty level. Adds to the score."""
        global new_count

        if get_diff.lower() == "easy":
            new_count += 1

        if get_diff.lower() == "medium":
            new_count += 2

        if get_diff.lower() == "hard":
            new_count += 3

        print("Your current score is: ", new_count)

    def score_keeping_minus():
        """If answer is wrong, this function subtracts from score"""
        global new_count

        if get_diff.lower() == "easy":
            new_count -= 1

        if get_diff.lower() == "medium":
            new_count -= 2

        if get_diff.lower() == "hard":
            new_count -= 3

        print("Your current score is: ", new_count)



    display_all()
    display_questions_answers()
    start_over()
    complete()


complete()







