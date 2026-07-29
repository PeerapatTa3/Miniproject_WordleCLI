"""
Wordle CLI
A terminal-based word guessing game built with Python fundamentals.
Demonstrates: LO1 (Data Structures), LO2 (Collections), LO3 (Control Flow),
LO4 (Defensive Programming), and LO5 (Process Ownership).
"""

import random

# =====================================================================
# LO1: DATA STRUCTURE SELECTION
# Immutable Configurations (Tuples): Constants that must remain static
# =====================================================================
GAME_CONFIG = (5, 6)  # (WORD_LENGTH, MAX_ATTEMPTS)
DEFAULT_WORDS = ("APPLE", "CRANE", "TRAIN", "PLANT", "SMART", "FLASH", "BRAIN")


def run_wordle_cli():
    # Dynamic Collections (Lists): State mutable across rounds
    word_pool = list(DEFAULT_WORDS)
    guess_history = []

    print("=======================================")
    print("      WELCOME TO CLI WORDLE          ")
    print("=======================================")

    # =====================================================================
    # LO3: INTERACTIVE CONTROL FLOW
    # Continuous menu-driven loop using while and multi-way conditionals
    # =====================================================================
    while True:
        print("\n--- MAIN MENU ---")
        print("1. Play Wordle")
        print("2. View & Sort Guess History")
        print("3. Remove a Word from Active Pool")
        print("4. Exit Game")

        choice = input("\nSelect an option (1-4): ").strip()

        if choice == "1":
            # Auto-reset word pool if depleted
            if len(word_pool) == 0:
                print(
                    "⚠️ Word pool is empty! Auto-resetting from default configuration..."
                )
                word_pool = list(DEFAULT_WORDS)

            secret_word = random.choice(word_pool)
            word_length, max_attempts = GAME_CONFIG
            attempts = 0
            game_won = False

            print(
                f"\n--- NEW GAME: Guess the {word_length}-letter word ({max_attempts} attempts) ---"
            )

            while attempts < max_attempts and not game_won:
                user_input = (
                    input(f"Attempt {attempts + 1}/{max_attempts}: ")
                    .upper()
                    .strip()
                )

                # =========================================================
                # LO4: DEFENSIVE PROGRAMMING
                # Validate length and type BEFORE mutating game state
                # =========================================================
                if (
                    len(user_input) != word_length
                    or not user_input.isalpha()
                ):
                    print(
                        f"❌ Invalid entry! Please enter exactly {word_length} letters."
                    )
                    continue

                # =========================================================
                # LO2: COLLECTION MANIPULATION (.append)
                # Store user attempt into history list
                # =========================================================
                guess_history.append(user_input)
                attempts += 1

                # Feedback calculation: ✓ = Correct position, - = Wrong position, x = Absent
                feedback = []
                for i in range(word_length):
                    if user_input[i] == secret_word[i]:
                        feedback.append("✓")
                    elif user_input[i] in secret_word:
                        feedback.append("-")
                    else:
                        feedback.append("x")

                print("Feedback: " + " ".join(feedback))

                if user_input == secret_word:
                    print(
                        f"🎉 You guessed '{secret_word}' in {attempts} attempt(s)!"
                    )
                    game_won = True

            if not game_won:
                print(f"❌ Out of attempts! The secret word was: {secret_word}")

        elif choice == "2":
            # =========================================================
            # LO2 & LO4: COLLECTION MANIPULATION (len, .sort) & GUARDING
            # =========================================================
            if len(guess_history) == 0:
                print("\nℹ️ No guesses recorded yet. Play a game first!")
            else:
                print(
                    f"\nTotal Guesses Recorded across games: {len(guess_history)}"
                )
                print(f"Original Order: {guess_history}")

                # In-place alphabetical sort
                guess_history.sort()
                print(f"Sorted Order:   {guess_history}")

        elif choice == "3":
            # =========================================================
            # LO4: DEFENSIVE PROGRAMMING & LO2 (.remove)
            # Proactively check membership BEFORE calling .remove()
            # =========================================================
            print(f"\nCurrent Active Pool ({len(word_pool)} words): {word_pool}")
            target_word = (
                input("Enter word to remove from active pool: ")
                .upper()
                .strip()
            )

            if target_word in word_pool:
                word_pool.remove(target_word)
                print(
                    f"✅ '{target_word}' removed. Pool size is now {len(word_pool)}."
                )
            else:
                print(
                    f"❌ Error: '{target_word}' was not found in active pool. No runtime crash occurred."
                )

            # Auto-reset if pool drops to zero
            if len(word_pool) == 0:
                print(
                    "⚠️ Pool is now empty! Auto-resetting from default configuration..."
                )
                word_pool = list(DEFAULT_WORDS)

        elif choice == "4":
            print("\nThanks for playing Wordle CLI! Goodbye.")
            break
        else:
            print("❌ Invalid menu choice. Please select 1, 2, 3, or 4.")


if __name__ == "__main__":
    run_wordle_cli()