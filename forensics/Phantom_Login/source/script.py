from os import getenv

questions = [
    {
        "question": "What are the attacker's IP addresses?\nFormat: IP1,IP2\tExample: 1.1.1.1,8.8.8.8\n",
        "answer": [
            "188.166.195.55,167.71.34.128",
            "167.71.34.128,188.166.195.55"
        ]
    },
    {
        "question": "What is the endpoint that the victim was directed to during the initial stage of the phishing attack?\nFormat: /example\n",
        "answer": [
            "/login.srf"
        ]
    },
    {
        "question": "what is the victim's username and password?\nFormat: Username,Password\n",
        "answer": [
            "captain_osama@outlook.com,blingblong4cricketcaptain"
        ]
    }
]

def start_quiz():
    correct_answers = 0

    for question in questions:
        print(question["question"])

        answered_correctly = False

        while not answered_correctly:
            answer = input("Your answer: ").strip()
            if answer.lower() in [a.lower() for a in question["answer"]]:
                print("Correct! ✅ Moving to the next question.")
                correct_answers += 1
                answered_correctly = True
            else:
                print("Incorrect! ❌ Try harder.")


    if correct_answers == len(questions):
        print(f"Good Job! You answered all questions correctly! 🔥 Here is your flag: {getenv('FLAG','METACTF{TESTING_FLAG}')}")

if __name__ == "__main__":
    start_quiz()
