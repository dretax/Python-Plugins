__author__ = 'DreTaX'
__version__ = '1.0'
import clr

clr.AddReferenceByPartialName("Fougerite")
clr.AddReferenceByPartialName("UnityEngine")
import UnityEngine
import Fougerite
from Fougerite import Player
from UnityEngine import Vector3

"""
    Class
"""

class ResourceSpawner:

    def On_Command(self, Player, cmd, args):
        if cmd == "spawn":
            if not Player.Admin and not Player.Moderator:
                Player.Message("You are not allowed to use this command!")
                return

            num = 1
            if len(args) == 2:
                numb = str(args[1])
                if numb.isnumeric():
                    num = int(numb)
                resource = args[0].lower()
            else:
                resource = str.join(' ', args).lower()
            loc = Util.Infront(Player, 10)
            y = World.GetGround(loc.x, loc.z)
            loc = Vector3(loc.x, y, loc.z)
            if resource == "wood":
                World.Spawn(";res_woodpile", loc, num)
                Player.Notice("\u2714", "Wood Pile has been spawned!", 3)
            elif resource == "sulfur":
                World.Spawn(";res_ore_1", loc, num)
                Player.Notice("\u2714", "Sulfur Ore has been spawned!", 3)
            elif resource == "metal":
                World.Spawn(";res_ore_2", loc, num)
                Player.Notice("\u2714", "Metal Ore has been spawned!", 3)
            elif resource == "stone":
                World.Spawn(";res_ore_3", loc, num)
                Player.Notice("\u2714", "Stone Ore has been spawned!", 3)
            elif resource == "stag":
                World.Spawn(":stag_prefab", loc, num)
                Player.Notice("\u2714", "Stag has been spawned!", 3)
            elif resource == "chicken":
                World.Spawn(":chicken_prefab", loc, num)
                Player.Notice("\u2714", "Chicken has been spawned!", 3)
            elif resource == "rabbit":
                World.Spawn(":rabbit_prefab_a", loc, num)
                Player.Notice("\u2714", "Rabbit has been spawned!", 3)
            elif resource == "bear":
                World.Spawn(":bear_prefab", loc, num)
                Player.Notice("\u2714", "Bear has been spawned!", 3)
            elif resource == "mbear":
                World.Spawn(":mutant_bear", loc, num)
                Player.Notice("\u2714", "Mutant Bear has been spawned!", 3)
            elif resource == "pig":
                World.Spawn(":boar_prefab", loc, num)
                Player.Notice("\u2714", "Pig has been spawned!", 3)
            elif resource == "wolf":
                World.Spawn(":wolf_prefab", loc, num)
                Player.Notice("\u2714", "Wolf has been spawned!", 3)
            elif resource == "mwolf":
                World.Spawn(":mutant_wolf", loc, num)
                Player.Notice("\u2714", "Mutant Wolf has been spawned!", 3)
            elif resource == "animals":
                loc1 = Util.Infront(Player, 16)
                y = World.GetGround(loc.x, loc.z)
                loc1 = Vector3(loc1.x, y, loc1.z)
                zonex = loc1.x
                zonez = loc1.z
                #  zoney = World.GetGround(loc1.x, loc1.z)
                for i in xrange(0, 15):
                    x = zonex + (i * 2)
                    y = World.GetGround(loc1.x, loc1.z)
                    loc1 = Vector3(x, y, loc1.z)
                    World.Spawn(":wolf_prefab", loc1)
                    z = zonez + (i * 2)
                    y = World.GetGround(loc1.x, loc1.z)
                    loc1 = Vector3(loc1.x, y, z)
                    World.Spawn(":wolf_prefab", loc1)
                    x = zonex - (i * 2)
                    y = World.GetGround(loc1.x, loc1.z)
                    loc1 = Vector3(x, y, loc1.z)
                    World.Spawn(":mutant_wolf", loc1)
                    z = zonez - (i * 2)
                    y = World.GetGround(loc1.x, loc1.z)
                    loc1 = Vector3(loc1.x, y, z)
                    World.Spawn(":mutant_wolf", loc1)
                Player.Notice("\u2714", "Animals has been spawned!", 3)
            elif resource == "airdrop":
                World.AirdropAtPlayer(Player)
                Player.Notice("\u2708", "Airdrop has been spawned!", 3)
            elif resource == "ammobox":
                World.Spawn("AmmoLootBox", loc, num)
                Player.Notice("\u2327", "Ammo Box has been spawned!", 3)
            elif resource == "medicalbox":
                World.Spawn("MedicalLootBox", loc, num)
                Player.Notice("\u2327", "Medical Box has been spawned!", 3)
            elif resource == "lootbox":
                World.Spawn("BoxLoot", loc, num)
                Player.Notice("\u2327", "Loot Box has been spawned!", 3)
            elif resource == "weaponbox":
                World.Spawn("WeaponLootBox", loc, num)
                Player.Notice("\u2327", "Weapon Box has been spawned!", 3)
            elif resource == "supplycrate":
                World.Spawn("SupplyCrate", loc, num)
                Player.Notice("\u2327", "SupplyCrate has been spawned!", 3)
                """elif resource == "Human".lower():
                    npc = World.Spawn(":player_soldier", loc, num)
                    Server.Broadcast(str(npc))
                    Player.Notice("\u2327", "Human has been spawned!", 3)"""
            else:
                Player.Message\
                    ("Spawnable: Wood, Sulfur, Metal, Stone, Stag, Chicken, Rabbit, Bear, MBear Pig, Wolf, MWolf")
                Player.Message\
                    ("Spawnable: Animals, Airdrop, AmmoBox, MedicalBox, LootBox, WeaponBox, SupplyCrate, Human")