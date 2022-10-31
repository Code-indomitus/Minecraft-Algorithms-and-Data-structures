"""
Game functionality used by the players. Both Solo and Multiplayer mode functionalities have been created and added.
"""
from __future__ import annotations
from constants import EPSILON
from heap import MaxHeap

from player import Player
from trader import HardTrader, RandomTrader, RangeTrader, Trader
from material import Material
from cave import Cave
from food import Food
from random_gen import RandomGen

__author__ = "Rachit Bhatia"

class Game:
    """
    The parent Game class which consists of all basic functionality required to create and initialise a Game.
    """

    MIN_MATERIALS = 5
    MAX_MATERIALS = 10

    MIN_CAVES = 5
    MAX_CAVES = 10

    MIN_TRADERS = 4
    MAX_TRADERS = 8

    MIN_FOOD = 2
    MAX_FOOD = 5


    def __init__(self) -> None:
        """
        Creates a Game object.
        """
        self.materials = []     
        self.caves = [] 
        self.traders = []

    def initialise_game(self) -> None:
        """
        Initialise all game objects: Materials, Caves, Traders.

        :complexity: Best-case = Worst-case = O(random materials generation) + O(random caves generation) + O(random traders generation)  
        """
        N_MATERIALS = RandomGen.randint(self.MIN_MATERIALS, self.MAX_MATERIALS)
        self.generate_random_materials(N_MATERIALS)
        print("Materials:\n\t", end="")
        print("\n\t".join(map(str, self.get_materials())))
        N_CAVES = RandomGen.randint(self.MIN_CAVES, self.MAX_CAVES)
        self.generate_random_caves(N_CAVES)
        print("Caves:\n\t", end="")
        print("\n\t".join(map(str, self.get_caves())))
        N_TRADERS = RandomGen.randint(self.MIN_TRADERS, self.MAX_TRADERS)
        self.generate_random_traders(N_TRADERS)
        print("Traders:\n\t", end="")
        print("\n\t".join(map(str, self.get_traders())))


    def initialise_with_data(self, materials: list[Material], caves: list[Cave], traders: list[Trader]) -> None:
        """
        Initialise the game by setting Materials, Caves, Traders using passed in lists.

        :param: materials: list of materials passed in to be set as the Game's materials
        :param: caves: list of caves passed in to be set as the Game's caves
        :param: traders: list of traders passed in to be set as the Game's traders

        :complexity: Best-case = Worst-case = O(1)
        """
        self.set_materials(materials)
        self.set_caves(caves)
        self.set_traders(traders)


    def set_materials(self, mats: list[Material]) -> None:
        """
        Sets the materials of the Game
        :param: mats: list of materials to be set as the Game's materials
        :complexity: Best-case = Worst-case = O(1)
        """
        self.materials = mats


    def set_caves(self, caves: list[Cave]) -> None:
        """
        Sets the caves of the Game
        :param: mats: list of caves to be set as the Game's caves
        :complexity: Best-case = Worst-case = O(1)
        """
        self.caves = caves


    def set_traders(self, traders: list[Trader]) -> None:
        """
        Sets the traders of the Game
        :param: mats: list of traders to be set as the Game's traders
        :complexity: Best-case = Worst-case = O(1)
        """
        self.traders = traders


    def get_materials(self) -> list[Material]:
        """
        Return the list of Materials of the Game
        :complexity: Best-case = Worst-case = O(1)
        """
        return self.materials

    def get_caves(self) -> list[Cave]:
        """
        Return the list of Caves of the Game
        :complexity: Best-case = Worst-case = O(1)
        """
        return self.caves


    def get_traders(self) -> list[Trader]:
        """
        Return the list of Traders of the Game
        :complexity: Best-case = Worst-case = O(1)
        """
        return self.traders


    def generate_random_materials(self, amount: int) -> None:
        """
        Generates <amount> random materials using Material.random_material
        Generated materials must all have different names and different mining_rates.
        (You may have to call Material.random_material more than <amount> times.)

        :param amount: the amount of materials to be set in the game 
        :complexity: Best-case = Worst-case = O(amount * N), where N is the number of materials in self.materials
        """
        while len(self.materials) < amount:
            new_material = Material.random_material()
            similar_material = False 

            #iterating through the Game's material list to check for existing materials with same name or mining rate
            for material in self.materials:
                if (new_material.name == material.name) or (abs(new_material.mining_rate - material.mining_rate) < EPSILON):
                    similar_material = True  
                    break
            
            #add the randomly generated material only if similar material doesn't already exist in the self.materials list
            if not similar_material:
                self.materials.append(new_material)


    def generate_random_caves(self, amount: int) -> None:
        """
        Generates <amount> random caves using Cave.random_cave
        Generated caves must all have different names
        (You may have to call Cave.random_cave more than <amount> times.)

        :param amount: the amount of caves to be set in the game 
        :complexity: Best-case = Worst-case = O(amount * N), where N is the number of caves in self.caves
        """
        while len(self.caves) < amount:
            new_cave = Cave.random_cave(self.materials)
            similar_cave = False 

            #iterating through the Game's caves list to check for existing caves with same name
            for cave in self.caves:
                if (new_cave.name == cave.name):
                    similar_cave = True
                    break

            #add the randomly generated cave only if a cave with the same name does not exist in the self.caves list
            if not similar_cave:
                self.caves.append(new_cave)


    def generate_random_traders(self, amount: int) -> None:
        """
        Generates <amount> random traders by selecting a random trader class
        and then calling <TraderClass>.random_trader()
        and then calling set_all_materials with some subset of the already generated materials.
        Generated traders must all have different names
        (You may have to call <TraderClass>.random_trader() more than <amount> times.)

        :param amount: the amount of traders to be set in the game 
        :complexity: Best-case = Worst-case = O(amount * N) + O(amount * S), where N is the number of traders in self.traders and
                     S is the length of the list subset which is copied to a new list in the random_traders_setup function
        """


        while len(self.traders) < amount:
            similar_trader = False
            trader_type_number = RandomGen.randint(1,3) #randomly generating a number to randomly choose a trader class
            
            if trader_type_number == 1:
                new_trader = self.random_traders_setup(RandomTrader) #RandomTrader selected if random number generated was 1

            elif trader_type_number == 2:
                new_trader = self.random_traders_setup(RangeTrader) #RangeTrader selected if random number generated was 2

            elif trader_type_number == 3:
                new_trader = self.random_traders_setup(HardTrader) #HardTrader selected if random number generated was 3


            #iterating through the Game's Traders list to check for existing traders with same name
            for trader in self.traders:
                if (new_trader.name == trader.name):
                    similar_trader = True
                    break
            
            #add the randomly generated Trader only if a trader with the same name does not exist in the self.traders list
            if not similar_trader:
                self.traders.append(new_trader)


    def random_traders_setup(self, trader_type: RandomTrader | RangeTrader | HardTrader) -> RandomTrader | RangeTrader | HardTrader:
        """
        Creates a random trader for the particular trader class passed in. 
        Sets the materials for the generated trader based on a randomly genreated subset of self.materials

        :param trader_type: The trader class for which a random trader is to be created
        :complexity: Best-case = Worst-case = O(S) where S is the length of the materials list subset generated
        """

        new_trader = trader_type.random_trader()
        RandomGen.random_shuffle(self.materials) #shuffling the materials list to ensure complete randomisation of materials for traders

        mats_subset_length = RandomGen.randint(1,len(self.materials))  #generating a random subset length
        mats_subset = self.materials[:mats_subset_length] #array slicing -> complexity = O(S)
        new_trader.set_all_materials(mats_subset) #complexity is also O(S)

        #Overall complexity = O(S + S) = O(S)
        return new_trader


    def finish_day(self) -> None:
        """
        DO NOT CHANGE
        Affects test results.
        """
        for cave in self.get_caves():
            if cave.quantity > 0 and RandomGen.random_chance(0.2):
                cave.remove_quantity(RandomGen.random_float() * cave.quantity)
            else:
                cave.add_quantity(round(RandomGen.random_float() * 10, 2))
            cave.quantity = round(cave.quantity, 2)

class SoloGame(Game):
    """
    The Single Player Game class. Extends basic functionality from Game class and runs the Game.
    """

    def initialise_game(self) -> None:
        """
        Calls super class function to initialise all Game objects - Materials, Caves, Traders
        Sets the Game objects for the Player

        :complexity: Best-case = Worst-case = O(random materials generation) + O(random caves generation) + O(random traders generation)
                     Complexity is same as that of super().initialise_game()
        """
        super().initialise_game()
        self.player = Player.random_player()
        self.player.set_materials(self.get_materials())
        self.player.set_caves(self.get_caves())
        self.player.set_traders(self.get_traders())


    def initialise_with_data(self, materials: list[Material], caves: list[Cave], traders: list[Trader], player_names: list[str], emerald_info: list[float]) -> None:
        """
        Initialise the game by setting Materials, Caves, Traders using passed in lists.

        :param: materials: list of materials passed in to be set as the Game's materials
        :param: caves: list of caves passed in to be set as the Game's caves
        :param: traders: list of traders passed in to be set as the Game's traders
        :param player_names: list containing the name of the player to be set
        :param: emeral_info: list containing the number of emeralds the player have at the start of the game

        :complexity: Best-case = Worst-case = O(1)
        """
        super().initialise_with_data(materials, caves, traders)
        self.player = Player(player_names[0], emeralds=emerald_info[0])
        self.player.set_materials(self.get_materials())
        self.player.set_caves(self.get_caves())
        self.player.set_traders(self.get_traders())


    def simulate_day(self) -> None:
        """
        Simulates a single day by running all the functions required for a day's setup in a Single Player Game

        :complexity: Best-case = Worst-Case = O(T + f + s + v), where T = number of trader in the game, f = number of food to be generated, 
                     s = complexity of select_food_and_caves, and v = complexity of verify_output_and_update_quantities
        """ 
        # 1. Traders make deals
        game_traders = self.get_traders()
        for trader in game_traders:
            trader.generate_deal()

        print("Traders Deals:\n\t", end="")
        print("\n\t".join(map(str, self.get_traders())))
        # 2. Food is offered
        food_num = RandomGen.randint(self.MIN_FOOD, self.MAX_FOOD)
        foods = []
        for _ in range(food_num):
            foods.append(Food.random_food())
        print("\nFoods:\n\t", end="")
        print("\n\t".join(map(str, foods)))
        self.player.set_foods(foods)
        # 3. Select one food item to purchase
        food, balance, caves = self.player.select_food_and_caves()   
        print(food, balance, caves)
        # 4. Quantites for caves is updated, some more stuff is added.
        self.verify_output_and_update_quantities(food, balance, caves)


    def verify_output_and_update_quantities(self, food: Food | None, balance: float, caves: list[tuple[Cave, float]]) -> None:
        """
        Verifes the result of the select_food_and_caves function to check if the values obtained make sense. Also conducts some sanity checks to verify outputs' nature.
        Updates the cave quantities and the player balance after conducting the checks.

        :param food: the selected food by the player
        :param balance: the expected balance of the player after purchasing food and performing mining to make trades
        :param caves: the caves mined by the player
        :raises ValueError: if food bought by player does not exist in the Game
        :raises ValueError: if expected balance of player is lesser than the bought food's price
        :raises ValueError: if calculated balance is not equal to expected balance
        :complexity: Best-case = Worst-case = O(C + C) = O(C) where C is the number of caves in the list of caves mined by the player
        """

        if food is not None:  
            if food not in self.player.get_foods():
                raise ValueError("Food not in list of foods.")
            if self.player.balance < food.price - EPSILON:
                raise ValueError("Player cannot afford food item.")

            total_emeralds_collected = 0

            for cave_tuple in caves:
                total_emeralds_collected = total_emeralds_collected + cave_tuple[1] * cave_tuple[0].material.get_current_best_price_for_sold()
            
            calculated_balance  = total_emeralds_collected + self.player.balance - food.price  #calculating the emerald balance of the player based on the mined caves and food selection

            if not abs(calculated_balance - balance) < EPSILON:
                raise ValueError("Incorrect balance calculated")
            
            # update the cave quantities
            for cave_tup in caves:
                cave_tup[0].remove_quantity(cave_tup[1])
            
            # update player emerald balance
            self.player.balance = balance


class MultiplayerGame(Game):
    """
    The Multiplayer Game class. Extends basic functionality from Game class and runs the Game.
    """

    MIN_PLAYERS = 2
    MAX_PLAYERS = 5

    def __init__(self) -> None:
        """
        Constructor. Calls Game class constructor to initalise Materials list, Caves list, Traders list
        """
        super().__init__()
        self.players = []


    def initialise_game(self) -> None:
        """
        Calls super class function to initialise all game objects - Materials, Caves, Traders
        Sets the Game objects for all Players

        :complexity: Best-case = Worst-case = 
                     O(random materials generation) + O(random caves generation) + O(random traders generation) + O(random players generation) + O(P)
                     where P is the number of players in self.players
        """
        super().initialise_game()
        N_PLAYERS = RandomGen.randint(self.MIN_PLAYERS, self.MAX_PLAYERS)
        self.generate_random_players(N_PLAYERS)
        for player in self.players:
            player.set_materials(self.get_materials())
            player.set_caves(self.get_caves())
            player.set_traders(self.get_traders())
        print("Players:\n\t", end="")
        print("\n\t".join(map(str, self.players)))


    def generate_random_players(self, amount) -> None:
        """
        Generate <amount> random players. Don't need anything unique, but you can do so if you'd like.
        
        :param amount: the number of players to be generated
        :complexity: Best-case = Worst-case = O(amount * P), where P is the number of players in self.players
        """
        while len(self.players) < amount:
            new_player = Player.random_player()
            similar_player = False

            #iterating through the Game's players list to check for existing players with same name
            for player in self.players:
                if player.name == new_player.name:
                    similar_player = True
                    break
            
            #add the randomly generated player only if a player with the same name does not exist in self.players
            if not similar_player:
                self.players.append(new_player)


    def initialise_with_data(self, materials: list[Material], caves: list[Cave], traders: list[Trader], player_names: list[str], emerald_info: list[float]) -> None:
        """
        Initialise the game by setting Materials, Caves, Traders using passed in lists.

        :param: materials: list of materials passed in to be set as the Game's materials
        :param: caves: list of caves passed in to be set as the Game's caves
        :param: traders: list of traders passed in to be set as the Game's traders
        :param player_names: list containing the names of the players to be set
        :param: emeral_info: list containing the number of emeralds the players have at the start of the game

        :complexity: Best-case = Worst-case = O(P) where P is the number of items in the player_names lists
        """
        super().initialise_with_data(materials, caves, traders)
        for player, emerald in zip(player_names, emerald_info):
            self.players.append(Player(player, emeralds=emerald))
            self.players[-1].set_materials(self.get_materials())
            self.players[-1].set_caves(self.get_caves())
            self.players[-1].set_traders(self.get_traders())
        print("Players:\n\t", end="")
        print("\n\t".join(map(str, self.players)))


    def simulate_day(self) -> None:
        """
        Simulates a single day by running all the functions required for a day's setup in a Single Player Game

        :complexity: Best-case = Worst-Case = O(T + s + v), where T = number of trader in the game, s = complexity of select_for_players, 
                     and v = complexity of verify_output_and_update_quantities
        """ 
        # 1. Traders make deals
        game_traders = self.get_traders()
        for trader in game_traders:
            trader.generate_deal()

        print("Traders Deals:\n\t", end="")
        print("\n\t".join(map(str, self.get_traders())))
        # 2. Food is offered
        offered_food = Food.random_food()
        print(f"\nFoods:\n\t{offered_food}")
        # 3. Each player selects a cave - The game does this instead.
        foods, balances, caves = self.select_for_players(offered_food)
        # 4. Quantites for caves is updated, some more stuff is added.
        self.verify_output_and_update_quantities(foods, balances, caves)


    def select_for_players(self, food: Food) -> tuple[list[Food|None], list[float], list[tuple[Cave, float]|None]]:
        """
        For each player, it selects the best cave such that by mining it, the player receives the highest amount of 
        emeralds when traded with a trader. Hence, it ensures that each player chooses the most optimal option.

        :param food: the food offered to the players in the Multiplayer game
        :returns: a list containing the food items or None depending on whether the player bought the Food, a list containing the temporary balances of every player, 
                  a list containing the caves (and the quantity mined from them) visited by each player or None if no Food was bought by the player.

        :complexity: Best-Case: O(M + T + C + C + P) = O(M + T + C + P). This case happens only when the best cases of both the get_max() and add() functions of MaxHeap are met.
                     In a scenario where after getting the max item from the heap, the last element of the heap does not sink to any position i.e. O(sink) = O(1) and also while 
                     adding an item to the heap, no the element does not rise to any position i.e. O(rise) = O(1), only then the complexity of this function would be O(M + T + C + P).

                     Worst_Case: O(M + T + C + C + P*(log C + log C)) = O(M + T + 2*C + 2*P*log C) = O(M + T + C + P*log C)     [since constants are ignored in Big-O complexity]

                     The complexity of the materials for loop (line 636) is O(M). Complexity of traders for loop (line 641) is O(T). Complexity of caves for loop (line 650) is O(C).
                     Complexity of players for loop (line 671) is O(P). A bottom-up heap is created in this function for which the complexity is always O(N) where N is the number of 
                     nodes to be added in the heap. Since a maximum of C nodes (length of self.caves) will be added to the heap, its complexity is O(C). The complexities of the get_max()
                     and add() functions of the heap are O(log C) * O(comparison) but since the comparison in this heap is done between keys of float types, O(comparison) = O(1). Thus, the
                     complexity of these functions becomes O(log C). All the other functions called in this function have a worst-case complexity of O(1). Based on these complexities, the 
                     overall complexity of tis function becomes O(M + T + C + P*log C)

        :approach: The primary purpose of this function is to select the cave which upon being mined, returns the highest emralds based on the trader's existing deals. So the approach was chosen
                   to calculate the emerald return for each cave and arrange these caves in a Max Heap by using their emerald returns as keys. The cave with the highest emerald return would be
                   placed at the top of the heap. Hence, for every player, the topmost item is extracted from the heap using the get_max() function. Following this, the chosen cave is added back to
                   the heap after the player has mined a certain quantity of material from the cave. Even when the cave is added back, the heap sets its position based on its new key by rising 
                   it up to the appropriate position. The traders loop (line 641) which is executed before the caves loop (line 650) sets the selling price for each material in the game based on 
                   the deals generated. This material price is then used to calculate the emrald returns of each cave in the calculate_cave_returns function. The emerald return of the caves was 
                   calculated without any data from the players as the multiplayer mode only offers a single food to all the players. Hence, the food price for all players will be the same which 
                   can thus be used to calculate the amount of material mined from each cave. 

                   A bottom up heap is constructed for the caves to arrange them in the descending order of their emerald returns. A bottom-up heap was chosen because it is the only adt which has a 
                   creation complexity of O(N) where N is the number of nodes in the heap. This heap can only be used when one is aware of all the items to be added into the heap before its creation. 
                   Since in this case, we already know the maximum number of nodes and have all the elements (caves) ready before the creation, we can use a bottom-up heap which eventually resulted
                   in a better efficiency in terms of time-complexity of the function.

        :example: A single day in a MultiPlayer Game is shown below:

                  Materials: 
                  gold = Material("gold Nugget", 27.24)
                  netherite = Material("Netherite Ingot", 20.95)
                  fishing_rod = Material("Fishing Rod", 26.93)

                  Traders:
                  waldo = RandomTrader("Waldo Morgan")
                  orson = RandomTrader("Orson Hoover")
                  lea = RandomTrader("Lea Carpenter")

                  Caves:
                  Cave("Boulderfall Cave", prismarine, 10)
                  Cave("Castle Karstaag Ruins", netherite, 4)
                  Cave("Glacial Cave", gold, 3)

                  Players:
                  Player("Rachit", 50)
                  Player("Jun Yu", 50)
                  Player("Jobin", 5)

                  Food:
                  Food("Cooked Chicken Cuts", 19, 19)

                  Demostration:
                  First each material's current best selling price is set to None.

                  Next, the traders set the price of each material based on the set deals:

                  waldo selling fishing rod for 10 emaralds
                  orson selling gold for 5 emeralds
                  lea selling netherite for 8 emeralds

                  -------------------End of Traders Loop-------------------


                  Next, the caves loop (line 650) is executed where teh temp quantity of each cave is set as the cave's current quantity.
                  1st iteration: Cave = ("Boulderfall Cave", prismarine, 10)
                  This iteration is skipped as the material in this cave is not sold by any traders (prismarine is not sold by any traders)


                  2nd iteration: Cave = ("Castle Karstaag Ruins", netherite, 4)
                  The calculate_cave_returns function is called on this cave since its material has a selling price set by the trader (lea)
                  In the calculate_cave_returns() function:
                    cave_quantity = 4
                    material_mining_rate = 20.95
                    total_mineable_quantity = 19 / 20.95 = 0.906921241050119
                    material_price = 8

                    quantity_mined = 0.906921241050119 (since total_mineable_quantity > cave_quantity)
                    cave_emerald_returns = 0.906921241050119 * 8 = 7.255369928400955

                  cave_emerald_returns = [(7.255369928400955, Castle Karstaag Ruins)]


                  3rd iteration: Cave = Cave("Glacial Cave", gold, 3)
                  The calculate_cave_returns function is called on this cave since its material has a selling price set by the trader (orson)
                  In the calculate_cave_returns() function:
                    cave_quantity = 3
                    material_mining_rate = 27.24
                    total_mineable_quantity = 19 / 27.24 = 0.697503671071953
                    material_price = 5

                    quantity_mined = 0.697503671071953 (since total_mineable_quantity > cave_quantity)
                    cave_emerald_returns = 0.697503671071953 * 5 = 3.487518355359765

                  cave_emerald_returns = [(7.255369928400955, Castle Karstaag Ruins), (3.487518355359765, Glacial Cave)]

                  -------------------End of Caves Loop-------------------

                  Next, the cave_emerald_returns list is arranged into a MaxHeap based on the keys of the two materials i.e. 7.255369928400955 & 3.487518355359765
                  The topmost element in the heap would be (7.255369928400955, Castle Karstaag Ruins) followed by (3.487518355359765, Glacial Cave) since
                  7.255369928400955 > 3.487518355359765


                  Next, the players loop (line 671) is executed.
                  1st iteration: Player = Player("Rachit", 50)
                  Since player balance (50) > food price (19), player Rachit will be able to mine a cave
                  food_selected = [Cooked Chicken Cuts]
                    Best cave returned from get_max() is Castle Karstaag Ruins since it is at the top of the heap. 
                    Current structure of the heap = [(3.487518355359765, Glacial Cave)]

                    best_cave_return = (7.255369928400955, Castle Karstaag Ruins)
                    optimal emarald return (opt_emerald_return) = 7.255369928400955
                    most_optimal_cave = Castle Karstaag Ruins
                    optimal mined quantity (opt_mined_quantity) = 0.906921241050119

                    balance = [38.255369928400955]
                    visited_caves = [(Castle Karstaag Ruins, 0.906921241050119)]
                    most_optimal_quantity new temp quantity = 4 - 0.906921241050119 = 3.093078758949881
                    The calculate_cave_returns function is called for the most_optimal_cave after which the following values are returned:
                    new_emerald_return = 7.255369928400955
                    new_mined_quantity = 0.906921241050119

                    Finally, the cave is added back to the heap making the structure of the heap to be [(7.255369928400955, Castle Karstaag Ruins), (3.487518355359765, Glacial Cave)]
                    since Castle Karstaag Ruins still has a higher emerald return (higher value of key) it will be placed at the top of the heap


                  2nd iteration: Player = Player("Jun Yu", 50)
                  Since player balance (50) > food price (19), player Jun Yu will be able to mine a cave
                  food_selected = [Cooked Chicken Cuts, Cooked Chicken Cuts]
                    Best cave returned from get_max() is Castle Karstaag Ruins since it is at the top of the heap. 
                    Current structure of the heap = [(3.487518355359765, Glacial Cave)]

                    best_cave_return = (7.255369928400955, Castle Karstaag Ruins)
                    optimal emarald return (opt_emerald_return) = 7.255369928400955
                    most_optimal_cave = Castle Karstaag Ruins
                    optimal mined quantity (opt_mined_quantity) = 0.906921241050119

                    balance = [38.255369928400955, 38.255369928400955]
                    visited_caves = [(Castle Karstaag Ruins, 0.906921241050119), (Castle Karstaag Ruins, 0.906921241050119)]
                    most_optimal_quantity new temp quantity = 3.093078758949881 - 0.906921241050119 = 2.186157517899762
                    The calculate_cave_returns function is called for the most_optimal_cave after which the following values are returned:
                    new_emerald_return = 7.255369928400955
                    new_mined_quantity = 0.906921241050119

                    Finally, the cave is added back to the heap making the structure of the heap to be [(7.255369928400955, Castle Karstaag Ruins), (3.487518355359765, Glacial Cave)]
                    since Castle Karstaag Ruins still has a higher emerald return (higher value of key) it will be placed at the top of the heap


                  3rd iteration: Player = Player("Jobin", 5)
                  Since player balance (5) < food price (19), player Jobin will not be able to mine a cave
                  food_selected = [Cooked Chicken Cuts, Cooked Chicken Cuts, None]
                  balance = [38.255369928400955, 38.255369928400955, 5]
                  visited_caves = [(Castle Karstaag Ruins, 0.906921241050119), (Castle Karstaag Ruins, 0.906921241050119), None]

                  -------------------End of Players Loop-------------------

                  The following values are returned:
                  food_selected = [Cooked Chicken Cuts, Cooked Chicken Cuts, None]
                  balance = [38.255369928400955, 38.255369928400955, 5]
                  visited_caves = [(Castle Karstaag Ruins, 0.906921241050119), (Castle Karstaag Ruins, 0.906921241050119), None]

                  -------------------End of Day-------------------
        """

        #initialising all lists to be returned as output of this function
        food_selected = [] 
        balance = []
        visited_caves = []
        cave_emerald_returns = []

        # resetting selling prices to avoid overlaps in material prices when this function is called more than once
        for material in self.materials: #O(M)
            material.current_best_price_for_sold = None    


        # Find the emerald per hunger bar of each material. This is to identify which are the better caves to go for mining
        for trader in self.traders: # O(T)
            current_deal = trader.current_deal() 
            trader_material = current_deal[0]
            material_price = current_deal[1]

            trader_material.set_current_best_price_for_sold(material_price)  #setting the price of each material


        # Calculating emerald returns of each cave
        for cave in self.caves: #O(C)
            
            #resetting temporary quantity for each time this function is called
            cave.set_temp_quantity(cave.quantity) 

            # skip iteration if the trader did not set material price for the current cave's material
            # This is done so that the materials which are not sold by any trader are not considered since they will not be of any use to the player.
            if cave.material.get_current_best_price_for_sold() is None:
                continue

            cave_emerald_return, mined_quantity = self.calculate_cave_returns(cave, food)  #calculate the emeralds returned by mining cave
            cave.set_mined_quantity(mined_quantity)
            cave_emerald_returns.append((cave_emerald_return, cave))    #add tuple of cave emarald returns and cave


        #the cave emerald returns list is converted into a max heap. 
        #since len(cave_emerald_returns list) <= len(self.caves), complexity = O(C) as there will be a maximum of C number of nodes

        caves_heap = MaxHeap(len(cave_emerald_returns), cave_emerald_returns) #O(C)


        for player in self.players: #O(P)
            if player.balance < food.price - EPSILON:
                food_selected.append(None)
                balance.append(player.balance)
                visited_caves.append(None)  #player cannot mine any cave if food is not purchased

            else:
                temp_balance = player.balance
                food_selected.append(food)
                temp_balance -= food.price  

                #complexity of get_max() is O(log C)*O(comparison) but since comparison is between float types, O(comparison) = O(1)
                best_cave_return = caves_heap.get_max() #O(log C)
                opt_emerald_return = best_cave_return[0]
                most_optimal_cave = best_cave_return[1]
                opt_mined_quantity = most_optimal_cave.get_mined_quantity()

                temp_balance += opt_emerald_return
                balance.append(temp_balance)

                visited_caves.append((most_optimal_cave, opt_mined_quantity))
                most_optimal_cave.set_temp_quantity(most_optimal_cave.get_temp_quantity() - opt_mined_quantity) #reducing temporary quantity of selected cave

                new_emerald_return, new_mined_quantity = self.calculate_cave_returns(most_optimal_cave, food)  #recalculating emerald returns for selected cave
                most_optimal_cave.set_mined_quantity(new_mined_quantity)

                 #complexiy of add() is O(log C)*O(comparison) but since comparison is between float types, O(comparison) = O(1)
                caves_heap.add((new_emerald_return, most_optimal_cave)) #O(log C)
        
        return food_selected, balance, visited_caves


    def calculate_cave_returns(self, cave: Cave, food: Food) -> tuple[float, float]:
        """
        Calculates the emeralds a player will get by mining the particular cave.

        :param cave: the current cave to check for its emerald return
        :param food: the food offered to players in the MultiPlayer Game
        :returns: a tuple containing the emeralds received by mining the particular cave and the quantity of material that is mined 
        :complexity: Best-case = Worst-case = O(1)
        """
        cave_quantity = cave.get_temp_quantity()    #the temporary quantity of the game 
        material_mining_rate = cave.material.get_mining_rate()  
        total_mineable_quantity = food.hunger_bars/material_mining_rate  #calculating the total quantity of material that can be mined based
        material_price = cave.material.get_current_best_price_for_sold()
        
        if cave_quantity <= total_mineable_quantity - EPSILON:
            quantity_mined = cave_quantity  #because mineable quantity is greater than quantity of cave
        else:
            quantity_mined = total_mineable_quantity   #because mineable quantity is lesser than quantity of cave

        cave_emerald_returns = quantity_mined * material_price  #calculating emeralds returned by mining the cave 

        return cave_emerald_returns, quantity_mined


    def verify_output_and_update_quantities(self, foods: list[Food | None], balances: list[float], caves: list[tuple[Cave, float]|None]) -> None:
        """
        Verifes the result of the select_food_and_caves function to check if the values obtained make sense. Also conducts some sanity checks to verify outputs' nature.
        Updates the cave quantities and the player balance after conducting the checks.

        :param food: list containing the food selected by the players
        :param balance: the expected balance of the players after purchasing food and performing mining to make trades
        :param caves: the caves mined by the players
        :raises ValueError: if length of all returned lists is not the same 
        :raises ValueError: if a player mined a cave even without buying the food
        :raises ValueError: if the price of the materials in the mined caves is None
        :raises ValueError: if the quantity of the material in a cave is lesser than what is mined by a player
        :raises ValueError: if the calculated balance of a player is not equal to its expected balance
        :complexity: Best-case = Worst-case = O(P) where P is the number of total players in the Game 
        """
        if not (len(foods) == len(self.players) and len(balances) == len(self.players) and len(caves) == len(self.players)):
            raise ValueError("Inaccurate lengths of caves, foods and balances regarding number of players present in multiplayer game.")

        for player, food, balance, cave_tup in zip(self.players, foods, balances, caves):
            
            if food is None:
                if not cave_tup is None:
                    raise ValueError("Player cannot mine without food.")
            else:
                if cave_tup[0].material.get_current_best_price_for_sold() is None:
                    raise ValueError("Material is not sold by any trader!")
                
                if (cave_tup[0].get_quantity() < cave_tup[1] - EPSILON):
                    raise ValueError("Player is trying to mine more than the cave has to offer")

                total_emeralds_collected = cave_tup[1] * cave_tup[0].material.get_current_best_price_for_sold()
                
                calculated_balance  = total_emeralds_collected + player.balance - food.price #calculating the emerald balance of the player based on the mined caves and food price

                if not (abs(calculated_balance - balance) < EPSILON):
                    raise ValueError("Incorrect balance calculated for player.")
                
                # # update the cave quantities
                cave_tup[0].remove_quantity(cave_tup[1])
            
                # update player emerald balance
                player.balance = balance

if __name__ == "__main__":

    r = 1234 # Change this to set a fixed seed.
    RandomGen.set_seed(r)
    print(r)

    g = SoloGame()
    g.initialise_game()

    g.simulate_day()
    g.finish_day()

    g.simulate_day()
    g.finish_day()
