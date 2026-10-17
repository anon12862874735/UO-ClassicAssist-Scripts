'''Crossheal Friends List by Magickal'''
'''Version 1.01'''

'''Attempts to automatically miniheal any player on your friends list,'''
'''rez them if they're dead and within one tile (can precast and run in'''
'''with target up), and cure poison.  Set to do not auto-interrupt.'''
'''Will target the lowest health friend on your friends list only for'''
'''miniheals, and will only heal if below 100% health.'''


'''Delay to pause after casting cure so you do not double-cure.'''
'''Set this to zero if you don't mind double-curing, or if it hasn't been a problem for you:'''
cureDelay = 120

'''Change this to true if you want your script to try to remove curse on a mortalled target:'''
tryRemoveMortal = False

'''List used to find loweat health friend to heal:'''
if not ListExists("HealTargets"):
    CreateList("HealTargets")
ClearList("HealTargets")

def DoResurrect(friend):
    if TargetExists('Beneficial'):
        Target(friend)
    else:
        Cast("Resurrection")
        WaitForTargetOrFizzle(2500)
        Target(friend)

def DoRemoveCurse(friend):
    if TargetExists('Beneficial'):
        Target(friend)
    elif TargetExists('Harmful'):
        CancelTarget()
    Cast("RemoveCurse")
    WaitForTargetOrFizzle(1800)
    Target(friend)

def DoHeal(friend):
    if friend == None:
        return
    global cureDelay
    if TargetExists('Beneficial'):
        Target(friend)
    elif TargetExists('Harmful'):
        CancelTarget()
    else:
        if Poisoned(friend):
            Cast("Cure")
            WaitForTargetOrFizzle(800)
            Target(friend)
            Pause(cureDelay)
        else:
            Cast("Heal")
            WaitForTargetOrFizzle(500)
            Target(friend)

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
