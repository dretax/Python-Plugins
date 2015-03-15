__author__ = 'DreTaX'
__version__ = '1.0'

import clr

clr.AddReferenceByPartialName("Pluton")
import Pluton
import Pluton.Events
import sys
arr = \
    ['DataStore', 'Server', 'Util', 'World', 'BuildingPart', 'ChatCommands',
        'ConsoleCommands', 'Entity', 'Inv', 'InvItem', 'LoadOut', 'LoadOutItem', 'NPC', 'OfflinePlayer',
        'Player', 'Zone2D'
    ]

event = \
    [
        'AuthEvent', 'BuildingEvent', 'ChatEvent',
        'ClientConsoleEvent', 'CombatEntityHurtEvent', 'CommandEvent', 'CommandPermissionEvent',
        'CorpseHurtEvent', 'CorpseInitEvent', 'CraftEvent', 'DeathEvent', 'DoorCodeEvent',
        'DoorUseEvent', 'EntityLootEvent', 'GatherEvent', 'HurtEvent', 'ItemLootEvent', 'LootEvent',
        'NPCDeathEvent', 'NPCHurtEvent',
        'PlayerDeathEvent', 'PlayerHurtEvent', 'PlayerLootEvent', 'PlayerTakeRadsEvent',
        'PlayerTakedmgEvent', 'RespawnEvent', 'ServerConsoleEvent'

    ]

class MethodVarsGetter:
    def On_PluginInit(self):
        for string in arr:
            globals()[string] = getattr(Pluton, string)
            for method in dir(globals()[string]):
                s = str(method)
                if s.startswith('__') and s.endswith('__'):
                    continue
                Plugin.Log(string, str(method))
        for string in event:
            globals()[string] = getattr(Pluton.Events, string)
            for method in dir(globals()[string]):
                s = str(method)
                if s.startswith('__') and s.endswith('__'):
                    continue
                Plugin.Log(string, str(method))