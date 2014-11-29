__author__ = 'DreTaX'


class PlayerList:

    def On_Command(self, cmd):
        Player = cmd.User
        if cmd.cmd == "players":
            all = ""
            for pl in Server.ActivePlayers:
                all = all + str(pl.Name) + ", "
            Player.MessageFrom("Online Players", all)