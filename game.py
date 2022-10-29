from __future__ import annotations
from constants import EPSILON

from player import Player
from trader import HardTrader, RandomTrader, RangeTrader, Trader
from material import Material
from cave import Cave
from food import Food
from random_gen import RandomGen

class Game:

    MIN_MATERIALS = 5
    MAX_MATERIALS = 10

    MIN_CAVES = 5
    MAX_CAVES = 10

    MIN_TRADERS = 4
    MAX_TRADERS = 8

    MIN_FOOD = 2
    MAX_FOOD = 5



    def __init__(self) -> None:
        #TODO
        #is this supposed to be a hash table?
        #but getters return a list
        self.materials = []
        self.caves = [] 
        self.traders = []

    def initialise_game(self) -> None:
        """Initialise all game objects: Materials, Caves, Traders."""
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

    def initialise_with_data(self, materials: list[Material], caves: list[Cave], traders: list[Trader]):
        self.set_materials(materials)
        self.set_caves(caves)
        self.set_traders(traders)

    def set_materials(self, mats: list[Material]) -> None:
        self.materials = mats

    def set_caves(self, caves: list[Cave]) -> None:
        self.caves = caves

    def set_traders(self, traders: list[Trader]) -> None:
        self.traders = traders

    def get_materials(self) -> list[Material]:
        return self.materials

    def get_caves(self) -> list[Cave]:
        return self.caves

    def get_traders(self) -> list[Trader]:
        return self.traders

    def generate_random_materials(self, amount):
        """
        Generates <amount> random materials using Material.random_material
        Generated materials must all have different names and different mining_rates.
        (You may have to call Material.random_material more than <amount> times.)
        """
        while len(self.materials) < amount:
            new_material = Material.random_material()
            similar_material = False 

            for material in self.materials:
                if (new_material.name == material.name) or (abs(new_material.mining_rate - material.mining_rate) < EPSILON):
                    similar_material = True
                    break
            
            if not similar_material:
                self.materials.append(new_material)


    def generate_random_caves(self, amount):
        """
        Generates <amount> random caves using Cave.random_cave
        Generated caves must all have different names
        (You may have to call Cave.random_cave more than <amount> times.)
        """
        while len(self.caves) < amount:
            new_cave = Cave.random_cave(self.materials)
            similar_cave = False 

            for cave in self.caves:
                if (new_cave.name == cave.name):
                    similar_cave = True
                    break
            
            if not similar_cave:
                self.caves.append(new_cave)


    def generate_random_traders(self, amount):
        """
        Generates <amount> random traders by selecting a random trader class
        and then calling <TraderClass>.random_trader()
        and then calling set_all_materials with some subset of the already generated materials.
        Generated traders must all have different names
        (You may have to call <TraderClass>.random_trader() more than <amount> times.)
        """


        while len(self.traders) < amount:
            similar_trader = False
            trader_type_number = RandomGen.randint(1,3)
            
            if trader_type_number == 1:
                new_trader = self.random_traders_setup(RandomTrader)

            elif trader_type_number == 2:
                new_trader = self.random_traders_setup(RangeTrader)

            elif trader_type_number == 3:
                new_trader = self.random_traders_setup(HardTrader)

            for trader in self.traders:
                if (new_trader.name == trader.name):
                    similar_trader = True
                    break
            
            if not similar_trader:
                self.traders.append(new_trader)


    def random_traders_setup(self, trader_type):

        new_trader = trader_type.random_trader()
        RandomGen.random_shuffle(self.materials)

        mats_subset_length = RandomGen.randint(1,len(self.materials))
        mats_subset = self.materials[:mats_subset_length]
        new_trader.set_all_materials(mats_subset)

        return new_trader


    def finish_day(self):
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

    def initialise_game(self) -> None:
        super().initialise_game()
        self.player = Player.random_player()
        self.player.set_materials(self.get_materials())
        self.player.set_caves(self.get_caves())
        self.player.set_traders(self.get_traders())

    def initialise_with_data(self, materials: list[Material], caves: list[Cave], traders: list[Trader], player_names: list[int], emerald_info: list[float]):
        super().initialise_with_data(materials, caves, traders)
        self.player = Player(player_names[0], emeralds=emerald_info[0])
        self.player.set_materials(self.get_materials())
        self.player.set_caves(self.get_caves())
        self.player.set_traders(self.get_traders())

    def simulate_day(self):
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

        if food is not None:  
            if food not in self.player.get_foods():
                raise ValueError("Food not in list of foods.")
            if self.player.balance < food.price - EPSILON:
                raise ValueError("Player cannot afford food item.")

            total_emeralds_collected = 0

            for cave_tuple in caves:
                total_emeralds_collected = total_emeralds_collected + cave_tuple[1] * cave_tuple[0].material.get_current_best_price_for_sold()
            
            calculated_balance  = total_emeralds_collected + self.player.balance - food.price

            if not abs(calculated_balance - balance) < EPSILON:
                raise ValueError("Incorrect balance calculated")
            
            # update the cave quantities
            for cave_tup in caves:
                cave_tup[0].remove_quantity(cave_tup[1])
            
            # update player emerald balance
            self.player.balance = balance


class MultiplayerGame(Game):

    MIN_PLAYERS = 2
    MAX_PLAYERS = 5

    def __init__(self) -> None:
        super().__init__()
        self.players = []


    def initialise_game(self) -> None:
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
        """Generate <amount> random players. Don't need anything unique, but you can do so if you'd like."""
        while len(self.players) < amount:
            new_player = Player.random_player()
            similar_player = False

            for player in self.players:
                if player.name == new_player.name:
                    similar_player = True
                    break
            
            if not similar_player:
                self.players.append(new_player)

    def initialise_with_data(self, materials: list[Material], caves: list[Cave], traders: list[Trader], player_names: list[int], emerald_info: list[float]):
        super().initialise_with_data(materials, caves, traders)
        for player, emerald in zip(player_names, emerald_info):
            self.players.append(Player(player, emeralds=emerald))
            self.players[-1].set_materials(self.get_materials())
            self.players[-1].set_caves(self.get_caves())
            self.players[-1].set_traders(self.get_traders())
        print("Players:\n\t", end="")
        print("\n\t".join(map(str, self.players)))


    def simulate_day(self):
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
        """
        food_selected = []
        balance = []
        visited_caves = []

        for cave in self.caves:
            cave.set_temp_quantity(cave.quantity)
            cave.material.current_best_price_for_sold = None

        # Find the emerald per hunger bar of each material .This is to identify which are the better caves to go for mining 
        for trader in self.traders: # O(T)
            current_deal = trader.current_deal() 
            trader_material = current_deal[0]
            material_price = current_deal[1]

            trader_material.set_current_best_price_for_sold(material_price)

        most_optimal_cave = None

        for player in self.players:
            if player.balance < food.price - EPSILON:
                food_selected.append(None)
                balance.append(player.balance)
                visited_caves.append(None)

            else:
                temp_balance = player.balance
                food_selected.append(food)
                temp_balance -= food.price

                opt_return = 0
                opt_mined_quantity = 0

                for cave in self.caves:

                    if cave.material.get_current_best_price_for_sold() is None:
                        continue
                    
                    #opt_return, opt_mined_quantity = self.calculate_cave_returns(most_optimal_cave, food)
                    new_return, new_mined_quantity = self.calculate_cave_returns(cave, food)

                    #comparing the emerald returns
                    if opt_return < new_return - EPSILON:
                        most_optimal_cave = cave
                        opt_mined_quantity = new_mined_quantity
                        opt_return = new_return

                temp_balance += opt_return
                balance.append(temp_balance)
                    
                visited_caves.append((most_optimal_cave, opt_mined_quantity))
                most_optimal_cave.set_temp_quantity(cave.get_temp_quantity() - opt_mined_quantity)
        
        return food_selected, balance, visited_caves

    def calculate_cave_returns(self, cave: Cave, food: Food) -> tuple[float, float]:
        cave_quantity = cave.get_temp_quantity()
        material_mining_rate = cave.material.get_mining_rate()
        total_mineable_quantity = food.hunger_bars/material_mining_rate
        material_price = cave.material.get_current_best_price_for_sold()
        
        if cave_quantity <= total_mineable_quantity - EPSILON:
            quantity_mined = cave_quantity
        else:
            quantity_mined = total_mineable_quantity

        cave_returns = quantity_mined * material_price

        return cave_returns, quantity_mined


    def verify_output_and_update_quantities(self, foods: list[Food | None], balances: list[float], caves: list[tuple[Cave, float]|None]) -> None:
        if not (len(foods) == len(self.players) and len(balances) == len(self.players) and len(caves) == len(self.players)):
            raise ValueError("Inaccurate lengths of caves, foods and balances regarding number of players present in multiplayer game.")

        for player, food, balance, cave_tup in zip(self.players, foods, balances, caves):
            
            if food is None:
                if not cave_tup is None:
                    raise ValueError("Player cannot mine without food.")
            else:
                if cave_tup[0].material.get_current_best_price_for_sold() is None:
                    raise ValueError("Material is not sold by any trader!")
                
                #TODO: REMOVE THIS SHIT!!!!!!!!!!
                # if (cave_tup[0].get_quantity() < cave_tup[1] - EPSILON):
                #     raise ValueError("Player is trying to mine more than the cave has to offer")

                total_emeralds_collected = cave_tup[1] * cave_tup[0].material.get_current_best_price_for_sold()
                
                calculated_balance  = total_emeralds_collected + player.balance - food.price

                print ("Calc: " + str(calculated_balance))
                print ("Actual: " + str(balance))
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
