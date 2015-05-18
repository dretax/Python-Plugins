__author__ = 'DreTaX'
__version__ = '1.0'
import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite

"""
    Class
"""

class ResourceSpawner:

    def isMod(self, id):
        if DataStore.ContainsKey("Moderators", id):
            return True
        return False

    def On_Command(self, Player, cmd, args):
        if cmd == "spawn":
            if not Player.Admin or not self.isMod(Player.SteamID):
                Player.Message("You are not allowed to use this command!")
                return

            loc = Player.Location
            loc.x = loc.x + 5
            loc.y = World.GetGround(loc.x, loc.z)
            resource = str.join(' ', args).lower()
            if resource == "Wood".lower():
                World.Spawn("res_woodpile", loc)
                Player.Notice("\u2714", "Wood Pile has been spawned!", 3)
            elif resource == "Sulfur".lower():
                World.Spawn("res_ore_1", loc)
                Player.Notice("\u2714", "Sulfur Ore has been spawned!", 3)
            elif resource == "Metal".lower():
                World.Spawn("res_ore_2", loc)
                Player.Notice("\u2714", "Metal Ore has been spawned!", 3)
            elif resource == "Stone".lower():
                World.Spawn("res_ore_3", loc)
                Player.Notice("\u2714", "Stone Ore has been spawned!", 3)
            elif resource == "Stag".lower():
                World.Spawn(":stag_prefab", loc)
                Player.Notice("\u2714", "Stag has been spawned!", 3)
            elif resource == "Chicken".lower():
                World.Spawn(":chicken_prefab", loc)
                Player.Notice("\u2714", "Chicken has been spawned!", 3)
            elif resource == "Rabbit".lower():
                World.Spawn(":rabbit_prefab_a", loc)
                Player.Notice("\u2714", "Rabbit has been spawned!", 3)
            elif resource == "Bear".lower():
                World.Spawn(":bear_prefab", loc)
                Player.Notice("\u2714", "Bear has been spawned!", 3)
            elif resource == "MBear".lower():
                World.Spawn(":mutant_bear", loc)
                Player.Notice("\u2714", "Mutant Bear has been spawned!", 3)
            elif resource == "Pig".lower():
                World.Spawn(":boar_prefab", loc)
                Player.Notice("\u2714", "Pig has been spawned!", 3)
            elif resource == "Wolf".lower():
                World.Spawn(":wolf_prefab", loc)
                Player.Notice("\u2714", "Wolf has been spawned!", 3)
            elif resource == "MWolf".lower():
                World.Spawn(":mutant_wolf", loc)
                Player.Notice("\u2714", "Mutant Wolf has been spawned!", 3)
            elif resource == "Animals".lower():
                loc1 = Player.Location
                zonex = loc1.x
                zonez = loc1.z
                #  zoney = World.GetGround(loc1.x, loc1.z)
                for i in xrange(0, 15):
                    loc1.x = zonex + (i * 2)
                    loc1.y = World.GetGround(loc1.x, loc1.z)
                    World.Spawn(":wolf_prefab", loc1)
                    loc1.z = zonez + (i * 2)
                    loc1.y = World.GetGround(loc1.x, loc1.z)
                    World.Spawn(":wolf_prefab", loc1)
                    loc1.x = zonex - (i * 2)
                    loc1.y = World.GetGround(loc1.x, loc1.z)
                    World.Spawn(":mutant_wolf", loc1)
                    loc1.z = zonez - (i * 2)
                    loc1.y = World.GetGround(loc1.x, loc1.z)
                    World.Spawn(":mutant_wolf", loc1)
                Player.Notice("\u2714", "Animals has been spawned!", 3)
            elif resource == "Airdrop".lower():
                World.AirdropAtPlayer(Player)
                Player.Notice("\u2708", "Airdrop has been spawned!", 3)
            elif resource == "AmmoBox".lower():
                World.Spawn("AmmoLootBox", loc)
                Player.Notice("\u2327", "Ammo Box has been spawned!", 3)
            elif resource == "MedicalBox".lower():
                World.Spawn("MedicalLootBox", loc)
                Player.Notice("\u2327", "Medical Box has been spawned!", 3)
            elif resource == "LootBox".lower():
                World.Spawn("BoxLoot", loc)
                Player.Notice("\u2327", "Loot Box has been spawned!", 3)
            elif resource == "WeaponBox".lower():
                World.Spawn("WeaponLootBox", loc)
                Player.Notice("\u2327", "Weapon Box has been spawned!", 3)
            elif resource == "SupplyCrate".lower():
                World.Spawn("SupplyCrate", loc)
                Player.Notice("\u2327", "SupplyCrate has been spawned!", 3)
            else:
                Player.Message\
                    ("Spawnable: Wood, Sulfur, Metal, Stone, Stag, Chicken, Rabbit, Bear, MBear Pig, Wolf, MWolf")
                Player.Message("Spawnable: Animals, Airdrop, AmmoBox, MedicalBox, LootBox, WeaponBox, SupplyCrate")