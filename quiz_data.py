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
    "Sila": get_media_url("Please_Welcome.jpg"),
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
    "Kawan": get_media_url("friend.jpg", "lesson2"),
    # Topic 3 -> lesson3 folder
    "Keluarga": get_media_url("family.jpg", "lesson3"),
    "Ayah": get_media_url("father.jpg", "lesson3"),
    "Ibu": get_media_url("mother.jpg", "lesson3"),
    "Orang": get_media_url("person.jpg", "lesson3"),
    "Abang": get_media_url("elder_brother.jpg", "lesson3"),
    "Kakak": get_media_url("elder_sister.jpg", "lesson3"),
    "Adik Lelaki": get_media_url("younger_brother.jpg", "lesson3"),
    "Adik Perempuan": get_media_url("younger_sister.jpg", "lesson3"),
    "Datuk": get_media_url("grandfather.jpg", "lesson3"),
    "Nenek": get_media_url("grandmother.jpg", "lesson3"),
    "Cucu": get_media_url("grandchild.jpg", "lesson3"),
    "Bayi": get_media_url("baby.jpg", "lesson3"),
    "Anak Sulung": get_media_url("first_born.jpg", "lesson3"),
    "Anak Bongsu": get_media_url("last_child.jpg", "lesson3"),
    "Kanak-kanak": get_media_url("children.jpg", "lesson3"),
        "Dewasa": get_media_url("adult.jpg", "lesson3"),
    "Pakcik": get_media_url("uncle.jpg", "lesson3"),
    "Makcik": get_media_url("auntie.jpg", "lesson3"),
    "Sepupu": get_media_url("cousin.jpg", "lesson3"),
    "Saudara": get_media_url("relative.jpg", "lesson3"),
    "Lelaki": get_media_url("male.jpg", "lesson3"),
    "Perempuan": get_media_url("female.jpg", "lesson3"),
    "Suami": get_media_url("husband.jpg", "lesson3"),
    "Isteri": get_media_url("wife.jpg", "lesson3"),
    "Kawan Rapat": get_media_url("close_friend.jpg", "lesson3"),
    # Topic 4 -> lesson4 folder
    "11": get_media_url("eleven.jpg", "lesson4"),
    "12": get_media_url("twelve.jpg", "lesson4"),
    "13": get_media_url("thirteen.jpg", "lesson4"),
    "14": get_media_url("fourteen.jpg", "lesson4"),
    "15": get_media_url("fifteen.jpg", "lesson4"),
    "16": get_media_url("sixteen.jpg", "lesson4"),
    "17": get_media_url("seventeen.jpg", "lesson4"),
    "18": get_media_url("eighteen.jpg", "lesson4"),
    "19": get_media_url("nineteen.jpg", "lesson4"),
    "20": get_media_url("twenty.jpg", "lesson4"),
    "Isnin": get_media_url("monday.jpg", "lesson4"),
    "Selasa": get_media_url("tuesday.jpg", "lesson4"),
    "Rabu": get_media_url("wednesday.jpg", "lesson4"),
    "Khamis": get_media_url("thursday.jpg", "lesson4"),
    "Jumaat": get_media_url("friday.jpg", "lesson4"),
    "Sabtu": get_media_url("saturday.jpg", "lesson4"),
    "Ahad": get_media_url("sunday.jpg", "lesson4"),
    "Minggu": get_media_url("week.jpg", "lesson4"),
    "Semalam": get_media_url("yesterday.jpg", "lesson4"),
    "Hari Ini": get_media_url("today.jpg", "lesson4"),
    "Esok": get_media_url("tomorrow.jpg", "lesson4"),
    "Jam/Pukul": get_media_url("hour.jpg", "lesson4"),
    "Minit": get_media_url("minute.jpg", "lesson4"),
    "Saat": get_media_url("second.jpg", "lesson4"),
    "Masa": get_media_url("time.jpg", "lesson4"),
    "Selalu": get_media_url("always.jpg", "lesson4"),
    "Kadang-kadang": get_media_url("sometimes.jpg", "lesson4"),
    "Pernah": get_media_url("ever.jpg", "lesson4"),
    "Belum": get_media_url("not_yet.jpg", "lesson4"),
    "Pagi": get_media_url("morning.jpg", "lesson4"),
    "Tengah Hari": get_media_url("noon.jpg", "lesson4"),
    "Petang": get_media_url("afternoon.jpg", "lesson4"),
    "Malam": get_media_url("night.jpg", "lesson4"),
    "Sekarang": get_media_url("now.jpg", "lesson4")
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
    "Selamat Jalan": {"conceptual": "A hand waving 'Goodbye.'", "action": ""},
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
    "Saya": {"conceptual": "Pointing the index finger directly to one's own chest.", "action": ""},
    "Anda / Kamu": {"conceptual": "Pointing the index finger directly toward the listener.", "action": ""},
    "Dia": {"conceptual": "Pointing the index finger to the side (at an imaginary third person).", "action": ""},
    "Nama": {"conceptual": "The word for one's identity.", "action": "Tapping chest or shoulder area."},
    "Tinggal": {"conceptual": "Refers to living or staying in a place.", "action": "Hands moving down as if settling into a location."},
    "Apa": {"conceptual": "Index finger shaking side-to-side (the 'What' look).", "action": ""},
    "Siapa": {"conceptual": "Index finger circling in front of the face (the 'Who' expression).", "action": ""},
    "Mana": {"conceptual": "Palms facing up, moving slightly side-to-side (the 'Where' look).", "action": ""},
    "A": {"conceptual": "First letter of the alphabet.", "action": "Fist with thumb resting against the side of the index finger."},
    "B": {"conceptual": "Second letter of the alphabet.", "action": "Flat hand with thumb tucked into the palm."},
    "C": {"conceptual": "Hand curved like the letter 'C'.", "action": "Hand in a curved shape."},
    "1": {"conceptual": "Number one.", "action": "Index finger pointed up."},
    "7": {"conceptual": "Number seven.", "action": "Thumb and ring finger touching."},
    # Topic 3 Hints
    "Keluarga": {"conceptual": "Both hands form a 'C' shape and move in a circular motion to meet.", "action": "Form 'C' shapes with both hands and draw a horizontal circle in front of the chest until the fingertips touch."},
    "Ayah": {"conceptual": "The thumb of an open hand taps the forehead (representing the 'cap' or male head).", "action": "Extend the thumb of an open hand and tap it twice against the center of the forehead."},
    "Ibu": {"conceptual": "The thumb of an open hand taps the chin/jawline (representing the 'veil' or female face).", "action": "Extend the thumb of an open hand and tap it twice against the side of the chin or jawline."},
    "Orang": {"conceptual": "The index finger points downward or moves in a slight vertical line.", "action": "Point the index finger downward and move it in a short, straight vertical motion."},
    "Abang": {"conceptual": "Hand at the forehead (Male) + an upward motion (Older).", "action": "Tap the forehead with the thumb, then move the hand upward to indicate seniority."},
    "Kakak": {"conceptual": "Hand at the chin (Female) + an upward motion (Older).", "action": "Tap the chin with the thumb, then move the hand upward to indicate seniority."},
    "Adik Lelaki": {"conceptual": "Hand at the forehead (Male) + a downward motion (Younger).", "action": "Tap the forehead with the thumb, then move the hand downward to indicate a younger sibling."},
    "Adik Perempuan": {"conceptual": "Hand at the chin (Female) + a downward motion (Younger).", "action": "Tap the chin with the thumb, then move the hand downward to indicate a younger sibling."},
    "Datuk": {"conceptual": "Similar to 'Ayah' but with a 'bent' finger or a double tap to show age.", "action": "Form a 'hooked' index finger near the forehead and tap twice to indicate an elder male."},
    "Nenek": {"conceptual": "Similar to 'Ibu' but with a 'bent' finger or a double tap to show age.", "action": "Form a 'hooked' index finger near the chin and tap twice to indicate an elder female."},
    "Cucu": {"conceptual": "Fingers spelling 'C-C' or a hand motion indicating a small person height.", "action": "Fingerspell the letter 'C' twice or move a flat hand downward to a child's height."},
    "Bayi": {"conceptual": "Arms crossed in front of the chest as if cradling/rocking a baby.", "action": "Fold arms across the chest and rock them side-to-side as if holding an infant."},
    "Anak Sulung": {"conceptual": "Pointing to the thumb or the 'top' of a list (The first).", "action": "Hold up one hand and use the other index finger to point specifically at the thumb."},
    "Anak Bongsu": {"conceptual": "Pointing to the pinky finger (The last/smallest).", "action": "Hold up one hand and use the other index finger to point specifically at the pinky finger."},
    "Kanak-kanak": {"conceptual": "Patting motions at a low height (as if patting children's heads).", "action": "Move the flat hand in several downward 'patting' motions at waist height."},
    "Dewasa": {"conceptual": "Hand moving from a low height to a high height (Growing up).", "action": "Start with a flat hand at waist height and move it steadily upward above the shoulder."},
    "Pakcik": {"conceptual": "The 'P' handshape placed near the forehead/temple.", "action": "Form the letter 'P' and tap the thumb-side against the side of the forehead."},
    "Makcik": {"conceptual": "The 'M' handshape placed near the jaw/chin.", "action": "Form the letter 'M' and tap the fingertips against the side of the jaw."},
    "Sepupu": {"conceptual": "The 'S' handshape moving in a slight circle or side-to-side.", "action": "Form the letter 'S' and move the fist in a small circular or shaking motion."},
    "Saudara": {"conceptual": "Two index fingers meeting or a 'hooking' motion showing a link.", "action": "Bring both index fingers together so they touch or hook around each other."},
    "Lelaki": {"conceptual": "Hand near the forehead/cap area.", "action": "Touch the thumb to the forehead with fingers spread or closed to indicate a male."},
    "Perempuan": {"conceptual": "Hand tracing the jawline.", "action": "Brush the back of the thumb or index finger along the jawline from ear to chin."},
    "Suami": {"conceptual": "Sign for 'Lelaki' (Male) followed by the 'Marriage/Ring' sign.", "action": "Perform the male forehead sign, then touch the ring finger of the left hand."},
    "Isteri": {"conceptual": "Sign for 'Perempuan' (Female) followed by the 'Marriage/Ring' sign.", "action": "Perform the female chin sign, then touch the ring finger of the left hand."},
    "Kawan Rapat": {"conceptual": "Two index fingers pressed tightly together (showing 'closeness').", "action": "Hold both index fingers vertically and press them tightly against each other side-by-side."},
    "Kawan": {"conceptual": "Two hands clasping or shaking each other once.", "action": "Clasp your own hands together or mimic a single firm handshake motion."},

    # Topic 4 Hints
    "11": {"conceptual": "Number 11.", "action": "Index finger flicks upward from behind the thumb twice."},
    "12": {"conceptual": "Flicking motion of the thumb and fingers.", "action": "Index and middle fingers flick upward together from behind the thumb."},
    "15": {"conceptual": "Number 15.", "action": "All four fingers (except thumb) flick upward or 'beckon' towards the palm."},
    "17": {"conceptual": "Number 17.", "action": "Thumb and middle finger touch and then snap/flick outward."},  
    "20": {"conceptual": "Two fingers + Zero shape.", "action": "Hand forms an 'L' shape (2) then snaps the index and thumb together to form a '0'."},
    "Isnin": {"conceptual": "Monday.", "action": "Hand forms an 'I' shape and moves in a small circular motion."},
    "Selasa": {"conceptual": "Tuesday.", "action": "Hand forms an 'S' shape and moves in a small circular motion."},
    "Rabu": {"conceptual": "Wednesday.", "action": "Hand forms an 'R' shape and moves in a small circular motion."},
    "Khamis": {"conceptual": "Thursday.", "action": "Hand forms a 'K' shape and moves in a small circular motion."},
    "Jumaat": {"conceptual": "Look for the 'J' motion.", "action": "The pinky finger draws the shape of the letter 'J' in the air."},
    "Sabtu": {"conceptual": "Saturday.", "action": "Hand forms an 'S' shape and remains stationary or rotates slightly."},
    "Ahad": {"conceptual": "Look for the circular motion.", "action": "Index finger points up and draws a circle in the air."},
    "Minggu": {"conceptual": "Week.", "action": "Index finger moves horizontally across the flat palm of the other hand."},
    "Semalam": {"conceptual": "Hand moves backward to indicate the past.", "action": "The thumb points backward over the shoulder."},
    "Hari Ini": {"conceptual": "Hand points down/central to indicate now.", "action": "Both hands move downward simultaneously in front of the body."},    
    "Esok": {"conceptual": "Hand moves forward to indicate the future.", "action": "Index finger moves in a forward arching motion from the cheek."},
    "Jam/Pukul": {"conceptual": "Points to the wrist like a watch.", "action": "Index finger of the dominant hand taps the back of the opposite wrist."},
    "Minit": {"conceptual": "Minutes.", "action": "Index finger taps the palm or makes a small 'tick' movement on a clock face."},
    "Saat": {"conceptual": "Seconds.", "action": "Index finger makes a very quick, sharp flicking or ticking motion."},    
    "Masa": {"conceptual": "Time.", "action": "Hands open out or index finger circles an imaginary clock area in the air."},
    "Selalu": {"conceptual": "A repeating motion usually indicates always.", "action": "Index finger rotates in a continuous, fast forward circular motion."},
    "Kadang-kadang": {"conceptual": "Sometimes.", "action": "The hand with palm facing up rocks side-to-side in a 'maybe' motion."},
    "Pernah": {"conceptual": "Have experienced/done something.", "action": "Hand moves from the chin or chest forward in a single, decisive flick."},
    "Belum": {"conceptual": "Not yet.", "action": "Hand with palm facing back shakes side-to-side near the shoulder (like saying 'no')."},
    "Pagi": {"conceptual": "Morning, sun is rising.", "action": "One hand/arm rises upward from a horizontal position (sun rising)."},
    "Tengah Hari": {"conceptual": "Noon, sun is overhead.", "action": "Elbow is supported by the other hand while the arm points straight up."},
    "Petang": {"conceptual": "Afternoon, sun is setting.", "action": "Arm starts at an angle and moves downward (sun setting)."},
    "Malam": {"conceptual": "Nighttime.", "action": "One hand arches over the other or both hands move down and cross over each other."},
    "Sekarang": {"conceptual": "Now.", "action": "Both hands move downward in front of the body."}
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
            "media_url": get_media_url("Please_Welcome.jpg")
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
            "text": "You are meeting a colleague for lunch at 12:00 PM. You sign:",
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



# Topic 3 Data
TOPIC_3_DATA = {
    18: [ # The Parents & Core
        {"type": "Visual", "text": "Identify this sign:", "target": "Keluarga", "media_url": SIGN_TO_MEDIA["Keluarga"]},
        {"type": "Visual", "text": "Identify this sign:", "target": "Ayah", "media_url": SIGN_TO_MEDIA["Ayah"]},
        {"type": "Visual", "text": "Identify this sign:", "target": "Ibu", "media_url": SIGN_TO_MEDIA["Ibu"]},
        {"type": "Visual", "text": "Identify this sign:", "target": "Orang", "media_url": SIGN_TO_MEDIA["Orang"]},
        {"type": "Logic", "text": "Which sign represents your male parent?", "target": "Ayah", "media_url": None},
        {"type": "Sequence", "text": "Sort to form: 'My Father'", "correct_sequence": ["Ayah", "Saya"], "options": ["Ayah", "Saya", "Ibu", "Keluarga"]},
        {"type": "Sequence", "text": "Sort to form: 'My Mother'", "correct_sequence": ["Ibu", "Saya"], "options": ["Ibu", "Saya", "Ayah", "Keluarga"]},
        {"type": "Sequence", "text": "Sort to form: 'Hello, Mother'", "correct_sequence": ["Hai / Hello", "Ibu"], "options": ["Hai / Hello", "Ibu", "Ayah", "Assalamualaikum"]},
        {"type": "Sequence", "text": "Sort to form: 'How are you, Father?'", "correct_sequence": ["Apa Khabar", "Ayah"], "options": ["Apa Khabar", "Ayah", "Ibu", "Siapa"]},
        {"type": "Context", "text": "Pointing to yourself means...?", "target": "Saya", "media_url": None}
    ],
    19: [ # Siblings & Gender
        {"type": "Visual", "text": "Identify this sign:", "target": "Abang", "media_url": SIGN_TO_MEDIA["Abang"]},
        {"type": "Visual", "text": "Identify this sign:", "target": "Kakak", "media_url": SIGN_TO_MEDIA["Kakak"]},
        {"type": "Visual", "text": "Identify this sign:", "target": "Adik Lelaki", "media_url": SIGN_TO_MEDIA["Adik Lelaki"]},
        {"type": "Visual", "text": "Identify this sign:", "target": "Adik Perempuan", "media_url": SIGN_TO_MEDIA["Adik Perempuan"]},
        {"type": "Visual", "text": "Identify this sign:", "target": "Lelaki", "media_url": SIGN_TO_MEDIA["Lelaki"]},
        {"type": "Visual", "text": "Identify this sign:", "target": "Perempuan", "media_url": SIGN_TO_MEDIA["Perempuan"]},
        {"type": "Sequence", "text": "Sort to form: 'My Elder Sister'", "correct_sequence": ["Kakak", "Saya"], "options": ["Kakak", "Saya", "Abang", "Dia"]},
        {"type": "Sequence", "text": "Sort to form: 'Your Younger Brother'", "correct_sequence": ["Adik Lelaki", "Anda / Kamu"], "options": ["Adik Lelaki", "Anda / Kamu", "Abang", "Saya"]},
        {"type": "Sequence", "text": "Sort to form: 'Is he a male?'", "correct_sequence": ["Dia", "Lelaki", "Apa"], "options": ["Dia", "Lelaki", "Apa", "Anda / Kamu"]},
        {"type": "Sequence", "text": "Sort to form: 'Goodbye, Brother'", "correct_sequence": ["Selamat Jalan", "Abang"], "options": ["Selamat Jalan", "Abang", "Sama-sama", "Kakak"]}
    ],
    20: [ # The Elders & Youth
        {"type": "Visual", "text": "Identify this sign:", "target": "Datuk", "media_url": SIGN_TO_MEDIA["Datuk"]},
        {"type": "Visual", "text": "Identify this sign:", "target": "Nenek", "media_url": SIGN_TO_MEDIA["Nenek"]},
        {"type": "Visual", "text": "Identify this sign:", "target": "Cucu", "media_url": SIGN_TO_MEDIA["Cucu"]},
        {"type": "Visual", "text": "Identify this sign:", "target": "Bayi", "media_url": SIGN_TO_MEDIA["Bayi"]},
        {"type": "Logic", "text": "Father's Father is...?", "target": "Datuk", "media_url": None},
        {"type": "Sequence", "text": "Sort to form: 'My Grandchild'", "correct_sequence": ["Cucu", "Saya"], "options": ["Cucu", "Saya", "Nenek", "Bayi"]},
        {"type": "Sequence", "text": "Sort to form: 'Her Grandmother'", "correct_sequence": ["Nenek", "Dia"], "options": ["Nenek", "Dia", "Datuk", "Saya"]},
        {"type": "Sequence", "text": "Sort to form: 'Thank you, Grandpa'", "correct_sequence": ["Terima Kasih", "Datuk"], "options": ["Terima Kasih", "Datuk", "Sama-sama", "Nenek"]},
        {"type": "Sequence", "text": "Sort to form: 'Where is the baby?'", "correct_sequence": ["Bayi", "Mana"], "options": ["Bayi", "Mana", "Apa", "Siapa"]},
        {"type": "Visual", "text": "Identify this sign:", "target": "Dewasa", "media_url": SIGN_TO_MEDIA["Dewasa"]}
    ],
    21: [ # Birth Order & Kids
        {"type": "Visual", "text": "Identify this sign:", "target": "Anak Sulung", "media_url": SIGN_TO_MEDIA["Anak Sulung"]},
        {"type": "Visual", "text": "Identify this sign:", "target": "Anak Bongsu", "media_url": SIGN_TO_MEDIA["Anak Bongsu"]},
        {"type": "Visual", "text": "Identify this sign:", "target": "Kanak-kanak", "media_url": SIGN_TO_MEDIA["Kanak-kanak"]},
        {"type": "Logic", "text": "First-born child is...?", "target": "Anak Sulung", "media_url": None},
        {"type": "Logic", "text": "Last-born child is...?", "target": "Anak Bongsu", "media_url": None},
        {"type": "Sequence", "text": "Sort to form: 'My First Born'", "correct_sequence": ["Anak Sulung", "Saya"], "options": ["Anak Sulung", "Saya", "Anak Bongsu", "Kanak-kanak"]},
        {"type": "Sequence", "text": "Sort to form: 'Your Last Child'", "correct_sequence": ["Anak Bongsu", "Anda / Kamu"], "options": ["Anak Bongsu", "Anda / Kamu", "Anak Sulung", "Saya"]},
        {"type": "Sequence", "text": "Sort to form: 'What are the children?'", "correct_sequence": ["Kanak-kanak", "Apa"], "options": ["Kanak-kanak", "Apa", "Mana", "Siapa"]},
        {"type": "Sequence", "text": "Sort to form: 'Who is the last child?'", "correct_sequence": ["Anak Bongsu", "Siapa"], "options": ["Anak Bongsu", "Siapa", "Apa", "Mana"]},
        {"type": "Visual", "text": "Identify this sign (Review):", "target": "Dewasa", "media_url": SIGN_TO_MEDIA["Dewasa"]}
    ],
    22: [ # Relatives & Friends
        {"type": "Visual", "text": "Identify this sign:", "target": "Pakcik", "media_url": SIGN_TO_MEDIA["Pakcik"]},
        {"type": "Visual", "text": "Identify this sign:", "target": "Makcik", "media_url": SIGN_TO_MEDIA["Makcik"]},
        {"type": "Visual", "text": "Identify this sign:", "target": "Sepupu", "media_url": SIGN_TO_MEDIA["Sepupu"]},
        {"type": "Visual", "text": "Identify this sign:", "target": "Kawan Rapat", "media_url": SIGN_TO_MEDIA["Kawan Rapat"]},
        {"type": "Visual", "text": "Identify this sign:", "target": "Saudara", "media_url": SIGN_TO_MEDIA["Saudara"]},
        {"type": "Sequence", "text": "Sort to form: 'My Cousin'", "correct_sequence": ["Sepupu", "Saya"], "options": ["Sepupu", "Saya", "Saudara", "Dia"]},
        {"type": "Sequence", "text": "Sort to form: 'Your Close Friend'", "correct_sequence": ["Kawan Rapat", "Anda / Kamu"], "options": ["Kawan Rapat", "Anda / Kamu", "Kawan", "Saya"]},
        {"type": "Logic", "text": "Identify Auntie", "target": "Makcik", "media_url": None},
        {"type": "Sequence", "text": "Sort to form: 'Hello, Uncle'", "correct_sequence": ["Hai / Hello", "Pakcik"], "options": ["Hai / Hello", "Pakcik", "Makcik", "Terima Kasih"]},
        {"type": "Sequence", "text": "Sort to form: 'Where is the relative?'", "correct_sequence": ["Saudara", "Mana"], "options": ["Saudara", "Mana", "Apa", "Siapa"]}
    ],
    23: [ # Marriage & Logic
        {"type": "Visual", "text": "Identify this sign:", "target": "Suami", "media_url": SIGN_TO_MEDIA["Suami"]},
        {"type": "Visual", "text": "Identify this sign:", "target": "Isteri", "media_url": SIGN_TO_MEDIA["Isteri"]},
        {"type": "Visual", "text": "Identify this sign:", "target": "Dia", "media_url": SIGN_TO_MEDIA["Dia"]},
        {"type": "Visual", "text": "Identify this sign:", "target": "Anda / Kamu", "media_url": SIGN_TO_MEDIA["Anda / Kamu"]},
        {"type": "Logic", "text": "A married woman is...?", "target": "Isteri", "media_url": None},
        {"type": "Sequence", "text": "Sort to form: 'My Wife'", "correct_sequence": ["Isteri", "Saya"], "options": ["Isteri", "Saya", "Suami", "Dia"]},
        {"type": "Sequence", "text": "Sort to form: 'Your Husband'", "correct_sequence": ["Suami", "Anda / Kamu"], "options": ["Suami", "Anda / Kamu", "Isteri", "Saya"]},
        {"type": "Sequence", "text": "Sort to form: 'Who is she?'", "correct_sequence": ["Dia", "Siapa"], "options": ["Dia", "Siapa", "Apa", "Mana"]},
        {"type": "Sequence", "text": "Sort to form: 'What is husband?'", "correct_sequence": ["Suami", "Apa"], "options": ["Suami", "Apa", "Mana", "Siapa"]},
        {"type": "Sequence", "text": "Sort to form: 'Thank you, Wife'", "correct_sequence": ["Terima Kasih", "Isteri"], "options": ["Terima Kasih", "Isteri", "Sama-sama", "Suami"]}
    ]
}



TOPIC_3_POOL = [
    "Keluarga", "Ayah", "Ibu", "Orang", "Abang", "Kakak", "Adik Lelaki", "Adik Perempuan",
    "Datuk", "Nenek", "Cucu", "Bayi", "Anak Sulung", "Anak Bongsu", "Kanak-kanak", "Dewasa",
    "Pakcik", "Makcik", "Sepupu", "Saudara", "Lelaki", "Perempuan", "Suami", "Isteri", "Kawan Rapat",
    "Kawan", "Saya", "Anda / Kamu", "Dia", "Siapa", "Mana", "Apa", "Selamat Jalan", "Hai / Hello", "Apa Khabar", "Terima Kasih", "Anak Sulung", "Anak Bongsu"
]

TOPIC_2_POOL = [
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
    "Saya", "Anda / Kamu", "Dia", "Nama", "Tinggal", "Apa", "Siapa", "Mana"
]

TOPIC_4_DATA = {
    26: [
        {"type": "Visual", "text": "Identify this sign:", "target": "11", "media_url": SIGN_TO_MEDIA["11"]},
        {"type": "Visual", "text": "Identify this sign:", "target": "15", "media_url": SIGN_TO_MEDIA["15"]},
        {"type": "Visual", "text": "Identify this sign:", "target": "20", "media_url": SIGN_TO_MEDIA["20"]},
        {"type": "Logic", "text": "Which sign is for '12'?", "target": "12", "media_url": None},
        {"type": "Logic", "text": "Which sign is for '20'?", "target": "20", "media_url": None},
        {"type": "Sequence", "text": "Sort to form: '11 and 12'", "correct_sequence": ["11", "12"], "options": ["11", "12", "13", "10"]},
        {"type": "Sequence", "text": "Sort to form: '13 Children'", "correct_sequence": ["13", "Kanak-kanak"], "options": ["Kanak-kanak", "13", "Dewasa", "15"]},
        {"type": "Sequence", "text": "Sort to form: 'My brother is 15'", "correct_sequence": ["Abang", "Saya", "15"], "options": ["Abang", "Saya", "15", "Kakak", "12"]},
        {"type": "Sequence", "text": "Sort to form: 'He has 11 relatives'", "correct_sequence": ["Dia", "11", "Saudara"], "options": ["Dia", "Saudara", "11", "Kawan", "14"]},
        {"type": "Visual", "text": "Identify this sign:", "target": "17", "media_url": SIGN_TO_MEDIA["17"]}
    ],
    27: [
        {"type": "Visual", "text": "Identify this sign:", "target": "Isnin", "media_url": SIGN_TO_MEDIA["Isnin"]},
        {"type": "Visual", "text": "Identify this sign:", "target": "Selasa", "media_url": SIGN_TO_MEDIA["Selasa"]},
        {"type": "Visual", "text": "Identify this sign:", "target": "Rabu", "media_url": SIGN_TO_MEDIA["Rabu"]},
        {"type": "Visual", "text": "Identify this sign:", "target": "Khamis", "media_url": SIGN_TO_MEDIA["Khamis"]},
        {"type": "Logic", "text": "Which day comes after Selasa?", "target": "Rabu", "media_url": None},
        {"type": "Logic", "text": "Which day comes before Selasa?", "target": "Isnin", "media_url": None},
        {"type": "Sequence", "text": "Sort to form: 'Today is Monday'", "correct_sequence": ["Hari Ini", "Isnin"], "options": ["Hari Ini", "Isnin", "Esok", "Selasa"]},
        {"type": "Sequence", "text": "Sort to form: 'Thursday is a week'", "correct_sequence": ["Khamis", "Minggu"], "options": ["Khamis", "Minggu", "Selasa", "Masa"]},
        {"type": "Sequence", "text": "Sort to form: 'Tomorrow is Tuesday'", "correct_sequence": ["Esok", "Selasa"], "options": ["Esok", "Selasa", "Hari Ini", "Isnin"]},
        {"type": "Sequence", "text": "Sort to form: 'Yesterday was Wednesday'", "correct_sequence": ["Semalam", "Rabu"], "options": ["Semalam", "Rabu", "Esok", "Khamis"]}
    ],
    28: [
        {"type": "Visual", "text": "Identify this sign:", "target": "Jumaat", "media_url": SIGN_TO_MEDIA["Jumaat"]},
        {"type": "Visual", "text": "Identify this sign:", "target": "Sabtu", "media_url": SIGN_TO_MEDIA["Sabtu"]},
        {"type": "Visual", "text": "Identify this sign:", "target": "Ahad", "media_url": SIGN_TO_MEDIA["Ahad"]},
        {"type": "Visual", "text": "Identify this sign:", "target": "Minggu", "media_url": SIGN_TO_MEDIA["Minggu"]},
        {"type": "Logic", "text": "Identify the sign for 'Minggu' (Week)", "target": "Minggu", "media_url": None},
        {"type": "Context", "text": "Which day is the weekend in Malaysia?", "target": "Ahad", "media_url": None},
        {"type": "Sequence", "text": "Sort to form: 'Next Friday'", "correct_sequence": ["Jumaat", "Esok"], "options": ["Jumaat", "Esok", "Semalam", "Sabtu"]},
        {"type": "Sequence", "text": "Sort to form: 'Today is Sunday'", "correct_sequence": ["Hari Ini", "Ahad"], "options": ["Hari Ini", "Ahad", "Jumaat", "Esok"]},
        {"type": "Sequence", "text": "Sort to form: 'Today is Friday'", "correct_sequence": ["Hari Ini", "Jumaat"], "options": ["Hari Ini", "Jumaat", "Esok", "Sabtu"]},
        {"type": "Sequence", "text": "Sort to form: 'Yesterday was Saturday'", "correct_sequence": ["Semalam", "Sabtu"], "options": ["Semalam", "Sabtu", "Hari Ini", "Minggu"]}
    ],
    29: [
        {"type": "Visual", "text": "Identify this sign:", "target": "Semalam", "media_url": SIGN_TO_MEDIA["Semalam"]},
        {"type": "Visual", "text": "Identify this sign:", "target": "Hari Ini", "media_url": SIGN_TO_MEDIA["Hari Ini"]},
        {"type": "Visual", "text": "Identify this sign:", "target": "Esok", "media_url": SIGN_TO_MEDIA["Esok"]},
        {"type": "Logic", "text": "If today is Tuesday, what was yesterday?", "target": "Isnin", "media_url": None},
        {"type": "Logic", "text": "'Esok' means...?", "target": "Esok", "media_url": None},
        {"type": "Logic", "text": "Contrast 'Semalam' vs 'Esok'. Hand moves backward for...", "target": "Semalam", "media_url": None},
        {"type": "Sequence", "text": "Sort to form: 'Tomorrow is Monday'", "correct_sequence": ["Esok", "Isnin"], "options": ["Esok", "Isnin", "Hari Ini", "Selasa"]},
        {"type": "Sequence", "text": "Sort to form: 'Yesterday was Saturday'", "correct_sequence": ["Semalam", "Sabtu"], "options": ["Semalam", "Sabtu", "Esok", "Minggu"]},
        {"type": "Sequence", "text": "Sort to form: 'Tomorrow is Friday'", "correct_sequence": ["Esok", "Jumaat"], "options": ["Esok", "Jumaat", "Semalam", "Sabtu"]},
        {"type": "Sequence", "text": "Sort to form: 'Today is Sunday'", "correct_sequence": ["Hari Ini", "Ahad"], "options": ["Hari Ini", "Ahad", "Esok", "Sabtu", "Masa"]}
    ],
    30: [
        {"type": "Visual", "text": "Identify this sign:", "target": "Jam/Pukul", "media_url": SIGN_TO_MEDIA["Jam/Pukul"]},
        {"type": "Visual", "text": "Identify this sign:", "target": "Minit", "media_url": SIGN_TO_MEDIA["Minit"]},
        {"type": "Visual", "text": "Identify this sign:", "target": "Masa", "media_url": SIGN_TO_MEDIA["Masa"]},
        {"type": "Logic", "text": "Which one is for time?", "target": "Jam/Pukul", "media_url": None},
        {"type": "Logic", "text": "'Saat' refers to...?", "target": "Saat", "media_url": None},
        {"type": "Context", "text": "Asking for the time usually involves...?", "target": "Jam/Pukul", "media_url": None},
        {"type": "Sequence", "text": "Sort to form: '11 o'clock'", "correct_sequence": ["Jam/Pukul", "11"], "options": ["Jam/Pukul", "11", "Masa", "12"]},
        {"type": "Sequence", "text": "Sort to form: '10 minutes'", "correct_sequence": ["10", "Minit"], "options": ["10", "Minit", "11", "Saat"]},
        {"type": "Sequence", "text": "Sort to form: 'The time is now'", "correct_sequence": ["Masa", "Sekarang"], "options": ["Masa", "Sekarang", "Jam/Pukul", "Esok"]},
        {"type": "Sequence", "text": "Sort to form: '12 o'clock tomorrow'", "correct_sequence": ["Esok", "Jam/Pukul", "12"], "options": ["Esok", "Jam/Pukul", "12", "Masa", "Hari Ini"]}
    ],
    31: [
        {"type": "Visual", "text": "Identify this sign:", "target": "Selalu", "media_url": SIGN_TO_MEDIA["Selalu"]},
        {"type": "Visual", "text": "Identify this sign:", "target": "Kadang-kadang", "media_url": SIGN_TO_MEDIA["Kadang-kadang"]},
        {"type": "Visual", "text": "Identify this sign:", "target": "Belum", "media_url": SIGN_TO_MEDIA["Belum"]},
        {"type": "Visual", "text": "Identify this sign:", "target": "Pernah", "media_url": SIGN_TO_MEDIA["Pernah"]},
        {"type": "Logic", "text": "'Not yet' in BIM is...?", "target": "Belum", "media_url": None},
        {"type": "Logic", "text": "A repeating motion usually indicates...?", "target": "Selalu", "media_url": None},
        {"type": "Sequence", "text": "Sort to form: 'Always today'", "correct_sequence": ["Selalu", "Hari Ini"], "options": ["Selalu", "Hari Ini", "Kadang-kadang", "Semalam"]},
        {"type": "Sequence", "text": "Sort to form: 'Not yet time'", "correct_sequence": ["Belum", "Masa"], "options": ["Belum", "Masa", "Pernah", "Sekarang"]},
        {"type": "Sequence", "text": "Sort to form: 'Sometimes yesterday'", "correct_sequence": ["Kadang-kadang", "Semalam"], "options": ["Kadang-kadang", "Semalam", "Selalu", "Hari Ini"]},
        {"type": "Sequence", "text": "Sort to form: 'Ever on Sunday?'", "correct_sequence": ["Pernah", "Ahad"], "options": ["Pernah", "Ahad", "Belum", "Sabtu"]}
    ],
    32: [
        {"type": "Visual", "text": "Identify this sign:", "target": "Pagi", "media_url": SIGN_TO_MEDIA["Pagi"]},
        {"type": "Visual", "text": "Identify this sign:", "target": "Malam", "media_url": SIGN_TO_MEDIA["Malam"]},
        {"type": "Visual", "text": "Identify this sign:", "target": "Petang", "media_url": SIGN_TO_MEDIA["Petang"]},
        {"type": "Visual", "text": "Identify this sign:", "target": "Tengah Hari", "media_url": SIGN_TO_MEDIA["Tengah Hari"]},
        {"type": "Logic", "text": "Sun is overhead:", "target": "Tengah Hari", "media_url": None},
        {"type": "Logic", "text": "Sun is setting:", "target": "Petang", "media_url": None},
        {"type": "Sequence", "text": "Sort to form: 'Tomorrow morning'", "correct_sequence": ["Esok", "Pagi"], "options": ["Esok", "Pagi", "Semalam", "Malam"]},
        {"type": "Sequence", "text": "Sort to form: 'Tonight'", "correct_sequence": ["Malam", "Hari Ini"], "options": ["Malam", "Hari Ini", "Petang", "Esok"]},
        {"type": "Sequence", "text": "Sort to form: 'Good night'", "correct_sequence": ["Selamat", "Malam"], "options": ["Selamat", "Malam", "Pagi", "Petang"]},
        {"type": "Sequence", "text": "Sort to form: '2pm in the afternoon'", "correct_sequence": ["Jam/Pukul", "2", "Petang"], "options": ["Jam/Pukul", "2", "Petang", "Malam", "Pagi"]}
    ]
}

TOPIC_4_POOL = [
    "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
    "Isnin", "Selasa", "Rabu", "Khamis", "Jumaat", "Sabtu", "Ahad", "Minggu",
    "Semalam", "Hari Ini", "Esok", "Jam/Pukul", "Minit", "Saat", "Masa",
    "Selalu", "Kadang-kadang", "Pernah", "Belum",
    "Pagi", "Tengah Hari", "Petang", "Malam",
    "Saya", "Dia", "Kanak-kanak", "Abang", "Saudara", "Sekarang",
    "11", "12", "10", "5", "Ahad", "Selamat"
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


    # Topic 3 Logic
    if topic_id == 3:
        pool = TOPIC_3_POOL
        if lesson_id == 24: # Final Mastery Exam
            all_questions = []
            for l_id in range(18, 24):
                all_questions.extend(TOPIC_3_DATA[l_id])
            
            # Tier 1: Fast Visual Identification (10 Qs)
            visual_qs = [q for q in all_questions if q['type'] == 'Visual']
            tier1 = random.sample(visual_qs, min(10, len(visual_qs)))
            
            # Tier 2: Complex Sorting (No sana, sini, itu, ini)
            tier2 = [
                {"type": "Sequence", "text": "Sort to form: 'My mother'", "correct_sequence": ["Ibu", "Saya"], "options": ["Ibu", "Saya", "Ayah", "Keluarga"]},
                {"type": "Sequence", "text": "Sort to form: 'Your cousin'", "correct_sequence": ["Sepupu", "Anda / Kamu"], "options": ["Sepupu", "Anda / Kamu", "Saudara", "Dia"]},
                {"type": "Sequence", "text": "Sort to form: 'His uncle'", "correct_sequence": ["Pakcik", "Dia"], "options": ["Pakcik", "Dia", "Makcik", "Saya"]},
                {"type": "Sequence", "text": "Sort to form: 'My youngest sister'", "correct_sequence": ["Adik Perempuan", "Saya"], "options": ["Adik Perempuan", "Anak Bongsu", "Saya", "Kakak", "Dewasa"]},
                {"type": "Sequence", "text": "Sort to form: 'My grandfather'", "correct_sequence": ["Datuk", "Saya"], "options": ["Datuk", "Saya", "Dewasa", "Kanak-kanak", "Nenek"]},
                {"type": "Sequence", "text": "Sort to form: 'Who is the relative?'", "correct_sequence": ["Saudara", "Siapa"], "options": ["Saudara", "Siapa", "Orang", "Mana"]},
                {"type": "Sequence", "text": "Sort to form: 'He is my best friend'", "correct_sequence": ["Dia", "Kawan Rapat", "Saya"], "options": ["Dia", "Kawan Rapat", "Saya", "Kawan", "Suami"]},
                {"type": "Sequence", "text": "Sort to form: 'My family'", "correct_sequence": ["Keluarga", "Saya"], "options": ["Keluarga", "Saya", "Ayah", "Ibu"]},
                {"type": "Sequence", "text": "Sort to form: 'Where is your cousin?'", "correct_sequence": ["Sepupu", "Anda / Kamu", "Mana"], "options": ["Sepupu", "Anda / Kamu", "Mana", "Apa"]},
                {"type": "Sequence", "text": "Sort to form: 'She is my wife'", "correct_sequence": ["Dia", "Isteri", "Saya"], "options": ["Dia", "Isteri", "Saya", "Perempuan", "Suami"]}
            ]
            
            # Tier 3: Integration (Greetings + Identity + Family)
            tier3 = [
                {"type": "Sequence", "text": "Sort to form: 'Hi, who is your close friend?'", "correct_sequence": ["Hai / Hello", "Kawan Rapat", "Anda / Kamu", "Siapa"], "options": ["Hai / Hello", "Kawan Rapat", "Anda / Kamu", "Siapa", "Apa"]},
                {"type": "Sequence", "text": "Sort to form: 'Thank you, grandpa'", "correct_sequence": ["Terima Kasih", "Datuk"], "options": ["Terima Kasih", "Datuk", "Nenek", "Sama-sama"]},
                {"type": "Sequence", "text": "Sort to form: 'Goodbye, uncle'", "correct_sequence": ["Selamat Jalan", "Pakcik"], "options": ["Selamat Jalan", "Pakcik", "Makcik", "Terima Kasih"]},
                {"type": "Sequence", "text": "Sort to form: 'How are you, brother?'", "correct_sequence": ["Apa Khabar", "Abang"], "options": ["Apa Khabar", "Abang", "Khabar Baik", "Adik Lelaki"]},
                {"type": "Sequence", "text": "Sort to form: 'Good morning, mother'", "correct_sequence": ["Selamat Pagi", "Ibu"], "options": ["Selamat Pagi", "Ibu", "Ayah", "Selamat Malam"]},
                {"type": "Sequence", "text": "Sort to form: 'Congratulations! Your baby is a boy'", "correct_sequence": ["Tahniah", "Bayi", "Anda / Kamu", "Lelaki"], "options": ["Tahniah", "Bayi", "Anak Sulung", "Anda / Kamu", "Lelaki", "Perempuan"]},
                {"type": "Sequence", "text": "Sort to form: 'Excuse me, where is your father?'", "correct_sequence": ["Maaf (Excuse)", "Ayah", "Anda / Kamu", "Mana"], "options": ["Maaf (Excuse)", "Ayah", "Anda / Kamu", "Mana", "Siapa"]},
                {"type": "Sequence", "text": "Sort to form: 'My name is...'", "correct_sequence": ["Nama", "Saya"], "options": ["Nama", "Saya", "Dia", "Anda / Kamu"]},
                {"type": "Sequence", "text": "Sort to form: 'What is your name, friend?'", "correct_sequence": ["Nama", "Anda / Kamu", "Apa", "Kawan"], "options": ["Nama", "Anda / Kamu", "Apa", "Kawan", "Siapa"]},
                {"type": "Sequence", "text": "Sort to form: 'Welcome, family'", "correct_sequence": ["Selamat Datang", "Keluarga"], "options": ["Selamat Datang", "Keluarga", "Orang", "Selamat Jalan"]}
            ]
            
            final_qs = []
            
            # Process Tier 1
            for idx, q in enumerate(tier1):
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
                
            # Process Tier 2 & 3
            word_building = tier2 + tier3
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
                    "id": idx + 11,
                    "text": q["text"],
                    "type": q["type"],
                    "media_url": None,
                    "media_type": None,
                    "options": options_objs,
                    "hide_option_text": True,
                    "correct_sequence": q["correct_sequence"],
                    "correct_option": ",".join(q["correct_sequence"]),
                    "hint": "Form the sentence by selecting signs in order."
                })
            return final_qs
            
        if lesson_id in TOPIC_3_DATA:
            questions = TOPIC_3_DATA[lesson_id]
            final_qs = []
            for idx, q in enumerate(questions):
                if q["type"] == "Sequence":
                    options_text = list(q["options"])
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
                        "media_url": None,
                        "media_type": None,
                        "options": options_objs,
                        "hide_option_text": True,
                        "correct_sequence": q["correct_sequence"],
                        "correct_option": ",".join(q["correct_sequence"]),
                        "hint": "Click the images in the correct grammatical order."
                    })
                else:
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
                    })
            return final_qs
            
    # Topic 4 Logic
    if topic_id == 4:
        pool = TOPIC_4_POOL
        if lesson_id == 33: # Final Mastery Challenge
            all_questions = []
            for l_id in range(26, 33):
                all_questions.extend(TOPIC_4_DATA[l_id])
            
            visual_logic_qs = [q for q in all_questions if q['type'] in ['Visual', 'Logic', 'Context']]
            seq_qs = [q for q in all_questions if q['type'] == 'Sequence']
            
            # Aim for 30 questions total (e.g. 20 visual/logic, 10 sequence)
            selected_vl = random.sample(visual_logic_qs, min(20, len(visual_logic_qs)))
            selected_seq = random.sample(seq_qs, min(10, len(seq_qs)))
            
            final_qs = []
            
            # Process Visual/Logic
            for idx, q in enumerate(selected_vl):
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
                    "media_url": q.get("media_url"),
                    "media_type": "image" if q.get("media_url") else None,
                    "options": options_objs,
                    "hide_option_text": True if not q.get("media_url") else False,
                    "correct_option": q["target"],
                    "hint": SIGN_HINTS.get(q["target"], {}).get("conceptual", "Topic 4 Mastery Question.")
                })
                
            # Process Sequencing
            start_id = len(final_qs) + 1
            for idx, q in enumerate(selected_seq):
                options_text = list(q["options"])
                random.shuffle(options_text)
                
                options_objs = []
                for opt in options_text:
                    options_objs.append({
                        "text": opt,
                        "media_url": SIGN_TO_MEDIA.get(opt, None)
                    })
                
                final_qs.append({
                    "id": start_id + idx,
                    "text": q["text"],
                    "type": q["type"],
                    "media_url": None,
                    "media_type": None,
                    "options": options_objs,
                    "hide_option_text": True,
                    "correct_sequence": q["correct_sequence"],
                    "correct_option": ",".join(q["correct_sequence"]),
                    "hint": "Form the sentence by selecting signs in order."
                })
            return final_qs
            
        if lesson_id in TOPIC_4_DATA:
            questions = TOPIC_4_DATA[lesson_id]
            final_qs = []
            for idx, q in enumerate(questions):
                if q["type"] == "Sequence":
                    options_text = list(q["options"])
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
                        "media_url": None,
                        "media_type": None,
                        "options": options_objs,
                        "hide_option_text": True,
                        "correct_sequence": q["correct_sequence"],
                        "correct_option": ",".join(q["correct_sequence"]),
                        "hint": "Click the images in the correct grammatical order."
                    })
                else:
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
                        "media_url": q.get("media_url"),
                        "media_type": "image" if q.get("media_url") else None,
                        "options": options_objs,
                        "hide_option_text": True if not q.get("media_url") else False,
                        "correct_option": q["target"],
                        "hint": SIGN_HINTS.get(q["target"], {}).get("conceptual", "Topic 4 lesson content.")
                    })
            return final_qs

    return []

def generate_generic_quiz():
    return []
