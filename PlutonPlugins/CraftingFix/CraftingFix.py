__author__ = 'DreTaX'
__version__ = '1.0'

import clr

clr.AddReferenceByPartialName("Pluton")
import Pluton

"""
    Class
"""

class CraftingFix:

    def On_PlayerStartCrafting(self, CraftEvent):
        CraftEvent.FreeCraft = False
        items = CraftEvent.Crafter.Inventory.AllItems().ToArray()
        ingreds = CraftEvent.bluePrint.ingredients.ToArray()
        Items = {}
        for item in items:
            l = item.Name.lower().replace('_', ' ')
            Items[l] = item.Quantity
        for ingred in ingreds:
            name = str(ingred.itemDef).replace(' (ItemDefinition)', '').lower().replace('_', ' ')
            if name not in Items.keys():
                CraftEvent.Stop("You don't have enough materials for this")
                return
            inventoryq = Items.get(name, None)
            if int(ingred.startAmount) > inventoryq:
                CraftEvent.Stop("You don't have enough materials for this")
                return
            CraftEvent.Crafter.Inventory._inv.Take(None, ingred.itemid, ingred.startAmount)