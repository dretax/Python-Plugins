__author__ = 'DreTaX'
__version__ = '1.0'
import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite

blue = "[color #0099FF]"
red = "[color #FF0000]"
pink = "[color #CC66FF]"
teal = "[color #00FFFF]"
green = "[color #009900]"
purple = "[color #6600CC]"
white = "[color #FFFFFF]"

class iConomy:

    #Plugin Settings
    __MoneyMark__ = None
    __DefaultMoney__ = None
    __Sys__ = None
    #Player Settings!
    __MoneyMode__ = None
    __KillPortion__ = None
    __KillPortion2__ = None
    __DeathPortion__ = None
    __DeathPortion2__ = None

    def iConomy(self):
        if not Plugin.IniExists("iConomy"):
            ini = Plugin.CreateIni("iConomy")
            ini.AddSetting("Settings", "DefaultMoney", "100.0")
            ini.AddSetting("Settings", "MoneyMark", "$")
            ini.AddSetting("Settings", "Sysname", "[iConomy]")
            ini.AddSetting("PlayerKillSettings", "PercentageOrExtra", "1")
            ini.AddSetting("PlayerKillSettings", "KillPortion", "1.25")
            ini.AddSetting("PlayerKillSettings", "DeathPortion", "0.75")
            ini.AddSetting("PlayerKillSettings", "DeathPortion2", "4.0")
            ini.AddSetting("PlayerKillSettings", "KillPortion2", "5.0")
            ini.AddSetting("bearKillSettings", "PercentageOrExtra", "1")
            ini.AddSetting("bearKillSettings", "KillPortion", "1.25")
            ini.AddSetting("bearKillSettings", "DeathPortion", "0.75")
            ini.AddSetting("bearKillSettings", "DeathPortion2", "4.0")
            ini.AddSetting("bearKillSettings", "KillPortion2", "5.0")
            ini.AddSetting("mutantbearKillSettings", "PercentageOrExtra", "1")
            ini.AddSetting("mutantbearKillSettings", "KillPortion", "1.25")
            ini.AddSetting("mutantbearKillSettings", "DeathPortion", "0.75")
            ini.AddSetting("mutantbearKillSettings", "DeathPortion2", "4.0")
            ini.AddSetting("mutantbearKillSettings", "KillPortion2", "5.0")
            ini.AddSetting("stagKillSettings", "PercentageOrExtra", "1")
            ini.AddSetting("stagKillSettings", "KillPortion", "1.25")
            ini.AddSetting("stagKillSettings", "DeathPortion", "0.75")
            ini.AddSetting("stagKillSettings", "DeathPortion2", "4.0")
            ini.AddSetting("stagKillSettings", "KillPortion2", "5.0")
            ini.AddSetting("wolfKillSettings", "PercentageOrExtra", "1")
            ini.AddSetting("wolfKillSettings", "KillPortion", "1.25")
            ini.AddSetting("wolfKillSettings", "DeathPortion", "0.75")
            ini.AddSetting("wolfKillSettings", "DeathPortion2", "4.0")
            ini.AddSetting("wolfKillSettings", "KillPortion2", "5.0")
            ini.AddSetting("mutantwolfKillSettings", "PercentageOrExtra", "1")
            ini.AddSetting("mutantwolfKillSettings", "KillPortion", "1.25")
            ini.AddSetting("mutantwolfKillSettings", "DeathPortion", "0.75")
            ini.AddSetting("mutantwolfKillSettings", "DeathPortion2", "4.0")
            ini.AddSetting("mutantwolfKillSettings", "KillPortion2", "5.0")
            ini.AddSetting("boarKillSettings", "PercentageOrExtra", "1")
            ini.AddSetting("boarKillSettings", "KillPortion", "1.25")
            ini.AddSetting("boarKillSettings", "DeathPortion", "0.75")
            ini.AddSetting("boarKillSettings", "KillPortion2", "5.0")
            ini.AddSetting("boarKillSettings", "DeathPortion2", "4.0")
            ini.AddSetting("chickenKillSettings", "PercentageOrExtra", "1")
            ini.AddSetting("chickenKillSettings", "KillPortion", "1.25")
            ini.AddSetting("chickenKillSettings", "DeathPortion", "0.75")
            ini.AddSetting("chickenKillSettings", "KillPortion2", "5.0")
            ini.AddSetting("chickenKillSettings", "DeathPortion2", "4.0")
            ini.Save()
        return Plugin.GetIni("iConomy")

    def GetQuoted(self, array):
        text = str.join(" ", array)
        groups = text.split('"')
        n = len(groups)
        list = []
        for x in xrange(0, n):
            if x % 2 != 0:
                list.append(str(groups[x]))
        return list

    def Shop(self):
        return Plugin.GetIni("Shop")

    def TrytoGrabID(self, Player):
        try:
            id = Player.SteamID
            return id
        except:
            return None

    """
        Economy Methods
    """

    def HandleMoney(self, Aid, Vid):
        am = round(self.GetMoney(Aid), 2)
        vm = round(self.GetMoney(Vid), 2)
        if self.__MoneyMode__ == 0:
            return
        elif self.__MoneyMode__ == 1:
            if am == 0.0:
                amoney = round(float((am + 20.0) * self.__KillPortion__), 2)
            else:
                amoney = round(float(am * self.__KillPortion__), 2)
            vmoney = round(float(vm * self.__DeathPortion__), 2)
            DataStore.Add("iConomy", Aid, amoney)
            if vmoney < 0.0:
                DataStore.Add("iConomy", Vid, 0.0)
                return str(amoney - am) + ":0"
            DataStore.Add("iConomy", Vid, vmoney)
            return str(amoney - am) + ":" + str(vm - vmoney)
        else:
            amoney = round(float(am + self.__KillPortion2__), 2)
            vmoney = round(float(vm - self.__DeathPortion2__), 2)
            DataStore.Add("iConomy", Aid, amoney)
            if vmoney < 0.0:
                DataStore.Add("iConomy", Vid, 0.0)
                return str(self.__KillPortion2__) + ":0"
            DataStore.Add("iConomy", Vid, vmoney)
            return str(self.__KillPortion2__) + ":" + str(self.__DeathPortion2__)

    def GiveMoney(self, id, amount, Player = None, FromPlayer = None):
        if Player is not None and FromPlayer is None:
            Player.MessageFrom(self.__Sys__, "You magically found " + str(amount) + self.__MoneyMark__)
        elif Player is not None and FromPlayer is not None:
            Player.MessageFrom(self.__Sys__, "You got " + str(amount) + self.__MoneyMark__ + " from " + FromPlayer.Name)
        m = self.GetMoney(id)
        DataStore.Add("iConomy", id, m + float(amount))

    def TakeMoney(self, id, amount, Player=None):
        m = self.GetMoney(id)
        c = m - float(amount)
        if c < 0.0:
            return 12
        if Player is not None:
            Player.MessageFrom(self.__Sys__, "You magically lost " + str(amount) + self.__MoneyMark__)
        DataStore.Add("iConomy", id, c)

    def SetMoney(self, id, amount, Player=None):
        if float(amount) < 0.0:
            return 12
        if Player is not None:
            Player.MessageFrom(self.__Sys__, "Your balance magically changed to " + str(amount) + self.__MoneyMark__)
        DataStore.Add("iConomy", id, float(amount))

    def GetMoney(self, id):
        if DataStore.ContainsKey("iConomy", id):
            m = DataStore.Get("iConomy", id)
        else:
            m = self.__DefaultMoney__
            DataStore.Add("iConomy", id, float(m))
        return float(m)

    """
        CheckV method based on Spock's method.
        Upgraded by DreTaX
        Can Handle Single argument and Array args.
        V4.1
    """

    def GetPlayerName(self, namee):
        try:
            name = namee.lower()
            for pl in Server.Players:
                if pl.Name.lower() == name:
                    return pl
            return None
        except:
            return None

    def CheckV(self, Player, args):
        systemname = self.__Sys__
        count = 0
        if hasattr(args, '__len__') and (not isinstance(args, str)):
            p = self.GetPlayerName(str.join(" ", args))
            if p is not None:
                return p
            for pl in Server.Players:
                for namePart in args:
                    if namePart.lower() in pl.Name.lower():
                        p = pl
                        count += 1
                        continue
        else:
            nargs = str(args).lower()
            p = self.GetPlayerName(nargs)
            if p is not None:
                return p
            for pl in Server.Players:
                if nargs in pl.Name.lower():
                    p = pl
                    count += 1
                    continue
        if count == 0:
            Player.MessageFrom(systemname, "Couldn't find [color#00FF00]" + str.join(" ", args) + "[/color]!")
            return None
        elif count == 1 and p is not None:
            return p
        else:
            Player.MessageFrom(systemname, "Found [color#FF0000]" + str(count) + "[/color] player with similar name. [color#FF0000] Use more correct name!")
            return None

    def IsAnimal(self, Entity):
        s = str(Entity)
        if "NPC" in s:
            return True
        return False

    def isMod(self, id):
        if DataStore.ContainsKey("Moderators", id):
            return True
        return False

    def On_PluginInit(self):
        ini = self.iConomy()
        #Plugin Settings
        self.__MoneyMark__ = ini.GetSetting("Settings", "MoneyMark")
        self.__DefaultMoney__ = float(ini.GetSetting("Settings", "DefaultMoney"))
        self.__Sys__ = ini.GetSetting("Settings", "Sysname")
        #Player Settings!
        self.__MoneyMode__ = int(ini.GetSetting("PlayerKillSettings", "PercentageOrExtra"))
        self.__KillPortion__ = float(ini.GetSetting("PlayerKillSettings", "KillPortion"))
        self.__KillPortion2__ = float(ini.GetSetting("PlayerKillSettings", "KillPortion2"))
        self.__DeathPortion__ = float(ini.GetSetting("PlayerKillSettings", "DeathPortion"))
        self.__DeathPortion2__ = float(ini.GetSetting("PlayerKillSettings", "DeathPortion2"))
        DataStore.Add("iConomy", "MoneyMark", str(self.__MoneyMark__))
        DataStore.Add("iConomy", "SysName", str(self.__Sys__))
        DataStore.Add("iConomy", "DefaultMoney", str(self.__DefaultMoney__))
        DataStore.Add("iConomy", "MoneyMode", str(self.__MoneyMode__))
        DataStore.Add("iConomy", "KillP", str(self.__KillPortion__))
        DataStore.Add("iConomy", "KillP2", str(self.__KillPortion2__))
        DataStore.Add("iConomy", "DeathP", str(self.__DeathPortion__))
        DataStore.Add("iConomy", "DeathP2", str(self.__DeathPortion2__))

    def GetPrices(self, Player, args):
        shop = self.Shop()
        Count = int(shop.GetSetting(args, "Count"))
        if Count >= 1:
            Player.MessageFrom(self.__Sys__, teal + args + ":")
            for i in xrange(1, Count + 1):
                ItemName = shop.GetSetting(args, str(i))
                Player.Message(green + ItemName)
        else:
            Player.MessageFrom(self.__Sys__, "That category does not exist!")

    def BuyItem(self, Player, Item, Quantity):
        shop = self.Shop()
        Money = self.GetMoney(Player.SteamID)
        item = self.Item(Item)
        price = shop.GetSetting("BuyPrices", item)
        qty = int(Quantity)
        if bool(shop.GetSetting("Settings", "Buy")):
            if price:
                pricesum = int(price) * qty
                if pricesum <= Money:
                    Player.Inventory.AddItem(item, qty)
                    self.TakeMoney(Player.SteamID, pricesum, Player)
                    Player.MessageFrom(self.__Sys__, "You have bought " + str(qty) + " " + item + "(s).")
                else:
                    Player.MessageFrom(self.__Sys__, "You do not have enough money to buy " + str(qty) + " " + item + "(s).")
            else:
                Player.MessageFrom(self.__Sys__, "You can't buy " + item + ".")
                Player.MessageFrom(self.__Sys__, "Contact an admin to see if it will be added later!")
        else:
            Player.MessageFrom(self.__Sys__, "Sorry, buying has been disabled.")

    def SellItem(self, Player, Item, Quantity):
        shop = self.Shop()
        item = self.Item(Item)
        price = shop.GetSetting("SellPrices", item)
        qty = int(Quantity)
        if bool(shop.GetSetting("Settings", "Sell")):
            if price and int(price) > 0:
                salesum = int(price) * qty
                if Player.Inventory.HasItem(item, qty):
                    Player.Inventory.RemoveItem(item, qty)
                    self.GiveMoney(Player.SteamID, salesum)
                    Player.MessageFrom(self.__Sys__, "You have sold " + str(qty) + " " + item + "(s).")
                else:
                    Player.MessageFrom(self.__Sys__, "You either don't have the item or the quantity wanted to sell. Try again.")
            else:
                Player.MessageFrom(self.__Sys__, "You can't sell " + item + ".")
                Player.MessageFrom(self.__Sys__, "Contact an admin to see if it will be added later!")
        else:
           Player.MessageFrom(self.__Sys__, "Sorry, selling has been disabled.")

    def Item(self, i):
        shop = self.Shop()
        newItem = shop.GetSetting("ItemNames", i)
        return newItem

    def On_Command(self, Player, cmd, args):
        if cmd == "money":
            if len(args) == 0:
                m = self.GetMoney(Player.SteamID)
                Player.MessageFrom(self.__Sys__, "You have " + str(m) + self.__MoneyMark__)
                return
            if len(args) > 0 and Player.Admin or self.isMod(Player.SteamID):
                playerr = self.CheckV(Player, args)
                if playerr is None:
                    return
                Player.MessageFrom(self.__Sys__, playerr.Name + " has " + str(self.GetMoney(playerr.SteamID)) + self.__MoneyMark__)
        elif cmd == "pay":
            if len(args) == 0:
                Player.MessageFrom(self.__Sys__, 'Usage: /pay "PlayerName" "amount"')
            elif len(args) > 0:
                playerr = self.CheckV(Player, args[0])
                if playerr is None:
                    return
                m = self.GetMoney(Player.SteamID)
                if m < float(args[1]):
                    Player.MessageFrom(self.__Sys__, "You can't pay more than you currently have.")
                    return
                if playerr.SteamID == Player.SteamID:
                    Player.MessageFrom(self.__Sys__, "You can't pay money to yourself.")
                    return
                self.GiveMoney(playerr.SteamID, args[1], playerr, Player)
                self.TakeMoney(Player.SteamID, args[1])
                Player.MessageFrom(self.__Sys__, "You payed " + args[1] + self.__MoneyMark__  + " to " + playerr.Name)
        elif cmd == "takemoney":
            if len(args) == 0:
                Player.MessageFrom(self.__Sys__, 'Usage: /takemoney "PlayerName" "amount"')
            elif len(args) > 0:
                if Player.Admin:
                    playerr = self.CheckV(Player, args[0])
                    if playerr is None:
                        return
                    d = self.TakeMoney(playerr.SteamID, args[1], playerr)
                    if d == 12:
                        Player.MessageFrom(self.__Sys__, "Player would have negative money. Cancelling.")
                        return
                    Player.MessageFrom(self.__Sys__, "You took " + args[1] + self.__MoneyMark__  + " from " + playerr.Name)
        elif cmd == "setmoney":
            if len(args) == 0:
                Player.MessageFrom(self.__Sys__, 'Usage: /setmoney "PlayerName" "amount"')
            elif len(args) > 0:
                if Player.Admin:
                    playerr = self.CheckV(Player, args[0])
                    if playerr is None:
                        return
                    d = self.SetMoney(playerr.SteamID, args[1], playerr)
                    if d == 12:
                        Player.MessageFrom(self.__Sys__, "Player would have negative money. Cancelling.")
                        return
                    Player.MessageFrom(self.__Sys__, "You set " + playerr.Name + "'s balance to " + args[1] + self.__MoneyMark__)
        elif cmd == "givemoney":
            if len(args) == 0:
                Player.MessageFrom(self.__Sys__, 'Usage: /givemoney "PlayerName" "amount"')
            elif len(args) > 0:
                if Player.Admin:
                    playerr = self.CheckV(Player, args[0])
                    if playerr is None:
                        return
                    self.GiveMoney(playerr.SteamID, args[1], playerr)
                    Player.MessageFrom(self.__Sys__, "You gave " + args[1] + self.__MoneyMark__ + " to " + playerr.Name)
        elif cmd == "flushiconomy":
            if Player.Admin:
                DataStore.Flush('iConomy')
                Player.MessageFrom(self.__Sys__, "DataBase Flushed.")
                for p in Server.Players:
                    DataStore.Add('iConomy', p.SteamID, self.__DefaultMoney__)
                    p.MessageFrom(self.__Sys__, "iConomy DataBase was Flushed.")
        elif cmd == "shop":
            Player.MessageFrom(self.__Sys__, "Economy Commands: /money, /buy [Item] [Quantity], /sell [Item] [Quantity], /price")
        elif cmd == "buy":
            if len(args) == 2:
                leng = len(args)
                array = self.GetQuoted(args)
                if not '"' in args[leng - 1]:
                    Player.MessageFrom(self.__Sys__, 'Try: /buy "Item" "Quantity"')
                    Player.MessageFrom(self.__Sys__, 'Quote signs (") are required.')
                    return
                self.BuyItem(Player, array[0], array[1])
            else:
                Player.MessageFrom(self.__Sys__, 'Try: /buy "Item" "Quantity"')
                Player.MessageFrom(self.__Sys__, 'Quote signs (") are required.')
        elif cmd == "sell":
            if len(args) == 2:
                leng = len(args)
                array = self.GetQuoted(args)
                if not '"' in args[leng - 1]:
                    Player.MessageFrom(self.__Sys__, 'Try: /sell "Item" "Quantity"')
                    return
                self.SellItem(Player, array[0], array[1])
            else:
                Player.MessageFrom(self.__Sys__, 'Try: /sell "Item" "Quantity"')
        elif cmd == "price":
            if len(args) == 1:
                self.GetPrices(Player, args[0])
                return
            shop = self.Shop()
            Player.MessageFrom(self.__Sys__, "Try: /price [List]")
            Player.MessageFrom(self.__Sys__, teal + "Lists:")
            Count = int(shop.GetSetting("Categories", "Count"))
            for i in xrange(1, Count + 1):
                ListName = shop.GetSetting("Categories", str(i))
                Player.MessageFrom(self.__Sys__, green + ListName)


    def On_PlayerConnected(self, Player):
        sid = self.TrytoGrabID(Player)
        if sid is None:
            try:
                Player.Disconnect()
            except:
                pass
            return
        if not DataStore.ContainsKey("iConomy", sid):
            DataStore.Add("iConomy", sid, self.__DefaultMoney__)
        Player.MessageFrom(self.__Sys__, "You have " + str(DataStore.Get("iConomy", sid)) + self.__MoneyMark__)

    def On_PlayerKilled(self, DeathEvent):
        if DeathEvent.DamageType is not None and DeathEvent.Victim is not None and DeathEvent.Attacker is not None:
            shop = self.Shop()
            if not bool(shop.GetSetting("Settings", "PlayerKills")):
                return
            victim = str(DeathEvent.Victim.Name)
            id = self.TrytoGrabID(DeathEvent.Attacker)
            vid = self.TrytoGrabID(DeathEvent.Victim)
            if id is None:
                return
            if long(id) == long(vid):
                return
            shop = self.Shop()
            if not bool(shop.GetSetting("Settings", "PlayerKills")):
                return
            s = self.HandleMoney(id, vid)
            s = s.split(':')
            DeathEvent.Attacker.MessageFrom(self.__Sys__, "You found " + str(s[0]) + self.__MoneyMark__)
            if float(s[1]) == 0.0:
                victim.MessageFrom(self.__Sys__, "You lost all the money you had.")
                return
            victim.MessageFrom(self.__Sys__, "You lost " + str(s[1]) + self.__MoneyMark__)

    def On_NPCKilled(self, DeathEvent):
        if DeathEvent.Victim is not None and DeathEvent.Attacker is not None:
            aid = self.TrytoGrabID(DeathEvent.Attacker)
            if aid is None:
                return
            shop = self.Shop()
            if not bool(shop.GetSetting("Settings", "AnimalKills")):
                return
            name = DeathEvent.Victim.Name.lower()
            #NPC Settings
            ini = self.iConomy()
            if ini.GetSetting(name + "KillSettings", "PercentageOrExtra") is None:
                return
            NMoneyMode = ini.GetSetting(name + "KillSettings", "PercentageOrExtra")
            if int(NMoneyMode) == 0:
                return
            NKillPortion = float(ini.GetSetting(name + "KillSettings", "KillPortion"))
            NKillPortion2 = float(ini.GetSetting(name + "KillSettings", "KillPortion2"))
            Aid = round(float(DataStore.Get("iConomy", aid)), 2)
            if int(NMoneyMode) == 1:
                n = None
                c = round(Aid * NKillPortion, 2)
                if Aid == 0.0:
                    n = 20.0
                    c = round(n * NKillPortion, 2)
                DataStore.Add("iConomy", aid, c)
                if n is not None:
                   DeathEvent.Attacker.MessageFrom(self.__Sys__, "You received: " + str(c - Aid) + self.__MoneyMark__)
                else:
                    DeathEvent.Attacker.MessageFrom(self.__Sys__, "You received: " + str(c - Aid) + self.__MoneyMark__)
            else:
                c = Aid + NKillPortion2
                DataStore.Add("iConomy", aid, c)
                DeathEvent.Attacker.MessageFrom(self.__Sys__, "You received: " + str(NKillPortion2) + self.__MoneyMark__)