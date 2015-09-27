__author__ = 'DreTaX'
__version__ = '1.0'

import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite

"""
    Class
"""

sysname = "InventoryViewer"
red = "[color #FF0000]"
green = "[color #009900]"

class InvLookup:

    def On_Command(self, Player, cmd, args):
        if cmd == "inv":
            if Player.Admin or Player.Moderator:
                if len(args) >= 1:
                    if args[0] == "reset":
                        self.returnInventory(Player)
                    else:
                        user = str.join(' ', args)
                        self.recordInventory(Player)
                        self.recordUserInventory(Player, user)
                        self.returnUserInventory(Player, user)
                else:
                    Player.MessageFrom(sysname,
                                       "/inv playername (Checks Inv),  /inv reset (Returns original inv)")
            else:
                Player.MessageFrom(sysname, "You can't use this command")

    def recordInventory(self, Player):
        Inventory = []
        id = Player.SteamID
        for Item in Player.Inventory.Items:
            if Item and Item.Name:
                myitem = {'name': Item.Name, 'quantity': Item.Quantity, 'slot': Item.Slot}
                Inventory.append(myitem)
        for Item in Player.Inventory.ArmorItems:
            if Item and Item.Name:
                myitem = {'name': Item.Name, 'quantity': Item.Quantity, 'slot': Item.Slot}
                Inventory.append(myitem)
        for Item in Player.Inventory.BarItems:
            if Item and Item.Name:
                myitem = {'name': Item.Name, 'quantity': Item.Quantity, 'slot': Item.Slot}
                Inventory.append(myitem)

        DataStore.Add("pinv", id, Inventory)
        DataStore.Save()
        Player.Inventory.ClearAll()

    def recordUserInventory(self, Player, userString):
        user = Server.FindPlayer(userString)
        Inventory = []
        id = user.SteamID
        for Item in user.Inventory.Items:
            if Item and Item.Name:
                myitem = {'name': Item.Name, 'quantity': Item.Quantity, 'slot': Item.Slot}
                Inventory.append(myitem)
        for Item in user.Inventory.ArmorItems:
            if Item and Item.Name:
                myitem = {'name': Item.Name, 'quantity': Item.Quantity, 'slot': Item.Slot}
                Inventory.append(myitem)
        for Item in user.Inventory.BarItems:
            if Item and Item.Name:
                myitem = {'name': Item.Name, 'quantity': Item.Quantity, 'slot': Item.Slot}
                Inventory.append(myitem)

        DataStore.Add("pinv", id, Inventory)
        DataStore.Save()

    def returnInventory(self, Player):
        id = Player.SteamID
        if DataStore.ContainsKey("pinv", id):
            Inventory = DataStore.Get("pinv", id)
            Player.Inventory.ClearAll()
            for dictionary in Inventory:
                if dictionary['name'] is not None:
                    Player.Inventory.AddItemTo(dictionary['name'], dictionary['slot'], dictionary['quantity'])
                else:
                    Player.MessageFrom(sysname, red + "No dictionary found in the for cycle?!")
            Player.MessageFrom(sysname, green + "Your have received your original inventory")
            DataStore.Remove("pinv", id)
        else:
            Player.MessageFrom(sysname, red + "No Items of your last inventory found!")

    def returnUserInventory(self, Player, userString):
        user = Server.FindPlayer(userString)
        if user is None:
            Player.MessageFrom(sysname, userString + " is not online")
        else:
            if DataStore.ContainsKey("pinv", user.SteamID):
                Player.Inventory.ClearAll()
                Inventory = DataStore.Get("pinv", user.SteamID)
                if Inventory:
                    for dictionary in Inventory:
                        if dictionary['name'] is not None:
                            Player.Inventory.AddItemTo(dictionary['name'], dictionary['slot'], dictionary['quantity'])
                        else:
                            Player.MessageFrom(sysname, red + "No dictionary found in the for cycle?!")
                    Player.MessageFrom(sysname, green + "Your inventory represents " + user.Name + "'s inventory")
                else:
                    Player.MessageFrom(sysname, "Inventory == null")
                DataStore.Remove("pinv", user.SteamID)
            else:
                Player.MessageFrom(sysname, red +  "No Items found!")