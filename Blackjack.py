import random

import db
from db import *

# Create a deck of cards with four suits and 13 cards for each suit
def getDeckOfCards():
    deckOfCards = []
    suits = ["\u2665", "\u2666", "\u2660", "\u2663"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
    for suit in suits:
        for rank in ranks:
            value = 0
            if rank in "JackQueenKing":
                value = 10
            elif rank == "Ace":
                value = 11
            else:
                value = int(rank)
            deckOfCards.append([suit, rank, value])
    return (deckOfCards)

# Get the total value of cards in a hand
def getValueOfHand(hand):
    value = 0
    aceCount = 0
    for card in hand:
        value += card[2]
        if card[2] == 11:
            aceCount += 1
    while value > 21 and aceCount > 0:
        value -= 10
        aceCount -= 1
    return value

# Get a random card from the deck of cards
def getRandomCard(deck_of_cards):
    dealtCard = random.choice(deck_of_cards)
    deck_of_cards.pop(deck_of_cards.index(dealtCard))
    return dealtCard, deck_of_cards

# Get a bet amount from the player
def getBetAmount():
    money = db.show_players_money()
    while True:
        try:
            betAmount = float(input("How much would you like to bet: "))
            if betAmount > money or betAmount < 5 or betAmount > 1000:
                raise ValueError
            if type(betAmount) not in [float, int]:
                raise TypeError
        except ValueError:
            print("Bet amount can not be greater than Player's money. Please try again")
        except TypeError:
            print("Bet amount must be an valid integer")
        else:
            return betAmount


# Update player's money
def updatePlayersMoney(updateAmount):
    playerMoney = show_players_money()
    playerMoney += updateAmount
    update_money(playerMoney)

# Check a hand of cards to see if it is Blackjack
def checkIfBlackjack(hand):
    if len(hand) > 2:
        return False
    if "Ace" in hand[0] or "Ace" in hand[1]:
        if getValueOfHand(hand) == 21:
            return True
    return False


def main():
    print()
    print("Let's Play BLACKJACK!")
    print("Blackjack payout is 3:2")
    print()

    while True:
        # get a deck of cards to start game
        deck = getDeckOfCards()

        # create a separate list to store dealer's hand and to store player's hand
        dealerHand = []
        playerHand = []

        # get player's money from text file and print amount to player
        playersMoney = db.show_players_money()
        print()
        print(f"You have ${playersMoney} in your pot")
        if playersMoney < 5:
            addMoney = input("Would you like to add money to your pot? (y/n)")
            if addMoney.lower() == "y":
                amountToAdd = float(input("Enter amount to add to pot: "))
                update_money(amountToAdd)
            else:
                break

        # Ask player how much money they would like to bet on hand
        betAmount = getBetAmount()
        updateAmount = -1 * betAmount

        # Deal two randon cards to dealer but only show face value of one card
        card, deck = getRandomCard(deck)
        dealerHand.append(card)
        card, deck = getRandomCard(deck)
        dealerHand.append(card)

        print("DEALER'S SHOW CARD: ")
        print(f"{dealerHand[0][1]} of {dealerHand[0][0]}")
        print()

        # Check if dealer's first hand has Blackjack
        if checkIfBlackjack(dealerHand) == True:
            print("Dealer's Cards:")
            for card in dealerHand:
                print(f"{card[1]} of {card[0]}")
            print(f"Total: {getValueOfHand(dealerHand)}")
            print()
            print("Dealer has Blackjack! You lose.")
            print()
            updatePlayersMoney(updateAmount)

            playersMoney = db.show_players_money()
            print(f"You now have ${playersMoney} in your pot")
            print()
            again = input("Play again? (y/n)")
            if again.lower() != "y":
                break
            else:
                continue

        # Deal two randon cards to player and show both cards
        card, deck = getRandomCard(deck)
        playerHand.append(card)
        card, deck = getRandomCard(deck)
        playerHand.append(card)
        print("YOUR CARDS:")
        print(f"{playerHand[0][1]} of {playerHand[0][0]}")
        print(f"{playerHand[1][1]} of {playerHand[1][0]}")
        print(f"Total: {getValueOfHand(playerHand)}")
        print()

        # Check if player's first hand has Blackjack
        if checkIfBlackjack(playerHand) == True:
            print("Blackjack! You won!")
            print()
            updateAmount = betAmount * 1.5
            updatePlayersMoney(updateAmount)

            playersMoney = db.show_players_money()
            print(f"You now have ${playersMoney} in your pot")
            print()
            again = input("Play again? (y/n)")
            if again.lower() != "y":
                break
            else:
                continue

        # get value of player's hand and ask if they want to hit or stay
        while getValueOfHand(playerHand) <= 21:
            playerChoice = input("Would you like to hit or stand: ").lower()
            print()
            # if player hits, deal another random card
            if playerChoice == "hit":
                card, deck = getRandomCard(deck)
                playerHand.append(card)
                print("YOUR CARDS:")
                for card in playerHand:
                    print(f"{card[1]} of {card[0]}")
                print(f"Total: {getValueOfHand(playerHand)}")
                print()
            # if player stands, end hand and go to dealer's play
            elif playerChoice == "stand":
                break

        # if player busts, go to dealer's play
        if getValueOfHand(playerHand) > 21:
            print("You bust")
            print()
            updatePlayersMoney(updateAmount)

            playersMoney = db.show_players_money()
            print(f"You now have ${playersMoney} in your pot")
            print()
            again = input("Play again? (y/n)")
            if again.lower() != "y":
                break
            else:
                continue

        # Show both cards in dealer's first hand
        print("DEALER'S TURNS OVER HIDDEN CARD\nDealer's Hand: ")
        for card in dealerHand:
            print(f"{card[1]} of {card[0]}")
        print(f"Total: {getValueOfHand(dealerHand)}")
        print()

        # Continue with dealer's play if dealer hand less than player's hand and dealer's hand less than 17
        while getValueOfHand(dealerHand) < getValueOfHand(playerHand) and getValueOfHand(dealerHand) < 17:
            card, deck = getRandomCard(deck)
            dealerHand.append(card)
            # show both dealer's card in first hand
            print("Dealer's Cards:")
            for card in dealerHand:
                print(f"{card[1]} of {card[0]}")
            print(f"Total: {getValueOfHand(dealerHand)}")
            print()

        # Dealer busts if hand is greater than 21
        if getValueOfHand(dealerHand) > 21:
            print("Dealer busts. You Win!")
            print()
            updateAmount = betAmount
            updatePlayersMoney(updateAmount)

            playersMoney = db.show_players_money()
            print(f"You now have ${playersMoney} in your pot")
            print()
            again = input("Play again? (y/n)")
            if again.lower() != "y":
                break
            else:
                continue

        # Push if both hands equal
        if getValueOfHand(playerHand) == getValueOfHand(dealerHand):
            print("Hands are tied - Push")
            print()
            updateAmount = 0
        # Player wins if player's hand is greater than dealer's hand
        elif getValueOfHand(playerHand) > getValueOfHand(dealerHand):
            print("You Win!!")
            print()
            updateAmount = betAmount
        # Dealer ins if dealer's hand is greater than player's hand
        elif getValueOfHand(dealerHand) > getValueOfHand(playerHand):
            print("Dealer Wins!")
            print()

        # save updated player's money after each round and show player's update bank
        updatePlayersMoney(updateAmount)

        playersMoney = db.show_players_money()
        print(f"You now have ${playersMoney} in your pot")
        print()

        again = input("Play again? (y/n)")
        if again.lower() != "y":
            break

    print("Thanks for playing")


if __name__ == "__main__":
    main()
