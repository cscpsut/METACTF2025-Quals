from os import getenv

questions = [
    {
        "question": "How did the attack trigger after the employee got phished?",
        "answer": ["macro", "macros"]
    },
    {
        "question": "If anything was left behind to keep access to the system, where could it be?",
        "answer": ["run key", "runkey"]
    },
    {
        "question": "What was the Run Key Name and Value that was implanted? Format: KeyName_\"KeyValue\"",
        "answer": [
            "FlightUpdater_\"powershell -WindowStyle Hidden -ExecutionPolicy Bypass -File 'C:\\Users\\AeroNimbusHR\\AppData\\Local\\Temp\\dropper.ps1'\""
        ]
    },
    {
        "question": "What is the full path of the original sensitive file that was exfiltrated? Format: \"C:\\Users\\user1\\Desktop\\HelloWorld.txt\"",
        "answer": [
            "C:\\Users\\AeroNimbusHR\\Documents\\crew_roster_backup.xlsx"
        ]
    },
    {
        "question": "What is the full path of the modified sensitive file that was exfiltrated? Format: \"C:\\Users\\user1\\Desktop\\HelloWorld.txt\"",
        "answer": [
            "C:\\ProgramData\\crew_data.xlsx"
        ]
    },
    {
        "question": "What is the full path of the file that activated the macros? Format: \"C:\\Users\\user1\\Desktop\\HelloWorld.txt\"",
        "answer": [
            "C:\\Users\\AeroNimbusHR\\Downloads\\Flight_Schedule_Q3.xlsm"
        ]
    },
    {
        "question": "What is the name of the executable that triggered the exfiltration?",
        "answer": [
            "onedrivecmd.exe"
        ]
    },
    {
        "question": "What is the name of the attacker and which department is he from? Example Format: \"Saleh Huneidi_Risk Advisory\"",
        "answer": [
            "Rami Abdulsalam_People Operations"
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
