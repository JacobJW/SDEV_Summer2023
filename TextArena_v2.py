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
    "new_enemy_intro":str("_eventActorA_ approaches as a new challenger! Begins _eventValue_ feet away."), # actor A is new enemy
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
    "no_move":str("There is no room to move."),
    "victory":str("_eventActorB_ is defeated! _eventActorA_ is victorious!"),
    "loss":str("_eventActorA_ is felled by _eventActorB_! Game over...")
    }
    # Use actor A for attacker/caster, and actor B for target (optional)
    # Use event value for damage points, healing points, or any other number (optional)

# These dictionaries hold all the stats for each class and enemy. Used as reference by game when calculating numbers and displaying information.
# maxHealth determines health at the start of the game, armor reduces damage suffered, moveSpeed determines maximum distance that can be covered in 1 turn
# meleeReach and rangedReach determine maximum distance you can attack from with respective weapons. DamageMin is minimum damage to roll for the attack, and DamageMax is the maximum to roll.
# accuracy represents the percent chance for any attack to hit the target.
# power shows the name of the character's special abilities. Currently, most are not implemented.
# desc writes details about the class. Ideally would be displayed in customization window.
# Monsters have portraits that determine the image file displayed when fighting them
global stats_FIGHTER
stats_FIGHTER = {
    "maxHealth":"125","armor":"20","moveSpeed":"30",
    "meleeReach":"8","meleeDamageMin":"22","meleeDamageMax":"44",
    "rangedReach":"30","rangedDamageMin":"15","rangedDamageMax":"55","rangedAmmo":"6",
    "accuracy":"75",
    "power":"SECOND WIND",
    "desc":"Heavily armored and wielding a large sword and backup pistol, the fighter is a deadly force in close range.\nIn addition, they can recover health between battles."
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
    "rangedReach":"90","rangedDamageMin":"25","rangedDamageMax":"50","rangedAmmo":"10",
    "accuracy":"85",
    "power":"DISSAPEAR",
    "desc":"The ranger can move quickly and fire deadly arrows from afar with great accuracy.\nIn addition, they can swiftly retreat from close fights."
    }
global stats_SKELETON
stats_SKELETON = {
    "maxHealth":"80","armor":"15","moveSpeed":"30",
    "meleeReach":"5","meleeDamageMin":"20","meleeDamageMax":"40",
    "rangedReach":"0","rangedDamageMin":"0","rangedDamageMax":"0","rangedAmmo":"0",
    "accuracy":"66",
    "power":"RATTLE",
    "portrait":"pixel-skull-clipart-1.png",
    "desc":"A walking skeletal corpse, armed with a rusty blade and covered in scraped armor."
    }
stats_GOBLIN = {
    "maxHealth":"80","armor":"8","moveSpeed":"40",
    "meleeReach":"5","meleeDamageMin":"14","meleeDamageMax":"28",
    "rangedReach":"20","rangedDamageMin":"12","rangedDamageMax":"35","rangedAmmo":"0",
    "accuracy":"70",
    "power":"COWER",
    "portrait":"goblin-archer-terraria.png",
    "desc":"A goblin archer."
    }


# SECTION 1.0: SETUP AND CHARACTER BUILD FUNCTIONS
def gameSetup():
    """Sets up the game on program startup"""
    # Set global variables
    global playerName # The displayed name of the player character
    playerName = "Champion"
    global playerClass # The class of the player character. Determines their stats
    playerClass = "FIGHTER"
    global list_classes # A list of all available classes (currently unused)
    list_classes = ["FIGHTER","WIZARD","ASSASSIN","RANGER"]

    global startupWindow
    startupWindow = tk.Tk() #Launch window to start game or enter customization
    startupWindow.title("Text Arena") # Write game title on window title
    rows = 3 # rows in the window
    columns = 3 # columns in the window

    for i in range(columns+1):
        startupWindow.columnconfigure(i, weight=1, minsize=80) # enables responsive columns
    for i in range(rows+1):
        startupWindow.rowconfigure(i, weight=1, minsize=30) # enables responsive rows

    lbl_title = tk.Label( # Displays the game's title on screen
        text="Text Battler",
        font=("TimesNewRoman",24)
        )
    lbl_title.grid(row=0,column=1,columnspan=2,padx=12,pady=20)

    frm_modifyBuild = tk.Frame( # Frame for button
        master=startupWindow,
        relief=tk.RAISED,
        borderwidth=6
        )
    btn_modifyBuild = tk.Button( # Button to open up character builder window to customize
        master=frm_modifyBuild,
        text="Modify Character",
        relief="raised",
        borderwidth=4,
        fg="white",
        bg="blue",
        font=("Arial",20),
        width=40,
        height=10,
        command=characterBuilder # Opens window and initializes varaibles
        )
    frm_modifyBuild.grid(row=1,column=2,padx=12,pady=12)
    btn_modifyBuild.pack(fill=tk.BOTH) # big button fills out frame

    frm_start = tk.Frame( # Frame for button
        master=startupWindow,
        relief=tk.RAISED,
        borderwidth=6
        )
    btn_start = tk.Button( # Button to close the launch window and start the game
        master=frm_start,
        text="Enter Battle",
        relief="raised",
        borderwidth=4,
        fg="white",
        bg="red",
        font=("Arial",20),
        width=40,
        height=10,
        command=beginFight
        )
    frm_start.grid(row=1,column=1,padx=12,pady=12)
    btn_start.pack(fill=tk.BOTH) # big button fills out frame

    startupWindow.mainloop() # Window loop

def characterBuilder():
    """Initializes the character customization window and all of its widgets"""
    # Create a new window to contain widgets for character creation.
    global charWindow
    charWindow = tk.Tk() # The window for editing character name and class
    charWindow.title("Character Builder")

    rows = 3 # rows in window
    columns = 5 # columns in window

    for i in range(columns+1):
        charWindow.columnconfigure(i, weight=1, minsize=75) # enables responsive column
    for i in range(rows+1):
        charWindow.rowconfigure(i, weight=1, minsize=50) # enables responsive row
    
    lbl_class = tk.Label(master=charWindow,text="Choose your class:") # Prompt text
    lbl_class.grid(row=1,column=0,padx=12,pady=12,sticky="W")

    global playerClass
    global selectedClass
    selectedClass = tk.StringVar(master=charWindow,value="FIGHTER") # Stringvar to be modified by radio buttons on class choice
    # Set up 3 radio buttons for the 3 classes
    rad_class1 = tk.Radiobutton(
        master=charWindow,
        text="Fighter",
        width=20,
        font=("Arial",12),
        variable = selectedClass,
        value="FIGHTER"
        )
    rad_class1.grid(row=1,column=1,padx=8,pady=12,sticky="W")
    
    rad_class2 = tk.Radiobutton(
        master=charWindow,
        text="Wizard",
        width=20,
        font=("Arial",12),
        variable = selectedClass,
        value="WIZARD"
        )
    rad_class2.grid(row=1,column=2,padx=8,pady=12,sticky="W")

    rad_class3 = tk.Radiobutton(
        master=charWindow,
        text="Ranger",
        width=20,
        font=("Arial",13),
        variable = selectedClass,
        value="RANGER"
        )
    rad_class3.grid(row=1,column=3,padx=8,pady=12,sticky="W")

    lbl_nameBar = tk.Label( # Prompt label
        master=charWindow,
        text="Name your champion:"
        )
    lbl_nameBar.grid(row=0,column=0,padx=8,pady=12)

    global ent_playerName # An entry bar to input custom character name
    ent_playerName = tk.Entry(
        master=charWindow,
        width=70,
        bg="white",
        fg="black",
        relief="groove"
        )
    ent_playerName.grid(row=0,column=1,padx=8,pady=12,columnspan=2)
    ent_playerName.insert(index=0,string="Champion") # Sets the default name in the bar

    btn_done = tk.Button( # Button to close the window and save changes
        master=charWindow,
        text="Finished",
        fg="white",
        bg="green",
        relief=tk.RAISED,
        borderwidth=4,
        width=100,
        command= commitCharacter # Complete customization, close window
        )
    btn_done.grid(row=2,column=1,padx=8,pady=8,columnspan=3)

    charWindow.mainloop() # Window loop

def commitCharacter():
    """Takes values input in character modifier and saves them"""
    global ent_playerName
    global selectedClass
    global playerName
    global playerClass
    playerName = ent_playerName.get() # get name from entry bar
    playerClass = selectedClass.get() # set class to selection from radio buttons
    print(playerName + " will be a " + playerClass) # Combine to make an output string
    global charWindow
    charWindow.destroy() # Closes the customization window after finish

    #print(playerName + " will be a " + playerClass) # Output

# SECTION 2.0: COMBAT INITATION
def beginFight():
    """Creates the battler window, sets up combat variables, and creates necessary buttons and labels."""
    global startupWindow
    startupWindow.destroy() # remove old window
    
    # Set up the global variables
    global roundCount # tracks number of rounds passed
    roundCount = 0
    global killCount # tracks the number of enemies defeated
    killCount = 0
    global killsToWin # the amount of kills needed to win the game
    killsToWin = 3
    global enemyKind # identifies the enemy block to use for stats
    enemyKind = "SKELETON"

    global playerHealth
    playerHealth = getClassStats(playerClass)["maxHealth"]
    global enemyHealth
    enemyHealth = getClassStats(enemyKind)["maxHealth"]

    global logEvents
    logEvents = [] # This list keeps track of every event that happens in battle, storing them as dictionaries.
    # Each event holds some names, values, and a translated text line to print to display

    global battleDistance # Tracks the distance between the player and their enemy. Changes when moving. Measured in feet
    battleDistance = rand.randint(25,60) # Generate a random beginning distance
    
    battleWindow = tk.Tk() # This window displays battle info like enemy, distance, and events
    battleWindow.title("Battle Log")
    columns=5 # columns in window
    rows=5 # rows in window

    global selectedWeapon # Determines whether player uses melee or ranged attack. 1 for melee, 2 for ranged
    selectedWeapon = tk.IntVar(master=battleWindow,value=1) # Set up stringvar to be modified by radio buttons
    selectedWeapon.set(1) # Default to 1 (melee)

    for i in range(columns+1):
        battleWindow.columnconfigure(i, weight=1, minsize=40) # enables responsive column
    for i in range(rows+1):
        battleWindow.rowconfigure(i, weight=1, minsize=10) # enables responsive row

    # Action buttons
    ## all following widgets are global so that they can be disabled with other functions
    global rad_pickMelee # Button to select melee for next attack
    rad_pickMelee = tk.Radiobutton( 
        master=battleWindow,
        text="Melee",
        value=1,
        variable=selectedWeapon
        )
    global rad_pickRanged # Button to select ranged for next attack
    rad_pickRanged = tk.Radiobutton( 
        master=battleWindow,
        text="Ranged",
        value=2,
        variable=selectedWeapon
        )
    global btn_attack # Button to attack the enemy
    btn_attack = tk.Button(
        master=battleWindow,
        text="Attack!",
        relief="groove",
        borderwidth=2,
        fg="red",
        bg="yellow",
        width=20,
        command=commandAttack
        )
    lbl_moveDistance = tk.Label( # Prompt label
        master=battleWindow,
        text="Input move distance here.\nUse neg (-) for backwards."
        )
    global btn_power # Button to activate special class power
    btn_power = tk.Button(
        master=battleWindow,
        text="Power",
        relief="groove",
        fg="white",
        bg="purple",
        width=20,
        command= commandUsePlayerPower
        )
    global ent_moveDistance # Enter a number in the bar to set next move distance
    ent_moveDistance = tk.Entry( 
        master=battleWindow,
        relief="sunken",
        borderwidth=4,
        fg="black",
        bg="white",
        width=23
        )
    global btn_move # Button to initiate movement, using value from entry bar
    btn_move= tk.Button( 
        master=battleWindow,
        text="Move",
        relief="groove",
        borderwidth=2,
        fg="white",
        bg="blue",
        width=20,
        command= commandMove
        )
    btn_quit = tk.Button( # Button to quit the game, closing the window
        master=battleWindow,
        text="Quit",
        width=20,
        borderwidth=2,
        fg="white",
        bg="red",
        relief="groove",
        command= lambda: battleWindow.destroy()
        )
    # Set up grid buttons for player action widgets
    btn_attack.grid(column=4,row=0,padx=8,pady=8,sticky="e")
    btn_power.grid(column=4,row=2,padx=8,pady=8,sticky="e")
    rad_pickMelee.grid(column=4,row=1,padx=8,pady=4,sticky="w")
    rad_pickRanged.grid(column=4,row=1,padx=8,pady=4,sticky="e")
    btn_move.grid(column=4,row=3,padx=8,pady=4,sticky="e")
    ent_moveDistance.grid(column=4,row=4,padx=8,pady=0,sticky="ne")
    lbl_moveDistance.grid(column=4,row=4,padx=8,pady=20,sticky="se")
    btn_quit.grid(column=4,row=5,padx=8,pady=32,sticky="se")

    # Set up global battle stats
    global lbl_playerHealth # Shows the player's remaining health
    global lbl_playerTitle # Shows player name and class
    global lbl_enemyName # Shows enemy name
    global lbl_enemyHealth # Shows the enemy's remaining health
    global lbl_battleDistance # Shows distance between opponents
    global lbl_rounds # Shows how many rounds have passed
    global lbl_kills # Shows how many enemies have been defeated
    
    # Player information labels
    lbl_playerHealth = tk.Label(
        master=battleWindow,
        text="Your health: " + str(playerHealth),
        fg="green"
        )
    lbl_playerHealth.config(font=("Courier",12))
    lbl_playerTitle = tk.Label(
        master=battleWindow,
        text=playerName+"\n "+playerClass, # Display player class under name
        fg="green"
        )
    lbl_playerTitle.config(font=("Courier",13))
    
    # Enemy information labels
    lbl_enemyName = tk.Label(
        master=battleWindow,
        text="Current Enemy\n " + enemyKind,
        fg="red"
        )
    lbl_enemyName.config(font=("Courier",11))
    lbl_enemyHealth = tk.Label(
        master=battleWindow,
        text="Enemy health: " + str(enemyHealth),
        fg="red"
        )
    lbl_enemyHealth.config(font=("Courier",11))
    
    # General information labels
    lbl_battleDistance = tk.Label(
        master=battleWindow,
        text="Distance to opponent: " + str(battleDistance),
        fg="blue"
        )
    lbl_battleDistance.config(font=("Courier",11))
    lbl_rounds = tk.Label(
        master=battleWindow,
        text="Round #" + str(roundCount+1),
        fg="blue"
        )
    lbl_rounds.config(font=("Courier",11))
    lbl_kills = tk.Label(
        master=battleWindow,
        text=str(killCount)+ " / " + str(killsToWin) + " enemies felled.",
        fg="blue"
        )
    lbl_kills.config(font=("Courier,12"))
    
    # Pack player stats
    lbl_playerTitle.grid(column=0,row=0)
    lbl_playerHealth.grid(column=1,row=0,sticky="e")
    # Pack enemy stats
    lbl_enemyName.grid(column=0,row=1)
    lbl_enemyHealth.grid(column=1,row=1,sticky="e")
    # Pack general info
    lbl_battleDistance.grid(column=0,row=3,sticky="sw")
    lbl_rounds.grid(column=0,row=4,sticky="nw")
    lbl_kills.grid(column=0,row=5,sticky="w")

    # Set up simple enemy icon
    iconFile = getClassStats(enemyKind)["portrait"]
    global img_enemyIcon # Stores the image file for enemy icon
    global lbl_enemyIcon # Displays the enemy icon image
    img_enemyIcon = tk.PhotoImage(
        master=battleWindow,
        file=iconFile
        )
    lbl_enemyIcon = tk.Label(
        master=battleWindow,
        image= img_enemyIcon
        )
    lbl_enemyIcon.grid(column=1,row=2,columnspan=3,rowspan=4)

    writeCombatLog(eventType="combat_intro",actorA=playerName,actorB=enemyKind,value=str(battleDistance)) # Introduce enemy and player in first round
    #firstTurnCoinFlip() # Randomly pick who goes first, then initiates round as usual. Disabled.
    battleWindow.mainloop() # Window loop

# SECTION 2.1: PROCESS PLAYER ACTIONS
def commandMove():
    """Reduces or increases distance to enemy by amount specified by player entry."""
    dist = ent_moveDistance.get() # Get distance from the movement entry bar
    maxDist = int(getClassStats(playerClass)["moveSpeed"]) # The maximum distance the player can cover with 1 turn
    global battleDistance # Get distance between opponents

    print("") # Print gap in lines
    
    if dist.lstrip("+-").isdigit() == True: # Check if valid integer
        if dist[0]=="-":
            neg=1 # Detect negative distance (backwards)
        else:
            neg=0 # Not negative distance (forwards)
            
        dist = abs(int(dist)) # Use absolute value for calculation
        if battleDistance >= 1 and dist >= 1 and dist <= maxDist: # Check if past the minimum 1 foot, move distance > 0, and if absolute distance is within move speed
            if neg == 0: # Move forward
                battleDistance -= dist # Reduce distance
                writeCombatLog(eventType="forward_move",actorA=playerName,value=str(dist)) # Write output
            else:
                battleDistance += dist # Increase distance
                writeCombatLog(eventType="back_move",actorA=playerName,value=str(dist)) # Write output
                    
            if battleDistance < 1:
                battleDistance = 1 # Sets a minimum distance of 1 foot
            writeCombatLog(eventType="distance_report",value=battleDistance) # Reports the new distance after the movement

            enemyAutoAction() # Enemt takes a turn
            return 1 #Indicates action successfully used and consumed
        else:
            writeCombatLog(eventType="no_move") # Reports that the action could not be used
            return 0 #Indicates action could be used, so try again
    else:
        print("You must enter an integer with no spaces for movement distance.") # Reports invalid input
        return 0 # Indicates action could not be used, so try again
    
def commandAttack():
    """Checks an attack against opponent using selected weapon. Deals damage if it hits."""
    global battleDistance # Get distance between opponents
    global selectedWeapon
    print("") # Print gap in lines
    
    if selectedWeapon.get() == 1: # melee
        #print("melee")
        attackAccuracy = int(getClassStats(playerClass)["accuracy"]) # Sets accuracy for attack
        reach = int(getClassStats(playerClass)["meleeReach"]) # Sets max distance to attack
        minDamage = int(getClassStats(playerClass)["meleeDamageMin"]) # Sets min damage to roll
        maxDamage = int(getClassStats(playerClass)["meleeDamageMax"])+1 # Sets max damage to roll. +1 to make range inclusive.
    elif selectedWeapon.get() == 2: # ranged
        #print("ranged")
        attackAccuracy = int(getClassStats(playerClass)["accuracy"]) # set accuracy for attack
        reach = int(getClassStats(playerClass)["rangedReach"]) # Set max distance to attack
        minDamage = int(getClassStats(playerClass)["rangedDamageMin"]) # Sets min damage to roll
        maxDamage = int(getClassStats(playerClass)["rangedDamageMax"])+1 # Sets max damage to roll. +1 to make range inclusive.
        if battleDistance <= int(getClassStats(enemyKind)["meleeReach"]): # Check if enemy too close
            attackAccuracy -= 25 # Ranged attacks have an accuracy penalty when in close quarters (or in enemy melee reach)
    
    if battleDistance <= reach: # Check if enemy is within maximum distance
        writeCombatLog(eventType="attack_on_target",actorA=playerName,actorB=enemyKind) # Print attack attempt
        acc = rand.randint(1,100) # Roll a chance to hit against accuracy
        if acc <= attackAccuracy:
            # Scores a hit
            attackDamage = rand.randint(minDamage,maxDamage) # Roll damage between min and max
            finalDamage =int(attackDamage - int(getClassStats(enemyKind)["armor"])) # Reduces damage by the enemy's armor
            if finalDamage >= 1:
                global enemyHealth
                enemyHealth = str(int(enemyHealth) - finalDamage) # Damage enemy health

            if attackDamage >= 1: # Print log if attack hits
                if finalDamage >= 1: # Print log if attack does damage
                    writeCombatLog(eventType="hit_deal_damage",actorB=enemyKind,value=finalDamage)
                else:# Print log if attack damage is fully negated by armor
                    writeCombatLog(eventType="hit_no_damage",actorB=enemyKind)
        else:
            writeCombatLog(eventType="hit_miss") # Print the attack failed to hit
            
        enemyAutoAction() # Enemy takes a turn
        return 1 # Indicates action successfully used
    else:
        writeCombatLog(eventType="enemy_out_reach",value=reach) # Print enemy is too far away
        return 0 # Indicates action could not be used, so try again

def commandUsePlayerPower():
    """Tries to activate a power based on player class"""
    if playerClass == "FIGHTER":
        rushAttack() # Activate fighter rush power
    elif playerClass == "WIZARD":
        castSpell() # Activate wizard spell power

def rushAttack():
    """Fighter class can use rush attack to close short distances before using melee attack"""
    global battleDistance
    global selectedWeapon
    meleeReach = int(getClassStats("FIGHTER")["meleeReach"]) # Get melee reach
    rushDist = 10 + meleeReach # Max dist to cover equals melee reach plus 10

    if battleDistance <= rushDist:
        selectedWeapon.set(1) # Set weapon to melee
        battleDistance = 5 # Instantly close distance, getting directly into melee
        print("\n" + playerName + " rushes towards the enemy!")
        commandAttack() # Prompt attack after rush

        return 1 # Indicates action successfully used
    else:
        writeCombatLog(eventType="enemy_out_reach",value=str(rushDist)) # Print enemy is too far away
        return 0 # Indicates action could not be used, so try again
    
def castSpell():
    """Wizard character casts a spell to cause a wild effect."""
    global battleDistance
    global playerHealth
    global enemyHealth

    print("") # Print gap in lines

    if battleDistance <= 20: # All spells have 20 feet max range
        i = rand.randint(0,3) # Pick random spell out of 4
        customText = playerName + " invokes magic to cast a spell..." # Write text to save to log
        writeCustomLog(eventType="cast_spell",text=customText,actorA=playerName,value=i) # Prints and saves a custom log text
    
        if i == 0: # Wind blast tosses far away
            battleDistance += 40 # Push enemy to make distance

            customText = playerName + " casts Wind Blast! " + enemyKind + " is flung 35 feet away!" # Write text to save to log
            writeCustomLog(eventType="spell_windblast",text=customText,actorA=playerName,actorB=enemyKind,value="40") # Prints and saves a custom log text
            writeCombatLog(eventType="distance_report",value=battleDistance) # Reports the new distance after the movement
            
        elif i == 1: # Steal life to damage enemy and heal self
            minDamage = 20 # minimum damage for this attack
            maxDamage = 36 # maximum damage for this attack

            customText = playerName + " casts Leeching at " + enemyKind +"!" # Write text to save to log
            writeCustomLog(eventType="spell_leeching",text=customText,actorA=playerName,actorB=enemyKind) # Prints and saves a custom log text
            
            attackDamage = rand.randint(minDamage,maxDamage+1) # Roll damage between min and max
            finalDamage =int(attackDamage - int(getClassStats(enemyKind)["armor"])) # Reduces damage by the enemy's armor
                
            if finalDamage >= 1:
                global enemyHealth
                enemyHealth = str(int(enemyHealth) - finalDamage) # Damage enemy health
                halfDamage = round(finalDamage/2) # Calculate half damage
                playerHealth = str(int(playerHealth) + halfDamage) # Heals player for half damage

            if attackDamage >= 1: # Print log if attack hits
                if finalDamage >= 1: # Print log if attack does damage
                    writeCombatLog(eventType="hit_deal_damage",actorB=enemyKind,value=finalDamage) # Print attack damage
                    customText = playerName + " heals " + str(halfDamage) + " health!" # Write text to save to log
                    writeCustomLog(eventType="spell_leeching",text=customText,actorA=playerName,actorB=enemyKind,value=str(halfDamage)) # Prints and saves a custom log text
                else:# Print log if attack damage is fully negated by armor
                    writeCombatLog(eventType="hit_no_damage",actorB=enemyKind)
        elif i == 2: # Fire ball does heavy damage that ignores armor, but can also damage self if too close to enemy
            minDamage = 15 # minimum damage for this attack
            maxDamage = 60 # maximum damage for this attack
            
            attackDamage = rand.randint(minDamage,maxDamage+1) # Roll damage between min and max
            halfDamage = round(attackDamage/2) # Calculate half damage
            enemyHealth = str(int(enemyHealth) - attackDamage) # Reduce health

            customText = playerName + " casts Fireball at " + enemyKind +"! Deals " + str(attackDamage) + " damage!" # Write text to save to log
            writeCustomLog(eventType="spell_fireball",text=customText,actorA=playerName,actorB=enemyKind,value=str(attackDamage)) # Prints and saves a custom log text

            if battleDistance <= 5: # Player takes damage if too close when casting this spell
                playerHealth = str(int(playerHealth) - halfDamage) # Reduce health

                customText = playerName + " is too close to the blast! Takes " + str(halfDamage) + " damage!" # Write text to save to log
                writeCustomLog(eventType="spell_fireball",text=customText,actorA=playerName,value=str(halfDamage)) # Prints and saves a custom log text
        elif i == 3: # Spell fail
            customText = "The spell flares, then fizzles out. Nothing happens..."
            writeCustomLog(eventType="spell_fireball",text=customText) # Prints and saves a custom log text

        enemyAutoAction() # Enemy takes a turn
        return 1 # Indicates action successfully used
    else:
        customText = "The enemy is too far! You can only cast spells out to 20 feet away."
        writeCustomLog(eventType="enemy_out_spell_range",text=customText) # Prints and saves a custom log text
        return 0 # Indicates action could not be used, so try again
        

# SECTION 2.2: PROCESS ENEMY ACTIONS
def enemyAutoAction():
    """The enemy automatically picks an action to take immediately after the player acts. Also tracks and checks some stats at the same time"""
    global roundCount
    global killCount
    roundCount += 1 # Increase rounds passed
    if int(enemyHealth) >= 1 and int(playerHealth) >= 1: # Check if both are living
        if enemyKind == "SKELETON":
            skeletonActions()
        elif enemyKind == "GOBLIN":
            goblinActions()
    elif int(playerHealth) <= 0:# Player is dead
        gameOver() 
    elif int(enemyHealth) <= 0:# Enemy is dead
        killCount += 1 # Add kill to count
        customText = enemyKind + " is defeated!"
        writeCustomLog(eventType="enemy_kill",text=customText,actorA=enemyKind) # Prints and saves a custom log text
        
        if killCount < killsToWin: # End game once enough enemies are killed
            newEnemy() # Summon a new enemy to take place of the slain
        else:
            winGame() # All enemies are defeated. Win the game

def newEnemy():
    """Summons a new enemy to take the place of the last opponent"""
    i = rand.randint(0,2) # Randomly selects next opponent
    if i == 0:
        newEnemy = "SKELETON"
    else:
        newEnemy = "GOBLIN"
        
    global battleDistance
    battleDistance = rand.randint(30,60) # Reset distance
    
    global enemyKind # Identifies the enemy block to use for stats
    enemyKind = newEnemy # Change enemy class
    writeCombatLog(eventType="new_enemy_intro",actorA=newEnemy,value=battleDistance) # Introduce the new enemy

    # Set up new portrait icon
    iconFile = getClassStats(newEnemy)["portrait"]
    global img_enemyIcon
    global lbl_enemyIcon
    img_enemyIcon["file"] = iconFile # Change image file to match new enemy
    lbl_enemyIcon["image"] = img_enemyIcon # Update portrait label

    global playerHealth 
    global enemyHealth # Resets enemy health
    enemyHealth = getClassStats(enemyKind)["maxHealth"]

    # Player regains some health after each enemy defeat
    playerHealth = str(int(playerHealth) + 25) # Restore health
    if int(playerHealth) > int(getClassStats("FIGHTER")["maxHealth"]): # Check if health exceeds max
        playerHealth = getClassStats("FIGHTER")["maxHealth"] # Enforce maximum
    customText = playerName + " gets a second wind! Recovers 25 health."
    writeCustomLog(eventType="enemy_kill",text=customText,actorA=playerName,value="25") # Prints and saves a custom log text
    
    
            
    # update labels to match new info
    updateBattleInfoLabels()
    updateHealthLabels()
    
def skeletonActions():
    """Used to determine auto-action selection for Skeleton class"""
    global battleDistance
    global playerHealth
    print("\nSkeleton chatters...") # Enemy idle text
    if battleDistance <= int(getClassStats(enemyKind)["meleeReach"]): # Player in reach, attack!
        attackAccuracy = int(getClassStats(enemyKind)["accuracy"]) # Set accuracy to roll against
        minDamage = int(getClassStats(enemyKind)["meleeDamageMin"]) # Minimum damage roll
        maxDamage = int(getClassStats(enemyKind)["meleeDamageMax"])+1 # Maximum damage roll, +1 to make range inclusive
        
        writeCombatLog(eventType="attack_on_target",actorA=enemyKind,actorB=playerName) # Print attack attempt
        acc = rand.randint(1,100) # Roll chance to hit vs accuracy
        if acc <= attackAccuracy: # Rolled under accuracy, score a hit
            attackDamage = rand.randint(minDamage,maxDamage) # rolls damage between min and max
            finalDamage =int(attackDamage - int(getClassStats(playerClass)["armor"])) # Subtract target armor from damage
            if finalDamage >= 1:
                playerHealth = str(int(playerHealth) - finalDamage) # Damage player

            if attackDamage >= 1: # Print if attack hit
                if finalDamage >= 1: # Print if attack deals damage
                    writeCombatLog(eventType="hit_deal_damage",actorB=playerName,value=finalDamage)
                else:# Print if attack damage is fully negated
                    writeCombatLog(eventType="hit_no_damage",actorB=playerName)
        else:
            writeCombatLog(eventType="hit_miss") # Print attack missed
    else:  # Approach the enemy to get in reach
        dist = int(getClassStats("SKELETON")["moveSpeed"]) # Get max move distance
        battleDistance -= dist # Reduce distance with forward move
        writeCombatLog(eventType="forward_move",actorA=enemyKind,value=dist) # Print movement report
        if battleDistance < 1: # Check minimum distance of 1 foot
            battleDistance = 1 # Enforce minimum distance
        writeCombatLog(eventType="distance_report",value=battleDistance) # Reports the new distance
def goblinActions():
    """Used to determine auto-action selection for Goblin class"""
    global battleDistance
    global playerHealth
    print("\nGoblin snickers...") # Enemy idle text

    if battleDistance <= 5: # Check if close to player
        chance = rand.randint(0,1) # Take 50% chance to flee or fight
        if chance == 0: # Choose attack
            if battleDistance <= int(getClassStats(enemyKind)["meleeReach"]): # Player in reach, attack!
                attackAccuracy = int(getClassStats(enemyKind)["accuracy"]) # Set accuracy to roll against
                minDamage = int(getClassStats(enemyKind)["meleeDamageMin"]) # Minimum damage roll
                maxDamage = int(getClassStats(enemyKind)["meleeDamageMax"])+1 # Maximum damage roll, +1 to make range inclusive
                
                writeCombatLog(eventType="attack_on_target",actorA=enemyKind,actorB=playerName) # Print attack attempt
                acc = rand.randint(1,100) # Roll chance vs accuracy
                if acc <= attackAccuracy: # Rolled under accuracy, score a hit
                    attackDamage = rand.randint(minDamage,maxDamage) # rolls damage between min and max
                    finalDamage =int(attackDamage - int(getClassStats(playerClass)["armor"])) # Subtract target armor from damage
                    if finalDamage >= 1:
                        playerHealth = str(int(playerHealth) - finalDamage) # Damage player

                    if attackDamage >= 1: # Print log if attack hit
                        if finalDamage >= 1: # Print if attack deals damage
                            writeCombatLog(eventType="hit_deal_damage",actorB=playerName,value=finalDamage)
                        else:# Print if attack damage is fully negated
                            writeCombatLog(eventType="hit_no_damage",actorB=playerName)
                else:
                    writeCombatLog(eventType="hit_miss") # Print if attack missed
        else: # Flee to get out of reach
            dist = int(getClassStats("GOBLIN")["moveSpeed"]) # Get max move distance
            battleDistance += dist # Increase distance with backwards move
            writeCombatLog(eventType="back_move",actorA=enemyKind,value=dist) # Print movement report
            if battleDistance < 1:# Check minimum distance of 1 foot
                battleDistance = 1 # Enforce minimum distance
            writeCombatLog(eventType="distance_report",value=battleDistance) # Report the new distance
    elif battleDistance <= int(getClassStats(enemyKind)["rangedReach"]): # Enemy in range, attack!
        attackAccuracy = int(getClassStats(enemyKind)["accuracy"]) # Set accuracy to roll against
        minDamage = int(getClassStats(enemyKind)["rangedDamageMin"]) # Minimum damage roll
        maxDamage = int(getClassStats(enemyKind)["rangedDamageMax"])+ 1 # Maximum damage roll, +1 to make range inclusive
        
        writeCombatLog(eventType="attack_on_target",actorA=enemyKind,actorB=playerName) # Print attack attempt
        acc = rand.randint(1,100) # Roll chance vs accuracy
        if acc <= attackAccuracy: # Rolled under accuracy, score a hit
            attackDamage = rand.randint(minDamage,maxDamage) # rolls damage between min and max
            finalDamage =int(attackDamage - int(getClassStats(playerClass)["armor"])) # Subtact target armor from damage
            if finalDamage >= 1:
                playerHealth = str(int(playerHealth) - finalDamage) # Damage player

            if attackDamage >= 1: # Print log if attack hit
                if finalDamage >= 1: # Print if attack deals damage
                    writeCombatLog(eventType="hit_deal_damage",actorB=playerName,value=finalDamage)
                else:# Print if attack damage is fully negated
                    writeCombatLog(eventType="hit_no_damage",actorB=playerName)
        else:
            writeCombatLog(eventType="hit_miss") # Print if attack missed
    else:  # Approach the enemy to get in reach
        dist = int(getClassStats("GOBLIN")["moveSpeed"]) # Get max move distance
        battleDistance -= dist # Reduce distance with forward move
        writeCombatLog(eventType="forward_move",actorA=enemyKind,value=dist) # Print movement report
        if battleDistance < 1: # Check minimum distance of 1 foot
            battleDistance = 1 # Enforce minimum distance
        writeCombatLog(eventType="distance_report",value=battleDistance) # Reports the new distance


# SECTION 2.3: WRITING LABELS FOR COMBAT LOG
def getLogText(eventType,actorA=None,actorB=None,value=0):
    """This function takes an event title and its values, then translates them to a text line to save in log and print out."""
    if eventType in logScripts.keys(): # Check if event type exists
        logText = logScripts[eventType] # Set script to modify

        # Replace variable strings in the script for output
        if "_eventActorA_" in logText: # Replace with A name
            logText = logText.replace("_eventActorA_",str(actorA))
        if "_eventActorB_" in logText: # Replace with B name
            logText = logText.replace("_eventActorB_",str(actorB))
        if "_eventValue_" in logText: # Replace with value
            logText = logText.replace("_eventValue_",str(value))
    return str(logText) # Return translated text line
def writeCombatLog(eventType,actorA=None,actorB=None,value=0):
    """Gets and prints event log, then compiles an event dictionary to append to logEvents list."""
    eventDict = {"event":eventType} # Create a dictionary to store event data
    
    if actorA != None: # Check if actor A is provided
        eventDict["eventActorA"]=actorA
    if actorB != None: # Check is actor B is provided
        eventDict["eventActorB"]=actorB
    if value != None: # Check if value is provided
        eventDict["eventValue"]=value
    
    logText = getLogText(eventType=eventType,actorA=actorA,actorB=actorB,value=value) # Gets a text line with names and values replaced to match the event
    print(logText) # Prints out the log text
    eventDict["text"]=logText # Saves text to dictionary

    updateHealthLabels() # Update global labels whenever new events are logged
    updateBattleInfoLabels() 

    global logEvents
    logEvents.append(eventDict) # Append dict to log event list
    return logText # Returns the new text
def writeCustomLog(eventType="Custom",text="Sample text",actorA=None,actorB=None,value=0):
    """Accepts a customized text line, then converts it into a log to save and print out."""
    customEvent = str(eventType + "*") # Asterisk marks a custom event
    eventDict = {"event":customEvent} # Creates a custom named event

    if actorA != None: # Check if actor A is provided
        eventDict["eventActorA"]=actorA
    if actorB != None: # Check is actor B is provided
        eventDict["eventActorB"]=actorB
    if value != None: # Check if value is provided
        eventDict["eventValue"]=value

    print(text) # Prints out the log text
    eventDict["text"]=text # Saves text to dictionary

    updateHealthLabels() # Update global labels whenever new events are logged
    updateBattleInfoLabels() 

# SECTION 3.0: INFO GATHERING
def getClassStats(className):
    """Takes a class or enemy name, then outputs the reference dictionary for its stats."""
    classDict = None # Default to return value
    
    if className == "FIGHTER": # Return Fighter dict
        classDict=stats_FIGHTER
    elif className == "WIZARD": # Return Wizard dict
        classDict=stats_WIZARD
    elif className == "RANGER": # Return Ranger dict
        classDict=stats_RANGER
    elif className == "SKELETON": # Return skeleton dict
        classDict=stats_SKELETON
    elif className == "GOBLIN": # Return goblin dict
        classDict=stats_GOBLIN

    return classDict # Returns the located dictionary, or None if it does not exist
def updateHealthLabels():
    """Updates global labels that display player and enemy health."""
    global lbl_playerHealth # Label
    global playerHealth # Current health
    lbl_playerHealth["text"]="Your health: " + str(playerHealth) # Update
    
    global lbl_enemyHealth # Label
    global enemyHealth # Current health
    lbl_enemyHealth["text"]="Enemy health: " + str(enemyHealth) # Update
def updateBattleInfoLabels():
    """Updates global labels that display kills, distance, and rounds."""
    global lbl_battleDistance
    global lbl_rounds
    global lbl_kills
    lbl_battleDistance["text"]="Distance: " + str(battleDistance) # Update to current value
    lbl_rounds["text"]="Round #" + str(roundCount) # Update to current value
    lbl_kills["text"]=str(killCount)+ " / " + str(killsToWin) + " enemies felled." # Update to current value of kills out of total enemies

# SECTION 4.0: GAME END
def winGame():
    """Announces victory and disables all buttons"""
    # Add: Creates a new popup window to end the game
    writeCombatLog(eventType="victory",actorA=playerName,actorB=enemyKind) # Print victory text
    disableWidgets() # Does as the name says
def gameOver():
    """Announces game over and disables all buttons"""
    # Add: Creates a new popup window to end the game
    writeCombatLog(eventType="loss",actorA=playerName,actorB=enemyKind) # Print loss text
    disableWidgets() # Does as the name says
def disableWidgets():
    """Deactivates all global interactive widgets of the battle window"""
    # Pick out the global widgets
    global rad_pickMelee
    global rad_pickRanged
    global btn_attack
    global ent_moveDistance
    global btn_move
    # Disable all the widgets
    rad_pickMelee.__setitem__(key="state",value="disabled")
    rad_pickRanged.__setitem__(key="state",value="disabled")
    btn_attack.__setitem__(key="state",value="disabled")
    ent_moveDistance.__setitem__(key="state",value="disabled")
    btn_move.__setitem__(key="state",value="disabled")
    btn_power.__setitem__(key="state",value="disabled")

gameSetup() # Start the game
