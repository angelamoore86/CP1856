import sys


def show_players_money():
    try:
        with open("money.txt") as file:
            money = file.read()
    except FileNotFoundError as e:
        print("Fine not found containing marks, Starting from scratch")
    except Exception as e:
        print("Unknown Exception, Closing Program")
        print(type(e), e)
        sys.exit(1)
    return float(money)


def update_money(money):
    try:
        with open("money.txt", "w") as file:
            file.write(str(money))
    except Exception as e:
        print("Unknown Exception, Closing Program")
        print(type(e), e)
        sys.exit(1)


def main():

    players_pot = 100
    update_money(players_pot)
    bet_amount = int(input("Enter a bet amount: "))
    money = players_pot - bet_amount
    update_money(money)
    print(money)
    # update_money(money)
    # print(show_players_money(filename))
    print()
    show_players_money()






if __name__ == "__main__":
    main()