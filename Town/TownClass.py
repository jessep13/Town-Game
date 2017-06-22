import os
import math
import random


class Town:
    day = 0
    m_id = 0
    month = "Spring"
    year = 1

    pop = 20
    food = 0
    growth = 0
    housing = 0
    gold = 0
    tax = 0.5

    farm = 5
    homes = 4
    shop = 0
    gold_mine = 0

    income = 0
    revenue = 0
    profit = 0

    jobs = 0
    unemp = 0

    town_hall = False

    event_id = 0

    """

    Note regarding event_id

    0: No event
    1: Good Harvest (All year; +60 food; 15%)
    2: Strike Gold (Min 1 Gold Mine; +70 gold; 10%)
    3: Murder (All year; -1 pop; 5%)
    4: Food loss (Winter; -50 food; 20%)
    5: Flood (Spring & Summer; -50 food & -50 gold; 10%)

    """

    def __init__(self, name):
        self.name = name

        while True:
            self.stat_update()
            self.town_menu()

    @staticmethod
    def per_chance(p):
        r = random.randint(0, 100)
        if r <= p:
            return True
        else:
            return False

    def stat_update(self):
        # Time update
        self.day += 1
        if self.day is 31:
            self.day = 1
            self.m_id += 1

            if self.m_id is 0:
                self.month = "Spring"
            elif self.m_id is 1:
                self.month = "Summer"
            elif self.m_id is 2:
                self.month = "Fall"
            elif self.m_id is 3:
                self.month = "Winter"
            else:
                self.m_id = 0
                self.month = "Spring"
                self.year += 1

        # Stat update
        if self.m_id is 1:
            self.growth = math.floor(10 * (self.farm * 6 * 2 * (1 - self.tax) - self.pop)) / 10
        elif self.m_id is 3:
            self.growth = math.floor(10 * (self.farm * 2 * 2 * (1 - self.tax) - self.pop)) / 10
        else:
            self.growth = math.floor(10 * (self.farm * 4 * 2 * (1 - self.tax) - self.pop)) / 10

        self.income = int(self.pop * self.tax) + self.shop + self.gold_mine * 3
        self.revenue = self.farm
        self.profit = self.income - self.revenue

        self.jobs = self.farm * 3 + self.shop * 4 + self.gold_mine * 2
        self.unemp = self.pop - self.jobs

        self.food = math.floor(10 * (self.food + self.growth)) / 10
        self.gold += self.profit

        self.housing = self.homes * 5

        # Pop growth/decay
        if self.growth > 0 and self.housing > self.pop and self.unemp < 0 and self.food >= 10:
            if self.per_chance(60) is True:
                self.pop += 1
                self.food -= 10
        elif self.food < 0 and self.pop > 0:
            self.pop -= 1
            self.food = 0
        elif self.unemp > 0 and self.pop > 0:
            if self.per_chance(75) is True: self.pop -= 1

        # Event
        if self.m_id is 0 and self.year is 1:
            self.event_id = 0
        else:
            if self.per_chance(15) is True:
                self.event_id = 1
                self.food += 60
            elif self.per_chance(10) is True:
                self.event_id = 2
                self.gold += 70
            elif self.per_chance(5) is True and self.gold_mine >= 1:
                self.event_id = 3
                self.pop -= 1
            elif self.per_chance(20) is True and self.m_id is 3:
                self.event_id = 4
                self.food -= 50
            elif self.per_chance(10) is True and (self.m_id is 0 or self.m_id is 1):
                self.event_id = 5
                self.food -= 50
                self.gold -= 50

    def town_menu(self):
        while True:
            os.system("cls")

            # Semi Stat Update
            if self.m_id is 1:
                growth = math.floor(10 * (self.farm * 6 * 2 * (1 - self.tax) - self.pop)) / 10
            elif self.m_id is 3:
                self.growth = math.floor(10 * (self.farm * 2 * 2 * (1 - self.tax) - self.pop)) / 10
            else:
                self.growth = math.floor(10 * (self.farm * 4 * 2 * (1 - self.tax) - self.pop)) / 10

            self.income = int(self.pop * self.tax) + self.shop + self.gold_mine * 3
            self.revenue = self.farm
            self.profit = self.income - self.revenue

            self.jobs = self.farm * 3 + self.shop * 4 + self.gold_mine * 2
            self.unemp = self.pop - self.jobs

            self.housing = self.homes * 5

            # Stat print
            print(self.name, ": Day", self.day, self.month, "Year", self.year)
            print("\n-- TOWN STATS --\n")
            print("Population:", self.pop, "/", self.housing)
            print("Food:", self.food, "(", self.growth, ")")
            print("Gold:", self.gold, "(", self.profit, ")")
            print("Jobs:", self.jobs)
            print("\n-- NOTICES/ALERTS --\n")

            # Alerts
            if self.growth < 0: print("* You're town is losing food. People will start dying if food runs out. "
                                 "Build more farms to produce more food.")
            if self.housing is self.pop: print("* You're town is running out of room for new citizens. "
                                     "Build more houses to increase population cap.")
            if self.unemp > 0: print("*  Some people don't have jobs. People will leave if there aren't any jobs. "
                                "Make more jobs to decrease unemployment")
            if self.profit < 0: print("* You are losing money. Tax more people, or build money producing buildings.")
            if self.growth is 0: print("* Food production is stagnate. Your population won't grow nor decay. "
                                  "Make food to grow, and to avoid decay.")
            if self.unemp is 0: print("* There aren't any extra jobs for people. "
                                 "Population won't grow until there are extra jobs available.")
            print("\n-- EVENT --\n")

            # Event print
            if self.event_id is 0:
                print("Nothing has happened today.")
            elif self.event_id is 1:
                print("Your farms had a good harvest. (+60 food)")
            elif self.event_id is 2:
                print("Your miners have struck gold! (+70 gold)")
            elif self.event_id is 3:
                print("Someone got murdered last night. (-1 pop)")
            elif self.event_id is 4:
                print("Your food suplies got spoiled in the cold. (-50 food)")
            elif self.event_id is 5:
                print("The town got flooded. (-50 food and gold)")

            print("\n----------------\n")

            # Input handle
            if self.town_hall is False:
                print("1: Next Day\n2: Build\n3: Buildings\nE: Exit Game")
            else:
                print("1: Next Day\n2: Build\n3: Buildings\n4: Town Management\nE: Exit Game")

            i = input("> ")

            if i is "1":
                break
            elif i is "E":
                exit()
            elif i is "2":
                self.build()
            elif i is "3":
                os.system("cls")
                print("Farms:", self.farm)
                print("Houses:", self.homes)
                print("Shops:", self.shop)
                print("Gold Mines:", self.gold_mine)
                input("PRESS ENTER TO GO BACK")
            elif i is "4" and self.town_hall is True:
                self.town_management()

    def build(self):
        os.system("cls")
        print("What would you like to build?")
        print("1: Farm (5G)\n2: House (10G)\n3: Shop (15G)\n4: Gold Mine (20G)\n"
              "5: Town Hall (100G)\n0: Exit Build Menu")

        i = int(input("> "))
        if i is 1 and self.gold >= 5:
            self.farm += 1
            self.gold -= 5
        elif i is 2 and self.gold >= 10:
            self.homes += 1
            self.gold -= 10
        elif i is 3 and self.gold >= 15:
            self.shop += 1
            self.gold -= 15
        elif i is 4 and self.gold >= 20:
            self.gold_mine += 1
            self.gold -= 20
        elif i is 5 and self.gold >= 100:
            self.gold -= 100
            self.town_hall = True

    def town_management(self):
        os.system("cls")
        print("1: Tax Rates\n2: Trade\n0: Exit Menu")

        i = int(input("> "))

        if i is 1:
            print("Enter the tax rate as a integer %")
            print("Current tax rate:", self.tax*100, "%")
            print("NOTE: Lower Tax = More Food; Higher Tax = Less Food")
            tax = float(int(input("> "))) / 100
        elif i is 2:
            print("What item will you trade for (F=Food, G=Gold)")
            i = input("> ")

            if i is "F":
                print("You can trade 2 gold for 1 food. Enter how much food you want. "
                      "Make sure you have enough to perform the transaction")
                i = int(input("> "))
                if self.gold >= i:
                    self.gold -= 2 * i
                    self.food += i
            if i is "G":
                print("You can trade 2 food for 1 gold. Enter how much gold you want. "
                      "Make sure you have enough to perform the transaction")
                i = int(input("> "))
                if self.food >= i:
                    self.food -= 2 * i
                    self.gold += i