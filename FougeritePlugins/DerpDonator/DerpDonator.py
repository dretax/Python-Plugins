__author__ = 'DreTaX'
__version__ = '1.0'
import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite

path = Util.GetRootFolder()
import sys
import datetime
sys.path.append(path + "\\Save\\Lib\\")

try:
    import random
    import string
except ImportError:
    raise ImportError("We need the LIBS!")

sysn = "DerpDonator"

Ranks = {
    1: 'Donator',
    2: 'BronzeDonator',
    3: 'SilverDonator',
    4: 'GoldDonator',
    5: 'VIPDonator',
    6: 'D-Staff',
    7: 'D-Mod',
    8: 'D-Admin',
    9: 'D-OP'
}

Tags = {
    1: 'Donator',
    2: 'Bronze',
    3: 'Silver',
    4: 'Gold',
    5: 'VIP',
    6: 'D-Staff',
    7: 'D-Mod',
    8: 'D-Admin',
    9: 'D-OP'
}

teal = "[color #00FFFF]"
gold = "[color #EEC900]"
silver = "[color #BFBFBF]"
bronze = "[color #A67D3D]"
yellow = "[color #EEEE00]"
red = "[color #FF0000]"
Donators = {

}

Colors = {

}

Selected = {

}
class DerpDonator:

    def On_PluginInit(self):
        self.Items()
        self.Users()
        cl = self.Colors()
        enum = cl.EnumSection("Colors")
        for name in enum:
            code = cl.GetSetting("Colors", name)
            Colors[name] = str(code)
        Plugin.CreateTimer("Announcement", 60000 * 10).Start()

    def GenerateKey(self, size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def Users(self):
        if not Plugin.IniExists("Users"):
            ini = Plugin.CreateIni("Users")
            ini.Save()
        return Plugin.GetIni("Users")

    def Colors(self):
        if not Plugin.IniExists("Colors"):
            ini = Plugin.CreateIni("Colors")
            ini.AddSetting("Colors", "red", "#FF0000")
            ini.Save()
        return Plugin.GetIni("Colors")


    def Items(self):
        if not Plugin.IniExists("Items"):
            ini = Plugin.CreateIni("Items")
            ini.AddSetting("2", "Supply Signal", "1")
            ini.AddSetting("3", "Supply Signal", "1")
            ini.AddSetting("3", "P250", "1")
            ini.AddSetting("3", "Shotgun", "1")
            ini.AddSetting("3", "Leather Helmet", "1")
            ini.AddSetting("3", "Leather Vest", "1")
            ini.AddSetting("3", "Leather Pants", "1")
            ini.AddSetting("3", "Leather Boots", "1")
            ini.AddSetting("3", "9mm Ammo", "100")
            ini.AddSetting("4", "Supply Signal", "2")
            ini.AddSetting("4", "Bolt Action Rifle", "1")
            ini.AddSetting("4", "Research Kit 1", "1")
            ini.AddSetting("4", "Kevlar Helmet", "1")
            ini.AddSetting("4", "Kevlar Vest", "1")
            ini.AddSetting("4", "Kevlar Pants", "1")
            ini.AddSetting("4", "Kevlar Boots", "1")
            ini.AddSetting("4", "Shotgun", "1")
            ini.AddSetting("4", "556 Ammo", "100")
            ini.AddSetting("5", "Supply Signal", "3")
            ini.AddSetting("5", "Bolt Action Rifle", "1")
            ini.AddSetting("5", "Research Kit 1", "3")
            ini.AddSetting("5", "Kevlar Helmet", "1")
            ini.AddSetting("5", "Kevlar Vest", "1")
            ini.AddSetting("5", "Kevlar Pants", "1")
            ini.AddSetting("5", "Kevlar Boots", "1")
            ini.AddSetting("5", "Wood Planks", "500")
            ini.AddSetting("5", "Large Medkit", "5")
            ini.AddSetting("5", "P250", "1")
            ini.AddSetting("5", "M4", "1")
            ini.AddSetting("5", "Shotgun", "1")
            ini.AddSetting("5", "556 Ammo", "250")
            ini.Save()
        return Plugin.GetIni("Items")

    def ValidUser(self, Player):
        if Player.Admin:
            return True
        Player.MessageFrom(sysn, "You aren't an admin!")
        return False

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
            Player.MessageFrom(sysn, "Couldn't find [color#00FF00]" + str.join(" ", args) + "[/color]!")
            return None
        elif count == 1 and p is not None:
            return p
        else:
            Player.MessageFrom(sysn, "Found [color#FF0000]" + str(count) +
                               "[/color] player with similar name. [color#FF0000] Use more correct name!")
            return None

    def bool(self, s):
        if s.lower() == 'true':
            return True
        elif s.lower() == 'false':
            return False
        else:
            raise ValueError

    def On_Chat(self, Player, ChatEvent):
        if Player in Donators.keys() and Player in Selected.keys():
            Text = ChatEvent.ToString()
            ChatEvent.NewText = "          "  # New text doesnt work when you color the msg?!
            c = "[color " + Selected[Player] + "] " + Text
            c = c.replace('"', '')
            Server.BroadcastFrom(Player.Name, c)

    def On_PlayerDisconnected(self, Player):
        if Player in Donators.keys():
            Donators.pop(Player, None)
        if Player in Selected.keys():
            Selected.pop(Player, None)

    def On_PlayerConnected(self, Player):
        id = Player.SteamID
        ini = self.Users()
        if ini.GetSetting(id, "Expires") is not None:
            b = ini.GetSetting(id, "Expires")
            n = b.split('-')
            date = datetime.date(int(n[0]), int(n[1]), int(n[2]))
            adrank = int(ini.GetSetting(id, "AdminRank"))
            if datetime.date.today() > date and 0 == adrank:
                Player.MessageFrom(sysn, red + "Your donator rank expired!")
                used = ini.GetSetting(id, "DateUsed")
                Plugin.Log("Expire", "-----")
                Plugin.Log("Expire", Player.Name + "|" + id + "| Rank expired.")
                Plugin.Log("Expire", "Used: " + used + " Expired: " + b)
                for x in ini.EnumSection(id):
                    ini.DeleteSetting(id, x)
                ini.Save()
            elif datetime.date.today() > date and 0 < adrank:
                rn = int(ini.GetSetting(id, "AdminRank"))
                Donators[Player] = rn
                Player.Name = "[" + Tags[rn] + "] " + Player.Name
            else:
                rn = int(ini.GetSetting(id, "Rank"))
                Donators[Player] = rn
                if 0 < adrank:
                    rn = adrank
                Player.Name = "[" + Tags[rn] + "] " + Player.Name

    def On_Command(self, Player, cmd, args):
        id = Player.SteamID
        ini = self.Users()
        if cmd == "dgenerate":
            if not self.ValidUser(Player):
                return
            rr = str(Ranks)
            rr = rr.replace('{', '')
            rr = rr.replace('}', '')
            rr = rr.replace("'", "")
            if len(args) != 1:
                Player.MessageFrom(sysn, "Usage: /dgenerate ranklevelnumber")
                Player.MessageFrom(sysn, rr)
                return
            key = self.GenerateKey()
            level = str.join(' ', args)
            if not level.isnumeric():
                Player.MessageFrom(sysn, "Specify a number.")
                Player.MessageFrom(sysn, rr)
                return
            level = int(level)
            if level not in Ranks.keys():
                Player.MessageFrom(sysn, "Couldn't find rank number!")
                Player.MessageFrom(sysn, rr)
                return
            Player.MessageFrom(sysn, "============================")
            Player.MessageFrom(sysn, "Generated key: " + key)
            Player.MessageFrom(sysn, "Key level: " + Ranks[level])
            Player.MessageFrom(sysn, "Any user is now allowed to use It")
            Player.MessageFrom(sysn, "============================")
            ini.AddSetting("Keys", key, str(level))
            ini.Save()
        elif cmd == "dusekey":
            if len(args) != 1:
                Player.MessageFrom(sysn, "Usage: /dusekey key")
                return
            key = str.join(' ', args)
            if ini.GetSetting("Keys", key) is None and not ini.GetSetting("Keys", key):
                Player.MessageFrom(sysn, "Couldn't find key!")
                return
            rank = int(ini.GetSetting("Keys", key))
            date = datetime.date.today()
            end_date = date + datetime.timedelta(days=30)
            Player.MessageFrom(sysn, "============================")
            Player.MessageFrom(sysn, "Used Key! " + key)
            Player.MessageFrom(sysn, "Usage of Date: " + str(date))
            Player.MessageFrom(sysn, "Type /ditems to receive your items!")
            Player.MessageFrom(sysn, "============================")
            ini.DeleteSetting("Keys", key)
            adn = 0
            if ini.GetSetting(id, "Rank") is not None:
                adn = int(ini.GetSetting(id, "AdminRank"))
                ini.SetSetting(id, "Name", Player.Name)
                ini.SetSetting(id, "Rank", str(rank))
                ini.SetSetting(id, "RankName", Ranks[rank])
                ini.SetSetting(id, "Expires", str(end_date))
                ini.SetSetting(id, "KeyUsed", str(key))
                ini.SetSetting(id, "ItemsReceived", "False")
                if adn > 0:
                    ini.SetSetting(id, "AdminRank", str(adn))
                else:
                    ini.SetSetting(id, "AdminRank", "0")
            else:
                ini.AddSetting(id, "Name", Player.Name)
                ini.AddSetting(id, "Rank", str(rank))
                ini.AddSetting(id, "RankName", Ranks[rank])
                ini.AddSetting(id, "DateUsed", str(date))
                ini.AddSetting(id, "KeyUsed", str(key))
                ini.AddSetting(id, "ItemsReceived", "False")
                ini.AddSetting(id, "Expires", str(end_date))
                if rank > 5:
                    ini.AddSetting(id, "AdminRank", str(rank))
                else:
                    ini.AddSetting(id, "AdminRank", "0")
            ini.Save()
            if adn == 0 or rank <= 5:
                Server.BroadcastFrom(sysn, red + "Just bought " + Tags[rank] + " !")
                Server.BroadcastFrom(sysn, red + "Thanks for supporting!")
            Donators[Player] = rank
            if adn > 0:
                Player.Name = "[" + Tags[adn] + "] " + Player.Name
            else:
                Player.Name = "[" + Tags[rank] + "] " + Player.Name
        elif cmd == "dplayer":
            if not self.ValidUser(Player):
                return
            if len(args) == 0:
                Player.MessageFrom(sysn, "Usage: /dplayer playername")
                return
            playerr = self.CheckV(Player, args)
            if playerr is None:
                return
            idr = playerr.SteamID
            if ini.GetSetting(idr, "Rank") is not None:
                Player.MessageFrom(sysn, "============================")
                Player.MessageFrom(sysn, "Name: " + playerr.Name)
                Player.MessageFrom(sysn, "Rank: " + ini.GetSetting(idr, "RankName"))
                Player.MessageFrom(sysn, "DateUsed: " + ini.GetSetting(idr, "DateUsed"))
                Player.MessageFrom(sysn, "Expires: " + ini.GetSetting(idr, "Expires"))
                Player.MessageFrom(sysn, "Requested Items: " + ini.GetSetting(idr, "ItemsReceived"))
                Player.MessageFrom(sysn, "Rank: " + ini.GetSetting(idr, "RankName"))
                Player.MessageFrom(sysn, "AdminRank: " + ini.GetSetting(idr, "AdminRank"))
                Player.MessageFrom(sysn, "============================")
            else:
                Player.MessageFrom(sysn, playerr.Name + " is not a donator.")
        elif cmd == "dinfo":
            rr = str(Ranks)
            rr = rr.replace('{', '')
            rr = rr.replace('}', '')
            rr = rr.replace("'", "")
            if len(args) != 1:
                Player.MessageFrom(sysn, "Usage: /dinfo ranknumber")
                Player.MessageFrom(sysn, rr)
                return
            level = str.join(' ', args)
            if not level.isnumeric():
                Player.MessageFrom(sysn, "Specify a number.")
                Player.MessageFrom(sysn, rr)
                return
            level = int(level)
            if level not in Ranks.keys():
                Player.MessageFrom(sysn, "Couldn't find rank number!")
                Player.MessageFrom(sysn, rr)
                return
            if level > 5:
                Player.MessageFrom(sysn, "No info for this rank.")
                return
            rank = Ranks.get(level)
            method = getattr(self, rank + "Info")
            method(Player)
        elif cmd == "ditems":
            if Player in Donators:
                if ini.GetSetting(id, "ItemsReceived") is not None:
                    b = self.bool(ini.GetSetting(id, "ItemsReceived"))
                    if not b:
                        rank = ini.GetSetting(id, "Rank")
                        if Donators[Player] > 5:
                            Player.MessageFrom(sysn, "You aren't a true donator. You can't get Items.")
                            return
                        ini2 = self.Items()
                        enum = ini2.EnumSection(rank)
                        if Player.Inventory.FreeSlots < len(enum):
                            Player.MessageFrom(sysn, "You need to have atleast " + str(len(enum))
                                               + " free slots in your inventory!")
                            return
                        for item in enum:
                            c = int(ini2.GetSetting(rank, item))
                            Player.Inventory.AddItem(item, c)
                        ini.SetSetting(id, "ItemsReceived", "True")
                        ini.Save()
                        Player.MessageFrom(sysn, "You received your items!")
                    else:
                        Player.MessageFrom(sysn, "You already got your items!")
                else:
                    Player.MessageFrom(sysn, "You aren't a donator!")
            else:
                Player.MessageFrom(sysn, "You aren't a donator!")
        elif cmd == "dcolor":
            if Player in Donators:
                if Donators[Player] > 5:
                    Player.MessageFrom(sysn, "You aren't a true donator. You can't get Items.")
                    return
                color = str.join(' ', args)
                if Colors.get(color) is None:
                    Player.MessageFrom(sysn, "Couldn't find color!")
                    Player.MessageFrom(sysn, "List of colors: ")
                    for x in Colors.keys():
                        Player.MessageFrom(sysn, "- " + str(x))
                    return
                Selected[Player] = Colors.get(color)
                Player.MessageFrom(sysn, "Color set!")
            else:
                Player.MessageFrom(sysn, "You aren't a donator!")
        elif cmd == "dkeys":
            Player.MessageFrom(sysn, "List of keys:")
            enum = ini.EnumSection("Keys")
            for key in enum:
                rank = Tags[int(ini.GetSetting("Keys", key))]
                Player.MessageFrom(sysn, "Key: " + key + " Rank: " + rank)
        elif cmd == "dhelp":
            Player.MessageFrom(sysn, "More INFO on TeamSpeak3! ts.derpteamgames.com")
            Player.MessageFrom(sysn, "/dinfo - View ranks")
            Player.MessageFrom(sysn, "/dusekey - Use your key to get your rank.")
            Player.MessageFrom(sysn, "/ditems - Receive donator items")
            Player.MessageFrom(sysn, "/dcolor - Set a color for the chat")
            if Player.Admin:
                Player.MessageFrom(sysn, "/dgenerate - Generate a key.")
                Player.MessageFrom(sysn, "/dplayer - Get information about player")
                Player.MessageFrom(sysn, "/dkeys - Lists all the keys")

    def AnnouncementCallback(self, timer):
        timer.Kill()
        Server.BroadcastNotice("Donation info: /dhelp")
        Plugin.CreateTimer("Announcement", 60000 * 10).Start()

    """
        Rank info
    """

    def DonatorInfo(self, Player):
        Player.MessageFrom(sysn, yellow + "Donator Rank - $2")
        ini = self.Items()
        for item in ini.EnumSection("1"):
            Player.MessageFrom(sysn, item + " - " + ini.GetSetting("1", item))
        Player.MessageFrom(sysn, "Colored Chat In Game For 1 Month")

    def BronzeDonatorInfo(self, Player):
        Player.MessageFrom(sysn, bronze + "Bronze Donator Rank - $5")
        ini = self.Items()
        for item in ini.EnumSection("2"):
            Player.MessageFrom(sysn, item + " - " + ini.GetSetting("2", item))
        Player.MessageFrom(sysn, "Colored Chat In Game For 1 Month")
        Player.MessageFrom(sysn, "TeamSpeak Donator Room For 2 Months")

    def SilverDonatorInfo(self, Player):
        Player.MessageFrom(sysn, silver + "Silver Donator Rank - $10")
        ini = self.Items()
        for item in ini.EnumSection("3"):
            Player.MessageFrom(sysn, item + " - " + ini.GetSetting("3", item))
        Player.MessageFrom(sysn, "Colored Chat In Game For 1 Month")
        Player.MessageFrom(sysn, "TeamSpeak Donator Room For 3 Months")

    def GoldDonatorInfo(self, Player):
        Player.MessageFrom(sysn, gold + "Gold Donator Rank - $15")
        ini = self.Items()
        for item in ini.EnumSection("4"):
            Player.MessageFrom(sysn, item + " - " + ini.GetSetting("4", item))
        Player.MessageFrom(sysn, "Colored Chat In Game For 1 Months")
        Player.MessageFrom(sysn, "TeamSpeak Donator Room For 4 Months")

    def VIPDonatorInfo(self, Player):
        Player.MessageFrom(sysn, teal + "VIP Donator Rank - $20")
        ini = self.Items()
        for item in ini.EnumSection("5"):
            Player.MessageFrom(sysn, item + " - " + ini.GetSetting("5", item))
        Player.MessageFrom(sysn, "Colored Chat In Game For 6 Months")
        Player.MessageFrom(sysn, "TeamSpeak Donator Room For 4 Months")