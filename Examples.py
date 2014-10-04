__author__ = 'Balu92'
import clr
import sys
clr.AddReferenceByPartialName("UnityEngine")
clr.AddReferenceByPartialName("Fougerite")
import UnityEngine
import Fougerite
from UnityEngine import Debug

class Test:
	def On_TablesLoaded(self, tables):
#		Debug.Log("On_TablesLoaded hooked with " + tables.Count.ToString() + " element, from Python")
		Plugin.DumpObjToFile("On_TablesLoaded.Tables", tables, 3, 20, True, True)
		return tables

	def On_AllPluginsLoaded(self):
		Debug.Log("The knights who say NI!")

	def On_ServerInit(self):
		Debug.Log("On_ServerInit hooked from Python")
		dic = Plugin.CreateDict()
		dic.Add("first", "timer is:")
		dic.Add("second", "working")
		Plugin.CreateTimer("testtimer", 5000, dic).Start()

	def testtimerCallback(self, dic):
		plug2 = Plugin.GetPlugin("Test2")
		plug2.Invoke("TestSharedFunction", dic["first"], dic["second"])
		Debug.Log(dic["first"])
		Debug.Log(dic["second"])
		Plugin.DumpObjToFile("testtimerCallback.dict", dic, 3, 20, True, True)
		Plugin.KillTimers()

	def On_PluginInit(self):
		Debug.Log("On_PluginInit hooked from Python")

	def On_ServerShutdown(self):
		Debug.Log("On_ServerShutdown hooked from Python")

	def On_ItemsLoaded(self, items):
#		Debug.Log("On_ItemsLoaded hooked with " + items.Count + " element, from Python")
		Plugin.DumpObjToFile("On_ItemsLoaded.Items", items, 3, 20, True, True)
		return items

	def On_Chat(self, Player, Text):
#		Debug.Log(Player.Name + " says: " + Text)
		Plugin.DumpObjToFile("On_Chat.Player", Player, 3, 20, True, True)
		Plugin.DumpObjToFile("On_Chat.Text", Text, 3, 20, True, True)

	def On_BlueprintUse(self, Player, BPUseEvent):
#		Debug.Log(Player.Name + " researched " + BPUseEvent.ItemName)
		Plugin.DumpObjToFile("On_BlueprintUse.Player", Player, 3, 20, True, True)
		Plugin.DumpObjToFile("On_BlueprintUse.BPUseEvent", BPUseEvent, 3, 20, True, True)

	def On_Command(self, Player, cmd, args):
#		Debug.Log("On_Command(" + Player.Name + ", " + cmd + ", " + args + ")")
		Plugin.DumpObjToFile("On_Command.Player", Player, 3, 20, True, True)
		Plugin.DumpObjToFile("On_Command.cmd", cmd, 3, 20, True, True)
		Plugin.DumpObjToFile("On_Command.args", args, 3, 20, True, True)

	def On_Console(self, Player, Arg):
#		Debug.Log(Player.Name + " used " + Arg.Class + "." + Arg.Function + " in console ")
		Plugin.DumpObjToFile("On_Console.Player", Player, 3, 20, True, True)
		Plugin.DumpObjToFile("On_Console.Arg", Arg, 3, 20, True, True)

	def On_DoorUse(self, Player, DoorEvent):
#		Debug.Log(Player.Name + " tried to use a door")
#		Debug.Log("Succeded? " + ("yes" if DoorEvent.Open else "no"))
		Plugin.DumpObjToFile("On_DoorUse.Player", Player, 3, 20, True, True)
		Plugin.DumpObjToFile("On_DoorUse.DoorEvent", DoorEvent, 3, 20, True, True)

	def On_EntityDecay(self, DecayEvent):
		Plugin.DumpObjToFile("On_EntityDecay.DecayEvent", DecayEvent, 3, 20, True, True)
		return DecayEvent.DamageAmount

	def On_EntityDeployed(self, Player, Entity):
		Plugin.DumpObjToFile("On_EntityDeployed.Player", Player, 3, 20, True, True)
		Plugin.DumpObjToFile("On_EntityDeployed.Entity", Entity, 3, 20, True, True)

	def On_EntityHurt(self, HurtEvent):
		Plugin.DumpObjToFile("On_EntityHurt.HurtEvent", HurtEvent, 3, 20, True, True)

	def On_EntityDestroyed(self, DestroyEvent):
		Plugin.DumpObjToFile("On_EntityDestroyed.DestroyEvent", DestroyEvent, 3, 20, True, True)

	def On_NPCKilled(self, DeathEvent):
		Plugin.DumpObjToFile("On_NPCKilled.DeathEvent", DeathEvent, 3, 20, True, True)

	def On_NPCHurt(self, HurtEvent):
		Plugin.DumpObjToFile("On_NPCHurt.HurtEvent", HurtEvent, 3, 20, True, True)

	def On_PlayerGathering(self, Player, GatherEvent):
		Plugin.DumpObjToFile("On_PlayerGathering.Player", Player, 3, 20, True, True)
		Plugin.DumpObjToFile("On_PlayerGathering.GatherEvent", GatherEvent, 3, 20, True, True)

	def On_PlayerSpawning(self, Player, SpawnEvent):
		Plugin.DumpObjToFile("On_PlayerSpawning.Player", Player, 3, 20, True, True)
		Plugin.DumpObjToFile("On_PlayerSpawning.SpawnEvent", SpawnEvent, 3, 20, True, True)
		return Util.CreateVector(SpawnEvent.X, SpawnEvent.Y, SpawnEvent.Z)

	def On_PlayerSpawned(self, Player, SpawnEvent):
		Plugin.DumpObjToFile("On_PlayerSpawned.Player", Player, 3, 20, True, True)
		Plugin.DumpObjToFile("On_PlayerSpawned.SpawnEvent", SpawnEvent, 3, 20, True, True)

	def On_PlayerKilled(self, DeathEvent):
		Plugin.DumpObjToFile("On_PlayerKilled.DeathEvent", DeathEvent, 3, 20, True, True)

	def On_PlayerHurt(self, HurtEvent):
		Plugin.DumpObjToFile("On_PlayerHurt.HurtEvent", HurtEvent, 3, 20, True, True)

	def On_PlayerConnected(self, Player):
		Plugin.DumpObjToFile("On_PlayerConnected.Player", Player, 3, 20, True, True)

	def On_PlayerDisconnected(self, Player):
		Plugin.DumpObjToFile("On_PlayerDisconnected.Player", Player, 3, 20, True, True)