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
        self.traders_list_best_deal = None

    def set_traders(self, traders_list: list[Trader]) -> None:
        '''
        Set the traders to the traders_list and also find the best deal among all the traders that are buying the same item.
        Time Complexity : Best Case = Worst Case = O(len(self.traders_list)*len(temp_traders_list_greatest_deal) + len(traders_list_best_deal))
        '''
        self.traders_list = traders_list

        temp_traders_list_greatest_deal=[]

        # Find any traders that are buying the same material. Only the trader with a higher buying price of the same material will be added to the traders_list_best_deal
        for i in range(len(self.traders_list)):
            same_offer = False
            for j in range(len(temp_traders_list_greatest_deal)) :
                if self.traders_list[i].current_deal()[0] == temp_traders_list_greatest_deal[j].current_deal()[0] : # If any traders are offering the same item , check which deal is better 
                    if self.traders_list[i].current_deal()[1] >= temp_traders_list_greatest_deal[j].current_deal()[1] :
                        temp_traders_list_greatest_deal[j] = self.traders_list[i] 
                    same_offer = True
            
            if same_offer == False :
                temp_traders_list_greatest_deal.append(self.traders_list[i])

        self.traders_list_best_deal = temp_traders_list_greatest_deal

        # Set the best price for sold of each material after checking through the deals offered by all the traders
        for trader in self.traders_list_best_deal :
            trader.current_deal()[0].set_current_best_price_for_sold(trader.current_deal()[1])

    
    def set_foods(self, foods_list: list[Food]) -> None:
        self.food_list = foods_list

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



    def select_food_and_caves(self) -> tuple[Food | None, float, list[tuple[Cave, float]]]:
        '''
        Complexity : Worst-Case complexity = Best-Case Complexity = O(T + F*( C*logC + C*logC )) = O(T + F*C*logC)
        '''
        
        food_selected = None
        balance = 0
        caves_selected = []    

        # Find the emerald per hunger bar of each material .This is to identify which are the better caves to go for mining 
        for traders in self.traders_list_best_deal: # O(T)
            current_deal = traders.current_deal() 
            trader_material = current_deal[0]
            material_price = current_deal[1]

            emerald_per_hunger_bar = material_price / trader_material.get_mining_rate() 

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
                try:          
                    temp_avl[cave.material.get_emerald_per_hunger_bar()] = cave  # O(log C)

                except ValueError:
                    temp_avl[cave.material.get_emerald_per_hunger_bar() + 00000.1] = cave # O(log C)

            # Retrive the caves in order starting from the cave that has the material of the highest emerald per hunger bar value. 
            for cave in self.caves_list :# O(C)
                
                # if the hunger_bar of the player is still not yet 0 , the day continues 
                if abs(temp_hunger_bars) > 0 - EPSILON :
                    
                    # Retrieve the cave with the highest emerald per hunger bar value
                    current_cave_selected = temp_avl.find_max_and_remove().item # O(log C)

                    material_in_cave = current_cave_selected.material
                    number_of_material = current_cave_selected.quantity
                    total_hunger_bars_needed_if_fully_mine = material_in_cave.get_mining_rate()*number_of_material

                    # If the player has enough hunger bar to mine all of the materials in this cave
                    if abs(temp_hunger_bars) >= total_hunger_bars_needed_if_fully_mine - EPSILON :
                        amount_mined = number_of_material
                        temp_balance = temp_balance + amount_mined*material_in_cave.get_current_best_price_for_sold()
                        temp_hunger_bars = temp_hunger_bars - total_hunger_bars_needed_if_fully_mine

                    # If the player does not have enough hunger bar to mine all of the materials in this cave 
                    else:
                        amount_mined = temp_hunger_bars / material_in_cave.get_mining_rate() 
                        temp_balance = temp_balance + amount_mined*material_in_cave.get_current_best_price_for_sold()
                        temp_hunger_bars = 0

                    temp_caves_selected.append((current_cave_selected,amount_mined))
                        
                else :
                    break
            

            # The most optimal solution
            if abs(temp_balance) > balance - EPSILON :
                food_selected = food
                balance = temp_balance
                caves_selected = temp_caves_selected
        

        return (food_selected,balance,caves_selected)
        
        
                
            
    def __str__(self) -> str:
        return "Player" + self.name + " has a balance of " + str(self.balance) + "emeralds"

if __name__ == "__main__":
    print(Player("Steve"))
    print(Player("Alex", emeralds=1000))
