"""
Wordle CLI
A terminal-based word guessing game built with Python fundamentals.
Demonstrates: LO1 (Data Structures), LO2 (Collections), LO3 (Control Flow),
LO4 (Defensive Programming), and LO5 (Process Ownership).
"""
import nltk
nltk.download('words')
from nltk.corpus import words
import random

# =====================================================================
# LO1: DATA STRUCTURE SELECTION
# Immutable Configurations (Tuples): ค่าคงที่ห้ามแก้ไขระหว่างโปรแกรมทำงาน
# =====================================================================
GAME_CONFIG = (5, 6)  # (WORD_LENGTH, MAX_ATTEMPTS)
DEFAULT_WORDS = ("APPLE", "CRANE", "TRAIN", "PLANT", "SMART", "FLASH", "BRAIN")

WORD_LIST = words.words()
FIVE_LETTER_WORDS = [w for w in WORD_LIST if len(w) == 5 and w.isalpha() and w.islower()]

# =====================================================================
# LO4: DEFENSIVE PROGRAMMING & LO5: LOGGING / DOCUMENTATION
# โครงสร้างฟังก์ชันแยกอิสระ พร้อม Docstrings และระบบตรวจสอบความถูกต้อง
# =====================================================================

def validate_input(user_input, word_length):
    """
    [LO5] Documentation: อธิบายหน้าที่ของฟังก์ชัน
    [LO4] Defensive Programming: ตรวจสอบความยาวและประเภทตัวอักษร (.isalpha())
          เพื่อป้องกัน Runtime Crash ก่อนนำไปคำนวณต่อ
    """
    if not user_input in FIVE_LETTER_WORDS:
        return False, "❌ Invalid entry! Please enter a valid 5-letter word."
    # LO2: ใช้ len() ตรวจสอบความยาวข้อมูล
    if len(user_input) != word_length or not user_input.isalpha():
        return False, f"❌ Invalid entry! Please enter exactly {word_length} letters."
    return True, None


def evaluate_guess(guess, secret):
    """
    [LO5] Documentation: บันทึกอธิบาย Two-pass algorithm ชัดเจน
    [LO1] Data Structures: ใช้ List (Mutable) กับ feedback และ secret_pool 
          เพราะต้องมีการแก้ไขค่าแบบ Dynamic ระหว่างรอบการประมวลผล
    """
    word_length = len(secret)
    feedback = ["x"] * word_length
    secret_pool = list(secret)

    # Pass 1: Exact matches
    for i in range(word_length):
        if guess[i] == secret[i]:
            feedback[i] = "✓"
            secret_pool[i] = None  # ทำเครื่องหมายว่าถูกใช้ไปแล้ว

    # Pass 2: Wrong-position matches
    for i in range(word_length):
        if feedback[i] == "✓":
            continue
        if guess[i] in secret_pool:
            feedback[i] = "-"
            secret_pool[secret_pool.index(guess[i])] = None

    return feedback


def format_feedback(feedback):
    """[LO2] Collection Manipulation: แปลง List เป็น Printable String"""
    return " ".join(feedback)


def play_single_game(FIVE_LETTER_WORDS, game_config):
    """
    [LO3] Interactive Control Flow: คุม Loop การเล่นในแต่ละรอบเกม
    [LO5] Data Logging: คืนค่า Dictionary รวมประวัติผลลัพธ์ของเกมนั้นๆ
    """
    word_length, max_attempts = game_config
    secret_word = random.choice(FIVE_LETTER_WORDS).upper()
    attempts = 0
    game_won = False
    
    # LO1: ใช้ Dynamic List สำหรับเก็บคำที่ผู้เล่นเดาเฉพาะเกมนี้
    guesses_this_game = []

    print(f"\n--- NEW GAME: Guess the {word_length}-letter word ({max_attempts} attempts) ---")

    # LO3: Control Flow ใช้ while loop ควบคุมรอบการเล่น
    while attempts < max_attempts and not game_won:
        user_input = input(f"Attempt {attempts + 1}/{max_attempts}: ").upper().strip()

        # LO4: Defensive check เรียกใช้ validation ก่อนดำเนินการ
        is_valid, error_message = validate_input(user_input, word_length)
        if not is_valid:
            print(error_message)
            continue

        attempts += 1
        feedback = evaluate_guess(user_input, secret_word)
        
        # LO2: ใช้ .append() เพิ่มข้อมูลคำเดาเข้า Collection
        guesses_this_game.append({"word": user_input, "feedback": feedback})
        print("Feedback: " + format_feedback(feedback))

        if user_input == secret_word:
            print(f"🎉 You guessed '{secret_word}' in {attempts} attempt(s)!")
            game_won = True

    if not game_won:
        print(f"❌ Out of attempts! The secret word was: {secret_word}")

    # LO1 & LO5: เก็บผลลัพธ์แบบ Dictionary และส่งกลับเพื่อนำไปบันทึกสถิติ
    return {
        "secret_word": secret_word,
        "guesses": guesses_this_game,
        "won": game_won,
        "attempts_used": attempts,
    }


# =====================================================================
# FEATURE FUNCTIONS (LO2, LO4, LO5)
# =====================================================================

def display_statistics(guess_history):
    """
    [LO4] Defensive Programming: เช็คความว่างเปล่าของข้อมูลก่อนคำนวณ
    [LO2] Collection Manipulation: ใช้ len(), sum(), reversed() สกัดข้อมูลสถิติ
    """
    # LO4: ตรวจสอบข้อมูลเพื่อป้องกัน ZeroDivisionError หรือ Index Errors
    if not guess_history:
        print("\nℹ️ No stats available yet. Play a game first!")
        return

    # LO2: ประมวลผลเซตข้อมูลด้วย len() และ List Comprehensions
    total_games = len(guess_history)
    wins = sum(1 for g in guess_history if g["won"])
    win_rate = (wins / total_games) * 100

    # LO2: วนลูปย้อนกลับจากข้อมูลล่าสุดเพื่อหา Streak ชัยชนะ
    current_streak = 0
    for g in reversed(guess_history):
        if g["won"]:
            current_streak += 1
        else:
            break

    print("\n=======================================")
    print("           PLAYER STATISTICS           ")
    print("=======================================")
    print(f"Games Played:    {total_games}")
    print(f"Win Rate:        {win_rate:.1f}%")
    print(f"Current Streak:  {current_streak}")
    
    print("\nGuess Distribution:")
    max_attempts = GAME_CONFIG[1]
    for attempt in range(1, max_attempts + 1):
        count = sum(1 for g in guess_history if g["won"] and g["attempts_used"] == attempt)
        bar = "█" * count
        print(f"  {attempt}: {bar} ({count})")


def display_how_to_play():
    """[LO5] Documentation: แสดงคู่มือการเล่นและอธิบายสัญลักษณ์"""
    word_length, max_attempts = GAME_CONFIG
    print("\n=======================================")
    print("             HOW TO PLAY               ")
    print("=======================================")
    print(f"1. Guess the secret word in {max_attempts} tries.")
    print(f"2. Each guess must be a valid {word_length}-letter word.")
    print("3. Feedback icons show how close your guess was:\n")
    print("   [ ✓ ] Correct letter in the correct spot.")
    print("   [ - ] Letter is in the word, but in wrong spot.")
    print("   [ x ] Letter is NOT in the word.")


# =====================================================================
# LO3: MAIN INTERACTIVE MENU LOOP
# =====================================================================

def run_wordle_cli():
    # LO1 & LO5: guess_history เป็น List of Dicts สะสมประวัติการเล่นทั้งหมดใน Runtime
    guess_history = []

    print("=======================================")
    print("        WELCOME TO CLI WORDLE          ")
    print("=======================================")

    # LO3: Interactive Menu Loop หลักที่รันต่อเนื่องด้วย while True
    while True:
        print("\n--- MAIN MENU ---")
        print("1. Play Wordle")
        print("2. View Guess History")
        print("3. View Player Statistics")
        print("4. How to Play")
        print("5. Exit Game")

        choice = input("\nSelect an option (1-5): ").strip()

        # LO3: โครงสร้างทางเลือก if/elif/else สำหรับเมนูตอบโต้
        if choice == "1":
            game_result = play_single_game(FIVE_LETTER_WORDS, GAME_CONFIG)
            
            # LO2: ปรับแต่งและบันทึกประวัติด้วย .append() และ len()
            game_result["game_number"] = len(guess_history) + 1
            guess_history.append(game_result)

        elif choice == "2":
            # LO4: Defensive programming เช็คข้อมูลก่อนแสดงผล
            if not guess_history:
                print("\nℹ️ No guesses recorded yet. Play a game first!")
            else:
                # LO2: ใช้ len() และ List Comprehension ดึงคำเดาเรียงตามลำดับจริง
                print(f"\nTotal Games Played: {len(guess_history)}")
                for game in guess_history:
                    words_this_game = [g["word"] for g in game["guesses"]]
                    status = "WON" if game["won"] else "LOST"
                    print(f"\nGame {game['game_number']} ({status}, secret: {game['secret_word']})")
                    print(f"  Guesses: {' -> '.join(words_this_game)}")

        elif choice == "3":
            display_statistics(guess_history)

        elif choice == "4":
            display_how_to_play()

        elif choice == "5":
            print("\nThanks for playing Wordle CLI! Goodbye.")
            break
        else:
            # LO4: Defensive programming ดักจับคำสั่งที่ไม่ถูกต้อง (Out-of-bound choices)
            print("❌ Invalid menu choice. Please select 1, 2, 3, 4, or 5.")


if __name__ == "__main__":
    run_wordle_cli()