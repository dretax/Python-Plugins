__author__ = 'DreTaX'
__version__ = '1.1'
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
        Text = re.sub(r'[0-9]+(?:\.[0-9]+){3}(:[0-9]+)?', '', Text)
        a = re.findall(r'([\.a-z]*\.)(com|en|org|de|ro|ru|hu|eu|net)(:[0-9]+)', Text)
        for x in a:
            n = str.join('', x)
            if n not in whitelist:
                Text = Text.replace(n, '')
        if ChatEvent.OriginalMessage.lower() != Text:
            Plugin.Log("Test", "- " + Player.Name + " : " + ChatEvent.OriginalMessage.lower())
            Player.Message("Please do not advertise!")
        ChatEvent.NewText = Text
