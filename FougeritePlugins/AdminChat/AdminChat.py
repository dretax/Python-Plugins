__author__ = 'DreTaX'
__version__ = '1.0'

import clr
clr.AddReferenceByPartialName("Fougerite")
import Fougerite

"""
    Class
"""

# Set It to False to disable
EnableForModerators = True

teal = "[color #00FFFF]"
green = "[color #009900]"
class AdminChat:

    """
        Methods
    """

    def On_PluginInit(self):
        Util.ConsoleLog("AdminChat by " + __author__ + " Version: " + __version__ + " loaded.", False)

    def On_Command(self, Player, cmd, args):
        if cmd == "adc":
            if Player.Admin or (Player.Moderator and EnableForModerators):
                if len(args) == 0:
                    Player.MessageFrom("AdminChat", "Usage /adc sentence")
                    return
                name = Player.Name
                sentence = str.join(" ", args)
                for x in Server.Players:
                    if x.Admin or (x.Moderator and EnableForModerators):
                        x.MessageFrom("AdminChat", green + name + " => " + teal + sentence)