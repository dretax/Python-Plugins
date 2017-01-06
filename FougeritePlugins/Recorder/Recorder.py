__author__ = "DreTaX"
__version__ = "1.2.1"
import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite
from Fougerite import Entity
import sys
path = Util.GetRootFolder()
sys.path.append(path + "\\Save\\Lib\\")

try:
    import random
except ImportError:
    raise ImportError("Get IronPython libs!")

prefabs = {
    "SingleBed": ";deploy_singlebed",
    "MetalCeiling": ";struct_metal_ceiling",
    "MetalDoorFrame": ";struct_metal_doorframe",
    "MetalFoundation": ";struct_metal_foundation",
    "MetalPillar": ";struct_metal_pillar",
    "MetalRamp": ";struct_metal_ramp",
    "MetalStairs": ";struct_metal_stairs",
    "MetalWall": ";struct_metal_wall",
    "MetalWindowFrame": ";struct_metal_windowframe",
    "WoodCeiling": ";struct_wood_ceiling",
    "WoodDoorFrame": ";struct_wood_doorway",
    "WoodFoundation": ";struct_wood_foundation",
    "WoodPillar": ";struct_wood_pillar",
    "WoodRamp": ";struct_wood_ramp",
    "WoodStairs": ";struct_wood_stairs",
    "WoodWall": ";struct_wood_wall",
    "WoodWindowFrame": ";struct_wood_windowframe",
    "Campfire": ";deploy_camp_bonfire",
    "ExplosiveCharge": ";explosive_charge",
    "Furnace": ";deploy_furnace",
    "LargeWoodSpikeWall": ";deploy_largewoodspikewall",
    "WoodBoxLarge": ";deploy_wood_storage_large",
    "MetalDoor": ";deploy_metal_door",
    "MetalBarsWindow": ";deploy_metalwindowbars",
    "RepairBench": ";deploy_repairbench",
    "SleepingBagA": ";deploy_camp_sleepingbag",
    "SmallStash": ";deploy_small_stash",
    "WoodSpikeWall": ";deploy_woodspikewall",
    "Barricade_Fence_Deployable": ";deploy_wood_barricade",
    "WoodGate": ";deploy_woodgate",
    "WoodGateway": ";deploy_woodgateway",
    "Wood_Shelter": ";deploy_wood_shelter",
    "WoodBox": ";deploy_wood_box",
    "WoodenDoor": ";deploy_wood_door",
    "Workbench": ";deploy_workbench"
}


class Recorder:

    st = None

    def On_PluginInit(self):
        DataStore.Flush("Recorder")
        DataStore.Flush("RecorderInit")
        self.st = Util.TryFindReturnType("StructureComponent")


    def On_Command(self, Player, cmd, args):
        if cmd == "record":
            if not Player.Admin:
                Player.MessageFrom("Recorder", "No Permissions")
                return
            id = Player.SteamID
            state = DataStore.Get("Recorder", id)
            if len(args) == 0:
                Player.MessageFrom("Recorder", "Usage: /record name")
                return
            name = args[0]
            if state is not None:
                Player.MessageFrom("Recorder", "Already Recording!")
                return
            DataStore.Flush("RecordedData" + Player.SteamID)
            DataStore.Add("Recorder", id, 1)
            DataStore.Add("Recorder_Name", id, name)
            Player.Message("Recording " + name + ".ini (/stop to finish!)")
        elif cmd == "spawn":
            if not Player.Admin:
                Player.MessageFrom("Recorder", "No Permissions")
                return
            id = Player.SteamID
            if len(args) <= 1:
                Player.MessageFrom("Recorder", "Usage: /spawn name distance")
                return
            file = Plugin.GetIni("Buildings\\" + args[0])
            if file is None:
                Player.Message("Building not found !")
                return
            if not args[1].isnumeric():
                Player.MessageFrom("Recorder", "Usage: /spawn name distance")
                return
            DataStore.Flush("SpawnedData" + id)
            DataStore.Remove("RecorderSMs", id)

            playerFront = Util.Infront(Player, float(args[1]))
            playerFront.y = World.GetGround(playerFront.x, playerFront.z)
            a = []
            array = file.Sections
            for x in array:
                if x != "Init":
                    a.append(x)
            cpt = len(a)
            for i in xrange(0, cpt):
                entPos = Util.CreateVector(float(file.GetSetting("Part" + str(i), "PosX")),
                                           float(file.GetSetting("Part" + str(i), "PosY")),
                                           float(file.GetSetting("Part" + str(i), "PosZ")))
                spawnPos = Util.CreateVector(entPos.x + playerFront.x, entPos.y + playerFront.y,
                                             entPos.z + playerFront.z)
                spawnRot = Util.CreateQuat(float(file.GetSetting("Part" + str(i), "RotX")),
                                           float(file.GetSetting("Part" + str(i), "RotY")),
                                           float(file.GetSetting("Part" + str(i), "RotZ")),
                                           float(file.GetSetting("Part" + str(i), "RotW")))
                sm = DataStore.Get("RecorderSMs", id)
                if sm is None:
                    sm = World.CreateSM(Player, spawnPos.x, spawnPos.y, spawnPos.z, spawnRot)
                    DataStore.Add("RecorderSMs", id, sm)
                try:
                    go = Entity(World.Spawn(file.GetSetting("Part" + str(i), "Prefab"), spawnPos.x,
                                            spawnPos.y, spawnPos.z, spawnRot))
                except:
                    pass
                if go.IsDeployableObject():
                    go.ChangeOwner(Player)
                    DataStore.Add("SpawnedData" + id, "Part" + str(i), go.Object.gameObject)
                elif go.IsStructure():
                    sm.AddStructureComponent(go.Object.gameObject.GetComponent[self.st]())
                    DataStore.Add("SpawnedData" + id, "Part" + str(i), go.Object.gameObject)
                    Player.Message("Added!")
                else:
                    DataStore.Add("SpawnedData" + id, "Part" + str(i), go)
            Player.Message(args[0] + " was spawned !")
        elif cmd == "cancel":
            if not Player.Admin:
                Player.MessageFrom("Recorder", "No Permissions")
                return
            id = Player.SteamID
            cpt = DataStore.Count("SpawnedData" + id)
            for i in xrange(0, len(cpt)):
                ent = DataStore.Get("SpawnedData" + id, "Part" + str(i))
                Util.DestroyObject(ent)
                DataStore.Add("Recorder", id, False)
                DataStore.Flush("RecordedData" + id)
                DataStore.Flush("SpawnedData" + id)
                DataStore.Remove("RecorderInit", id)
                DataStore.Remove("RecorderSMs", id)
            DataStore.Flush("SpawnedData" + id)
            Player.Message("Cancelled recording")
        elif cmd == "stop":
            if not Player.Admin:
                Player.MessageFrom("Recorder", "No Permissions")
                return
            id = Player.SteamID
            name = DataStore.Get("Recorder_Name", id)
            file = Plugin.GetIni("Buildings\\" + name)
            if file is not None:
                num = random.randint(0, 100)
                Player.Message(name + ".ini already exists ! renaming..")
                name = DataStore.Get("Recorder_Name", id) + str(num)
                file = Plugin.CreateIni("Buildings\\" + name)
                rfile = Plugin.GetIni("Buildings\\" + name)
            else:
                file = Plugin.CreateIni("Buildings\\" + name)
                rfile = Plugin.GetIni("Buildings\\" + name)
            loc = DataStore.Get("RecorderInit", id)
            loc.y = World.GetGround(loc.x, loc.z)
            cpt = DataStore.Count("RecordedData" + id)
            if cpt is None:
                DataStore.Flush("RecordedData" + id)
                return
            for i in xrange(0, cpt):
                ent = DataStore.Get("RecordedData" + id, "Part" + str(i))
                entPos = Util.CreateVector((ent.X - loc.x), (ent.Y - loc.y), (ent.Z - loc.z))
                spawnRot = ent.Object.transform.rotation
                rfile.AddSetting("Part" + str(i), "Prefab", self.GetPrefabName(ent.Name))
                rfile.AddSetting("Part" + str(i), "PosX", str(entPos.x))
                rfile.AddSetting("Part" + str(i), "PosY", str(entPos.y))
                rfile.AddSetting("Part" + str(i), "PosZ", str(entPos.z))
                rfile.AddSetting("Part" + str(i), "RotX", str(spawnRot.x))
                rfile.AddSetting("Part" + str(i), "RotY", str(spawnRot.y))
                rfile.AddSetting("Part" + str(i), "RotZ", str(spawnRot.z))
                rfile.AddSetting("Part" + str(i), "RotW", str(spawnRot.w))

            DataStore.Add("Recorder", id, False)
            DataStore.Flush("RecordedData" + id)
            DataStore.Flush("SpawnedData" + id)
            DataStore.Remove("RecorderInit", id)
            DataStore.Remove("RecorderSMs", id)
            DataStore.Flush("SpawnedData" + id)
            rfile.Save()
            Player.Message(name + ".ini was saved !")

    def On_EntityDeployed(self, Player, Entity):
        state = DataStore.Get("Recorder", Player.SteamID)
        if state is not None:
            cpt = DataStore.Count("RecordedData" + Player.SteamID)
            if cpt == 0:
                DataStore.Add("RecorderInit", Player.SteamID, Util.CreateVector(Entity.X, Entity.Y, Entity.Z))
            DataStore.Add("RecordedData" + Player.SteamID, "Part" + str(cpt), Entity)

    def GetPrefabName(self, name):
        prefab = prefabs.get(name)
        return prefab
