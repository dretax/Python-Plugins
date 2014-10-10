import clr
import sys

clr.AddReferenceByPartialName("UnityEngine")
clr.AddReferenceByPartialName("Pluton")
import UnityEngine
import Pluton
from Pluton import InvItem
from System import *
from UnityEngine import *


class Test:
    def On_Respawn(self, re):
        re.GiveDefault = False
        loadout = None
        if re.Player.Admin:
            loadout = Server.LoadOuts["admin"]
        else:
            loadout = Server.LoadOuts["starter"]
        loadout.ToInv(re.Player.Inventory)

    def On_LoadingCommands(self):
        Commands.RegisterCommand("kit", " <name of the kit>", "Gives you the appropriate kit if you are eligible.")
        Commands.RegisterCommand("tpto", " \"<name of the player>\"", "Sends a teleport request to the selected player, use full name, if it qontains spaces then put the name in double quotes.")

    def On_PlayerConnected(self, player):
        for p in Server.ActivePlayers:
            if (p.Name != player.Name):
                p.Message(String.Format("{0} has joined the server!", player.Name))

    def On_PlayerDisconnected(self, player):
        for p in Server.ActivePlayers:
            if (p.Name != player.Name):
                p.Message(String.Format("{0} has left the server!", player.Name))

    def On_Command(self, cmd):
        Player = cmd.User
        args = cmd.args
        if cmd.cmd == "kit":
            if Player.Admin or Player.Moderator or Player.Owner:
                if len(args) == 0:
                    Player.Message("Available kits: starter, admin")
                    return
                if Server.LoadOuts.ContainsKey(args[0]):
                    loadout = Server.LoadOuts[args[0]]
                    loadout.ToInv(Player.Inventory)
                    return
                else:
                    Player.Message(String.Format("Kit {0} not found!", cmd.args[0]))
                    return
            else:
                Player.Message("You get the default kit on every respawn soo..")
                Player.Message("You can use /tpa for now")

        elif cmd.cmd == "tpto":
            if not cmd.User.Moderator:
                Player.Message("You aren't an admin!")
                return
            pl = Server.FindPlayer(cmd.quotedArgs[0])
            if pl is not None:
                cmd.User.Teleport(pl.Location)
                return
            else:
                cmd.User.Message(String.Format("Couldn't find player: {0}", cmd.quotedArgs[0]))
                return
        elif cmd.cmd == "tphere":
            if not cmd.User.Moderator:
                Player.Message("You aren't an admin!")
                return
            pl = Server.FindPlayer(cmd.quotedArgs[0])
            if pl is not None:
                pl.Teleport(Player.Location)
                return
            else:
                cmd.User.Message(String.Format("Couldn't find player: {0}", cmd.quotedArgs[0]))
                return