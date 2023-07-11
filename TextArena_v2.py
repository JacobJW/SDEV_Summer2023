# Title: Text Battler
# created by Jacob W. for SDEV final project
# Desc: turn based game where player and enemy go back and forth in a fight.

# SECTION 0.1: IMPORT MODULES
import tkinter as tk
import random as rand

# SECTION 0.2: CREATE GLOBAL DICTIONARIES
# logScripts dictionary holds all event -> text associations used in the combat log.
global logScripts
logScripts = {
    "combat_intro":str("_eventActorA_ faces _eventActorB_! Combat begins with _eventValue_ feet between them."),
    "attack_on_target":str("_eventActorA_ attacks _eventActorB_!"), # actor A is attacker, actor B is attack target
    "hit_deal_damage":str("A hit! Deals _eventValue_ damage to _eventActorB_!"), # value is damage points, actor B is attack target
    "hit_no_damage":str("A hit, but _eventActorB_ blocks all the damage!"), # occurs if attack hits but damage is fully negated by armor; actorB is target
    "hit_miss":str("A miss!"),
    "enemy_defeated":str("_eventActorA_ is slain!"),
    "player_defeated":str("_eventActorA_ is defeated! Too bad.."),
    "forward_move":str("_eventActorA_ moves _eventValue_ feet towards the opponent..."), # value is distance covered
    "back_move":str("_eventActorA_ backs _eventValue_ feet away from the opponent..."), # value is distance covered
    "enemy_out_reach":str("The target is too far! You can only attack within _eventValue_ feet."), # value is weapon reach
    "distance_report":str("There are _eventValue_ feet between the opponents."), # value is distance
    "health_report":str("_eventActorA_ is at _eventValue_ health."), # value is remaining health
    "new_round":str("A new round begins..."),
    "no_move":str("There is no room to move.") 
    }
    # Use actor A for attacker/caster, and actor B for target. Optional.
    # Use event value for damage points, healing points, or any other number. Optional.

# These dictionaries hold the stats for each class. Used as reference by game
global stats_FIGHTER
stats_FIGHTER = {
    "maxHealth":"125","armor":"20","moveSpeed":"30",
    "meleeReach":"8","meleeDamageMin":"22","meleeDamageMax":"44",
    "rangedReach":"24","rangedDamageMin":"15","rangedDamageMax":"55","rangedAmmo":"6",
    "accuracy":"75",
    "power":"SECOND WIND",
    "desc":"Heavily armored and wielding a large sword and backup pistol, the fighter is a deadly force in close range.\nIn addition, they can recover health fast."
    }
global stats_WIZARD
stats_WIZARD = {
    "maxHealth":"100","armor":"10","moveSpeed":"30",
    "meleeReach":"8","meleeDamageMin":"16","meleeDamageMax":"32",
    "rangedReach":"40","rangedDamageMin":"24","rangedDamageMax":"24","rangedAmmo":"15",
    "accuracy":"75",
    "power":"MAGIC SURGE",
    "desc":"The wizard wields a long staff from which they can fire bolts over short distances.\nIn addition, they can cast spells to cause random effects."
    }
global stats_RANGER
stats_RANGER = {
    "maxHealth":"100","armor":"15","moveSpeed":"45",
    "meleeReach":"5","meleeDamageMin":"15","meleeDamageMax":"30",
    "rangedReach":"90","rangedDamageMin":"25","rangedDamageMax":"50","rangedAmmo":"6",
    "accuracy":"85",
    "power":"DISSAPEAR",
    "desc":"The ranger can move quickly and fire deadly arrows from afar with great accuracy.\nIn addition, they can swiftly retreat from close fights."
    }
# These dictionaries hold the stats for each monster. Used as reference by game
global stats_SKELETON
stats_SKELETON = {
    "maxHealth":"125","armor":"15","moveSpeed":"30",
    "meleeReach":"5","meleeDamageMin":"20","meleeDamageMax":"40",
    "rangedReach":"0","rangedDamageMin":"0","rangedDamageMax":"0","rangedAmmo":"0",
    "accuracy":"75",
    "power":"RATTLE",
    "desc":"A walking skeletal corpse, armed with a rusty blade and covered in scraped armor."
    }


# SECTION 1.0: SETUP AND CHARACTER BUILD FUNCTIONS
def gameSetup():
    # Set up the global variables
    global playerName
    playerName = "Champion"
    global playerClass
    playerClass = "FIGHTER"
    global list_classes
    list_classes = ["FIGHTER","WIZARD","ASSASSIN","RANGER"]

    global startupWindow
    startupWindow = tk.Tk()
    startupWindow.title("Text Battler")
    rows = 3
    columns = 3

    for i in range(columns+1):
        startupWindow.columnconfigure(i, weight=1, minsize=100) # enables responsive column
    for i in range(rows+1):
        startupWindow.rowconfigure(i, weight=1, minsize=50) # enables responsive row

    lbl_title = tk.Label(
        text="Text Battler",
        font=("Arial",24)
        )
    lbl_title.grid(row=0,column=1,columnspan=2,padx=12,pady=20)

    # Button to open up character builder window
    frm_modifyBuild = tk.Frame(
        master=startupWindow,
        relief=tk.RAISED,
        borderwidth=6
        )
    btn_modifyBuild = tk.Button(
        master=frm_modifyBuild,
        text="Modify Character",
        relief="raised",
        borderwidth=4,
        fg="white",
        bg="blue",
        font=("Arial",20),
        width=40,
        height=10,
        state="disabled"
        #command=lambda: characterBuilder()
        )
    frm_modifyBuild.grid(row=1,column=2,padx=12,pady=12)
    btn_modifyBuild.pack(fill=tk.BOTH)
    # Button to start battle
    frm_start = tk.Frame(
        master=startupWindow,
        relief=tk.RAISED,
        borderwidth=6
        )
    btn_start = tk.Button(
        master=frm_start,
        text="Enter Battle",
        relief="raised",
        borderwidth=4,
        fg="white",
        bg="red",
        font=("Arial",20),
        width=40,
        height=10,
        command=lambda: beginFight()
        )
    frm_start.grid(row=1,column=1,padx=12,pady=12)
    btn_start.pack(fill=tk.BOTH)

    startupWindow.mainloop() # MAIN LOOP- MUST COME LAST

# SECTION 2.0: COMBAT INITATION
def beginFight():
    global startupWindow
    startupWindow.destroy() # remove old window
    
    # Set up the global variables
    global roundCount # tracks number of rounds passed
    roundCount = 0
    global enemyKind # identifies the enemy block to use for stats
    enemyKind = "SKELETON"

    global playerHealth
    playerHealth = getClassStats(playerClass)["maxHealth"]
    global enemyHealth
    enemyHealth = getClassStats(enemyKind)["maxHealth"]

    global logEvents
    logEvents = [] # This list keeps track of every event that happens in battle, storing them as dictionaries.
    # Each event holds some values and a translated text line to print to display

    global battleDistance
    battleDistance = rand.randint(25,75) # generates distance between opponents at combat start. Measured in feet
    
    # This window displays battle info like enemy, distance, and events
    battleWindow = tk.Tk()
    battleWindow.title("Battle Log")
    columns=4
    rows=6

    for i in range(columns+1):
        battleWindow.columnconfigure(i, weight=1, minsize=75) # enables responsive column
    for i in range(rows+1):
        battleWindow.rowconfigure(i, weight=1, minsize=50) # enables responsive row

    # Action buttons
    btn_meleeAttack = tk.Button(
        master=battleWindow,
        text="Melee Attack",
        relief="groove",
        borderwidth=2,
        fg="red",
        bg="yellow",
        width=16,
        command=lambda: commandMeleeAttack()
        )
    btn_rangedAttack = tk.Button(
        master=battleWindow,
        text="Ranged Attack",
        relief="groove",
        borderwidth=2,
        fg="red",
        bg="yellow",
        width=16,
        state="disabled" # temporary disable until fixed
        #command=lambda: commandRangedAttack()
        )
    btn_moveForward = tk.Button(
        master=battleWindow,
        text="Forward",
        relief="groove",
        borderwidth=2,
        fg="white",
        bg="blue",
        width=16,
        command=lambda: promptMoveDistance("forward")
        )
    btn_moveBack = tk.Button(
        master=battleWindow,
        text="Back",
        fg="white",
        bg="blue",
        width=16,
        command=lambda: promptMoveDistance("back")
        )
    # Set up grid buttons for player actions
    btn_meleeAttack.grid(column=3,row=0,padx=8,pady=8,sticky="e")
    btn_rangedAttack.grid(column=3,row=1,padx=8,pady=8,sticky="e")
    btn_moveForward.grid(column=3,row=2,padx=8,pady=8,sticky="e")
    btn_moveBack.grid(column=3,row=3,padx=8,pady=8,sticky="e")

    # Statuses
    global lbl_playerHealth
    global lbl_playerTitle
    global lbl_enemyName
    global lbl_enemyHealth
    global lbl_battleDistance
    global lbl_rounds
    lbl_playerHealth = tk.Label(
        master=battleWindow,
        text="Your health: " + str(playerHealth),
        fg="green"
        )
    lbl_playerTitle = tk.Label(
        master=battleWindow,
        text=playerName + ", " + playerClass,
        fg="green"
        )
    lbl_enemyName = tk.Label(
        master=battleWindow,
        text="Enemy is " + enemyKind,
        fg="red"
        )
    lbl_enemyHealth = tk.Label(
        master=battleWindow,
        text="Enemy health: " + str(enemyHealth),
        fg="red"
        )
    lbl_battleDistance = tk.Label(
        master=battleWindow,
        text="Distance: " + str(battleDistance),
        fg="blue"
        )
    lbl_rounds = tk.Label(
        master=battleWindow,
        text="Round #" + str(roundCount+1),
        fg="blue"
        )
    # Pack player stats
    lbl_playerTitle.grid(column=0,row=0,sticky="w")
    lbl_playerHealth.grid(column=1,row=0,sticky="e")
    # Pack enemy stats
    lbl_enemyName.grid(column=0,row=1,sticky="w")
    lbl_enemyHealth.grid(column=1,row=1,sticky="e")
    # Pack general info
    lbl_battleDistance.grid(column=0,row=4,sticky="sw")
    lbl_rounds.grid(column=0,row=5,sticky="nw")

    # initiate combat
    writeCombatLog(eventType="combat_intro",actorA=playerName,actorB=enemyKind,value=str(battleDistance))
    #firstTurnCoinFlip() # randomly pick who goes first, then initiates turns
    battleWindow.mainloop() # MAIN LOOP- MUST COME LAST

# SECTION 2.1: PROCESS PLAYER ACTIONS
def commandMoveForward(dist=0):
    global moveWindow
    moveWindow.destroy() # remove distance selection window
    
    global battleDistance
    if battleDistance > 1 and int(dist) <= int(getClassStats(playerClass)["moveSpeed"]):
        battleDistance -= int(dist) # reduce distance on approach
        writeCombatLog(eventType="forward_move",actorA=playerName,value=dist)
        if battleDistance < 1:
            battleDistance = 1 # set minimum distance of 1 foot
        writeCombatLog(eventType="distance_report",value=battleDistance) # reports the new distance

        enemyAutoAction() # enemy turn
        return 1 #indicates action successfully used and consumed
    else:
        writeCombatLog(eventType="no_move")
        return 0 #indicates action cannot be used, try again
def commandMoveBack(dist=0):
    global moveWindow
    moveWindow.destroy() # remove distance selection window
    
    global battleDistance
    if battleDistance < 120 and int(dist) <= int(getClassStats(playerClass)["moveSpeed"]): # 120 is maximum distance
        battleDistance += int(dist) # increase distance on retreat
        writeCombatLog(eventType="back_move",actorA=playerName,value=dist)
        if battleDistance > 120:
            battleDistance = 120 # set maximum distance of 120 foot
        writeCombatLog(eventType="distance_report",value=battleDistance) # reports the new distance

        
        enemyAutoAction() # enemy turn
        return 1 #indicates action successfully used and consumed
    else:
        writeCombatLog(eventType="no_move")
        return 0 #indicates action cannot be used, try again

def commandMeleeAttack(): # Checks a melee attack against opponent. Deals damage on a hit.
    global battleDistance
    if battleDistance <= int(getClassStats(playerClass)["meleeReach"]):
        writeCombatLog(eventType="attack_on_target",actorA=playerName,actorB=enemyKind) # Log attack attempt
        acc = rand.randint(1,100) # roll chance to hit
        attackAccuracy = int(getClassStats(playerClass)["accuracy"]) # set accuracy for attack
        if acc <= attackAccuracy:
            # score hit
            attackDamage = rand.randint(int(getClassStats(playerClass)["meleeDamageMin"]),
                                        int(getClassStats(playerClass)["meleeDamageMax"])) # rolls damage between min and max
            finalDamage =int(attackDamage - int(getClassStats(enemyKind)["armor"])) # damage minus armor
            if finalDamage >= 1:
                global enemyHealth
                enemyHealth = str(int(enemyHealth) - finalDamage)

            if attackDamage >= 1: # Write log if attack hit
                if finalDamage >= 1: # Log if attack does any damage after armor reduction
                    writeCombatLog(eventType="hit_deal_damage",actorB=enemyKind,value=finalDamage)
                else:# Log if attack damage is negated by armor
                    writeCombatLog(eventType="hit_no_damage",actorB=enemyKind)
        else:
            writeCombatLog(eventType="hit_miss")
            
        enemyAutoAction() # enemy turn
        return 1 # indicates action successfully used
    else:
        writeCombatLog(eventType="enemy_out_reach",value=str(getClassStats(playerClass)["meleeReach"])) # write that enemy is too far away
        return 0 # indicates action cannot be used, try again

def promptMoveDistance(direction="forward",maxDist=120):
    dist = 0
    global moveWindow
    moveWindow = tk.Tk()
    moveWindow.title("Move")

    frm_main = tk.Frame( # main frame hold other frames
        master=moveWindow,
        bg="gray",
        width=300,
        height=400
        )
    lbl_move = tk.Label(
        master=frm_main,
        text="How far do you want to move?"
        )
    frm_move = tk.Frame(
        master=frm_main,
        width=50,
        relief="sunken"
        )
    ent_move = tk.Entry(
        master=frm_move
        )
    frm_main.pack()
    lbl_move.pack()
    frm_move.pack()
    ent_move.pack()

    if direction=="forward":
        btn_confirm = tk.Button(
            master=frm_main,
            width=20,
            height=5,
            text="Confirm",
            relief="raised",
            borderwidth=2,
            fg="white",
            bg="green",
            command=lambda: commandMoveForward(ent_move.get())
            ) # move dist forwards on confirm
    if direction=="back":
        btn_confirm = tk.Button(
            master=frm_main,
            width=20,
            height=5,
            text="Confirm",
            relief="raised",
            borderwidth=2,
            fg="white",
            bg="green",
            command=lambda: commandMoveBack(ent_move.get())
            ) # move dist forwards on confirm
    btn_cancel = tk.Button(
        master=frm_main,
        width=20,
        height=5,
        text="Cancel",
        relief="raised",
        borderwidth=2,
        fg="white",
        bg="red",
        command=lambda: moveWindow.destroy()
        ) # cancels the action
    btn_confirm.pack()
    btn_cancel.pack()

    moveWindow.mainloop()

# SECTION 2.2: PROCESS ENEMY ACTIONS
def enemyAutoAction():
    # The enemy auto-selects a command to use
    if enemyKind == "SKELETON":
        skeletonActions()
def skeletonActions():
    # used to determine auto-action selection for Skeleton class
    global battleDistance
    print("Skeleton chatters...")
    if battleDistance <= int(getClassStats(enemyKind)["meleeReach"]): # attack!
        writeCombatLog(eventType="attack_on_target",actorA=enemyKind,actorB=playerClass) # Log attack attempt
        acc = rand.randint(1,100) # roll chance to hit
        attackAccuracy = int(getClassStats(enemyKind)["accuracy"]) # set accuracy for attack
        if acc <= attackAccuracy:
            # score hit
            attackDamage = rand.randint(int(getClassStats(enemyKind)["meleeDamageMin"]),
                                        int(getClassStats(enemyKind)["meleeDamageMax"])) # rolls damage between min and max
            finalDamage =int(attackDamage - int(getClassStats(playerClass)["armor"])) # damage minus armor
            if finalDamage >= 1:
                global playerHealth
                playerHealth = str(int(playerHealth) - finalDamage)

            if attackDamage >= 1: # Write log if attack hit
                if finalDamage >= 1: # Log if attack does any damage after armor reduction
                    writeCombatLog(eventType="hit_deal_damage",actorB=playerName,value=finalDamage)
                else:# Log if attack damage is negated by armor
                    writeCombatLog(eventType="hit_no_damage",actorB=playerName)
        else:
            writeCombatLog(eventType="hit_miss")
    else: # approach to get in reach
        battleDistance -= int(getClassStats("SKELETON")["moveSpeed"])
        writeCombatLog(eventType="forward_move",actorA=enemyKind,value=dist)
        if battleDistance < 1:
            battleDistance = 1 # set minimum distance of 1 foot
        writeCombatLog(eventType="distance_report",value=battleDistance) # reports the new distance


# SECTION 2.3: WRITING LABELS FOR COMBAT LOG
def getLogText(eventType,actorA=None,actorB=None,value=0):
    # This function takes an event title and its values, then translates them to a text line to display in log.
    if eventType in logScripts.keys():
        logText = logScripts[eventType] # set to matching script

        # Replace variable strings in the script for output
        if "_eventActorA_" in logText:
            logText = logText.replace("_eventActorA_",str(actorA))
        if "_eventActorB_" in logText:
            logText = logText.replace("_eventActorB_",str(actorB))
        if "_eventValue_" in logText:
            logText = logText.replace("_eventValue_",str(value))

        #logText = logText + "\n" # add a newline char
    return str(logText)
def writeCombatLog(eventType,actorA=None,actorB=None,value=0):
    # Compiles an event dictionary, then appends that dict to the logEvents list
    eventDict = {"event":eventType}
    
    if actorA != None:
        eventDict["eventActorA"]=actorA
    if actorB != None:
        eventDict["eventActorB"]=actorB
    if value != None:
        eventDict["eventValue"]=value
    
    logText = getLogText(eventType=eventType,actorA=actorA,actorB=actorB,value=value) # gets a text line translation of the event and its variables
    print(logText) # prints text : REPLACE THIS WITH UPDATING GUI LABELS!
    eventDict["text"]=logText

    updateHealthLabels() # updates labels whenever new events are logged
    updateBattleInfoLabels() 

    global logEvents
    logEvents.append(eventDict) # append dictionary onto log
    return logText


# SECTION 3.0: INFO GATHERING
def getClassStats(className):
    global classDict # variable represents which class is used as reference for player stats
    classDict = None # default return value
    
    if className == "FIGHTER":
        classDict=stats_FIGHTER
    elif className == "WIZARD":
        classDict=stats_WIZARD
    elif className == "RANGER":
        classDict=stats_RANGER
    elif className == "SKELETON":
        classDict=stats_SKELETON

    return classDict
def updateHealthLabels():
    global lbl_playerHealth
    global playerHealth
    lbl_playerHealth["text"]="Your health: " + str(playerHealth)
    
    global lbl_enemyHealth
    global enemyHealth
    lbl_enemyHealth["text"]="Enemy health: " + str(enemyHealth)
def updateBattleInfoLabels():
    global lbl_battleDistance
    global lbl_rounds
    lbl_battleDistance["text"]="Distance: " + str(battleDistance)
    lbl_rounds["text"]="Round #" + str(roundCount)

gameSetup() # start the game
