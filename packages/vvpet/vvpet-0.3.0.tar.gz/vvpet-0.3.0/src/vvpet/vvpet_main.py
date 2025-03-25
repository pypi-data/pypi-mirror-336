from time import sleep
from random import randint, choice
from vvpet_color import color

def game():
    #Main class for keeping petstats in check
    class VvPet:
        def __init__(self, name, type, color):
            self.name = name
            self.type = type
            self.color = color

            self.health = 10
            self.hunger = 10
            self.thirst = 10
            self.fun = 10

            self.mood = "Perfect"

    #For food used in shop
    class Food:
        def __init__(self, name, price, hunger, thirst, fun):
            self.name = name
            self.price = price
            self.hunger = hunger
            self.thirst = thirst
            self.fun = fun

    #INIT
    print("Hi, come get your pet")
    input_type = input("What type of pet do you want? ")
    input_name = input("What will be the name of your pet? ")
    input_color = int(input(f"""What color will your pet be?
1. {color.PINK}PINK{color.END}
2. {color.BLUE}BLUE{color.END}
3. {color.CYAN}CYAN{color.END}
4. {color.GREEN}GREEN{color.END}
5. {color.YELLOW}YELLOW{color.END}
6. {color.RED}RED{color.END}
"""))
    colors = [color.PINK, color.BLUE, color.CYAN, color.GREEN, color.YELLOW, color.RED]
    print(f"Great, your pet will be a {input_type} named {colors[input_color-1]}{input_name}{color.END}")

    pet = VvPet(input_name, input_type, colors[input_color-1])
    money = 100


    def pet_stats():
        print(f"""
    {pet.color}{pet.name}{color.END} has the current stats:
    Health = {pet.health}
    
    Hunger = {pet.hunger}
    Thirst = {pet.thirst}
    Entertainment = {pet.fun}
    """)


    def show_pet():
        typ = pet.type
        if typ == "smile":
            #vvpet_draw.smile()
            pass


    def tick():
        pet.hunger -= randint(1,3)
        pet.thirst -= randint(1,3)
        pet.fun -= randint(1,3)
        check_max()
        mood()


    apple = Food("Apple", 10, 2, 1, 1)
    cake = Food("Cake", 25, 5, 0, 5)
    juice = Food("Juice Packet", 10, 0, 3, 2)
    steak = Food("Steak", 45, 7, 3, 2)

    shop_list = [apple, cake, juice, steak]
    inventory = []

    def inventory_show():
        if len(inventory) > 0:
            print("Your inventory contains:")
            si = 0
            for i in inventory:
                print(f"{si+1}, {i.name}, providing {i.hunger} hunger, {i.thirst} thirst and {i.fun} entertainment")
                si += 1
        else:
            print("Your inventory is empty")


    def shop(money):
        print(f"{color.GREEN}Welcome to the shop, we have:{color.END}")
        shopping = True
        while shopping:
            si = 0
            for i in shop_list:
                print(f"{color.GREEN}{si+1}{color.END}. {i.name} for {color.YELLOW}{i.price} crowns{color.END}, providing {color.RED}{i.hunger} hunger{color.END}, {color.CYAN}{i.thirst} thirst{color.END} and {color.PINK}{i.fun} entertainment{color.END}")
                si += 1
            purchase = input("What do you wanna purchase? (type 'exit' to exit) [number] ")
            if purchase == "exit":
                return money
            else:
                purchase = int(purchase)

            if money >= shop_list[purchase-1].price:
                money -= shop_list[purchase-1].price
                inventory.append(shop_list[purchase-1])
                print(f"You purchased {shop_list[purchase-1].name}")

            else:
                print("You dont have enough crowns for this")

        return money


    def check_max():
        if pet.hunger > 10:
            pet.hunger = 10
        if pet.thirst > 10:
            pet.thirst = 10
        if pet.fun > 10:
            pet.fun = 10

        if pet.hunger <= 0:
            pet.health -= 1
        if pet.thirst <= 0:
            pet.health -= 1
        if pet.fun <= 0:
            pet.hunger -= 1
            pet.thirst -= 1


    def mood():
        sum_stats = pet.health + pet.thirst + pet.fun + pet.hunger

        if sum_stats > 30:
            pet.mood = "Perfect"
        elif sum_stats > 20 and sum_stats <= 30:
            pet.mood = "Good"
        elif sum_stats <= 20 and sum_stats > 10:
            pet.mood = "Meh"
        elif sum_stats <= 10 and sum_stats > 4:
            pet.mood = "Bad"
        else:
            pet.mood = "Terrible"


    def feed():
        if len(inventory) > 0:
            inventory_show()
        else:
            print(f"You have nothing to feed {pet.color}{pet.name}{color.END}")
        feed_num = int(input(f"What do you wanna feed to {pet.color}{pet.name}{color.END}? [number] "))
        pet.hunger += inventory[feed_num-1].hunger
        pet.thirst += inventory[feed_num-1].thirst
        pet.fun += inventory[feed_num-1].fun
        check_max()


    def pet_pet():
        pet.fun += 5
        print(f"{pet.color}{pet.name}{color.END} liked that very much")
        check_max()


    def work(money):
        print("Going into work")
        sleep(0.5)
        print("Working..")
        sleep(0.5)
        randcash = randint(10,20)
        print(f"You earned {randcash} crowns!")
        money += randcash
        return money


    def casino(casmoney):

        def roulette():
            bet = int(input(f"How much do you want to {color.YELLOW}bet{color.END}? "))
            if bet > casmoney:
                print(f"{color.RED}You dont have enough money{color.END}")
                return casmoney

            bet_chc = input("Bet on number or color? ")
            roul_num = randint(1, 20)
            roul_col = choice(["black", "red"])
            if bet_chc == "number":
                bet_num = input("Place your bet [1-20] ")
                print(f"{color.PINK}L{color.END}{color.RED}e{color.END}{color.BLUE}t{color.END}{color.CYAN}s {color.END}{color.GREEN}r{color.END}{color.YELLOW}o{color.END}{color.PINK}l{color.END}{color.RED}l{color.END}{color.CYAN}!{color.END}")
                for i in range(4):
                    sleep(1)
                    dot = "."
                    print(dot * (i + 1))
                if bet_num == roul_num:
                    print(f"{color.YELLOW}You won {bet * 4} crowns!{color.END}")
                    return (casmoney - bet) + (bet * 4)
                else:
                    print(f"{color.RED}You lost.{color.END} Better luck next time!")
                    return casmoney - bet

            elif bet_chc == "color":
                bet_col = input("Place your bet [black/red] ")
                print(f"{color.PINK}L{color.END}{color.RED}e{color.END}{color.BLUE}t{color.END}{color.CYAN}s {color.END}{color.GREEN}r{color.END}{color.YELLOW}o{color.END}{color.PINK}l{color.END}{color.RED}l{color.END}{color.CYAN}!{color.END}")
                for i in range(4):
                    sleep(1)
                    dot = "."
                    print(dot * (i + 1))
                if bet_col == roul_col:
                    print(f"{color.YELLOW}You won {bet * 2} crowns!{color.END}")
                    return (casmoney - bet) + (bet * 2)
                else:
                    print(f"{color.RED}You lost.{color.END} Better luck next time!")
                    return casmoney - bet

        bj_cards = [2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,6,7,7,7,7,8,8,8,8,9,9,9,9,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,"ACE","ACE","ACE","ACE"]

        def bj():
            bet = int(input(f"How much do you want to {color.YELLOW}bet{color.END}? "))
            if bet > casmoney:
                print(f"{color.RED}You dont have enough money{color.END}")
                return casmoney

            print("Lets play!")
            dealer_num = 0
            player_num = 0


            def dealer_hit(hand : list):
                crd = choice(bj_cards)
                bj_cards.pop(bj_cards.index(crd))
                hand.append(crd)
                return hand

            def player_hit(hand : list):
                crd = choice(bj_cards)
                bj_cards.pop(bj_cards.index(crd))
                hand.append(crd)
                return hand

            def count(hand):
                cardsum = 0
                for i in hand:
                    if i != "ACE":
                        cardsum += i
                    else:
                        if (cardsum + 11) > 21:
                            cardsum += 1
                        else:
                            cardsum += 11
                return cardsum

            dealer_t = dealer_hit([])
            dealer_t = dealer_hit(dealer_t)
            player_t = player_hit([])
            playing = True
            dealer_done = False
            while dealer_num < 21 or player_num < 21:
                if playing:

                    player_t = player_hit(player_t)

                dealer_num = count(dealer_t)
                player_num = count(player_t)

                if not playing:
                    while dealer_num < 17:
                        dealer_t = dealer_hit(dealer_t)
                        dealer_num = count(dealer_t)
                        print(f"""
                {color.RED}DEALER{color.END}
                {dealer_t}  {color.GREEN}sum = {dealer_num}{color.END}
                ---------
                {player_t}  {color.GREEN}sum = {player_num}{color.END}
                {pet.color}PLAYER{color.END}
                """)
                    dealer_done = True

                print(f"""
                {color.RED}DEALER{color.END}
                {dealer_t}  {color.GREEN}sum = {dealer_num}{color.END}
                ---------
                {player_t}  {color.GREEN}sum = {player_num}{color.END}
                {pet.color}PLAYER{color.END}
                """)


                if player_num == 21 or dealer_num > 21:
                    print(f"{color.YELLOW}You won!! Your balance increases by {bet * 2}!{color.END}")
                    return (casmoney - bet) + (bet * 2)
                if player_num > 21:
                    print(f"{color.RED}Sorry, you lost.{color.END}")
                    return (casmoney - bet)
                if dealer_done:
                    if (21 - dealer_num) < (21 - player_num):
                        print(f"{color.RED}Sorry, you lost.{color.END}")
                        return (casmoney - bet)
                    else:
                        print(f"{color.YELLOW}You won!! Your balance increases by {bet * 2}!{color.END}")
                        return (casmoney - bet) + (bet * 2)


                if playing:
                    cont = input(f"Do you want to {color.GREEN}hit{color.END} or {color.RED}pass{color.END}? ")
                    if cont == "hit":
                        continue
                    elif cont == "pass":
                        playing = False


        chc = int(input(f"""
Welcome to the {color.YELLOW}casino{color.END}!
What game do you want to play? 
    {color.BLUE}1. Roulette{color.END}
    {color.CYAN}2. Blackjack{color.END}
        """))
        if chc == 1:
            casmoney = roulette()
            return casmoney
        elif chc == 2:
            casmoney = bj()
            return casmoney

    play = True
    while play:
        action = input("What will be your next action? Type 'help' for help ")
        action = action.lower()
        if action == "end" or action == "exit":
            play = False
        elif action == "help":
            print(f"""
            {color.BLUE}UTILITY{color.END}
            stats = show pet stats
            balance = see your crowns balance
            inventory = see your inventory
            mood = show the mood of your pet
            
            {color.CYAN}ACTIONS{color.END}
            shop = buy food for your pet
            feed = feed your pet
            pet = pet your pet
            work = go make some money
            casino / gamble = go make money in a different way
            
            end = end the game
            """)
        elif action == "admin.tick":
            tick()
        elif action == "stats":
            pet_stats()
        elif action == "show":
            show_pet()
        elif action == "balance":
            print(f"You have {color.YELLOW}{money} crowns{color.END}")
        elif action == "shop":
            money = shop(money)
        elif action == "inventory":
            inventory_show()
        elif action == "feed":
            feed()
            mood()
        elif action == "mood":
            print(f"{pet.color}{pet.name}{color.END} is doing {pet.mood}")
        elif action == "pet":
            pet_pet()
        elif action == "work":
            money = work(money)
            tick()
        elif action == "gamble" or action == "casino":
            money = casino(money)
            tick()

if __name__ == "__main__":
    game()