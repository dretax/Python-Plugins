__author__ = 'DreTaX'
__version__ = '1.0'

import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite

"""
    Class
"""

# Use notifications instead of messages? False/True
Notice = False
sys = "DamageDisplay"


class DamageDisplay:

    def On_PlayerHurt(self, HurtEvent):
        if HurtEvent.Attacker is None or HurtEvent.Victim is None:
            return
        if HurtEvent.AttackerIsPlayer and HurtEvent.VictimIsPlayer:
            if Notice:
                HurtEvent.Attacker.Notice("Remaining Health: " + str(HurtEvent.Victim.Health))
            else:
                HurtEvent.Attacker.MessageFrom(sys, "Remaining Health: " + str(HurtEvent.Victim.Health))

    def On_NPCHurt(self, HurtEvent):
        if HurtEvent.Attacker is None or HurtEvent.Victim is None:
            return
        if HurtEvent.AttackerIsPlayer:
            if Notice:
                HurtEvent.Attacker.Notice("Remaining Health: " + str(HurtEvent.Victim.Health))
            else:
                HurtEvent.Attacker.MessageFrom(sys, "Remaining Health: " + str(HurtEvent.Victim.Health))
