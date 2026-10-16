'''Tailor BOD Reset Filler by Magickal'''
'''Version 1.0'''



'''Craftable items such as leather tunics.'''
'''Pass in boolean value for isCloth, and gump IDs for categoryGump and itemGump:'''
class CraftableItem:
    def __init__(self, isCloth, categoryGump, itemGump):
        self.isCloth = isCloth
        self.categoryGump = categoryGump
        self.itemGump = itemGump

'''Leather Armor:'''
tunic = CraftableItem(False, _LEATHERARMOR, _TUNIC)
gloves = CraftableItem(False, _LEATHERARMOR, _GLOVES)
gorget = CraftableItem(False, _LEATHERARMOR, _GORGET)
sleeves = CraftableItem(False, _LEATHERARMOR, _SLEEVES)
cap = CraftableItem(False, _LEATHERARMOR, _CAP)
legs = CraftableItem(False, _LEATHERARMOR, _LEGS)
japTunic = CraftableItem(False, _LEATHERARMOR, _JAPTUNIC)
japGorget = CraftableItem(False, _LEATHERARMOR, _JAPGORGET)
japSleeves = CraftableItem(False, _LEATHERARMOR, _JAPSLEEVES)
japCap = CraftableItem(False, _LEATHERARMOR, _JAPCAP)
japLegs = CraftableItem(False, _LEATHERARMOR, _JAPLEGS)
japLegs2 = CraftableItem(False, _LEATHERARMOR, _JAPLEGS2)
ninjaGloves = CraftableItem(False, _LEATHERARMOR, _NINJAGLOVES)
ninjaTunic = CraftableItem(False, _LEATHERARMOR, _NINJATUNIC)
ninjaLegs = CraftableItem(False, _LEATHERARMOR, _NINJALEGS)

'''Clothing:'''
shirt = CraftableItem(True, _SHIRTS, _SHIRT)
doublet = CraftableItem(True, _SHIRTS, _DOUBLET)
fancyShirt = CraftableItem(True, _SHIRTS, _FANCYSHIRT)
hakama = CraftableItem(True, _SHIRTS, _HAKAMA)
obi = CraftableItem(True, _MISC, _OBI)

'''Finish these when serial numbers and gump buttons are available'''

'''BOD class.'''
'''Pass in boolean for exceptional, as well as all items to craft and their quantities.'''
'''Quantity and item must match indices in arrays for this to work:'''
class BOD():
    def __init__(self, serial, exceptional=False, items=None, quantities=None):
        self.serial = serial
        self.exceptional = exceptional
        self.items = items if items is not None else []
        self.quantities = quantities if quantities is not None else []

class Material:
    Leather = 0
    Spined = 1
    Horned = 2
    Barbed = 3

'''Collect list of tailor BODs in backpack:'''
def ListBODs():
    SysMessage("Finding Tailor BODs in backpack...")
    if not ListExists("TailorResets"):
        CreateList("TailorResets")
    ClearList("TailorResets")
    while FindType(_TAILORBOD, -1, "Backpack"):
        PushList("TailorResets", "Found")
        IgnoreObject("Found")
    ClearIgnoreList()
    for t in GetList("TailorResets"):
        if Property(t, "Large Bulk") or Property(t, "Spined Leather") or Property(t, "Horned Leather") or Property(t, "Barbed Leather"):
            PopList("TailorResets", t)
            '''Confirm that the above code works'''
    SysMessage("Creating BOD objects...")
    BODs = []
    for t in GetList("TailorResets"):
        serial = t
        exceptional = Property(t, "Exceptional")
        items = []
        quantities = []
        '''TODO: Need a way to get each property with a quantity!'''
        BODs.append(BOD(serial, exceptional, items, quantities))
    SysMessage("Reset BODs Found : " + List("TailorResets"))
    return BODs

'''Crafts the specified item with the correct material:'''
def CraftItem(item,  material):
    while FindType(_TAILORKIT, 0, "Backpack"):
        UseType(_TAILORKIT, 0, "Backpack")
        WaitForGump(_TAILORGUMP, 200)
        if isCloth == False:
            ReplyGump(_TAILORGUMP, materialGump)
            WaitForGump(_TAILORGUMP, 200)
        ReplyGump(_TAILORGUMP, categoryGump)
        WaitForGump(_TAILORGUMP, 200)
        ReplyGump(_TAILORGUMP, itemGump)

'''Read properties of the reset BOD and fill it:'''
def FillBOD(BOD):
    SysMessage("Filling BOD : " + str(BOD.serial))
    '''Check for exceptional and leather type:'''
    isExceptional = False
    material = Material.Leather
    if Property(BOD.serial, "Exceptional"):
        isExceptional = True
    if Property(BOD.serial, "Spined"):
        material = Material.Spined
    elif Property(BOD.serial, "Horned"):
        material = Material.Horned
    elif Property(BOD.serial, "Barbed"):
        material = Material.Barbed
