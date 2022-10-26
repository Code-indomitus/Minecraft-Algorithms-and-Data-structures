from random import Random
from random_gen import RandomGen

# Material names taken from https://minecraft-archive.fandom.com/wiki/Items
RANDOM_MATERIAL_NAMES = [
    "Arrow",
    "Axe",
    "Bow",
    "Bucket",
    "Carrot on a Stick",
    "Clock",
    "Compass",
    "Crossbow",
    "Exploration Map",
    "Fire Charge",
    "Fishing Rod",
    "Flint and Steel",
    "Glass Bottle",
    "Dragon's Breath",
    "Hoe",
    "Lead",
    "Map",
    "Pickaxe",
    "Shears",
    "Shield",
    "Shovel",
    "Sword",
    "Saddle",
    "Spyglass",
    "Totem of Undying",
    "Blaze Powder",
    "Blaze Rod",
    "Bone",
    "Bone meal",
    "Book",
    "Book and Quill",
    "Enchanted Book",
    "Bowl",
    "Brick",
    "Clay",
    "Coal",
    "Charcoal",
    "Cocoa Beans",
    "Copper Ingot",
    "Diamond",
    "Dyes",
    "Ender Pearl",
    "Eye of Ender",
    "Feather",
    "Spider Eye",
    "Fermented Spider Eye",
    "Flint",
    "Ghast Tear",
    "Glistering Melon",
    "Glowstone Dust",
    "Gold Ingot",
    "Gold Nugget",
    "Gunpowder",
    "Ink Sac",
    "Iron Ingot",
    "Iron Nugget",
    "Lapis Lazuli",
    "Leather",
    "Magma Cream",
    "Music Disc",
    "Name Tag",
    "Nether Bricks",
    "Paper",
    "Popped Chorus Fruit",
    "Prismarine Crystal",
    "Prismarine Shard",
    "Rabbit's Foot",
    "Rabbit Hide",
    "Redstone",
    "Seeds",
    "Beetroot Seeds",
    "Nether Wart Seeds",
    "Pumpkin Seeds",
    "Wheat Seeds",
    "Slimeball",
    "Snowball",
    "Spawn Egg",
    "Stick",
    "String",
    "Wheat",
    "Netherite Ingot",
]

class Material:
    """

    """
    
    def __init__(self, name: str, mining_rate: float) -> None:
        '''
        Constructor for Material
        Attributes :
        1) name
        2) mining rate
        '''
        self.name = name
        self.mining_rate = mining_rate
        self.current_best_price_for_sold = None
        self.emerald_per_hunger_bar = None
    
    def __str__(self) -> str:
        return self.name + " with mining rate of " + str(self.mining_rate)

    @classmethod
    def random_material(cls):
        '''
        Generate random material 
        '''
        random_name = RandomGen.random_choice(RANDOM_MATERIAL_NAMES)
        random_mining_rate = RandomGen.randint(1,50) + RandomGen.random_float()
        return Material(random_name,random_mining_rate)

    def get_mining_rate(self):
        return self.mining_rate

    def set_emerald_per_hunger_bar(self,value):
        self.emerald_per_hunger_bar = value
        
    def get_emerald_per_hunger_bar(self):
        return self.emerald_per_hunger_bar


    def set_current_best_price_for_sold(self,value):
        if self.current_best_price_for_sold is None:
            self.current_best_price_for_sold = value
        else:
            if abs(value) > self.current_best_price_for_sold :
                self.current_best_price_for_sold = value

    def get_current_best_price_for_sold(self):
        return self.current_best_price_for_sold

if __name__ == "__main__":
    print(Material("Coal", 4.5))
