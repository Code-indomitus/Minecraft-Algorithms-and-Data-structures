from __future__ import annotations
from aset import ASet
from avl import AVLTree
from bst import BinarySearchTree

from cave import Cave
from heap import MaxHeap
from material import Material
from random_gen import RandomGen
from constants import EPSILON

from trader import Trader
from food import Food

# List taken from https://minecraft.fandom.com/wiki/Mob
PLAYER_NAMES = [
    "Steve",
    "Alex",
    "ɘᴎiɿdoɿɘH",
    "Allay",
    "Axolotl",
    "Bat",
    "Cat",
    "Chicken",
    "Cod",
    "Cow",
    "Donkey",
    "Fox",
    "Frog",
    "Glow Squid",
    "Horse",
    "Mooshroom",
    "Mule",
    "Ocelot",
    "Parrot",
    "Pig",
    "Pufferfish",
    "Rabbit",
    "Salmon",
    "Sheep",
    "Skeleton Horse",
    "Snow Golem",
    "Squid",
    "Strider",
    "Tadpole",
    "Tropical Fish",
    "Turtle",
    "Villager",
    "Wandering Trader",
    "Bee",
    "Cave Spider",
    "Dolphin",
    "Enderman",
    "Goat",
    "Iron Golem",
    "Llama",
    "Panda",
    "Piglin",
    "Polar Bear",
    "Spider",
    "Trader Llama",
    "Wolf",
    "Zombified Piglin",
    "Blaze",
    "Chicken Jockey",
    "Creeper",
    "Drowned",
    "Elder Guardian",
    "Endermite",
    "Evoker",
    "Ghast",
    "Guardian",
    "Hoglin",
    "Husk",
    "Magma Cube",
    "Phantom",
    "Piglin Brute",
    "Pillager",
    "Ravager",
    "Shulker",
    "Silverfish",
    "Skeleton",
    "Skeleton Horseman",
    "Slime",
    "Spider Jockey",
    "Stray",
    "Vex",
    "Vindicator",
    "Warden",
    "Witch",
    "Wither Skeleton",
    "Zoglin",
    "Zombie",
    "Zombie Villager",
    "H̴͉͙̠̥̹͕͌̋͐e̸̢̧̟͈͍̝̮̹̰͒̀͌̈̆r̶̪̜͙̗̠̱̲̔̊̎͊̑̑̚o̷̧̮̙̗̖̦̠̺̞̾̓͆͛̅̉̽͘͜͝b̸̨̛̟̪̮̹̿́̒́̀͋̂̎̕͜r̸͖͈͚̞͙̯̲̬̗̅̇̑͒͑ͅi̶̜̓̍̀̑n̴͍̻̘͖̥̩͊̅͒̏̾̄͘͝͝ę̶̥̺̙̰̻̹̓̊̂̈́̆́̕͘͝͝"
]

class Player():

    DEFAULT_EMERALDS = 50

    MIN_EMERALDS = 14
    MAX_EMERALDS = 40

    def __init__(self, name, emeralds=None) -> None:
        self.name = name
        self.balance = self.DEFAULT_EMERALDS if emeralds is None else emeralds
        self.traders_list = None
        self.food_list = None
        self.materials_list = None
        self.caves_list = None 

    def set_traders(self, traders_list: list[Trader]) -> None:
        '''
        Set the traders to the traders_list and also find the best deal among all the traders that are buying the same item.
        Time Complexity : Best Case = Worst Case = O(len(self.traders_list)*len(temp_traders_list_greatest_deal) + len(traders_list_best_deal))
        '''
        self.traders_list = traders_list

    
    def set_foods(self, foods_list: list[Food]) -> None:
        '''
        Sets the player's food list
        '''
        self.food_list = foods_list

    def get_foods(self) -> list[Food]:
        '''
        Returns the player's food list
        '''
        return self.food_list

    @classmethod
    def random_player(self) -> Player:
        '''
        Generate a random player 
        Time Complexity : Best Case = Worst Case = O(1)
        '''
        random_name = RandomGen.random_choice(PLAYER_NAMES)
        random_emeralds_amount = RandomGen.randint(self.MIN_EMERALDS,self.MAX_EMERALDS)
        return Player(random_name,random_emeralds_amount)

    def set_materials(self, materials_list: list[Material]) -> None:
        '''
        Set the materials to the materials_list attribute of Player class
        '''
        self.materials_list = materials_list

    def set_caves(self, caves_list: list[Cave]) -> None:
        '''
        Set the caves to the caves_list attribute of Player class
        '''
        self.caves_list = caves_list

    def get_caves(self) -> list[Cave]:
        '''
        Returns the caves_list of the Player
        '''
        return self.caves_list


    def select_food_and_caves(self) -> tuple[Food | None, float, list[tuple[Cave, float]]]:
        '''
        Complexity : Worst-Case complexity = Best-Case Complexity = O(M + T + F*( C*logC + C*logC )) = O(M + T + F*C*logC)
    
        The first for loop is to iterate through the whole list of traders. At each iteration, the information in regards to the deal generated that is 
        the material and the selling price of that material of that particular trader are retrieved. The price of that material is then set to to the current_best_price_for_sold 
        attribute of the material.If there is a case where two or more different traders are buying the same item, only the highest price among them will be set to the 
        current_best_price_for_sold attribute of the material. The emerald per hunger bar of each material is then calculated by using the current_best_price_for_sold of the material
        divided by the mining rate. By using this emerald per hunger bar calculated for each material, better caves can be selected. In other words, a cave with the material of higher emerald 
        per hunger bar should be prioritised more against other caves with materials of lower emerald per hunger bar. Emerald per hunger bar shows how many emeralds the player can obtain by
        selling the material for each hunger bar used when mining.  

        The second for loop is the main loop to choose the best choice of food and caves that will leave the highest balance at the end of the day. The first nested for loop inside this main loop
        is to insert every cave into an AVL tree which will sort the caves in accordance to the priority determined by the emerald per hunger bar of the material inside that cave. The second
        for loop inside this main loop is to keep the game going. If the player's hunger bar is still not yet 0 , then the best cave which is the one that contains the material of the 
        highest emerald per hunger bar is retrieved from the AVL tree. Then, it will check if the player has enough hunger bar to mine the full quantity of material inside that cave. If no, 
        it will calculate the how much of the material can be mined by the player with the remaning hunger bar left. The balance of the player is then added with the price of selling
        by using the amount mined multiplied with the current_best_price_for_sold of that material.At the end of the loop, there is a if statement to check if the food bought at this iteration
        has a greater balance than the previous food. If it is greater, then it will set this current food as the most optimal solution. This main loop is done repeatedly untill either the 
        player's hunger bar is 0 or all the caves are already finished mining.

        The complexity of this function is explained in further detail through in-line comments in the code

        Example :
        Player("Hello",50)
        Food :
        bread = Food("bread", 60, 30),
        rice = Food("Rice", 100, 28),

        Materials :
        gold = Material("Gold Nugget", 16.74)
        netherite = Material("Netherite Ingot", 21.58)
        fishing_rod = Material("Fishing Rod", 23.44)

        Caves:
        Cave("Ashfall's Tear", gold, 5)
        Cave("Benkongerike", netherite, 3)
        Cave("Blackbone Isle Grotto", gold, 4)
        Cave("Bleakcoast Cave", fishing_rod, 3)

        Traders:
        waldo = RandomTrader("Waldo Morgan") selling gold for 8 emeralds
        orson = RandomTrader("Orson Hoover") selling netherite for 6.50 emeralds
        lea = RandomTrader("Lea Carpenter") selling gold for 6.22 emeralds
        ruby = RandomTrader("Ruby Goodman") selling fishing rod for 7.54 emeralds

        Demonstration : 

        gold's current_best_price_for sold = 8 emeralds
        netherite's current_best_price_for = 6.50 emeralds
        fishing_rod's current_best_price_for = 7.54 emeralds

        for every material the emerald_per_hunger_bar is calculated,
        gold = 8 / 16.74 = 0.4779 emeralds/ hunger bar
        netherite = 6.50 / 21.58 = 0.3012 emeralds/ hunger bar
        fishing_rod = 7.54 / 23.44 =  0.32167 

        From the emerald_per_hunger_bar calculated, the caves rankings are :
        1) Ashfall's Tear and Blackbone Isle Grotto (since they contain gold that has highest emerald_per_hunger_bar)
        2) Bleakcoast Cave ( since it contains fishing rod that has the second highest emerald_per_hunger_bar)
        3) Benkongerike ( since it contains netherite that has least emerald_per_hunger_bar )
        

        for bread,
        balance after buying bread = 50-30 = 20
        hunger bar gained = 60

        ------ First Cave : Blackbone Isle Grotto ------------
        hunger bar needed to mine full quantity of gold in Blackbone Isle Grotto = 16.74*4 = 66.96
        player hunger bar is 60 which is not enough to mine all of the gold that requires 66.96 hunger bar.
        amount mined = 3.584229390681004
        balance after mining = 20 + 3.584229390681004*8 = 48.673835125448036   
        hunger bar left = 0

        ------------- Day ends---------------

        for rice, 
        balance after buying rice = 50-28 = 22
        hunger bar gained = 100

        ------ First Cave : Blackbone Isle Grotto ------------
        hunger bar needed to mine full quantity of gold in Blackbone Isle Grotto = 16.74*4 = 66.96
        amount mined = 4
        balance after mining = 22 + 4*8 = 54
        hunger bar left = 100 - 66.96 = 33.040000000000006

        ------ Second Cave: Ashfall's Tear --------------
        hunger bar needed to mine full quantity of gold in Blackbone Isle Grotto = 16.74*5 = 83.7
        player hunger bar is 33.040000000000006 which is not enough to mine all of the gold that requires 83.7 hunger bar
        amount mined = 1.9737156511350065
        balance after mining = 54 + 1.9737156511350065*8 = 69.78972520908005
        hunger bar left = 0

        -------------- Day ends---------------

        optimal solution : 
        food selected = rice
        caves selected = Blackbone Isle Grotto , Ashfall's Tear
        balance = 69.78972520908005
        '''
        
        food_selected = None
        balance = 0
        caves_selected = []  

        # Resetting the emerald per hunger bar for every material that might have been set to a value in previous calls to this function
        for material in self.materials_list: # O(M)
            material.set_emerald_per_hunger_bar(None)  
            material.current_best_price_for_sold = None

        # Find the emerald per hunger bar of each material .This is to identify which are the better caves to go for mining 
        for traders in self.traders_list: # O(T)
            current_deal = traders.current_deal() 
            trader_material = current_deal[0]
            material_price = current_deal[1]

            trader_material.set_current_best_price_for_sold(material_price)

            emerald_per_hunger_bar = trader_material.get_current_best_price_for_sold() / trader_material.get_mining_rate() 

            trader_material.set_emerald_per_hunger_bar(emerald_per_hunger_bar)

        # Find the food and list of caves that will give the most optimal result that is the highest amount of balance(emeralds) at the end of the day.
        for food in self.food_list : # O(F)

            temp_avl = AVLTree()     
            temp_balance = self.balance - food.price
            temp_hunger_bars = food.hunger_bars
            temp_caves_selected = []

            # Add the caves into the Avl tree by using the emerald per hunger bar calculated as the key and cave as the item . AVL helps to sort the caves in order based on the 
            # emerald per hunger bar of material
            for cave in self.caves_list : # O(C)

                
                if cave.material.get_emerald_per_hunger_bar() is None:
                    continue

                try:          
                    temp_avl[cave.material.get_emerald_per_hunger_bar()] = cave  # O(log C)

                except ValueError:
                    temp_avl[cave.material.get_emerald_per_hunger_bar() + 0.00001] = cave # O(log C)

            # Retrive the caves in order starting from the cave that has the material of the highest emerald per hunger bar value. 
            for cave in self.caves_list :# O(C)
                
                
                if cave.material.get_emerald_per_hunger_bar() is None:
                    continue

                # if the hunger_bar of the player is still not yet 0 , the day continues 
                if 0 < temp_hunger_bars - EPSILON:
                    
                    # Retrieve the cave with the material of the highest emerald per hunger bar value
                    current_cave_selected = temp_avl.find_max_and_remove().item # O(log C)

                    material_in_cave = current_cave_selected.material
                    number_of_material = current_cave_selected.quantity
                    total_hunger_bars_needed_if_fully_mine = material_in_cave.get_mining_rate()*number_of_material

                    # If the player has enough hunger bar to mine all of the materials in this cave
                    if total_hunger_bars_needed_if_fully_mine <= temp_hunger_bars - EPSILON :
                        amount_mined = number_of_material
                        temp_hunger_bars = temp_hunger_bars - total_hunger_bars_needed_if_fully_mine

                    # If the player does not have enough hunger bar to mine all of the materials in this cave 
                    else:
                        amount_mined = temp_hunger_bars / material_in_cave.get_mining_rate() 
                        temp_hunger_bars = 0

                    temp_balance = temp_balance + amount_mined*material_in_cave.get_current_best_price_for_sold()
                    temp_caves_selected.append((current_cave_selected,amount_mined))
                        
                else :
                    break
            

            # The most optimal solution
            if balance < temp_balance - EPSILON:
                food_selected = food
                balance = temp_balance
                caves_selected = temp_caves_selected
        

        return (food_selected,balance,caves_selected)
        
        
                
            
    def __str__(self) -> str:
        return "Player" + self.name + " has a balance of " + str(self.balance) + "emeralds"

if __name__ == "__main__":
    print(Player("Steve"))
    print(Player("Alex", emeralds=1000))
