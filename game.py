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
        #mats_subset = self.materials
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
        #self.verify_output_and_update_quantities(food, balance, caves)

    def verify_output_and_update_quantities(self, food: Food | None, balance: float, caves: list[tuple[Cave, float]]) -> None:
        if food not in self.player.get_foods:
            raise ValueError

        for item in caves:
            if item[0] not in self.player.get_caves:
                raise ValueError

        
           

class MultiplayerGame(Game):

    MIN_PLAYERS = 2
    MAX_PLAYERS = 5

    def __init__(self) -> None:
        super().__init__()
        self.players = []
        #FIXME: Do I change this list?

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
        for _ in range(amount):
            self.players.append(Player.random_player())

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
        #raise NotImplementedError() #TODO: Remove this
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
        caves_selected = []  

        # Resetting the emerald per hunger bar for every material that might have been set to a value in previous calls to this function
        for material in self.materials: # O(M)
            material.set_emerald_per_hunger_bar(None)  
            material.current_best_price_for_sold = None

        # Find the emerald per hunger bar of each material .This is to identify which are the better caves to go for mining 
        for trader in self.traders: # O(T)
            current_deal = trader.current_deal() 
            trader_material = current_deal[0]
            material_price = current_deal[1]

            trader_material.set_current_best_price_for_sold(material_price)

            emerald_per_hunger_bar = trader_material.get_current_best_price_for_sold() / trader_material.get_mining_rate() 

            trader_material.set_emerald_per_hunger_bar(emerald_per_hunger_bar)
        
        for player in self.players:
            if player.balance < food.price:
                food_selected.append(None)
                balance.append(player.balance)
                caves_selected.append(None)
            
            else:
                pass # logic to check for the best cave

    def verify_output_and_update_quantities(self, foods: list[Food | None], balances: list[float], caves: list[tuple[Cave, float]|None]) -> None:
        raise NotImplementedError()

if __name__ == "__main__":

    r = RandomGen.seed # Change this to set a fixed seed.
    RandomGen.set_seed(r)
    print(r)

    g = SoloGame()
    g.initialise_game()

    g.simulate_day()
    g.finish_day()

    g.simulate_day()
    g.finish_day()
