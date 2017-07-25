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

    efm = 0
    egm = 0

    farm = 5
    homes = 4
    shop = 0
    granary = 3
    gold_mine = 0
    lab = 0

    income = 0
    revenue = 0
    profit = 0

    jobs = 0
    unemp = 0

    town_hall = False

    event_id = 0

    rp = 0
    dr = False
    rt = "nothing"

    farm_lvl = 1
    gm_lvl = 1
    house_lvl = 1

    farm_rc = 20
    gm_rc = 20
    house_rc = 20

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

    @staticmethod
    def clear():
        os.system("cls")

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
            self.growth = math.floor(10 * (self.farm * 6 * 2 * (1 - self.tax) - self.pop) * self.farm_lvl) / 10
        elif self.m_id is 3:
            self.growth = math.floor(10 * (self.farm * 2 * 2 * (1 - self.tax) - self.pop) * self.farm_lvl) / 10
        else:
            self.growth = math.floor(10 * (self.farm * 4 * 2 * (1 - self.tax) - self.pop) * self.farm_lvl) / 10

        self.income = int(self.pop * self.tax) + self.shop + self.gold_mine * 3 * self.gm_lvl
        self.revenue = self.farm + self.lab * 5
        self.profit = self.income - self.revenue

        self.jobs = self.farm * 3 + self.shop * 4 + self.gold_mine * 2
        self.unemp = self.pop - self.jobs

        self.food = math.floor(10 * (self.food + self.growth)) / 10

        if self.food > self.granary * 10: self.food = self.granary * 10

        self.gold += self.profit

        self.housing = self.homes * 5 * self.house_lvl

        self.efm = 10 ** math.floor(math.log10(self.food+1))
        self.egm = 10 ** math.floor(math.log10(self.gold+1))

        self.research_points()
        self.pop_growth()
        self.events()

    def research_points(self):
        if self.dr is True:
            self.rp += self.lab * 2
            if self.rt is "farm" and self.rp >= self.farm_rc:
                self.rp -= self.farm_rc
                self.farm_lvl += 1
                self.farm_rc += 10
                self.dr = False
            elif self.rt is "gm" and self.rp >= self.gm_rc:
                self.rp -= self.gm_rc
                self.gm_lvl += 1
                self.gm_rc += 10
                self.dr = False
            elif self.rt is "house" and self.rp >= self.house_rc:
                self.rp -= self.house_rc
                self.house_lvl += 1
                self.house_rc += 10
                self.dr = False

    def pop_growth(self):
        if self.growth > 0 and self.housing > self.pop and self.unemp < 0 and self.food >= self.pop * 2:
            if self.per_chance(60) is True:
                self.pop += 1
                self.food -= 10
        elif self.food < 0 and self.pop > 0:
            self.pop -= 1
            self.food = 0
        elif self.unemp > 0 and self.pop > 0:
            if self.per_chance(75) is True: self.pop -= 1

    def events(self):
        if self.per_chance(15) is True:
            self.event_id = 1
            self.food += 60 * self.efm
        elif self.per_chance(10) is True:
            self.event_id = 2
            self.gold += 70 * self.egm
        elif self.per_chance(5) is True and self.gold_mine >= 1:
            self.event_id = 3
            self.pop -= 1
        elif self.per_chance(20) is True and self.m_id is 3:
            self.event_id = 4
            self.food -= 50 * self.efm
        elif self.per_chance(10) is True and (self.m_id is 0 or self.m_id is 1):
            self.event_id = 5
            self.food -= 50 * self.efm
            self.gold -= 50 * self.egm
        else:
            self.event_id = 0

    def town_menu(self):
        while True:
            self.clear()

            # Semi Stat Update
            if self.m_id is 1:
                self.growth = math.floor(10 * (self.farm * 6 * 2 * (1 - self.tax) - self.pop) * self.farm_lvl) / 10
            elif self.m_id is 3:
                self.growth = math.floor(10 * (self.farm * 2 * 2 * (1 - self.tax) - self.pop) * self.farm_lvl) / 10
            else:
                self.growth = math.floor(10 * (self.farm * 4 * 2 * (1 - self.tax) - self.pop) * self.farm_lvl) / 10

            self.income = int(self.pop * self.tax) + self.shop + self.gold_mine * 3 * self.gm_lvl
            self.revenue = self.farm + self.lab * 5
            self.profit = self.income - self.revenue

            self.jobs = self.farm * 3 + self.shop * 4 + self.gold_mine * 2
            self.unemp = self.pop - self.jobs

            self.housing = self.homes * 5 * self.house_lvl

            # Stat print
            print(self.name, ": Day", self.day, self.month, "Year", self.year)
            print("\n-- TOWN STATS --\n")
            print("Population:", self.pop, "/", self.housing)
            print("Food:", self.food, "/", self.granary*10, "(", self.growth, ")")
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
            if self.lab >= 1 and self.dr is False: print("* Your town isn't researching. "
                                                         "You can schedule research in the research menu.")
            if self.food == self.granery*10: print("* You are making extra food that can't be stored in your granaries. build more to increase food storgae")
            print("\n-- EVENT --\n")

            # Event print
            if self.event_id is 0:
                print("Nothing has happened today.")
            elif self.event_id is 1:
                print("Your farms had a good harvest. (+60 base food)")
            elif self.event_id is 2:
                print("Your miners have struck gold! (+70 base gold)")
            elif self.event_id is 3:
                print("Someone got murdered last night. (-1 base pop)")
            elif self.event_id is 4:
                print("Your food supplies got spoiled in the cold. (-50 base food)")
            elif self.event_id is 5:
                print("The town got flooded. (-50 base food and gold)")

            print("\n----------------\n")

            # Input handle
            print("1: Next Day\n2: Build\n3: Buildings")
            if self.town_hall is True: print("4: Town Management")
            if self.lab >= 1: print("5: Research")
            print("E: Exit Game")

            i = input("> ")

            if i is "1":
                break
            elif i is "E":
                exit()
            elif i is "2":
                self.build()
            elif i is "3":
                self.clear()
                print("Farms:", self.farm)
                print("Houses:", self.homes)
                print("Shops:", self.shop)
                print("Granaries:", self.granary)
                print("Gold Mines:", self.gold_mine)
                input("PRESS ENTER TO GO BACK")
            elif i is "4" and self.town_hall is True:
                self.town_management()
            elif i is "5" and self.lab >= 1:
                self.research()

    def build(self):
        self.clear()
        print("What would you like to build?")
        print("1: Farm (5G)\n2: House (10G)\n3: Shop (15G)\n4: Granary (20G)\n5: Gold Mine (20G)")
        if self.town_hall is False:
            print("6: Town Hall (100G)")
        else:
            print("6: Research Lab (70G)")
        print("0: Exit Build Menu")

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
            self.granary += 1
            self.gold -= 20
        elif i is 5 and self.gold >= 20:
            self.gold_mine += 1
            self.gold -= 20
        elif i is 6 and self.town_hall is False and self.gold >= 100:
            self.gold -= 100
            self.town_hall = True
        elif i is 6 and self.town_hall is True and self.gold >= 70:
            self.gold -= 70
            self.lab += 1

    def town_management(self):
        self.clear()
        print("1: Tax Rates\n2: Trade\n0: Exit Menu")

        i = int(input("> "))
        if i is 1:
            print("Enter the tax rate as a integer %")
            print("Current tax rate:", self.tax*100, "%")
            print("NOTE: Lower Tax = More Food; Higher Tax = Less Food")
            self.tax = float(int(input("> "))) / 100
        elif i is 2:
            print("What item will you trade for (F=Food, G=Gold)")
            i = input("> ")

            if i is "F" or i is "f":
                print("You can trade 2 gold for 1 food. Enter how much food you want. "
                      "Make sure you have enough to perform the transaction")
                i = int(input("> "))
                if self.gold >= i:
                    self.gold -= 2 * i
                    self.food += i
            if i is "G" or i is "g":
                print("You can trade 2 food for 1 gold. Enter how much gold you want. "
                      "Make sure you have enough to perform the transaction")
                i = int(input("> "))
                if self.food >= i:
                    self.food -= 2 * i
                    self.gold += i

    def research(self):
        self.clear()
        if self.dr is True:
            if self.rt is "farm": print("Research:", self.rp, "/", self.farm_rc)
            if self.rt is "gm": print("Research:", self.rp, "/", self.gm_rc)
            if self.rt is "house": print("Research:", self.rp, "/", self.house_rc)
        print("Enter a research project to begin. This will cancel the current project though")
        print("1: Farm Lvl", self.farm_lvl + 1)
        print("2: Gold Mine Lvl", self.gm_lvl + 1)
        print("3: House Lvl", self.house_lvl + 1)
        print("0: Exit")

        i = int(input("> "))
        if i is 1:
            self.rp = 0
            self.dr = True
            self.rt = "farm"
        elif i is 2:
            self.rp = 0
            self.dr = True
            self.rt = "gm"
        elif i is 3:
            self.rp = 0
            self.dr = True
            self.rt = "house"
