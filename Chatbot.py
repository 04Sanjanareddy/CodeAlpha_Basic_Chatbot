# ------------------------------------------------------
#  🤖 PyBot — Console Chatbot with Enhanced Quiz
#  Concepts: functions, loops, if/elif, input/output, strings
#  No external libraries required.
# ------------------------------------------------------

def normalize(s): return s.strip()
def is_int(s):
    s = s.strip()
    return (s[1:].isdigit() if s.startswith("-") else s.isdigit())

def parse_two_numbers(parts):
    if len(parts) == 3 and is_int(parts[1]) and is_int(parts[2]):
        return True, int(parts[1]), int(parts[2])
    return False, 0, 0

# ---------- Small helpers ----------
def show_help():
    print("🤖 PyBot Commands:")
    print("  hello / hi / hey")
    print("  how are you")
    print("  compliment / joke / fact / riddle")
    print("  quiz            — start a mixed quiz")
    print("  quiz <category> — start a category quiz (general, science, tech, geo)")
    print("  score           — show your quiz stats")
    print("  reset score     — reset quiz stats")
    print("  repeat after me — I’ll echo your next line")
    print("  call me <name>  | what's my name")
    print("  reverse <text>  | upper <text> | lower <text>")
    print("  count <text>    | pal <text>")
    print("  add a b | sub a b | mul a b | div a b")
    print("  bye / exit      — end the chat")

def handle_fact(last_fact):
    last_fact += 1
    if last_fact == 1:
        print("🤖 PyBot: Did you know? Honey never spoils — archaeologists found 3000-year-old edible honey! 🍯")
    elif last_fact == 2:
        print("🤖 PyBot: Octopuses have three hearts and blue blood! 🐙")
    else:
        print("🤖 PyBot: Bananas are berries, but strawberries are not! 🍌🍓")
        last_fact = 0
    return last_fact

def handle_compliment(turn, name):
    if turn % 3 == 0:
        print(f"🤖 PyBot: You’re amazing, {name}! Keep shining 🌟")
    elif turn % 3 == 1:
        print(f"🤖 PyBot: You have such a positive energy, {name}! 💫")
    else:
        print(f"🤖 PyBot: {name}, you’re one of a kind! 🌈")
    return turn + 1

def handle_greet(turn, name):
    if turn % 2 == 0:
        print(f"🤖 PyBot: Hello {name}! 👋")
    else:
        print(f"🤖 PyBot: Hey there, {name}!")
    return turn + 1

def small_math(parts):
    op = parts[0]
    ok, a, b = parse_two_numbers(parts)
    if not ok:
        print(f"🤖 PyBot: Usage: {op} a b (integers)")
        return
    if op == "add": print(a + b)
    elif op == "sub": print(a - b)
    elif op == "mul": print(a * b)
    elif op == "div":
        if b == 0: print("🤖 PyBot: Cannot divide by zero.")
        else:      print(a / b)

# ---------- Quiz database ----------
# Each question: {q, options:[A,B,C,D], answer:"a"/"b"/"c"/"d", hint}
QUIZ_DB = {
    "general": [
        {"q": "What is the capital of France?",
         "options": ["Paris", "Madrid", "Rome", "Berlin"], "answer": "a", "hint": "City of Light"},
        {"q": "Which planet is known as the Red Planet?",
         "options": ["Venus", "Mars", "Jupiter", "Mercury"], "answer": "b", "hint": "Fourth from the Sun"},
        {"q": "How many continents are there on Earth?",
         "options": ["5", "6", "7", "8"], "answer": "c", "hint": "More than six"},
    ],
    "science": [
        {"q": "Water boils at what temperature at sea level (°C)?",
         "options": ["90", "95", "100", "110"], "answer": "c", "hint": "Three digits"},
        {"q": "What gas do plants primarily absorb for photosynthesis?",
         "options": ["Oxygen", "Carbon dioxide", "Nitrogen", "Helium"], "answer": "b", "hint": "CO₂"},
        {"q": "The basic unit of heredity is the…",
         "options": ["Cell", "Chromosome", "Gene", "Protein"], "answer": "c", "hint": "Smaller than a chromosome"},
    ],
    "tech": [
        {"q": "HTML stands for…",
         "options": ["Hyperlinks and Text Markup Language", "HyperText Markup Language", "Home Tool Markup Language", "HighText Markdown Language"],
         "answer": "b", "hint": "Second option"},
        {"q": "Which one is a backend language?",
         "options": ["CSS", "HTML", "Python", "Figma"], "answer": "c", "hint": "Snakes 🐍"},
        {"q": "In computing, CPU stands for…",
         "options": ["Central Processing Unit", "Computer Personal Unit", "Central Print Unit", "Core Processing Utility"],
         "answer": "a", "hint": "Central … Unit"},
    ],
    "geo": [
        {"q": "Which is the largest ocean on Earth?",
            "options": ["Atlantic", "Indian", "Pacific", "Arctic"], "answer": "c", "hint": "Covers ~1/3 of Earth"},
        {"q": "Mount Everest is located in which mountain range?",
            "options": ["Andes", "Himalayas", "Alps", "Rockies"], "answer": "b", "hint": "South Asia"},
        {"q": "Which country has the most natural lakes?",
            "options": ["Canada", "USA", "Russia", "Brazil"], "answer": "a", "hint": "Maple leaf 🇨🇦"},
    ],
}

ALL_CATEGORIES = ("general", "science", "tech", "geo")

def present_question(qobj):
    print(f"❓ {qobj['q']}")
    print("   A) " + qobj["options"][0])
    print("   B) " + qobj["options"][1])
    print("   C) " + qobj["options"][2])
    print("   D) " + qobj["options"][3])
    print("   (answer with A/B/C/D, or type: hint | 50-50 | skip | quit quiz)")

def apply_5050(qobj):
    # reveal two options: correct + one random wrong (simple deterministic pick without random)
    # We'll keep A and B if answer is among them; else keep correct + A.
    ans = qobj["answer"]  # 'a'..'d'
    keep = []
    if ans in ("a", "b"):
        keep = ["a", "b"]
    else:
        keep = [ans, "a"]
    # Build masked options
    labeled = ["A) "+qobj["options"][0], "B) "+qobj["options"][1], "C) "+qobj["options"][2], "D) "+qobj["options"][3]]
    masked = []
    for i, lab in enumerate(("a","b","c","d")):
        if lab in keep:
            masked.append(labeled[i])
        else:
            masked.append("--")
    print("🔎 50-50:")
    print("   " + masked[0])
    print("   " + masked[1])
    print("   " + masked[2])
    print("   " + masked[3])

def ask_quiz_question(state, name):
    """Handles one question interaction loop. Returns True if continuing quiz, False if quitting quiz."""
    q = state["current_q"]
    present_question(q)

    while True:
        ans = input(f"{name} (quiz): ").strip().lower()

        if not ans:
            print("🤖 PyBot: Please enter A/B/C/D, or type hint / 50-50 / skip / quit quiz.")
            continue

        if ans in ("quit quiz", "quit", "q"):
            print("🛑 Quiz ended.")
            return False

        if ans in ("hint", "h"):
            print("💡 Hint:", q["hint"])
            continue

        if ans in ("50-50", "5050", "50 50"):
            if not state["lifeline_used"]:
                apply_5050(q)
                state["lifeline_used"] = True
            else:
                print("🚫 You already used 50-50 for this question.")
            continue

        if ans in ("skip", "idk", "i don't know", "dont know", "don't know", "s"):
            print("➡️  Skipped. The answer was:", q["answer"].upper(), "-", q["options"][ord(q["answer"]) - ord('a')])
            state["skipped"] += 1
            return True

        # accept a/b/c/d or full text match
        if ans in ("a","b","c","d"):
            if ans == q["answer"]:
                print("✅ Correct!")
                state["score"] += 1
            else:
                correct_text = q["options"][ord(q["answer"]) - ord('a')]
                print(f"❌ Not quite. Correct: {q['answer'].upper()} — {correct_text}")
                state["wrong"] += 1
            return True
        else:
            # try full text match
            text_opts = [o.lower() for o in q["options"]]
            if ans in text_opts:
                idx = text_opts.index(ans)
                letter = chr(ord('a') + idx)
                if letter == q["answer"]:
                    print("✅ Correct!")
                    state["score"] += 1
                else:
                    print(f"❌ Not quite. Correct: {q['answer'].upper()} — {q['options'][ord(q['answer']) - ord('a')]}")
                    state["wrong"] += 1
                return True

            print("🤖 PyBot: I didn't get that. Enter A/B/C/D, or type: hint | 50-50 | skip | quit quiz.")

def next_question(state):
    # rotate through chosen category list deterministically (no random used)
    cat = state["category"]
    pool = state["pool_map"][cat] if cat != "mixed" else state["mixed_pool"]
    if not pool:
        return None
    # pop next question in round-robin fashion
    q = pool[state["index"] % len(pool)]
    state["index"] += 1
    state["lifeline_used"] = False
    return q

def start_quiz(state, category):
    if category == "":
        category = "mixed"
    category = category.lower().strip()
    if category not in ALL_CATEGORIES and category != "mixed":
        print("📚 Categories:", ", ".join(ALL_CATEGORIES), "| or use: mixed")
        return False

    state["active"] = True
    state["category"] = category
    state["index"] = 0
    state["lifeline_used"] = False
    print(f"🎯 Quiz started — Category: {category.upper() if category!='mixed' else 'MIXED'}")
    return True

def show_score(state, name):
    total = state["score"] + state["wrong"]
    print(f"📊 {name}'s Quiz Stats:")
    print(f"   Correct: {state['score']}")
    print(f"   Wrong:   {state['wrong']}")
    print(f"   Skipped: {state['skipped']}")
    print(f"   Total answered: {total}  |  Accuracy: {(state['score']*100/total if total else 0):.1f}%")

def reset_score(state):
    state["score"] = 0
    state["wrong"] = 0
    state["skipped"] = 0
    print("🔄 Quiz stats reset.")

# ---------- Main chatbot ----------
def chatbot():
    print("🤖 Chatbot: Hi! I'm PyBot — your friendly Python chatbot.")
    name = input("🤖 Chatbot: What's your name? ").strip() or "Friend"
    print(f"🤖 Chatbot: Nice to meet you, {name}! Type 'help' to see what I can do.")

    # general state
    turn = 0
    bot_mood = "happy"
    repeat_mode = False
    last_fact = 0

    # quiz state
    quiz = {
        "active": False,
        "category": "mixed",
        "index": 0,
        "score": 0,
        "wrong": 0,
        "skipped": 0,
        "lifeline_used": False,
        # build pools (lists) once
        "pool_map": {k: QUIZ_DB[k][:] for k in QUIZ_DB},   # copy lists
        "mixed_pool": QUIZ_DB["general"] + QUIZ_DB["science"] + QUIZ_DB["tech"] + QUIZ_DB["geo"],
        "current_q": None,
    }

    while True:
        # If quiz is active, drive question loop inside the main loop
        if quiz["active"]:
            # fetch next question
            q = next_question(quiz)
            if not q:
                print("🎉 No more questions in this category. Type 'score' to see results or start another quiz.")
                quiz["active"] = False
            else:
                quiz["current_q"] = q
                cont = ask_quiz_question(quiz, name)
                if not cont:
                    quiz["active"] = False
                # loop back to main prompt
                continue

        user = input(f"{name}: ").strip()
        msg = user.lower()

        # one-shot echo mode
        if repeat_mode:
            print(f"🤖 PyBot: {user}")
            repeat_mode = False
            continue

        # greetings
        if msg in ("hi", "hello", "hey"):
            turn = handle_greet(turn, name)

        # small acknowledgements
        elif msg in ("ok", "okay", "k", "okk", "cool", "nice", "great", "fine"):
            print("🤖 PyBot: 👍 Got it!")

        # thanks variants
        elif msg in ("thanks", "thank you", "thx", "ty", "tq"):
            print(f"🤖 PyBot: You're welcome, {name}! 😊")

        # mood
        elif msg in ("how are you", "how r u", "how are u", "how's it going"):
            if bot_mood == "happy":
                print(f"🤖 PyBot: I'm feeling great today, {name}! 😄")
            else:
                print("🤖 PyBot: Not my best day, but talking to you helps!")
            bot_mood = "happy" if bot_mood == "sad" else "happy"

        # exit
        elif msg in ("bye", "goodbye", "exit", "quit"):
            print(f"🤖 PyBot: Goodbye {name}! It was nice chatting with you 👋")
            break

        # rename
        elif msg.startswith("call me"):
            raw = user[7:].strip(" :")
            new_name = raw.capitalize()
            if new_name:
                name = new_name
                print(f"🤖 PyBot: Got it! I’ll call you {name} from now on 🥰")
            else:
                print("🤖 PyBot: Hmm, what should I call you then?")

        elif msg in ("what is my name", "what's my name"):
            print(f"🤖 PyBot: You're {name}.")

        # quiz controls
        elif msg == "quiz":
            if start_quiz(quiz, "mixed"):
                continue
        elif msg.startswith("quiz "):
            cat = user[5:].strip()
            if start_quiz(quiz, cat):
                continue
        elif msg == "score":
            show_score(quiz, name)
        elif msg == "reset score":
            reset_score(quiz)

        # help
        elif msg == "help":
            show_help()

        # compliment / joke / fact
        elif msg == "compliment":
            turn = handle_compliment(turn, name)

        elif msg == "joke":
            print("🤖 PyBot: Why don’t programmers like nature? It has too many bugs! 🐛😂")

        elif msg == "fact":
            last_fact = handle_fact(last_fact)

        # riddle (with retry + skip)
        elif msg == "riddle":
            print("🤖 PyBot: I speak without a mouth and hear without ears. What am I?")
            while True:
                guess = input(f"{name}: ").strip().lower()
                if not guess:
                    print("🤖 PyBot: Give it a shot, or type 'skip'.")
                    continue
                if "echo" in guess:
                    print("🤖 PyBot: Exactly! You got it right 👏")
                    break
                if guess in ("skip", "idk", "i don't know"):
                    print("🤖 PyBot: It’s an echo! 😄")
                    break
                print("🤖 PyBot: Close! Try again, or 'skip'.")

        # repeat mode
        elif msg == "repeat after me":
            print("🤖 PyBot: Okay, I’ll repeat your next line 👂")
            repeat_mode = True

        # text utilities
        elif msg.startswith("reverse "):
            payload = user[8:]
            print(payload[::-1] if payload else "🤖 PyBot: Usage: reverse <text>")

        elif msg.startswith("upper "):
            payload = user[6:]
            print(payload.upper() if payload else "🤖 PyBot: Usage: upper <text>")

        elif msg.startswith("lower "):
            payload = user[6:]
            print(payload.lower() if payload else "🤖 PyBot: Usage: lower <text>")

        elif msg.startswith("count "):
            payload = user[6:]
            if not payload:
                print("🤖 PyBot: Usage: count <text>")
            else:
                words = payload.split()
                print(f"Words: {len(words)}, Characters: {len(payload)}")

        elif msg.startswith("pal "):
            payload = user[4:]
            if not payload:
                print("🤖 PyBot: Usage: pal <text>")
            else:
                stripped = "".join(ch.lower() for ch in payload if ch != " ")
                print("Palindrome ✅" if stripped == stripped[::-1] else "Not a palindrome ❌")

        # tiny arithmetic
        elif msg.split()[0] in ("add", "sub", "mul", "div"):
            small_math(msg.split())

        # default
        else:
            print(f"🤖 PyBot: I didn't understand that, {name}. Type 'help' to see what I can do.")

# Run
if __name__ == "__main__":
    chatbot()
