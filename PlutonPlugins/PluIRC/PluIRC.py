__author__ = 'DreTaX'
__version__ = '1.0'
__about__ = 'Communication on server, with the Pluton Staff'

import clr
clr.AddReferenceByPartialName("Pluton")

import Pluton
import sys
import socket
import re

path = Util.GetPublicFolder()
sys.path.append(path + "\\Python\\Lib\\")

try:
    import threading
    import random
except ImportError:
    raise ImportError("Download the extralibs!")


"""
    Global Variables
"""

sysname = "PluIRC"
server = "irc.freenode.net"
channel = "#pluton"

PlayersWithThreads = {

}

PlayersWithSockets = {

}

"""
    Global Methods
"""


def ColorText(color, part):
    return '<color=' + color + '>' + part + '</color>'

"""
    Class
"""


class PluIRC:

    def On_PluginDeinit(self):
        PlayersWithThreads.clear()
        for x in PlayersWithSockets.keys():
            PlayersWithSockets[x].close()
        PlayersWithSockets.clear()

    def On_PluginInit(self):
        Commands.Register("irc") \
            .setCallback("irc") \
            .setDescription("Contact staff on #pluton channel ingame.") \
            .setUsage("/irc - Join/Quit")

    def On_Chat(self, ChatEvent):
        Player = ChatEvent.User
        if Player in PlayersWithThreads.keys():
            irc = PlayersWithSockets[Player]
            msg = ChatEvent.OriginalText
            Player.MessageFrom(sysname, ColorText("teal", "You sent: ") + ColorText("green", msg))
            irc.send('PRIVMSG ' + channel + ' :' + msg + ' \r\n')
            ChatEvent.FinalText = ""

    def DefaultSample(self, Player):
        irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Player.MessageFrom(sysname, "Connecting to IRC.....")
        name = Player.Name.replace(' ', '')
        a = re.match('^[a-zA-Z0-9_!+?%()<>/\@#,.\\s\[\]-]+$', name)
        if not a:
            name = re.sub('^[a-zA-Z0-9_!+?%()<>/\@#,.\\s\[\]-]+$', "", name)
        if len(name) <= 2:
            name = "PlutonUser" + str(random.randint(1, 100))
        name = name + "-PluIRC"
        irc.connect((server, 6667))
        irc.send("USER " + name + " " + name + " " + name + " Just logging in:\n")
        irc.send("NICK " + name + "\n")
        # irc.send("PRIVMSG nickserv ) TODO
        irc.send("JOIN " + channel + "\n")
        PlayersWithSockets[Player] = irc
        Player.MessageFrom(sysname, ColorText("green", "Connected! Receiving messages..."))
        while 1:
            if Player not in PlayersWithThreads.keys():
                return
            try:
                text = irc.recv(2040)
            except:
                continue
            if text.find('PING') != -1:
                irc.send('PONG ' + text.split()[1] + '\r\n')
            else:
                if "Welcome to freenode - supporting the free and open source" not in text:
                    if "!~" in text:
                        text = text.split("!~")
                        Player.MessageFrom(sysname, ColorText("green", "[IRC]: " + ColorText("yellow",
                                                                                             text[0].replace(':', ''))))

    def irc(self, args, Player):
        args = Util.GetQuotedArgs(args)
        if not Player.Admin:
            Player.MessageFrom(sysname, ColorText("red", "You aren't an admin!"))
            return
        name = Player.Name
        if Player not in PlayersWithThreads.keys():
            Player.MessageFrom(sysname, ColorText("green", "Launching!"))
            setattr(self, name + "Caller", self.DefaultSample)
            caller = getattr(self, name + "Caller")
            t = threading.Thread(target=caller, args=(Player,))
            PlayersWithThreads[Player] = t
            t.start()
        else:
            if len(args) > 0:
                if args[0] == "list":
                    Player.MessageFrom(sysname, ColorText("blue", "Current Users Online: "))
                    PlayersWithSockets[Player].send("NAMES " + "\n")
                return
            Player.MessageFrom(sysname, ColorText("green", "Removing!"))
            PlayersWithThreads.pop(Player)
            PlayersWithSockets[Player].close()
            PlayersWithSockets.pop(Player)