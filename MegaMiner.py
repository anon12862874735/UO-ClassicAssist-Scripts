'''Mega Miner by Magickal'''
'''Version 1.0'''

import clr
import System
clr.AddReference("System.Core")
clr.ImportExtensions(System.Linq)
from Assistant import Engine

'''Setup the variables below according to your own miner.'''

'''Dropoff/Forge runebook.  First 3 runes should be dropoff/forge/ankh in that order.'''
'''If you do not need the ankh or forge because your dropoff has a forge, just place'''
'''the dropoff point in rune slot 1.'''
'''The ankh is only used for tithing if you do not have 100% LRC and are using Sacred'''
'''Journey to recall:'''
dropoffRB = 0x429818e7

'''The container to drop the ingots/gems into, and where to grab reagents from if you don't have LRC:'''
dropoffContainer = 0x400e9ace

'''Does the dropoff rune have a forge?  If so, set this to True to avoid extra recalls:'''
dropoffHasForge = True

'''Forge to smelt ore:'''
forge = 0x400faf44

'''List of runebooks to be used.  It is recommended to use 4 or more.'''
'''The script expects each runebook to be filled with 16 mining runes:'''
runebooks = [0x45fc6ec6, 0x4071f0ec, 0x4071f14a, 0x4071f0bd]

'''Name of spell to use for recalling ("Recall", "Sacred Journey", or "Gate Travel" are your only options):'''
recallSpell = "Sacred Journey"

'''Time in milliseconds to wait after casting your recall spell of choice before returning to mining:'''
recallWaitTime = 1000

'''Time in milliseconds to wait after casting a spell:'''
castRecoveryDelay = 0

'''If you have a 100% LRC suit, set this to True, otherwise set it to False:'''
hasLRC = True

'''Target weight to start dropping off/smelting:'''
dropoffWeight = 400

'''If you want to use your bank box as a dropoff point, set this to True:'''
useBankAsDropoff = False

'''Auto-tithing has not been implemented yet!'''
'''If you want to automatically tithe gold when you are low on points, set this to True:'''
tithe = False

'''Amount of gold to not go below if you are tithing:'''
titheGoldMin = 60000

'''TODO: Add the ability to use a beetle/fire beetle'''


'''XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'''
'''******************** DO NOT TOUCH ANYTHING BEYOND THIS POINT UNLESS YOU KNOW WHAT YOU'RE DOING! ********************'''
'''XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'''

'''List of gump IDs to be used for Recall:'''
gumpIDRecall = [
    5, 11, 17, 23,
    29, 35, 41, 47,
    53, 59, 65, 71,
    77, 83, 89, 95
]

'''List of gump IDs to be used for Sacred Journey:'''
gumpIDSacred = [
    7, 13, 19, 25,
    31, 37, 43, 49,
    55, 61, 67, 73,
    79, 85, 91, 97
]

'''List of gump IDs to be used for Gate Travel:'''
'''TODO: check if this works'''
gumpIDGate = [
    6, 12, 18, 24,
    30, 36, 42, 48,
    54, 60, 66, 72,
    78, 84, 90, 96
]

'''List of gemstones:'''
if not ListExists("gemstones"):
    CreateList("gemstones")
    PushList("gemstones", 0x3192)
    PushList("gemstones", 0x3193)
    PushList("gemstones", 0x3194)
    PushList("gemstones", 0x3195)
    PushList("gemstones", 0x3196)
    PushList("gemstones", 0x3197)
    PushList("gemstones", 0x3198)

'''Current index to recall to:'''
recallIndex = 0

'''Current runebook index:'''
runebookIndex = 0

'''Gets the next rune/runebook to use:'''
def GetNextIndex():
    global recallIndex, runebookIndex
    if recallIndex >= 15:
        recallIndex = 0
        runebookIndex += 1
        if runebookIndex > len(runebooks) - 1:
            runebookIndex = 0
    else:
        recallIndex += 1

'''Dispels any moongate found on top of the player, if casting gate fails.'''
'''This way, nobody can gate your miner away:'''
def DispelMoongate(gate):
    SysMessage("~Dispelling moongate~")
    Cast("Dispel Field")
    WaitForTargetOrFizzle(2500)
    Target(gate)
    Pause(castRecoveryDelay)

'''Recalls to the next mining spot:'''
def RecallNext(next):
    SysMessage("~Recalling to next point~")
    ClearJournal()
    if next == True:
        GetNextIndex()
    SysMessage("    Runebook : " + str(format(hex(runebooks[runebookIndex]))))
    SysMessage("    Book Number : " + str(runebookIndex + 1))
    SysMessage("    Index : " + str(recallIndex + 1))
    UseObject(runebooks[runebookIndex])
    WaitForGump(0x554b87f3, 3000)
    if recallSpell == "Recall":
        ReplyGump(0x554b87f3, gumpIDRecall[recallIndex])
    elif recallSpell == "Sacred Journey":
        ReplyGump(0x554b87f3, gumpIDSacred[recallIndex])
    elif recallSpell == "Gate Travel":
        ReplyGump(0x554b87f3, gumpIDGate[recallIndex])
    Pause(recallWaitTime)
    if recallSpell == "Gate Travel":
        if InJournal("There is already a gate there"):
            while FindType(0xf6c, 0, "Ground") or FindType(0xdda, 0, "Ground"):
                DispelMoongate("Found")
            RecallNext(False)
        elif FindType(0xf6c, 0, "Ground") or FindType(0xdda, 0, "Ground"):
            Pause(900)
            UseItem("Found")
            WaitForGump(0xdd8b146a, 5000)
            ReplyGump(0xdd8b146a, 1)
    if InJournal("location is blocked") or InJournal("already there"):
        RecallNext(True)
    elif InJournal(" mana for this spell"):
        RecallNext(False)

'''Locations used to recall to when dropping off, smelting, or tithing:'''
class Location:
    Dropoff = 0
    Forge = 1
    Ankh = 2

'''Recalls to dropoff/forge/ankh:'''
def RecallToDropoffOrAnkh(location):
    ClearJournal()
    UseObject(0x429818e7)
    WaitForGump(0x554b87f3, 3000)
    gumpButton = 0
    '''True if you're going to tithe gold, false if you're going to drop off resources:'''
    if location == Location.Ankh:
        if recallSpell == "Recall":
            gumpButton = 17
        elif recallSpell == "Sacred Journey":
            gumpButton = 19
        elif recallSpell == "Gate Travel":
            gumpButton = 18
        SysMessage("Recalling to Ankh to tithe...")
    elif location == Location.Dropoff:
        if recallSpell == "Recall":
            gumpButton = 5
        elif recallSpell == "Sacred Journey":
            gumpButton = 7
        elif recallSpell == "Gate Travel":
            gumpButton = 6
        SysMessage("Recalling to Dropoff...")
    elif location == Location.Forge:
        if recallSpell == "Recall":
            gumpButton = 11
        elif recallSpell == "Sacred Journey":
            gumpButton = 13
        elif recallSpell == "Gate Travel":
            gumpButton = 12
        SysMessage("Recalling to Forge...")
    '''SysMessage("    Gump Button : " + str(gumpButton))'''
    ReplyGump(0x554b87f3, gumpButton)
    Pause(recallWaitTime)
    if recallSpell == "Gate Travel":
        if InJournal("There is already a gate there"):
            while FindType(0xf6c, 0, "Ground") or FindType(0xdda, 0, "Ground"):
                DispelMoongate("Found")
            RecallToDropoffOrAnkh(location)
        elif FindType(0xf6c, 0, "Ground") or FindType(0xdda, 0, "Ground"):
            Pause(900)
            UseItem("Found")
            WaitForGump(0xdd8b146a, 3000)
            ReplyGump(0xdd8b146a, 1)
    if InJournal("location is blocked"):
        RecallToDropoffOrAnkh(location)
    else:
        if useBankAsDropoff == True:
            Msg("Bank")
            Pause(100)

'''Smelt all ore into ingots:'''
def SmeltOre():
    SysMessage("Smelting...")
    while FindType(0x19b9, -1, "Backpack"):
        UseObject("found")
        WaitForTarget(150)
        '''Small forge:'''
        Target(forge)
    while FindType(0x19ba, -1, "Backpack"):
        UseObject("found")
        WaitForTarget(150)
        Target(forge)
    while FindType(0x19b8, -1, "Backpack"):
        UseObject("found")
        WaitForTarget(150)
        Target(forge)
    while FindType(0x19b7, -1, "Backpack"):
        MoveItem("found", dropoffContainer)
    '''Small ores must be handled in this stupid way because there's no way to easily get the quantity of each stack:'''
    '''
    smallOres = Engine.Player.Backpack.Container.SelectEntities(lambda i: i.ID == 0x19b7)
    for o in smallOres:
        while o.Count > 1:
            UseObject("found")
            WaitForTarget(150)
            Target(forge)
    '''
    Pause(1000)
    

'''List of all tinker tools in backpack:'''
if not ListExists("tinkerTools"):
    CreateList("tinkerTools")
ClearList("tinkerTools")

'''List of all shovels in backpack:'''
if not ListExists("pickaxes"):
    CreateList("pickaxes")
ClearList("pickaxes")

'''Drops off smelted ingots, crafts Tinker Tools/Shovels as needed:'''
def DropoffAndRestock():
    SysMessage("Dropping off...")
    UseObject(dropoffContainer)
    Pause(900)
    while FindType(0x1bf2, -1, "Backpack"):
        MoveItem("Found", dropoffContainer)
    for g in GetList("gemstones"):
        while FindType(g, -1, "Backpack"):
            MoveItem("Found", dropoffContainer)
    Pause(900)
    while not FindType(0x1bf2, -1, "Backpack", 0):
        MoveType(0x1bf2, dropoffContainer, "Backpack", 0, 0, 0, 0, 200)
        Pause(900)
    ClearList("tinkerTools")
    ClearList("pickaxes")
    ClearIgnoreList()
    SysMessage("Crafting tools...")
    while FindType(0x1eb8, -1, "Backpack"):
        PushList("tinkerTools", "Found")
        IgnoreObject("Found")
    while List("tinkerTools") < 3:
        UseType(0x1eb8)
        WaitForGump(0x38920abd, 3000)
        ReplyGump(0x38920abd, 23)
        Pause(900)
        if FindType(0x1eb8, -1, "Backpack"):
            PushList("tinkerTools", "Found")
    while FindType(0xe86, -1, "Backpack"):
        PushList("pickaxes", "Found")
        IgnoreObject("Found")
    while List("pickaxes") < 5:
        UseType(0x1eb8)
        WaitForGump(0x38920abd, 3000)
        ReplyGump(0x38920abd, 114)
        Pause(900)
        if FindType(0xe86, -1, "Backpack"):
            PushList("pickaxes", "Found")
    ClearIgnoreList()
    '''TODO: Check reagents and tithing points, collect reagents from dropoff point and tithe gold'''

def MineOre():
    if FindType(0xe86, 0, "Backpack"):
        SetAlias('pickaxe', "Found")
        TargetByResource('pickaxe', 'Ore')

'''***** ~ MAIN LOOP ~ *****'''
running = True

while running == True:
    ClearJournal()
    while Weight() < dropoffWeight and not InJournal("There is no metal") and not InJournal("Target cannot be seen") and not InJournal("can't mine"):
        MineOre()
    Pause(250)
    if Weight() >= dropoffWeight:
        if dropoffHasForge == True:
            SysMessage("Recalling to dropoff/forge...")
            RecallToDropoffOrAnkh(Location.Dropoff)
        else:
            SysMessage("Recalling to forge...")
            RecallToDropoffOrAnkh(Location.Forge)
        SmeltOre()
        if dropoffHasForge == False:
            SysMessage("Recalling to dropoff...")
            RecallToDropoffOrAnkh(Location.Dropoff)
        DropoffAndRestock()
        RecallNext(False)
    else:
        RecallNext(True)
