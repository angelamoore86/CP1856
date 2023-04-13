import random

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
    #if len(hand) == 1:
    #    value = hand[2]
    for card in hand:
        value += card[2]
    return value


def getRandomCard(deck_of_cards):
    dealtCard = random.choice(deck_of_cards)
    deck_of_cards.pop(deck_of_cards.index(dealtCard))
    return dealtCard, deck_of_cards


def main():
    print("BLACKJACK!")
    print("Blackjack payout is 3:2")
    print()

    while True:
        deck = getDeckOfCards()
        dealerHand = []
        playerHand = []
        card, deck = getRandomCard(deck)
        dealerHand.append(card)
        print("DEALER'S SHOW CARD: ")
        print(f"{dealerHand[0][1]} of {dealerHand[0][0]}")
        print()
        card, deck = getRandomCard(deck)
        playerHand.append(card)
        card, deck = getRandomCard(deck)
        playerHand.append(card)
        print("YOUR CARDS:")
        print(f"{playerHand[0][1]} of {playerHand[0][0]}")
        print(f"{playerHand[1][1]} of {playerHand[1][0]}")
        print()

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

            #To Do  pay double bet
            continue

        if getValueOfHand(playerHand) == getValueOfHand(dealerHand):
            print("Push")
            print()
            #To Do return bet amount
        elif getValueOfHand(playerHand) > getValueOfHand(dealerHand):
            print("You Win")
            print()
            #To Do pay double bet
        elif getValueOfHand(dealerHand) > getValueOfHand(playerHand):
            print("Dealer Wins")
            print()

        again = ("Play again? (y/n)")
        if again.lower() != "y":
            break

if __name__ == "__main__":
    main()
