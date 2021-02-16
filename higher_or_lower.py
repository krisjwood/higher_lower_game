# Higher or Lower - a number guessing game
# CaineCode 2021

from random import randint
import site
import datetime
import pytz
import sqlite3 as sql

def intro():
    '''Introduction'''
    print("###########################")
    print("Welcome to Higher or Lower\nThe number guessing game")
    print("###########################")
    print("\nRULES:")
    print("1. Pick your level\n2. Guess the number before you run out of chances")
    print("3. Try beat the champion or get on the leaderboard")
    print("4. Pick a level:\nLevel 1 (Easy) - 30 chances\nLevel 2 (Medium) - 20 chances\nLevel 3 (Hard) - 10 chances")

    datetime_object = datetime.datetime.now()
    timezone = pytz.timezone("Pacific/Auckland")
    d_aware = timezone.localize(datetime_object)
    datetime_stamp = d_aware.strftime('%a %d/%m/%Y %H:%M (%z %Z)')
    print(f"Date and time: {datetime_stamp}")

    return datetime_stamp

def chances():
    '''Establish what level the player wants to play and define chances'''

    game = False
    while game == False:
        # Ask user for level
        game_level = input("\nWhat level do you want to play? ")    
        # Validate input as interger
        try:
            game_level = int(game_level)
        except:
            print("Only intergers allowed")
        else:
            # Validate level
            if game_level >= 1 and game_level <= 3:
                # Define chances based on choosen level
                if game_level == 3:
                    chances = 10
                elif game_level == 2:
                    chances = 20
                else:
                    chances = 30
                # Allow game to start
                game = True
            else:    
                print("Invalid level entry. Only 1-3 allowed.")
    
    return chances

def play_game(chances, datetime_stamp):
    '''Boot game and loop guesses until correct number is guessed or run out of chaances'''
    
    clarify = f'''You have {chances} chances to guess the random number between 1-1000'''
    print(clarify)
    print("Lets get started!")

    # Generate random number between 1 and 1000
    random_num = randint(1,1001)
    print(random_num)

    # Adjust score based on level - Easy minus 1000, medium minus 500, hard minus zero
    score = 9999
    if chances == 30:
        score = score - 1000
    elif chances == 20:
        score = score - 500
    
    # Guess loop until chances run out
    num_guess = 1
    while num_guess <= chances:
        # Validate guess
        valid_guess = False
        while valid_guess == False:
            guess = input(f"\nGuess {num_guess} of {chances}: ")
            try:
                guess = int(guess)
            except:
                print("Invalid format.")
            else:
                if guess < 1 or guess > 1000:
                    print("Invalid guess. Between 1-1000")
                else:
                    valid_guess = True
        # Check guess against random number
        if guess == random_num:
            print(f"Correct! It took you {num_guess} guess(s). Well done!\n")
            # score = calculate_score(score, chances, num_guess)
            player = input("Player name for record (max 4 characters): ")
            player = player[:4]
            record_score(score, datetime_stamp, player)
            exit()
        elif guess < random_num:
            print("Higher")
            num_guess += 1
            if num_guess != 1:
               score = int(score - (score / 100 * 1))
        elif guess > random_num:
            print("Lower")
            num_guess += 1
            if num_guess != 1:
                score = int(score - (score / 100 * 1))
        
    print("\nGame over. You ran out of chances.")
    print(f"The correct number was {random_num}.\n")

def record_score(score, date, player):
    '''If guessed correctly the score is recorded in a text file with date and time to record performance'''
    
    # Establish connection with database and insert score into table
    conn = sql.connect('game_scores.db')
    cursor = conn.cursor()

    # Check if new score beats current champion
    current_champ = cursor.execute('SELECT * FROM higher_lower ORDER BY score DESC LIMIT 1')
    for position in current_champ:
        if position[1] < score:
            print("\nYou are the new champion!")
            print("Leaderboard:\n")
        else:
            print(f"\nYou did not beat the current champion.")
            print("Leaderboard:\n")

    # Insert new score
    cursor.execute('INSERT INTO higher_lower (score, date, player) VALUES (?, ?, ?)', (score, date, player))
    conn.commit()
    
    # Print leaderboard
    cursor = conn.cursor()
    leaderboard = cursor.execute('SELECT * FROM higher_lower ORDER BY score DESC LIMIT 10')
    for position, player in enumerate(leaderboard, start=1):
        print(position, player[1], player[3], player[2])
    print()

if __name__ == '__main__':
    datetime_stamp = intro()
    chances = chances()
    play_game(chances, datetime_stamp)