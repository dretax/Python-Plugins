__author__ = 'DreTaX'
import clr
import sys
"""
This method has to be uncommented when you will use the plugin on your live server.
"""
#clr.AddReferenceByPartialName("Fougerite")

"""
The below method in the place where our Fougerite.dll is.
This will define our IDE where to look for the functions
In python we use double \\ when giving paths.

Note: sys.path and clr.AddReferenceToFile is not required when running the plugin on a live server.
When ever you are planning to try the plugin, please COMMENT these two lines.
"""
sys.path.Add("d:\\Python33\\Fougerite\\")

"""
As above, we have given our IDE the path where to look for the libraries.
Now we define which dlls do we need.
"""
clr.AddReferenceToFile("Fougerite.dll")

#This might show errors in your IDE, if it does, just hover your mouse on the red lamp and click to ignore reference.
import Fougerite
