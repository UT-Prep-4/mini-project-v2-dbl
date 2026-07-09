
# Word bank
words = ["Mermaid" , "Coach Spoddick" , "Unnicorn" , "Ocean" , "Hippopotomonstrosesquipedaliophobia"]
# Pick a random word
word = random.choice(words)

guessed = ""
lives = 4

print("Welcome to Hangman!")

while lives > 0:
    display = ""

    for letter in word:
        if letter in guessed:
            display = display + "_"

print("/nWord:" , display)
if display  == word:
    print("You won!")
    break

guess = input("Guess a letter: ")



if lives == 0:
    print("/nGame Over!")
    print("The word was:" , word) 
elif guess in guessed:
    print("You already guessed that letter.")
elif guess in word:
    print("Correct!")
    guessed = guessed + guess
else:
    print("Wrong! HAHA")
    lives = lives - 1
    guessed = guessed + guess
    print("Lives left:" , lives)
       
