import random
number=random.randint(1,100)
print "Hi-Lo number Guessing Game: between 0 and 100 inclusive."
print

guessString=raw_input("Guess a number:")
guess=int(guessString)
while 0<=guess<=100:
	if guess>number:
		print "Guessed too High:"
	elif guess<number:
		print "Guessed too Low."
	else:
		print "You guessed it.The number was:",number
		break
	guessString=raw_input("Guess a number: ")
	guess=int(guessString)
else:
	print"you quit early,the number was:",number
