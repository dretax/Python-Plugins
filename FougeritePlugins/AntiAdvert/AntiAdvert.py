__author__ = 'DreTaX'
__version__ = '1.0'
import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite
import re

whitelist = ["equinoxgamers.com", "dretaxmc.eu"]


class AntiAdvert:

    def On_Chat(self, Player, ChatEvent):
        if Player.Admin or Player.Moderator:
            return
        Text = ChatEvent.OriginalMessage.lower()
        Text = re.sub(r'[0-9]+(?:\.[0-9]+){3}', '', Text)
        a = re.findall(r'([\.a-z]*\.)(com|en|org|de|ro|ru|hu|eu)', Text)
        for x in a:
            n = str.join('', x)
            if n not in whitelist:
                Text = Text.replace(n, '')
        ChatEvent.NewText = Text
