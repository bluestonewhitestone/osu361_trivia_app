import requests
import json
import random

response = requests.get("https://the-trivia-api.com/v2/questions")

user_welcome = "Welcome to Quizzical Trivia"
user_difficulty_easy = "Easy"
user_difficulty_medium = "Medium"
user_difficulty_hard = "Hard"

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


print(user_welcome)
print("")
print("Choose one:")
print(user_difficulty_easy, user_difficulty_medium, user_difficulty_hard)
user_difficulty = input("")


if user_difficulty.upper() == user_difficulty_easy.upper() or user_difficulty_medium.upper() or user_difficulty_hard.upper():

    print("You've selected:", user_difficulty.lower())
else:
    user_difficulty = input("Please select a difficulty provided")


def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)



def select_choice():
    count = 0

    for index in range(10):
        if (response.json()[index]["difficulty"]) == user_difficulty.lower():
            jprint(response.json()[index]["question"]["text"])

            choice_list = (response.json()[index]["incorrectAnswers"])
            choice_list.append(response.json()[index]["correctAnswer"])

            random.shuffle(choice_list)
            print(choice_list)

            answer_choice = input("Select an answer")

            answer_input(answer_choice, choice_list, response.json()[count]["correctAnswer"])

        else:
            count += 1


def answer_input(x, y, z):
    score = 0

    if x == z:
        print("CORRECT")
        score += 1
        print("Score:", score)

    else:
        score -= 1
        print("Score:", score)


select_choice()

#
# def possible_answers():
#     if response.json()[0]["correctAnswer"] ==






# jprint((response.json()[0]["question"]["text"]))
#
# y = (jprint(response.json()[0]["correctAnswer"]))
#
#
# for index in range(3):
#     jprint(response.json()[0]["incorrectAnswers"][index])
#
#
# x = input("Write the Correct Answer")
#
# if str(x) == y:
#
#     print("correct")



