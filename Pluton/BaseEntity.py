__author__ = 'DreTaX'
__version__ = '1.0'

"""
    This file was created for plugin developers to be able to use the correct functions
    without looking at the wiki or the api.
    API showoff purposes only, and nothing else.
"""

class BaseEntity:
    enableSaving = True
    model = None
    ragdoll = None
    flags = None
    parentEntity = None
    rpcCache = None
    globalBroadcast = None
    syncPosition = None
    parentBone = None
    radiationLevel = None
    currentTemperature = None

    def DebugServer(IntRep, FloatTime):
        return

    def OnDebugStart(self):
        return

    def HasFlag(BaseEntityFlags):
        return

    def SetFlag(BaseEntityFlags, bool):
        return

    def IsOn(self):
        return

    def IsOpen(self):
        return

    def IsOnFire(self):
        return

    def IsLocked(self):
        return

    def IsDebugging(self):
        return

    def IsDisabled(self):
        return

    def OnFlagsChanged(BaseEntityFlagsold, BaseEntityFlagsnext):
        return

    def GetParentEntity(self):
        return

    def SetParent(BaseEntity, stringstrBone = ""):
        return


    def SV_RPCMessage(uintnameID, NetworkMessage):
        return


    def ClientRPC(ConnectionsourceConnection, BasePlayer, stringfuncName, paramsobjectlistobj):
        return

    def ClientRPC(ConnectionsourceConnection, stringfuncName, paramsobjectobj):
        return

    def FindRPCMessage(uintnameID):
        return

    def RadiationExposureFraction(self):
        return 1.0

    def ServerInit(self):
        return

    def GetEstimatedWorldPosition(self):
        return

    def TransformChanged(self):
        return

    def DoMovingWithoutARigidBodyCheck(self):
        return

    def SpawnAsMapEntity(self):
        return

    def OnInvalidPosition(self):
        return

    def DropCorpse(stringCorpsePrefab):
        return

    def UpdateNetworkGroup(self):
        return

    def AddChild(BaseEntity):
        return

    def RemoveChild(BaseEntity):
        return

    def OnDeployed(BaseEntity):
        return

    def ShouldNetworkTo(BasePlayer):
        return

    def AttackerInfo(PlayerLifeStoryDeathInfo):
        return

    def Push(Vector3):
        return

    def SetVelocity(Vector3):
        return

    def SetAngularVelocity(Vector3):
        return

    def GetDropPosition(self):
        return

    def GetDropVelocity(self):
        return

    def SignalBroadcast(BaseEntitySignal, Connection):
        return

    def HasAnySlot(self):
        return

    def GetSlot(BaseEntitySlot):
        return

    def SetSlot(BaseEntitySlot, BaseEntity):
        return

    def HasSlot(BaseEntitySlot):
        return

    def ToPlayer(self):
        return

    def EnterTrigger(TriggerBase):
        return

    def LeaveTrigger(TriggerBase):
        return

    def RemoveFromTriggers(self):
        return

    def OnEnterWater(WaterLevel):
        return

    def OnLeaveWater(WaterLevel):
        return

    def OnThinkWater(self):
        return

    def Stability(self):
        return -1

    def Health(self):
        return 0.0

    def MaxHealth(self):
        return 0.0

    def OnAttacked(HitInfo):
        return

    def TestAttack(HitInfo):
        return

    def GetItem(self):
        return

    def GiveItem(Item):
        return

    def DistanceTo(BaseEntity):
        return

    def CanBeLooted(BasePlayer):
        return

    def Save(BaseNetworkableSaveInfo):
        return

    def Load(BaseNetworkableLoadInfo):
        return

    def SaveAll(Save):
        return

    def Signal(Enum):
        return

    def Slot(Enum):
        return

    def FindTargets(stringFilter, boolonlyPlayers):
        return