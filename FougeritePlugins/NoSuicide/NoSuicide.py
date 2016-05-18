__author__ = 'DreTaX'
__version__ = '1.0'

import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite


class NoSuicide:

    def On_PlayerHurt(self, HurtEvent):
        if HurtEvent.AttackerIsPlayer and HurtEvent.VictimIsPlayer:
            if HurtEvent.Attacker is None or HurtEvent.Victim is None:
                return
            if HurtEvent.Attacker.UID == HurtEvent.Victim.UID:
                if HurtEvent.DamageType == "Bleeding" and str(HurtEvent.DamageAmount) == "inf" \
                        and HurtEvent.WeaponName == "Fall Damage":
                    HurtEvent.DamageAmount = 0
                    HurtEvent.Victim.MessageFrom("NoSuicide", "Why would you kill yourself retard?")
