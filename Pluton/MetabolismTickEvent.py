__author__ = 'DreTaX'
__version__ = '1.0'

"""
    This file was created for plugin developers to be able to use the correct functions
    without looking at the wiki or the api.
    API showoff purposes only, and nothing else.
"""
import Player
import PlayerMetabolism
class MetabolismTickEvent :
    Victim = Player

    CurrentTemperature = 0.0
    FutureTemperature = 0.0

    debug = 0.0
    debug2 = 0.0

    CaloriesHealthChange = 0.0
    HydrationHealthChange = 0.0
    CaloriesChange = 0.0
    HydrationChange = 0.0
    HeartrateValue = 0.0
    OxygenValue = 0.0
    WetnessValue = 0.0
    BleedingValue = 0.0
    PoisonValue = 0.0
    RadiationValue = 0.0
    PreventDamage = False
    metabolism = None