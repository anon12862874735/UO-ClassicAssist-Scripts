def FindLowestOld():
    ClearList("HealTargets")
    while GetFriend(["Any"], "Both", "Next", "Any", 10) and not InList("HealTargets", "Friend"):
        PushList("HealTargets", "Friend")
    lowest = "Friend"
    for f in GetList("HealTargets"):
        if Hits(f) < Hits(lowest):
            lowest = f
    return lowest

def FindLowest():
    if GetFriend(["Any"], "Both", "Closest", "Lowest", 10):
        return "friend"
    return None

'''***** ~ MAIN LOOP ~ *****'''
running = True
while running == True:
    if GetFriend(["Any"], "Both", "Next", "Dead", 1):
        DoResurrect("Friend")
    elif GetFriend(["Any"], "Both", "Next", "Mortaled", 10) and tryRemoveMortal == True:
        DoRemoveCurse("Friend")
    elif GetFriend(["Any"], "Both", "Next", "Poisoned", 10):
        DoHeal("Friend")
    else:
        lowest = FindLowest()
        DoHeal(lowest)
    Stop("Crossheal")
