__author__ = 'DreTaX'
__version__ = '1.0'

import clr

clr.AddReferenceByPartialName("Pluton")
import Pluton

class TClans:

    """
        Clan Methods.
    """

    def ClansConfig(self):
        if not Plugin.IniExists("ClansConfig"):
            ini = Plugin.CreateIni("ClansConfig")
            ini.AddSetting("Settings", "Sys", "[Clans]")
            ini.Save()
        return Plugin.GetIni("ClansConfig")

    def Clans(self):
        if not Plugin.IniExists("Clans"):
            ini = Plugin.CreateIni("Clans")
            ini.Save()
        return Plugin.GetIni("Clans")

    def HasClan(self, ID):
        ini = self.Clans()
        if ini.GetSetting("ClanMembers", ID) is not None:
            return True
        if ini.GetSetting("ClanOwners", ID) is not None:
            return True
        return False

    def GetClanMember(self, Clan, ID):
        ini = self.Clans()
        if ini.GetSetting(Clan, ID) is not None:
            return ini.GetSetting(Clan, ID)
        return None

    def GetClanOfPlayer(self, ID):
        ini = self.Clans()
        if ini.GetSetting("ClanMembers", ID) is not None:
            return ini.GetSetting("ClanMembers", ID)
        if ini.GetSetting("ClanOwners", ID) is not None:
            return ini.GetSetting("ClanOwners", ID)
        return None

    def GetClanPopulation(self, Clan):
        ini = self.Clans()
        return len(ini.EnumSection(Clan))

    def GetClanRank(self, ID):
        ini = self.Clans()
        if ini.GetSetting("ClanMembers", ID) is not None:
            return 1
        if ini.GetSetting("ClanOfficers", ID) is not None:
            return 2
        if ini.GetSetting("ClanOwners", ID) is not None:
            return 3
        return None

    def CreateClan(self, Clan, ID, Name):
        ini = self.Clans()
        ini.AddSetting(Clan, ID, Name)
        ini.AddSetting("ClanOwners", ID, Name)
        ini.Save()

    def DeleteClan(self, Clan):
        ini = self.Clans()
        ini.DeleteSetting(Clan)
        sec = ini.EnumSection("ClanMembers")
        sec2 = ini.EnumSection("ClanOwners")
        sec3 = ini.EnumSection("ClanOfficers")
        for p in sec:
            n = ini.GetSetting("ClanMembers", p)
            if n == Clan:
                ini.DeleteSetting("ClanMembers", p)
        for p in sec2:
            n = ini.GetSetting("ClanOwners", p)
            if n == Clan:
                ini.DeleteSetting("ClanOwners", p)
        for p in sec3:
            n = ini.GetSetting("ClanOfficers", p)
            if n == Clan:
                ini.DeleteSetting("ClanOfficers", p)
        ini.Save()

    def AddPlayerToClan(self, Clan, ID, Name, Rank = None):
        ini = self.Clans()
        ini.AddSetting(Clan, ID, Name)
        if Rank == 1 or Rank == None:
            ini.AddSetting("ClanMembers", ID, Name)
        elif Rank == 2:
            ini.AddSetting("ClanOfficers", ID, Name)
        elif Rank == 3:
            ini.AddSetting("ClanOwners", ID, Name)
        ini.Save()

    def PromotePlayer(self, ID):
        ini = self.Clans()
        cur = self.GetClanRank(ID)
        if cur == 1:
            ini.DeleteSetting("ClanMembers", ID)
            ini.AddSetting("ClanOfficers", ID)
        elif cur == 2:
            ini.DeleteSetting("ClanOfficers", ID)
            ini.AddSetting("ClanOwners", ID)
        else:
            return None
        ini.Save()

    def DemotePlayer(self, ID):
        ini = self.Clans()
        cur = self.GetClanRank(ID)
        if cur == 2:
            ini.DeleteSetting("ClanOfficers", ID)
            ini.AddSetting("ClanMembers", ID)
        elif cur == 3:
            ini.DeleteSetting("ClanOwners", ID)
            ini.AddSetting("ClanOfficers", ID)
        else:
            return None
        ini.Save()

    def RemovePlayerFromClan(self, Clan, ID):
        ini = self.Clans()
        ini.DeleteSetting(Clan, ID)
        ini.DeleteSetting("ClanMembers", ID)
        ini.Save()

    def GetClanMembers(self, Clan):
        ini = self.Clans()
        sec = ini.EnumSection(Clan)
        s = ""
        for m in sec:
            s = s + m +", "
        return s

    """
        Events/Methods.
    """

    #TODO: Start working out the commands, and the events.