import requests
import zmq
import json


def generate_question_pool(question_pool, difficulties, categories):
    """
    Generates a pool of trivia questions by quering the trivia api.
    Iterates over predefined lists of difficulties and categories to fetch questions

    :param question_pool: A dictionary to store the fetched trivia questions.
    :param difficulty: String representing the difficulty level of the question
    :param category: String representing the category of the question
    :return: None. Updates 'question_pool' dictionary in place
    """

    for difficulty in difficulties:
        for category in categories:
            response = requests.get(
                f"https://the-trivia-api.com/v2/questions?limit=5&difficulties={difficulty}&categories={category}"
            )
            question_pool[f"{difficulty}{category}"] = response.json()


def refresh_questions(question_pool, difficulty, category):
    """
    Refreshes the question pool for a specific difficulty and category

    :param question_pool: A dictionary to store the fetched trivia questions.
    :param difficulty: String representing the difficulty level of the question
    :param category: String representing the category of the question
    :return: None. Updates "question_pool" dictionary in place
    """

    response = requests.get(
        f"https://the-trivia-api.com/v2/questions?limit=5&difficulties={difficulty}&categories={category}"
    )
    question_pool[f"{difficulty}{category}"] = response.json()


# Main logic
def main():
    """
    TODO: Add random categories and random difficulties
    """
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    difficulties = ["easy", "medium", "hard"]
    categories = ["music", "sport_and_leisure", "film_and_tv", "arts_and_literature", "history", "society_and_culture",
                  "science", "geography", "food_and_drink", "general_knowledge"]
    question_pool = {}

    generate_question_pool(question_pool, difficulties, categories)

    print("Ready")

    while True:
        #  Wait for next request from client
        message = socket.recv()
        message_str = message.decode('UTF-8')
        request = json.loads(message_str)
        print(f"Received request: {request}")

        if request["request"] != "getQuestion":
            continue

        received_difficulty = request["difficulty"]
        received_category = request["category"]

        questions = question_pool[f"{received_difficulty}{received_category}"]
        if len(questions) == 1:
            refresh_questions(question_pool, received_difficulty, received_category)

        # Convert question array into bytes and send
        question = json.dumps(questions.pop()).encode('UTF-8')  # Maintains double quotes
        socket.send(question)


if __name__ == "__main__":
    main()

