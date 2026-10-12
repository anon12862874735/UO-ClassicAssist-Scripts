'''Mega Miner by Magickal'''
'''Version 1.0'''

'''Setup the variables below according to your own miner.'''

'''Dropoff/Forge runebook.  First 3 runes should be dropoff/forge/ankh in that order.'''
'''You may only need two runes because your dropoff might have a forge, but if so then'''
'''fill the middle spot with a junk rune if you still need to use the ankh.'''
'''The ankh is only used for tithing if you do not have 100% LRC and are using Sacred'''
'''Journey to recall'''
dropoffRB = _DROPOFFRB

'''The container to drop the ingots/gems into, and where to grab reagents from if you don't have LRC:'''
dropoffContainer = _DROPOFFCONTAINER

'''Does the dropoff rune have a forge?  If so, set this to True to avoid extra recalls:'''
dropoffHasForge = True

'''Forge to smelt ore:'''
forge = _FORGE

'''List of runebooks to be used.  It is recommended to use 4 or more.'''
'''The script expects each runebook to be filled with 16 mining runes:'''
runebooks = [_RUNEBOOK1, _RUNEBOOK2, _RUNEBOOK3, _RUNEBOOK4]

'''Name of spell to use for recalling ("Recall", "Sacred Journey", or "Gate Travel" are your only options):'''
recallSpell = "Sacred Journey"

'''Time in milliseconds to wait after casting your recall spell of choice before returning to mining:'''
recallWaitTime = 2000

'''Time in milliseconds to wait after casting a spell:'''
castRecoveryDelay = _CASTRECOVERYDELAY

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
'''TODO: implement'''
gumpIDRecall = [
    1, 2, 3, 4,
    5, 6, 7, 8,
    9, 10, 11, 12,
    13, 14, 15, 16
]

'''List of gump IDs to be used for Sacred Journey:'''
'''DOUBLE-CHECK THIS BEFORE RUNNING!'''
gumpIDSacred = [
    13, 19, 25, 31,
    37, 43, 49, 55,
    61, 67, 73, 79,
    85, 91, 97, 103
]

'''List of gump IDs to be used for Gate Travel:'''
'''TODO: implement'''
gumpIDGate = [
    1, 2, 3, 4,
    5, 6, 7, 8,
    9, 10, 11, 12,
    13, 14, 15, 16
]

'''Current index to recall to:'''
recallIndex = 0

'''Current runebook index:'''
runebookIndex = 0

'''Gets the next rune/runebook to use:'''
def GetNextIndex():
    if recallIndex >= 15:
        recallIndex = 0
        if runebookIndex > len(runebooks) - 1:
            runebookIndex = 0
        else:
            runebookIndex += 1
    else:
        recallIndex += 1

'''Dispels any moongate found on top of the player, if casting gate fails.'''
'''This way, nobody can gate your miner away:'''
def DispelMoongate(gate):
    Cast("Dispel Field")
    WaitForTargetOrFizzle(2500)
    Target(gate)
    Pause(_CASTRECOVERYDELAY)

'''Recalls to the next mining spot:'''
def RecallNext(next):
    ClearJournal()
    if next == True:
        GetNextIndex()
    UseObject(runebooks[runebookIndex])
    WaitForGump(_RUNEBOOKGUMP, 3000)
    if recallSpell == "Recall":
        ReplyGump(_RUNEBOOKGUMP, gumpIDRecall[i])
    elif recallSpell == "Sacred Journey":
        ReplyGump(_RUNEBOOKGUMP, gumpIDSacred[i])
    elif recallSpell == "Gate Travel":
        ReplyGump(_RUNEBOOKGUMP, gumpIDGate[i])
    Pause(recallWaitTime)
    if recallSpell == "Gate Travel":
        if InJournal("There is already a gate there"):
            while FindType(_BLUEMOONGATEID, 0, "Ground") or FindType(_REDMOONGATEID, 0, "Ground"):
                DispelMoongate("Found")
            RecallNext(False)
        elif FindType(_BLUEMOONGATEID, 0, "Ground") or FindType(_REDMOONGATEID, 0, "Ground"):
            Pause(900)
            UseItem("Found")
            WaitForGump(_MOONGATEGUMPID, 5000)
            ReplyGump(_MOONGATEGUMPID, _MOONGATEGUMPACCEPTBUTTON)
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
    UseObject(_DROPOFFRB)
    WaitForGump(_RUNEBOOKGUMP, 3000)
    gumpButton = 0
    '''True if you're going to tithe gold, false if you're going to drop off resources:'''
    if location == Location.Ankh:
        if recallSpell == "Recall":
            gumpButton = _RECALLANKHBUTTON
        elif recallSpell == "Sacred Journey":
            gumpButton = _SACREDANKHBUTTON
        elif recallSpell == "Gate Travel":
            gumpButton = _GATEANKHBUTTON
    elif location == Location.Dropoff:
        if recallSpell == "Recall":
            gumpButton = _RECALLDROPOFFBUTTON
        elif recallSpell == "Sacred Journey":
            gumpButton = _SACREDDROPOFFBUTTON
        elif recallSpell == "Gate Travel":
            gumpButton = _GATEDROPOFFBUTTON
    elif location == Location.Forge:
        if recallSpell == "Recall":
            gumpButton = _RECALLFORGEBUTTON
        elif recallSpell == "Sacred Journey":
            gumpButton = _SACREDFORGEBUTTON
        elif recallSpell == "Gate Travel":
            gumpButton = _GATEFORGEBUTTON
    ReplyGump(_RUNEBOOKGUMP, gumpButton)
    Pause(recallWaitTime)
    if recallSpell == "Gate Travel":
        if InJournal("There is already a gate there"):
            while FindType(_BLUEMOONGATEID, 0, "Ground") or FindType(_REDMOONGATEID, 0, "Ground"):
                DispelMoongate("Found")
            RecallToDropoffOrAnkh(location)
        elif FindType(_BLUEMOONGATEID, 0, "Ground") or FindType(_REDMOONGATEID, 0, "Ground"):
            Pause(900)
            UseItem("Found")
            WaitForGump(_MOONGATEGUMPID, 3000)
            ReplyGump(_MOONGATEGUMPID, _MOONGATEGUMPACCEPTBUTTON)
    if InJournal("location is blocked"):
        RecallToDropoffOrAnkh(location)
    else:
        if useBankAsDropoff == True:
            Msg("Bank")
            Pause(100)

'''Smelt all ore into ingots:'''
def SmeltOre():
    while FindType(_ORETYPE1, 0, "Backpack"):
        UseType("Found")
        WaitForTarget(150)
        Target(forge)
    while FindType(_ORETYPE2, 0, "Backpack"):
        UseType("Found")
        WaitForTarget(150)
        Target(forge)
    while FindType(_ORETYPE3, 0, "Backpack"):
        UseType("Found")
        WaitForTarget(150)
        Target(forge)
    while FindType(_ORETYPE4, 0, "Backpack"):
        UseType("Found")
        WaitForTarget(150)
        Target(forge)
    Pause(1000)
    '''TODO: ensure that the tiny ores which require 2-stacks to smelt are dealt with properly'''

'''List of all tinker tools in backpack:'''
if not ListExists("tinkerTools"):
    CreateList("tinkerTools")
ClearList("tinkerTools")

'''List of all shovels in backpack:'''
if not ListExists("shovels"):
    CreateList("shovels")
ClearList("shovels")

'''Drops off smelted ingots, crafts Tinker Tools/Shovels as needed:'''
def DropoffAndRestock():
    while FindType(_INGOTS, 0, "Backpack"):
        MoveItem("Found", _DROPOFFCONTAINER)
    for g in GetList("gemstones"):
        while FindType(g, 0, "Backpack"):
            MoveItem("Found", _DROPOFFCONTAINER)
    while not FindType(_INGOTS, 0, "Backpack", 0) and FindType(_INGOTS, 2, _DROPOFFCONTAINER, 0):
        MoveItem("Found", "BackPack", 200)
    ClearList("tinkerTools")
    ClearList("shovels")
    ClearIgnoreList()
    while FindType(_TINKERTOOL, 0, "Backpack"):
        PushList("tinkerTools", "Found")
        IgnoreObject("Found")
    if List("tinkerTools") < 3:
        UseType(_TINKERTOOL)
        WaitForGump(_TINKERTOOLGUMP, 3000)
        ReplyGump(_TINKERTOOLGUMO, _MAKETINKERTOOLGUMPBUTTON)
        Pause(900)
    while FindType(_TINKERTOOL, 0, "Backpack"):
        PushList("tinkerTools", "Found")
        IgnoreObject("Found")
    if List("shovels") < 5:
        UseType(_TINKERTOOL)
        WaitForGump(_TINKERTOOLGUMP, 3000)
        ReplyGump(_TINKERTOOLGUMO, _MAKESHOVELGUMPBUTTON)
        Pause(900)
    '''TODO: Check reagents and tithing points, collect reagents from dropoff point and tithe gold!'''

def MineOre():
    if TargetExists():
        TargetByResource('Shovel', 'Ore')
    UseType(_SHOVEL)
    WaitForTarget(150)
    '''Haven't used this yet.  Will it work, and if so, how?'''
    TargetByResource('Shovel', 'Ore')


'''***** ~ MAIN LOOP ~ *****'''
running = True

while running == True:
    RecallNext(True)
    ClearJournal()
    while Weight() < dropoffWeight:
        while not InJournal("There is no metal") or InJournal("Target cannot be seen") or InJournal("can't mine that"):
            MineOre()
    Pause(1000)
    if dropoffHasForge == True:
        RecallToDropoffOrAnkh(Location.Dropoff)
    else:
        RecallToDropoffOrAnkh(Location.Forge)
    while Weight() >= dropoffWeight:
        SmeltOre()
        if dropoffHasForge == False:
            RecallToDropoffOrAnkh(Location.Dropoff)
        DropoffAndRestock()
