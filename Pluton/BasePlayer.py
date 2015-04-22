__author__ = 'DreTaX'
__version__ = '1.0'

"""
    This file was created for plugin developers to be able to use the correct functions
    without looking at the wiki or the api.
    API showoff purposes only, and nothing else.
"""

class BasePlayer:
    sleepingPlayerList = None
    playerModel = None
    networkQueue = None
    playerFlags = None
    vActiveItem = None
    eyes = None
    inventory = None
    blueprints = None
    metabolism = None
    input = None
    movement = None
    collision = None
    belt = None
    userID = None
    displayName = None
    hasPreviousLife = None
    estimatedVelocity = None
    estimatedSpeed = None
    currentComfort = None
    timeSinceLastTick = None
    isStalled = None
    wasStalled = None
    secondsSinceWoundedStarted = None


    def CanBeLooted(BasePlayer):
        return

    def RPC_LootPlayer(BaseEntityRPCMessage):
        return

    def RPC_Assist(BaseEntityRPCMessage):
        return


    def GetQueuedUpdateCount(BasePlayerNetworkQueue):
        return

    def SendSnapshots(BaseNetworkableList):
        return

    def QueueUpdate(BasePlayerNetworkQueue, BaseNetworkable):
        return

    def SendPositionUpdate(FloatDeltaTime):
        return

    def SendEntityUpdate(FloatDeltaTime):
        return

    def HasPlayerFlag(BasePlayerPlayerFlags):
        return


    def IsReceivingSnapshot(self):
        return


    def IsAdmin(self):
        return

    def IsDeveloper(self):
        return


    def SetPlayerFlag(BasePlayerPlayerFlags, b):
        return


    def IsSleeping(self):
        return


    def IsSpectating(self):
        return


    def SetInsideBuildingPrivilege(BuildingPrivlidgeprivlidge, inside):
        return

    def CanBuild(self):
        return

    def OnProjectileAttack(BaseEntityRPCMessage):
        return

    def HasNoteFiredProjectile(int):
        return


    def NoteFiredProjectile(ItemDefinition, int):
        return

    def SharedProjectileAttack(HitInfo):
        return


    def Save(BaseNetworkableSaveInfo):
        return


    def Load(BaseNetworkableLoadInfo):
        return

    def IsConnected(self):
        return

    def ServerInit(self):
        return

    def PlayerInit(Connection):
        return

    def SendDeathInformation(self):
        return

    def SendRespawnOptions(self):
        return


    def StartSleeping(self):
        return

    def EndSleeping(self):
        return

    def EndLooting(self):
        return

    def OnDisconnected(self):
        return

    def SendFullSnapshot(self):
        return

    def GetNetworkRotation(self):
        return

    def CheckDeathCondition(HitInfo):
        return

    def OnKilled(HitInfo):
        return

    def Respawn(newPos = True):
        return

    def IsImmortal(self):
        return

    def Hurt(HitInfo):
        return

    def FindByID(ulonguserID):
        return

    def FindSleeping(ulonguserID):
        return

    def Command(stringstrCommand, paramsobjectarguments):
        return


    def OnInvalidPosition(self):
        return

    def Find(stringstrNameOrIDOrIP):
        return

    def SendConsoleCommand(stringcommand, paramsobjectobj):
        return

    def SendEffect(stringeffectName):
        return

    def UpdateRadiation(floatfAmount):
        return

    def RadiationExposureFraction(self):
        return

    def OnHealthChanged(floatoldvalue, floatnewvalue):
        return

    def SV_ClothingChanged(self):
        return

    def GiveItem(Item):
        return

    def AttackerInfo(PlayerLifeStoreDeathInfo):
        return

    def Die(HitInfo = None):
        return

    def Kick(stringreason):
        return

    def GetDropPosition(self):
        return

    def GetDropVelocity(self):
        return

    def UpdateSpectateTarget(stringstrName):
        return

    def StartSpectating(self):
        return

    def StopSpectating(self):
        return

    def Teleport(stringstrName, playersOnly):
        return

    def OnReceivedTick(bytelistmsg):
        return

    def CanMoveTo(Vector3):
        return

    def IsWounded(self):
        return

    def StartWounded(self):
        return

    def ToPlayer(self):
        return

    def StartHealth(self):
        return

    def StartMaxHealth(self):
        return 100

    def Awake(self):
        return

    def InitShared(self):
        return

    def DestroyShared(self):
        return

    def Update(self):
        return

    def MaxDeployDistance(Item):
        return 8

    def GetSpeed(bRunning, bDucking):
        return

    def OnAttacked(HitInfo):
        return

    def UpdatePlayerCollider(bEnabled, bDucked):
        return

    def CanAttack(self):
        return

    def IsOnGround(self):
        return

    def IsRunning(self):
        return

    def IsDucked(self):
        return

    def ChatMessage(stringmsg):
        return

    def ConsoleMessage(stringmsg):
        return

    def CameraMode(Enum):
        return

    def NetworkQueue(Enum):
        return

    queueInternal = None
    Length = None

    def Contains(BaseNetworkableent):
        return

    def Add(BaseNetworkableent):
        return

    def Add(BaseNetworkableent):
        return

    def PlayerFlags(Enum):
        return