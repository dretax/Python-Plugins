__author__ = 'DreTaX'
__version__ = '1.0'
import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite
import random

Players = []

class Recorder:

    prefabs = {
            "SingleBed": "deploy_singlebed",
            "MetalCeiling": "struct_metal_ceiling",
            "MetalDoorFrame": "struct_metal_doorframe",
            "MetalFoundation": "struct_metal_foundation",
            "MetalPillar": "struct_metal_pillar",
            "MetalRamp": "struct_metal_ramp",
            "MetalStairs": "struct_metal_stairs",
            "MetalWall": "struct_metal_wall",
            "MetalWindowFrame": "struct_metal_windowframe",
            "WoodCeiling": "struct_wood_ceiling",
            "WoodDoorFrame": "struct_wood_doorway",
            "WoodFoundation": "struct_wood_foundation",
            "WoodPillar": "struct_wood_pillar",
            "WoodRamp": "struct_wood_ramp",
            "WoodStairs": "struct_wood_stairs",
            "WoodWall": "struct_wood_wall",
            "WoodWindowFrame": "struct_wood_windowframe",
            "Campfire": "deploy_camp_bonfire",
            "ExplosiveCharge": "explosive_charge",
            "Furnace": "deploy_furnace",
            "LargeWoodSpikeWall": "deploy_largewoodspikewall",
            "WoodBoxLarge": "deploy_wood_storage_large",
            "MetalDoor": "deploy_metal_door",
            "MetalBarsWindow": "deploy_metalwindowbars",
            "RepairBench": "deploy_repairbench",
            "SleepingBagA": "deploy_camp_sleepingbag",
            "SmallStash": "deploy_small_stash",
            "WoodSpikeWall": "deploy_woodspikewall",
            "Barricade_Fence_Deployable": "deploy_wood_barricade",
            "WoodGate": "deploy_woodgate",
            "WoodGateway": "deploy_woodgateway",
            "Wood_Shelter": "deploy_wood_shelter",
            "WoodBox": "deploy_wood_box",
            "WoodenDoor": "deploy_wood_door",
            "Workbench": "deploy_workbench"
    }

    def On_Command(self, Player, cmd, args):
        if cmd == 'record':
            state = DataStore.Get('Recorder', Player.SteamID)
            name = args[0]
            if bool(state) :
                Player.MessageFrom('BRecorder', 'Already Recording!')
                return
            DataStore.Add('Recorder', Player.SteamID, True)
            DataStore.Add('Recorder_Name', Player.SteamID, name)
            Player.Message("Recording " + name + ".ini (/stop to finish!)")
        elif cmd == 'spawn':
            file = Plugin.GetIni("Buildings\\" + args[0])
            if file is None:
                Player.Message('Building not found !')
                return
            DataStore.Flush('SpawnedData' + Player.SteamID)
            DataStore.Remove('RecorderSMs', Player.SteamID)

            playerFront = Util.Infront(Player, 10)
            playerFront.y = World.GetGround(playerFront.x, playerFront.z)
            cpt = file.Count()
            for i in xrange(0, len(cpt)):
                entPos = Util.CreateVector(file.GetSetting('Part' + i, 'PosX'), file.GetSetting('Part' + i, 'PosY'), file.GetSetting('Part' + i, 'PosZ'))
                spawnPos = Util.CreateVector(entPos.x + playerFront.x, entPos.y + playerFront.y, entPos.z + playerFront.z)
                spawnRot = Util.CreateQuat(file.GetSetting('Part' + i, 'RotX'), file.GetSetting('Part' + i, 'RotY'), file.GetSetting('Part' + i, 'RotZ'), file.GetSetting('Part' + i, 'RotW'))
                sm = DataStore.Get('RecorderSMs', Player.SteamID)
                if sm is None:
                    sm = World.CreateSM(Player, spawnPos.x, spawnPos.y, spawnPos.z, spawnRot)
                    DataStore.Add('RecorderSMs', Player.SteamID, sm)
                    return
                go = World.Spawn(file.GetSetting('Part' + i, 'Prefab'), spawnPos.x, spawnPos.y, spawnPos.z, spawnRot)

                if go.IsDeployableObject():
                    go.ChangeOwner(Player)
                    DataStore.Add('SpawnedData' + Player.SteamID, 'Part' + i, go.Object.gameObject)
                    if len(args) == 2 and args[1] == "protect":
                        World.Protect(go)
                elif go.IsStructure():
                    sm.AddStructureComponent(go.Object)
                    DataStore.Add('SpawnedData' + Player.SteamID, 'Part' + i, go.Object.gameObject)
                    Player.Message("Added!")
                else:
                    DataStore.Add('SpawnedData' + Player.SteamID, 'Part' + i, go)
                Player.Message(args[0] + " was spawned !")
        elif cmd == 'cancel':
            cpt = DataStore.Count('SpawnedData' + Player.SteamID)
            for i in xrange(0, len(cpt)):
                ent = DataStore.Get('SpawnedData' + Player.SteamID, 'Part' + i)
                Util.DestroyObject(ent)
                DataStore.Add('Recorder', Player.SteamID, False)
                DataStore.Flush('RecordedData' + Player.SteamID)
                DataStore.Flush('SpawnedData' + Player.SteamID)
                DataStore.Remove('RecorderInit', Player.SteamID)
                DataStore.Remove('RecorderSMs', Player.SteamID)
            DataStore.Flush('SpawnedData' + Player.SteamID)
            Player.Message("Cancelled recording")
        elif cmd == 'stop':
            name = DataStore.Get("Recorder_Name", Player.SteamID)
            file = Plugin.GetIni("Buildings\\" + name)
            if file is not None:
                num = random.randint(0, 100)
                Player.Message(name + ".ini already exists ! renaming..")
                name = DataStore.Get("Recorder_Name", Player.SteamID) + num
            file = Plugin.CreateIni("Buildings\\" + name)
            loc = DataStore.Get('RecorderInit', Player.SteamID)
            loc.y = World.GetGround(loc.x, loc.z)
            cpt = DataStore.Count('RecordedData' + Player.SteamID)
            for i in xrange(0, len(cpt)):
                ent = DataStore.Get('RecordedData' + Player.SteamID, 'Part' + i)
                entPos = Util.CreateVector((ent.X - loc.x), (ent.Y - loc.y), (ent.Z - loc.z))
                spawnRot = ent.Object.transform.rotation
                #Todo: name rewrite
                file.AddSetting('Part' + i, 'Prefab', GetPrefabName(ent.Name))
                file.AddSetting('Part' + i, 'PosX', entPos.x)
                file.AddSetting('Part' + i, 'PosY', entPos.y)
                file.AddSetting('Part' + i, 'PosZ', entPos.z)
                file.AddSetting('Part' + i, 'RotX', spawnRot.x)
                file.AddSetting('Part' + i, 'RotY', spawnRot.y)
                file.AddSetting('Part' + i, 'RotZ', spawnRot.z)
                file.AddSetting('Part' + i, 'RotW', spawnRot.w)

                DataStore.Add('Recorder', Player.SteamID, False)
                DataStore.Flush('RecordedData' + Player.SteamID)
                DataStore.Flush('SpawnedData' + Player.SteamID)
                DataStore.Remove('RecorderInit', Player.SteamID)
                DataStore.Remove('RecorderSMs', Player.SteamID)
            DataStore.Flush('SpawnedData' + Player.SteamID)
            file.Save()
            Player.Message(name + ".ini was saved !")

    def On_EntityDeployed(self, Player, e):
        state = DataStore.Get('Recorder', Player.SteamID)
        if state is not None and state:
            cpt = int(DataStore.Count('RecordedData' + Player.SteamID))
            if cpt == 0:
                DataStore.Add('RecorderInit', Player.SteamID, Util.CreateVector(e.X, e.Y, e.Z))
            DataStore.Add('RecordedData' + Player.SteamID, 'Part' + cpt, e)

    """def GetPrefabName(name)
        for(var i = 0 i <  prefabs.length i++)
            if(prefabs[i][0] == name)
                Util.Log(prefabs[i][1])
                return prefabs[i][1]"""