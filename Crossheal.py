'''Crossheal Friends List by Magickal'''
'''Version 1.0'''

'''Attempts to automatically miniheal any player on your friends list,'''
'''rez them if they're dead and within one tile (can precast and run in'''
'''with target up), break paralyze with feeblemind, andcure poison.'''
'''Will target the lowest health friend on your friends list only for'''
'''miniheals, and will only heal if below 100% health.'''


'''Delay to pause after casting cure so you do not double-cure:'''
cureDelay = 50

'''Change this to true if you want your script to try to remove curse on a mortalled target:'''
tryRemoveMortal = False

def DoResurrect(friend):
    if TargetExists('Beneficial'):
        Target(friend)
    else:
        Cast("Resurrection")
        WaitForTargetOrFizzle(2500)
        Target(friend)

def DoParalyzeBreak(friend):
    if TargetExists('Beneficial'):
        Target(friend)
    Cast("Feeblemind")
    WaitForTargetOrFizzle(500)
    Target(friend)

def DoRemoveCurse(friend):
    if TargetExists('Beneficial'):
        Target(friend)
    elif TargetExists('Harmful'):
        CancelTarget()
    Cast("RemoveCurse")
    WaitForTargetOrFizzle(1800)
    Target(friend)

def FindLowest(friend):
    GetFriendListOnly(["Any"], "Lowest", ["Humanoid", "Transformation"], 10)
    if "Found" == friend:
        return True
    else:
        return False

def DoHeal(friend):
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

'''***** ~ MAIN LOOP ~ *****'''
while GetFriendListOnly(["Next"], ["Humanoid", "Transformation"], 10):
    if Dead("Found") and InRange("Found", 1):
        DoResurrect("Found")
    elif Paralyzed("Found"):
        DoParalyzeBreak("Found")
    elif YellowHits("Found") and tryRemoveMortal == True:
        DoRemoveCurse("Found")
    elif Poisoned("Found"):
        DoHeal("Found")
    elif Hits("Found") < MaxHits("Found") and FindLowest("Found") == True:
        DoHeal("Found")
