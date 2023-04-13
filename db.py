

def show_players_money():
    with open("money.txt") as file:
        money = file.read()
    return float(money)



def update_money(money):
    with open("money.txt", "w") as file:
        file.write(str(money))




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