import random

import db
from db import *


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


def getRandomCard(deck_of_cards):
    dealtCard = random.choice(deck_of_cards)
    deck_of_cards.pop(deck_of_cards.index(dealtCard))
    return dealtCard, deck_of_cards


def getBetAmount():
    money = db.show_players_money()
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


def updatePlayersMoney(updateAmount):
    playerMoney = show_players_money()
    playerMoney += updateAmount
    update_money(playerMoney)


def checkIfBlackjack(hand):
    if len(hand) > 2:
        return False
    if "Ace" in hand[0] or "Ace" in hand[1]:
        if getValueOfHand(hand) == 21:
            return True
    return False


def main():
    print("Let's Play BLACKJACK!")
    print("Blackjack payout is 3:2")
    print()

    while True:
        deck = getDeckOfCards()
        dealerHand = []
        playerHand = []

        playersMoney = db.show_players_money()
        print(f"You have ${playersMoney} in your pot")

        betAmount = getBetAmount()
        updateAmount = -1 * betAmount

        card, deck = getRandomCard(deck)
        dealerHand.append(card)
        card, deck = getRandomCard(deck)
        dealerHand.append(card)

        print("DEALER'S SHOW CARD: ")
        print(f"{dealerHand[0][1]} of {dealerHand[0][0]}")
        print()

        if checkIfBlackjack(dealerHand) == True:
            print("Dealer has Blackjack!")
            updatePlayersMoney(updateAmount)
            again = input("Play again? (y/n)")
            if again.lower() != "y":
                break
            else:
                continue

        card, deck = getRandomCard(deck)
        playerHand.append(card)
        card, deck = getRandomCard(deck)
        playerHand.append(card)
        print("YOUR CARDS:")
        print(f"{playerHand[0][1]} of {playerHand[0][0]}")
        print(f"{playerHand[1][1]} of {playerHand[1][0]}")
        print()

        if checkIfBlackjack(playerHand) == True:
            print("Blackjack! You won!")
            updateAmount = betAmount * 1.5
            updatePlayersMoney(updateAmount)

            again = input("Play again? (y/n)")
            if again.lower() != "y":
                break
            else:
                continue

        while getValueOfHand(playerHand) <= 21:
            playerChoice = input("Would you like to hit or stand: ").lower()
            print()
            if playerChoice == "hit":
                card, deck = getRandomCard(deck)
                playerHand.append(card)
                print("YOUR CARDS:")
                for card in playerHand:
                    print(f"{card[1]} of {card[0]}")
                print()
            elif playerChoice == "stand":
                break

        if getValueOfHand(playerHand) > 21:
            print("You bust")
            print()
            updatePlayersMoney(updateAmount)

            again = input("Play again? (y/n)")
            if again.lower() != "y":
                break
            else:
                continue

        while getValueOfHand(dealerHand) < getValueOfHand(playerHand) and getValueOfHand(dealerHand) < 17:
            card, deck = getRandomCard(deck)
            dealerHand.append(card)
            print("Dealer's Cards:")
            for card in dealerHand:
                print(f"{card[1]} of {card[0]}")
            print()
        if getValueOfHand(dealerHand) > 21:
            print("Dealer busts. You Win!")
            print()
            updateAmount = betAmount
            updatePlayersMoney(updateAmount)

            again = input("Play again? (y/n)")
            if again.lower() != "y":
                break
            else:
                continue

        if getValueOfHand(playerHand) == getValueOfHand(dealerHand):
            print("Push")
            print()
            updateAmount = 0
        elif getValueOfHand(playerHand) > getValueOfHand(dealerHand):
            print("You Win")
            print()
            updateAmount = betAmount
        elif getValueOfHand(dealerHand) > getValueOfHand(playerHand):
            print("Dealer Wins")
            print()

        updatePlayersMoney(updateAmount)

        again = input("Play again? (y/n)")
        if again.lower() != "y":
            break

    print("Thanks for playing")


if __name__ == "__main__":
    main()
