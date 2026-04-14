import random

def get_media_url(filename, lesson="lesson1"):
    return f"/static/quiz_media/{lesson}/{filename}"

SIGN_TO_MEDIA = {
    "Hai / Hello": get_media_url("Hi_Hello.jpg"),
    "Assalamualaikum": get_media_url("Peace_be_Upon_You.jpg"),
    "Waalaikumussalam": get_media_url("And_unto_you_peace.jpg"),
    "Apa Khabar": get_media_url("How_are_you.jpg"),
    "Khabar Baik": get_media_url("Fine.jpg"),
    "Terima Kasih": get_media_url("Thank_You.jpg"),
    "Sama-sama": get_media_url("You_Are_Welcome.jpg"),
    "Sila": get_media_url("Please.jpg"),
    "Selamat Pagi": get_media_url("Good_Morning.jpg"),
    "Selamat Tengah Hari": get_media_url("Good_Afternoon.jpg"),
    "Selamat Petang": get_media_url("Good_Evening.jpg"),
    "Selamat Malam": get_media_url("Good_Night.jpg"),
    "Selamat": get_media_url("Well.jpg"),
    "Selamat Datang": get_media_url("Welcome.jpg"),
    "Maaf (Excuse)": get_media_url("Excuse.jpg"),
    "Maaf (Sorry)": get_media_url("Sorry.jpg"),
    "Tolong": get_media_url("Please.jpg"), 
    "Selamat Jalan": get_media_url("Good_Bye.jpg"),
    "Salam": get_media_url("Salam.jpg"),
    "Salam (Regards)": get_media_url("Regards.jpg"),
    "Tahniah": get_media_url("Congratulations.jpg"),
    "Selamat Hari Jadi": get_media_url("Happy_Birthday.jpg", "lesson1"),
    "Selamat Ulangtahun": get_media_url("Happy_Anniversary.jpg", "lesson1"),
    # Topic 2 -> lesson2 folder
    "A": get_media_url("a.jpg", "lesson2"),
    "B": get_media_url("b.jpg", "lesson2"),
    "C": get_media_url("c.jpg", "lesson2"),
    "D": get_media_url("d.jpg", "lesson2"),
    "E": get_media_url("e.jpg", "lesson2"),
    "F": get_media_url("f.jpg", "lesson2"),
    "G": get_media_url("g.jpg", "lesson2"),
    "H": get_media_url("h.jpg", "lesson2"),
    "I": get_media_url("i.jpg", "lesson2"),
    "J": get_media_url("j.jpg", "lesson2"),
    "K": get_media_url("k.jpg", "lesson2"),
    "L": get_media_url("l.jpg", "lesson2"),
    "M": get_media_url("m.jpg", "lesson2"),
    "N": get_media_url("n.jpg", "lesson2"),
    "O": get_media_url("o.jpg", "lesson2"),
    "P": get_media_url("p.jpg", "lesson2"),
    "Q": get_media_url("q.jpg", "lesson2"),
    "R": get_media_url("r.jpg", "lesson2"),
    "S": get_media_url("s.jpg", "lesson2"),
    "T": get_media_url("t.jpg", "lesson2"),
    "U": get_media_url("u.jpg", "lesson2"),
    "V": get_media_url("v.jpg", "lesson2"),
    "W": get_media_url("w.jpg", "lesson2"),
    "X": get_media_url("x.jpg", "lesson2"),
    "Y": get_media_url("y.jpg", "lesson2"),
    "Z": get_media_url("z.jpg", "lesson2"),
    "1": get_media_url("1.jpg", "lesson2"),
    "2": get_media_url("2.jpg", "lesson2"),
    "3": get_media_url("3.jpg", "lesson2"),
    "4": get_media_url("4.jpg", "lesson2"),
    "5": get_media_url("5.jpg", "lesson2"),
    "6": get_media_url("6.jpg", "lesson2"),
    "7": get_media_url("7.jpg", "lesson2"),
    "8": get_media_url("8.jpg", "lesson2"),
    "9": get_media_url("9.jpg", "lesson2"),
    "10": get_media_url("10.jpg", "lesson2"),
    "Saya": get_media_url("i_me.jpg", "lesson2"),
    "Anda / Kamu": get_media_url("you.jpg", "lesson2"),
    "Dia": get_media_url("he_she.jpg", "lesson2"),
    "Nama": get_media_url("name.jpg", "lesson2"),
    "Tinggal": get_media_url("stay.jpg", "lesson2"),
    "Apa": get_media_url("what.jpg", "lesson2"),
    "Siapa": get_media_url("who.jpg", "lesson2"),
    "Mana": get_media_url("where.jpg", "lesson2"),
    "Kawan": get_media_url("friend.jpg", "lesson2")
}

SIGN_HINTS = {
    "Hai / Hello": {
        "conceptual": "A universal greeting to say you are friendly.",
        "action": "Palm moving from the forehead outwards."
    },
    "Assalamualaikum": {
        "conceptual": "A formal Islamic greeting wishing peace upon someone.",
        "action": "Hand touches the forehead and then moves to the chest."
    },
    "Waalaikumussalam": {
        "conceptual": "The standard reply when someone wishes you peace.",
        "action": "Hand touches the chest and then moves back to the forehead."
    },
    "Apa Khabar": {
        "conceptual": "Asking someone how they are doing.",
        "action": "Hand moving from the chin down and forward."
    },
    "Khabar Baik": {
        "conceptual": "A positive response indicating you are doing well.",
        "action": "Showing a thumbs up gesture."
    },
    "Terima Kasih": {
        "conceptual": "Expressing gratitude to someone.",
        "action": "Hand moving outward from the chin/mouth."
    },
    "Sama-sama": {
        "conceptual": "The polite reply after someone thanks you.",
        "action": "Both hands form fists with thumbs up, moving together."
    },
    "Sila": {
        "conceptual": "Inviting or politely asking someone to do something.",
        "action": "Hand sweeps forward with palm open, inviting."
    },
    "Selamat Pagi": {
        "conceptual": "Greeting used early in the day when the sun rises.",
        "action": "Sign for 'Safe/Well' followed by arms rising up like a morning sun."
    },
    "Selamat Tengah Hari": {
        "conceptual": "Greeting used at noon when the sun is highest.",
        "action": "Sign for 'Safe/Well' followed by a hand pointing straight up."
    },
    "Selamat Petang": {
        "conceptual": "Greeting used in the late afternoon.",
        "action": "Sign for 'Safe/Well' followed by a hand sloping downward like a setting sun."
    },
    "Selamat Malam": {
        "conceptual": "Greeting used before going to bed.",
        "action": "Sign for 'Safe/Well' followed by hands closing together to rest."
    },
    "Selamat": {
        "conceptual": "The base word for 'Safe' or 'Good'.",
        "action": "Fists pulling back towards the body, symbolizing safety."
    },
    "Selamat Datang": {
        "conceptual": "Greeting a guest who has just arrived.",
        "action": "Hand sweeps inward as if receiving someone."
    },
    "Maaf (Excuse)": {
        "conceptual": "Polite phrase used when passing through or excusing yourself.",
        "action": "Fingers brushing against the back of the other hand."
    },
    "Maaf (Sorry)": {
        "conceptual": "Apologizing for a mistake.",
        "action": "Rubbing the chest in a circular motion."
    },
    "Tolong": {
        "conceptual": "Asking for assistance.",
        "action": "One hand lifting the other palm upwards."
    },
    "Selamat Jalan": {
        "conceptual": "Wishing a safe trip to someone departing.",
        "action": "Sign for 'Safe/Well' followed by fingers moving forward like walking."
    },
    "Salam": {
        "conceptual": "A respectful greeting, often used with elders.",
        "action": "Extending both hands gracefully."
    },
    "Salam (Regards)": {
        "conceptual": "Sending good wishes to someone.",
        "action": "Extending both hands gracefully."
    },
    "Tahniah": {
        "conceptual": "Praising someone for an achievement.",
        "action": "Hands shaking slightly in front, celebrating."
    },
    "Selamat Hari Jadi": {
        "conceptual": "Celebrating someone's birth.",
        "action": "Sign for 'Safe/Well' followed by patting the stomach area."
    },
    "Selamat Ulangtahun": {
        "conceptual": "Celebrating a yearly milestone like an anniversary.",
        "action": "Hands making a circular motion representing a full year passed."
    },
    # Topic 2 Hints
    "Saya": {"conceptual": "Referring to yourself.", "action": "Pointing to your own chest."},
    "Anda / Kamu": {"conceptual": "Referring to the person you are talking to.", "action": "Pointing forward towards the other person."},
    "Dia": {"conceptual": "Referring to a third person.", "action": "Pointing to the side."},
    "Nama": {"conceptual": "The word for one's identity.", "action": "Tapping chest or shoulder area."},
    "Tinggal": {"conceptual": "Refers to living or staying in a place.", "action": "Hands moving down as if settling into a location."},
    "Apa": {"conceptual": "Asking for information about something.", "action": "Hands up with palms open, slight shrug."},
    "Siapa": {"conceptual": "Asking about a person's identity.", "action": "Index finger circling near the lips."},
    "Mana": {"conceptual": "Asking about a location.", "action": "Hands moving side to side as if searching."},
    "A": {"conceptual": "First letter of the alphabet.", "action": "Fist with thumb resting against the side of the index finger."},
    "B": {"conceptual": "Second letter of the alphabet.", "action": "Flat hand with thumb tucked into the palm."},
    "C": {"conceptual": "Hand curved like the letter 'C'.", "action": "Hand in a curved shape."},
    "1": {"conceptual": "Number one.", "action": "Index finger pointed up."},
    "7": {"conceptual": "Number seven.", "action": "Thumb and ring finger touching."}
}

# Data structure mapping Topic 1 -> Lessons 1 to 8
TOPIC_1_DATA = {
    1: [
        {
            "type": "Visual",
            "text": "What does this sign mean?",
            "target": "Hai / Hello",
            "media_url": get_media_url("Hi_Hello.jpg")
        },
        {
            "type": "Visual",
            "text": "What does this sign mean?",
            "target": "Assalamualaikum",
            "media_url": get_media_url("Peace_be_Upon_You.jpg")
        },
        {
            "type": "Context",
            "text": "Someone says 'Assalamualaikum' to you. What do you sign?",
            "target": "Waalaikumussalam",
            "media_url": None
        },
        {
            "type": "Visual",
            "text": "What does this sign mean?",
            "target": "Apa Khabar",
            "media_url": get_media_url("How_are_you.jpg")
        },
        {
            "type": "Scenario",
            "text": "You meet a new friend and want to ask 'How are you?'. You sign:",
            "target": "Apa Khabar",
            "media_url": None
        },
        {
            "type": "Visual",
            "text": "What does this sign mean?",
            "target": "Khabar Baik",
            "media_url": get_media_url("Fine.jpg")
        },
        {
            "type": "Logic",
            "text": "Which of these is a response to 'Apa Khabar'?",
            "target": "Khabar Baik",
            "media_url": None
        },
        {
            "type": "Visual",
            "text": "What does this sign mean?",
            "target": "Waalaikumussalam",
            "media_url": get_media_url("And_unto_you_peace.jpg")
        }
    ],
    2: [
        {
            "type": "Visual",
            "text": "What does this sign mean?",
            "target": "Terima Kasih",
            "media_url": get_media_url("Thank_You.jpg")
        },
        {
            "type": "Visual",
            "text": "What does this sign mean?",
            "target": "Sama-sama",
            "media_url": get_media_url("You_Are_Welcome.jpg")
        },
        {
            "type": "Scenario",
            "text": "Someone holds the door for you. You sign:",
            "target": "Terima Kasih",
            "media_url": None
        },
        {
            "type": "Logic",
            "text": "What is the polite response after someone says 'Terima Kasih'?",
            "target": "Sama-sama",
            "media_url": None
        },
        {
            "type": "Visual",
            "text": "What does this sign mean?",
            "target": "Sila",
            "media_url": get_media_url("Please.jpg")
        },
        {
            "type": "Scenario",
            "text": "You want to invite someone to sit down. You sign:",
            "target": "Sila",
            "media_url": None
        },
        {
            "type": "Visual",
            "text": "What does this sign mean?",
            "target": "Khabar Baik",
            "media_url": get_media_url("Fine.jpg")
        },
        {
            "type": "Identification",
            "text": "Which sign means 'You are welcome'?",
            "target": "Sama-sama",
            "media_url": None
        }
    ],
    3: [
        {
            "type": "Visual",
            "text": "What does this sign mean?",
            "target": "Selamat Pagi",
            "media_url": get_media_url("Good_Morning.jpg")
        },
        {
            "type": "Visual",
            "text": "What does this sign mean?",
            "target": "Selamat Tengah Hari",
            "media_url": get_media_url("Good_Afternoon.jpg")
        },
        {
            "type": "Scenario",
            "text": "You see your teacher at 8:30 AM. You sign:",
            "target": "Selamat Pagi",
            "media_url": None
        },
        {
            "type": "Scenario",
            "text": "You are meeting a colleague for lunch at 1:00 PM. You sign:",
            "target": "Selamat Tengah Hari",
            "media_url": None
        },
        {
            "type": "Visual",
            "text": "What does this sign mean?",
            "target": "Selamat",
            "media_url": get_media_url("Well.jpg")
        },
        {
            "type": "Logic",
            "text": "Which sign is used at 9:00 PM?",
            "target": "Selamat Malam",
            "media_url": None
        },
        {
            "type": "Identification",
            "text": "Which sign represents 12:00 PM?",
            "target": "Selamat Tengah Hari",
            "media_url": None
        },
        {
            "type": "Visual",
            "text": "What does this sign mean?",
            "target": "Selamat",
            "media_url": get_media_url("Well.jpg")
        }
    ],
    4: [
        {
            "type": "Visual",
            "text": "What does this sign mean?",
            "target": "Selamat Petang",
            "media_url": get_media_url("Good_Evening.jpg")
        },
        {
            "type": "Visual",
            "text": "What does this sign mean?",
            "target": "Selamat Malam",
            "media_url": get_media_url("Good_Night.jpg")
        },
        {
            "type": "Scenario",
            "text": "You are entering a café at 3:00 PM. You sign:",
            "target": "Selamat Petang",
            "media_url": None
        },
        {
            "type": "Scenario",
            "text": "You are saying goodbye before going to bed. You sign:",
            "target": "Selamat Malam",
            "media_url": None
        },
        {
            "type": "Visual",
            "text": "What does this sign mean?",
            "target": "Selamat Datang",
            "media_url": get_media_url("Welcome.jpg")
        },
        {
            "type": "Scenario",
            "text": "A guest enters your house. You sign:",
            "target": "Selamat Datang",
            "media_url": None
        },
        {
            "type": "Logic",
            "text": "Which sign is for late afternoon/evening?",
            "target": "Selamat Petang",
            "media_url": None
        },
        {
            "type": "Identification",
            "text": "Match the sign for 'Goodnight'.",
            "target": "Selamat Malam",
            "media_url": None
        }
    ],
    5: [
        {
            "type": "Visual",
            "text": "What does this sign mean?",
            "target": "Maaf (Excuse)",
            "media_url": get_media_url("Excuse.jpg")
        },
        {
            "type": "Visual",
            "text": "What does this sign mean?",
            "target": "Maaf (Sorry)",
            "media_url": get_media_url("Sorry.jpg")
        },
        {
            "type": "Scenario",
            "text": "You want to pass through a crowd. You sign:",
            "target": "Maaf (Excuse)",
            "media_url": None
        },
        {
            "type": "Scenario",
            "text": "You accidentally stepped on someone's foot. You sign:",
            "target": "Maaf (Sorry)",
            "media_url": None
        },
        {
            "type": "Visual",
            "text": "What does this sign mean?",
            "target": "Tolong",
            "media_url": get_media_url("Please.jpg")
        },
        {
            "type": "Scenario",
            "text": "You need help carrying a heavy box. You sign:",
            "target": "Tolong",
            "media_url": None
        },
        {
            "type": "Visual",
            "text": "What does this sign mean?",
            "target": "Sila",
            "media_url": get_media_url("Please_Welcome.jpg")
        },
        {
            "type": "Logic",
            "text": "Which sign is used to ask for help?",
            "target": "Tolong",
            "media_url": None
        }
    ],
    6: [
        {
            "type": "Visual",
            "text": "What does this sign mean?",
            "target": "Selamat Jalan",
            "media_url": get_media_url("Good_Bye.jpg")
        },
        {
            "type": "Visual",
            "text": "What does this sign mean?",
            "target": "Salam (Regards)",
            "media_url": get_media_url("Regards.jpg")
        },
        {
            "type": "Visual",
            "text": "What does this sign mean?",
            "target": "Salam",
            "media_url": get_media_url("Salam.jpg")
        },
        {
            "type": "Scenario",
            "text": "Your friend is leaving for a trip. You sign:",
            "target": "Selamat Jalan",
            "media_url": None
        },
        {
            "type": "Scenario",
            "text": "You want to say 'Greetings/Regards' to someone. You sign:",
            "target": "Salam (Regards)",
            "media_url": None
        },
        {
            "type": "Logic",
            "text": "Which sign is used specifically when someone is going away?",
            "target": "Selamat Jalan",
            "media_url": None
        },
        {
            "type": "Visual",
            "text": "What does this sign mean?",
            "target": "Selamat Datang",
            "media_url": get_media_url("Welcome.jpg")
        },
        {
            "type": "Scenario",
            "text": "You meet an elder and use a respectful greeting.",
            "target": "Salam",
            "media_url": None
        }
    ],
    7: [
        {
            "type": "Visual",
            "text": "What does this sign mean?",
            "target": "Tahniah",
            "media_url": get_media_url("Congratulations.jpg")
        },
        {
            "type": "Visual",
            "text": "What does this sign mean?",
            "target": "Selamat Hari Jadi",
            "media_url": get_media_url("Happy_Birthday.jpg")
        },
        {
            "type": "Visual",
            "text": "What does this sign mean?",
            "target": "Selamat Ulangtahun",
            "media_url": get_media_url("Happy_Anniversary.jpg")
        },
        {
            "type": "Scenario",
            "text": "Your brother just won a race. You sign:",
            "target": "Tahniah",
            "media_url": None
        },
        {
            "type": "Scenario",
            "text": "Today is your mother's 40th birthday. You sign:",
            "target": "Selamat Hari Jadi",
            "media_url": None
        },
        {
            "type": "Scenario",
            "text": "It is your parents' wedding anniversary. You sign:",
            "target": "Selamat Ulangtahun",
            "media_url": None
        },
        {
            "type": "Logic",
            "text": "Which sign translates to 'Congratulations'?",
            "target": "Tahniah",
            "media_url": None
        },
        {
            "type": "Identification",
            "text": "Which sign is used for 'Happy Anniversary'?",
            "target": "Selamat Ulangtahun",
            "media_url": None
        }
    ]
}

# Topic 2 Data
TOPIC_2_DATA = {
    1: [ # Alphabet A-G
        {"type": "Visual", "text": "Identify this letter:", "target": "A", "media_url": SIGN_TO_MEDIA["A"]},
        {"type": "Visual", "text": "Identify this letter:", "target": "B", "media_url": SIGN_TO_MEDIA["B"]},
        {"type": "Visual", "text": "Identify this letter:", "target": "C", "media_url": SIGN_TO_MEDIA["C"]},
        {"type": "Identification", "text": "Which sign is 'D'?", "target": "D", "media_url": None},
        {"type": "Visual", "text": "Identify this letter:", "target": "E", "media_url": SIGN_TO_MEDIA["E"]},
        {"type": "Identification", "text": "Which sign is 'F'?", "target": "F", "media_url": None},
        {"type": "Visual", "text": "Identify this letter:", "target": "G", "media_url": SIGN_TO_MEDIA["G"]},
        {"type": "Identification", "text": "Which sign is 'A'?", "target": "A", "media_url": None}
    ],
    2: [ # Alphabet H-N
        {"type": "Visual", "text": "Identify this letter:", "target": "H", "media_url": SIGN_TO_MEDIA["H"]},
        {"type": "Visual", "text": "Identify this letter:", "target": "I", "media_url": SIGN_TO_MEDIA["I"]},
        {"type": "Visual", "text": "Identify this letter:", "target": "J", "media_url": SIGN_TO_MEDIA["J"]},
        {"type": "Identification", "text": "Which sign is 'K'?", "target": "K", "media_url": None},
        {"type": "Visual", "text": "Identify this letter:", "target": "L", "media_url": SIGN_TO_MEDIA["L"]},
        {"type": "Identification", "text": "Which sign is 'M'?", "target": "M", "media_url": None},
        {"type": "Visual", "text": "Identify this letter:", "target": "N", "media_url": SIGN_TO_MEDIA["N"]},
        {"type": "Identification", "text": "Which sign is 'H'?", "target": "H", "media_url": None}
    ],
    3: [ # Alphabet O-U
        {"type": "Visual", "text": "Identify this letter:", "target": "O", "media_url": SIGN_TO_MEDIA["O"]},
        {"type": "Visual", "text": "Identify this letter:", "target": "P", "media_url": SIGN_TO_MEDIA["P"]},
        {"type": "Visual", "text": "Identify this letter:", "target": "Q", "media_url": SIGN_TO_MEDIA["Q"]},
        {"type": "Identification", "text": "Which sign is 'R'?", "target": "R", "media_url": None},
        {"type": "Visual", "text": "Identify this letter:", "target": "S", "media_url": SIGN_TO_MEDIA["S"]},
        {"type": "Identification", "text": "Which sign is 'T'?", "target": "T", "media_url": None},
        {"type": "Visual", "text": "Identify this letter:", "target": "U", "media_url": SIGN_TO_MEDIA["U"]},
        {"type": "Identification", "text": "Which sign is 'S'?", "target": "S", "media_url": None}
    ],
    4: [ # Alphabet V-Z
        {"type": "Visual", "text": "Identify this letter:", "target": "V", "media_url": SIGN_TO_MEDIA["V"]},
        {"type": "Visual", "text": "Identify this letter:", "target": "W", "media_url": SIGN_TO_MEDIA["W"]},
        {"type": "Visual", "text": "Identify this letter:", "target": "X", "media_url": SIGN_TO_MEDIA["X"]},
        {"type": "Identification", "text": "Which sign is 'Y'?", "target": "Y", "media_url": None},
        {"type": "Visual", "text": "Identify this letter:", "target": "Z", "media_url": SIGN_TO_MEDIA["Z"]},
        {"type": "Identification", "text": "Which sign is 'V'?", "target": "V", "media_url": None},
        {"type": "Visual", "text": "Identify this letter:", "target": "A", "media_url": SIGN_TO_MEDIA["A"]},
        {"type": "Identification", "text": "Which sign is 'Z'?", "target": "Z", "media_url": None}
    ],
    5: [ # Pronouns
        {"type": "Visual", "text": "What does this pronoun mean?", "target": "Saya", "media_url": SIGN_TO_MEDIA["Saya"]},
        {"type": "Visual", "text": "What does this pronoun mean?", "target": "Anda / Kamu", "media_url": SIGN_TO_MEDIA["Anda / Kamu"]},
        {"type": "Visual", "text": "What does this pronoun mean?", "target": "Dia", "media_url": SIGN_TO_MEDIA["Dia"]},
        {"type": "Scenario", "text": "You want to say 'I am a student'. Which sign do you start with?", "target": "Saya", "media_url": None},
        {"type": "Scenario", "text": "You are pointing to your friend sitting next to you. You sign:", "target": "Dia", "media_url": None},
        {"type": "Scenario", "text": "You are talking directly to someone. You sign:", "target": "Anda / Kamu", "media_url": None},
        {"type": "Identification", "text": "Match the sign for 'He/She'.", "target": "Dia", "media_url": None},
        {"type": "Logic", "text": "Which sign represents the first person pronoun?", "target": "Saya", "media_url": None}
    ],
    6: [ # Numbers
        {"type": "Visual", "text": "Identify this number:", "target": "1", "media_url": SIGN_TO_MEDIA["1"]},
        {"type": "Visual", "text": "Identify this number:", "target": "2", "media_url": SIGN_TO_MEDIA["2"]},
        {"type": "Visual", "text": "Identify this number:", "target": "3", "media_url": SIGN_TO_MEDIA["3"]},
        {"type": "Identification", "text": "Which sign represents 8?", "target": "8", "media_url": None},
        {"type": "Visual", "text": "Identify this number:", "target": "5", "media_url": SIGN_TO_MEDIA["5"]},
        {"type": "Identification", "text": "Which sign represents 9?", "target": "9", "media_url": None},
        {"type": "Visual", "text": "Identify this number:", "target": "10", "media_url": SIGN_TO_MEDIA["10"]},
        {"type": "Logic", "text": "What number comes after 6?", "target": "7", "media_url": None}
    ],
    7: [ # Questions
        {"type": "Visual", "text": "What does this question word mean?", "target": "Apa", "media_url": SIGN_TO_MEDIA["Apa"]},
        {"type": "Visual", "text": "What does this question word mean?", "target": "Siapa", "media_url": SIGN_TO_MEDIA["Siapa"]},
        {"type": "Visual", "text": "What does this question word mean?", "target": "Mana", "media_url": SIGN_TO_MEDIA["Mana"]},
        {"type": "Scenario", "text": "You want to ask 'What is your name?'. You sign 'Nama', 'Anda', then:", "target": "Apa", "media_url": None},
        {"type": "Scenario", "text": "You want to ask 'Who is that?'. You sign:", "target": "Siapa", "media_url": None},
        {"type": "Scenario", "text": "You want to ask 'Where do you live?'. You sign 'Anda', 'Tinggal', then:", "target": "Mana", "media_url": None},
        {"type": "Identification", "text": "Match the sign 'Siapa' with its meaning.", "target": "Siapa", "media_url": None},
        {"type": "Logic", "text": "To ask about a location, which sign is used?", "target": "Mana", "media_url": None}
    ],
    8: [ # Full Intro
        {"type": "Visual", "text": "What does this sign mean?", "target": "Nama", "media_url": SIGN_TO_MEDIA["Nama"]},
        {"type": "Visual", "text": "What does this sign mean?", "target": "Tinggal", "media_url": SIGN_TO_MEDIA["Tinggal"]},
        {"type": "Scenario", "text": "What is the first sign you use when introducing yourself?", "target": "Saya", "media_url": None},
        {"type": "Scenario", "text": "To state where you reside, you sign:", "target": "Tinggal", "media_url": None},
        {"type": "Logic", "text": "Which sign is used before your name during an intro?", "target": "Nama", "media_url": None}
    ]
}

# Isolated pools to prevent bleed
TOPIC_1_POOL = [
    "Hai / Hello", "Assalamualaikum", "Waalaikumussalam", "Apa Khabar", "Khabar Baik",
    "Terima Kasih", "Sama-sama", "Sila", "Selamat Pagi", "Selamat Tengah Hari",
    "Selamat Petang", "Selamat Malam", "Selamat", "Selamat Datang",
    "Maaf (Excuse)", "Maaf (Sorry)", "Tolong", "Selamat Jalan", "Salam",
    "Salam (Regards)", "Tahniah", "Selamat Hari Jadi", "Selamat Ulangtahun"
]

TOPIC_2_POOL = [
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
    "Saya", "Anda / Kamu", "Dia", "Nama", "Tinggal", "Apa", "Siapa", "Mana"
]

def generate_topic_quiz(topic_id, lesson_id):
    if topic_id == 1:
        pool = TOPIC_1_POOL
        if lesson_id == 8:
            all_questions = []
            for l_id in range(1, 8):
                all_questions.extend(TOPIC_1_DATA[l_id])
            
            selected_q = random.sample(all_questions, min(30, len(all_questions)))
            final_qs = []
            for idx, q in enumerate(selected_q):
                distractors = random.sample([o for o in pool if o != q["target"]], 3)
                options_text = distractors + [q["target"]]
                random.shuffle(options_text)
                
                options_objs = []
                for opt in options_text:
                    options_objs.append({
                        "text": opt,
                        "media_url": SIGN_TO_MEDIA.get(opt, None)
                    })
                
                final_qs.append({
                    "id": idx + 1,
                    "text": q["text"],
                    "type": q["type"],
                    "media_url": q["media_url"],
                    "media_type": "image" if q["media_url"] else None,
                    "options": options_objs,
                    "hide_option_text": True if not q["media_url"] else False,
                    "correct_option": q["target"],
                    "hint": SIGN_HINTS.get(q["target"], {}).get("conceptual", "Think about what this sign represents.")
                })
            return final_qs
        
        if lesson_id in TOPIC_1_DATA:
            questions = TOPIC_1_DATA[lesson_id]
            final_qs = []
            for idx, q in enumerate(questions):
                distractors = random.sample([o for o in pool if o != q["target"]], 3)
                options_text = distractors + [q["target"]]
                random.shuffle(options_text)
                
                options_objs = []
                for opt in options_text:
                    options_objs.append({
                        "text": opt,
                        "media_url": SIGN_TO_MEDIA.get(opt, None)
                    })
                
                final_qs.append({
                    "id": idx + 1,
                    "text": q["text"],
                    "type": q["type"],
                    "media_url": q["media_url"],
                    "media_type": "image" if q["media_url"] else None,
                    "options": options_objs,
                    "correct_option": q["target"],
                    "hint": SIGN_HINTS.get(q["target"], {}).get("conceptual", "Topic 1 lesson content.")
                })
            return final_qs
    
    # Topic 2 Logic
    if topic_id == 2:
        pool = TOPIC_2_POOL
        if lesson_id == 9: # Mastery Quiz
            all_questions = []
            for l_id in range(1, 9):
                all_questions.extend(TOPIC_2_DATA[l_id])
            
            selected_q = random.sample(all_questions, min(25, len(all_questions)))
            
            # Word Building questions for keys 26-30 (Sequencing Mode)
            word_building = [
                {
                    "type": "Sequence", 
                    "text": "Build the phrase in correct order: 'My name is...'", 
                    "correct_sequence": ["Nama", "Saya"], 
                    "options": ["Nama", "Saya", "Dia", "Anda / Kamu"]
                },
                {
                    "type": "Sequence", 
                    "text": "Build the phrase in correct order: 'I live in...'", 
                    "correct_sequence": ["Saya", "Tinggal"], 
                    "options": ["Saya", "Tinggal", "Mana", "Apa"]
                },
                {
                    "type": "Sequence", 
                    "text": "How do you ask 'What is your name?' in order?", 
                    "correct_sequence": ["Apa", "Nama", "Anda / Kamu"], 
                    "options": ["Apa", "Nama", "Anda / Kamu", "Siapa"]
                },
                {
                    "type": "Sequence", 
                    "text": "Build the phrase: 'Who is he/she?'", 
                    "correct_sequence": ["Siapa", "Dia"], 
                    "options": ["Siapa", "Dia", "Anda / Kamu", "Saya"]
                },
                {
                    "type": "Sequence", 
                    "text": "Correct intro: 'Greetings, my name is...'", 
                    "correct_sequence": ["Salam", "Nama", "Saya"], 
                    "options": ["Salam", "Nama", "Saya", "Hai / Hello"]
                }
            ]
            
            final_qs = []
            # First 25 random
            for idx, q in enumerate(selected_q):
                distractors = random.sample([o for o in pool if o != q["target"]], 3)
                options_text = distractors + [q["target"]]
                random.shuffle(options_text)
                
                options_objs = []
                for opt in options_text:
                    options_objs.append({
                        "text": opt,
                        "media_url": SIGN_TO_MEDIA.get(opt, None)
                    })
                
                final_qs.append({
                    "id": idx + 1,
                    "text": q["text"],
                    "type": q["type"],
                    "media_url": q["media_url"],
                    "media_type": "image" if q["media_url"] else None,
                    "options": options_objs,
                    "hide_option_text": True if not q["media_url"] else False,
                    "correct_option": q["target"],
                    "hint": SIGN_HINTS.get(q["target"], {}).get("conceptual", "Mastery level question.")
                })
                
            # Questions 26-30
            for idx, q in enumerate(word_building):
                options_text = list(q["options"])
                random.shuffle(options_text)
                
                options_objs = []
                for opt in options_text:
                    options_objs.append({
                        "text": opt,
                        "media_url": SIGN_TO_MEDIA.get(opt, None)
                    })
                
                final_qs.append({
                    "id": idx + 26,
                    "text": q["text"],
                    "type": q["type"],
                    "media_url": None,
                    "media_type": None,
                    "options": options_objs,
                    "hide_option_text": True, # User wants images only
                    "correct_sequence": q["correct_sequence"],
                    "correct_option": ",".join(q["correct_sequence"]), # Fallback for compatibility
                    "hint": "Click the images in the correct grammatical order."
                })
            return final_qs
            
        if lesson_id in TOPIC_2_DATA:
            questions = TOPIC_2_DATA[lesson_id]
            final_qs = []
            for idx, q in enumerate(questions):
                distractors = random.sample([o for o in pool if o != q["target"]], 3)
                options_text = distractors + [q["target"]]
                random.shuffle(options_text)
                
                options_objs = []
                for opt in options_text:
                    options_objs.append({
                        "text": opt,
                        "media_url": SIGN_TO_MEDIA.get(opt, None)
                    })
                
                final_qs.append({
                    "id": idx + 1,
                    "text": q["text"],
                    "type": q["type"],
                    "media_url": q["media_url"],
                    "media_type": "image" if q["media_url"] else None,
                    "options": options_objs,
                    "correct_option": q["target"],
                    "hint": SIGN_HINTS.get(q["target"], {}).get("conceptual", "Topic 2 lesson content.")
                })
            return final_qs

    return []

def generate_generic_quiz():
    return []
