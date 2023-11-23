import requests
import json
import random
import time
import zmq


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


def introduction():
    user_name = input("What is your name?")
    print(user_welcome + ", " + user_name)
    print("")
    time.sleep(1)
    print("uno")
    time.sleep(1)
    print("dos")
    time.sleep(1)
    print("tres")
    time.sleep(1)
    print("")
    print("")







introduction()

print('\n'.join([", ".join([category for category in categories[i:i + 3]]) for i in range(0, len(categories), 3)]))
get_category = input("Which category would you like to try?")
print("")
print("Easy, Medium, or Hard?")
get_diff = input("Select a difficulty")

def complete():

    # print('\n'.join([", ".join([category for category in categories[i:i + 3]]) for i in range(0, len(categories), 3)]))
    # get_category = input("Which category would you like to try?")
    # print("")
    # print("Easy, Medium, or Hard?")
    # get_diff = input("Select a difficulty")


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
    # print(received)
    # print(received["question"])



    def display_all():
        category_check = input("Would you like to see the question and answer? Y/N")

        if category_check.lower() == "y":
            print("")
            print(received["question"]["text"])
            print("Correct answer:", received["correctAnswer"])
            print("")
            complete()

        elif category_check.lower() == "n":
            print("")

        elif category_check.lower() != ("y" or "n"):
            print("Please select either Y/N")
            display_all()


    def display_questions_answers():
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
        score_count = 0
        user_input = input("Choose an answer:")

        if user_input == received["correctAnswer"]:
            print("correct")
            score_count += 1
        else:
            print("Incorrect")
            print(received["correctAnswer"])
            score_count -= 1




    display_all()
    display_questions_answers()
    complete()

complete()



