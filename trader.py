from __future__ import annotations

from abc import abstractmethod, ABC

from avl import AVLTree
from material import Material
from random_gen import RandomGen

# Generated with https://www.namegenerator.co/real-names/english-name-generator
TRADER_NAMES = [
    "Pierce Hodge",
    "Loren Calhoun",
    "Janie Meyers",
    "Ivey Hudson",
    "Rae Vincent",
    "Bertie Combs",
    "Brooks Mclaughlin",
    "Lea Carpenter",
    "Charlie Kidd",
    "Emil Huffman",
    "Letitia Roach",
    "Roger Mathis",
    "Allie Graham",
    "Stanton Harrell",
    "Bert Shepherd",
    "Orson Hoover",
    "Lyle Randall",
    "Jo Gillespie",
    "Audie Burnett",
    "Curtis Dougherty",
    "Bernard Frost",
    "Jeffie Hensley",
    "Rene Shea",
    "Milo Chaney",
    "Buck Pierce",
    "Drew Flynn",
    "Ruby Cameron",
    "Collie Flowers",
    "Waldo Morgan",
    "Winston York",
    "Dollie Dickson",
    "Etha Morse",
    "Dana Rowland",
    "Eda Ryan",
    "Audrey Cobb",
    "Madison Fitzpatrick",
    "Gardner Pearson",
    "Effie Sheppard",
    "Katherine Mercer",
    "Dorsey Hansen",
    "Taylor Blackburn",
    "Mable Hodge",
    "Winnie French",
    "Troy Bartlett",
    "Maye Cummings",
    "Charley Hayes",
    "Berta White",
    "Ivey Mclean",
    "Joanna Ford",
    "Florence Cooley",
    "Vivian Stephens",
    "Callie Barron",
    "Tina Middleton",
    "Linda Glenn",
    "Loren Mcdaniel",
    "Ruby Goodman",
    "Ray Dodson",
    "Jo Bass",
    "Cora Kramer",
    "Taylor Schultz",
]

class Trader(ABC):
    
    def __init__(self, name: str) -> None:
        """
        Constructor for trader
        
        Args:
            name (str): Name of the Trader
        """

        self.name = name
        self.inventory = AVLTree() 
        self.active_deal = None
        self.trader_type = None
 
    @classmethod
    @abstractmethod
    def random_trader(cls) -> Trader:
        '''
        Generate random instance of Trader
        '''

        pass
    
    # @abstractmethod
    def set_all_materials(self, mats: list[Material]) -> None:
        """
        Setting all the materials into the trader's inventory
        
        Args:
            mats (list[Material]): The list of materials that the trader would sell
        """

        self.inventory = AVLTree()
        for material in mats:
            self.add_material(material)
    
    def add_material(self, mat: Material) -> None:
        """
        Adding the material into the trader's inventory
        
        Args:
            mat (Material): The material that is added to the trader's inventory
        """

        self.inventory[mat.mining_rate] = mat
    
    def remove_material(self, mat: Material) -> None:
        """
        Removing the known material from the traders inventory
        
        Args:
            mat (Material): The material that is removed from the trader's inventory
        """

        del self.inventory[mat.mining_rate]
    
    def is_currently_selling(self) -> bool:
        """
        Checks if the trader is currently selling a deal

        Returns:
            bool: Returns the state of the active deal
        """

        if self.active_deal is None:
            return False
        else:
            return True

    def current_deal(self) -> tuple[Material, float]:
        """
        It would be showing the current deal of the material to the user
 
        Returns:
            tuple[Material, float]: Returns the material and its price in a tuple format
        """

        if self.active_deal is None:
            raise ValueError()
        return self.active_deal

    @abstractmethod
    def generate_deal(self) -> None:
        """
        Generating the deal of the material
        """

        pass

    def generate_price(self) -> float:
        """
        Generating the price of the material
        """

        return round(2 + 8 * RandomGen.random_float(), 2)

    def stop_deal(self) -> None:
        """
        The trader stops the current deal
        """

        self.active_deal = None

    def __str__(self) -> str:
        """
        It would be representing the trader's deal in the terminal
 
        Returns:
            str: Returns the traders' names and what they would be selling into the terminal
        """

        if not self.is_currently_selling():
            result  = "<{}: {} not currently buying>".format(self.trader_type, self.name)
        else:
            material = self.active_deal[0]
            price = self.active_deal[1]
            result = "<{}: {} buying [{}: {}🍗/💎] for {}💰>".format(self.trader_type, self.name, material.name, material.mining_rate, price)
        
        return result

class RandomTrader(Trader):
    def __init__(self, name: str) -> None:
        """
        Constructor for random trader type
        
        Args:
            name (str): Name of the Random Trader
        """

        Trader.__init__(self, name)
        self.trader_type = "RandomTrader"
    

    def generate_deal(self) -> None:
        """
        Generating the deal of the material
        """

        material_list = self.inventory.range_between(0, len(self.inventory) - 1)
        material = RandomGen.random_choice(material_list)
        price = self.generate_price()
        self.active_deal = (material, price)
    
    @classmethod
    def random_trader(cls) -> Trader:
        '''
        Generate random instance of Random Trader
        '''

        random_name = RandomGen.random_choice(TRADER_NAMES)
        return RandomTrader(random_name)

class RangeTrader(Trader):
    def __init__(self, name: str) -> None:
        """
        Constructor for range trader type
        
        Args:
            name (str): Name of the Range Trader
        """

        Trader.__init__(self, name)
        self.trader_type = "RangeTrader"
   

    def generate_deal(self) -> None:
        """
        Generating the deal of the material
        """

        i = RandomGen.randint(1, len(self.inventory))
        j = RandomGen.randint(i, len(self.inventory))

        material_list = self.materials_between(i - 1, j - 1) 
        material = RandomGen.random_choice(material_list)
        price = self.generate_price()
        self.active_deal = (material, price)

    def materials_between(self, i: int, j: int) -> list[Material]:
        """
        Gets the material between the list of all the materials in the game
        
        Args:
            i (int): the index of the easiest to mine in the list of materials
            j (int): the index of the easiest to mine in the list of materials
        
        Returns:
            list[material]: Gets the list of materials between the index i and j
        """
        
        return self.inventory.range_between(i, j)
    
    @classmethod
    def random_trader(cls) -> Trader:
        '''
        Generate random instance of Random Trader
        '''

        random_name = RandomGen.random_choice(TRADER_NAMES)
        return RangeTrader(random_name)

class HardTrader(Trader):
    def __init__(self, name: str) -> None:
        """
        Constructor for hard trader type
        
        Args:
            name (str): Name of the Hard Trader
        """

        Trader.__init__(self, name)
        self.trader_type = "HardTrader"


    def generate_deal(self) -> None:
        """
        Generating the deal of the material
        """

        material_list = self.inventory.range_between(0, len(self.inventory) - 1)
        material = material_list[-1]
        self.remove_material(material)
        price = self.generate_price()
        self.active_deal = (material, price)
    
    @classmethod
    def random_trader(cls) -> Trader:
        '''
        Generate random instance of Random Trader
        '''

        random_name = RandomGen.random_choice(TRADER_NAMES)
        return HardTrader(random_name)

if __name__ == "__main__":
    trader = RangeTrader("Jackson")
    print(trader)
    trader.set_materials([
        Material("Coal", 4.5),
        Material("Diamonds", 3),
        Material("Redstone", 20),
    ])
    trader.generate_deal()
    print(trader)
    trader.stop_deal()
    print(trader)

