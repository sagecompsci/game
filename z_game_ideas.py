def nothing(): pass

"""
 - create monster killing quest
 - craft cooked drumstick
 - more ui info

                                 
to-do
    - figure out location and uses
    - redo creating monsters
    - figure out actual stats and drops
    - create npcs
    - create quests
    - generate village
    - create shops
    - create simple version of journal
    - change data and inventory 
        - combine armor, bracelets, necklaces, rings into one named tuple
        - create accessories inventory

    
    - wake up by a silver tree.
    - after you get certain number of tiles away you come across an injured centaur
        - gives you quest, their caravan was attacked by a pack of wolves and they need help
        - they ask you to go to the nearest village and find help, village shows up on map, and they give you directions
        - centaurs gives you flint, wood, and some food
    - once you get to village you talk to guards and tell them what happened
    - you go with the guards back to the centaur camp
    - the healer gives another quest to ask if you can gather some materials
    - healer gives you recipe for medicinal brew
    - if you don't accept the first quest everyone dies
    - if you don't accept the second quest some die

- wake up in a bed in the village
- leave the room/house to find someone

    - you were found passed out in the field? what happened?
    - I don't remember anything
    - maybe if you make it to the bottom you can wish for your memories back
- kill weeds in an abandoned house. Give food to take. There is one regular weed
    - in return i'll show you how to craft simple items

general 
    - floors are in upside pyramid, floors get smaller as you go down
    - the tower is the world tree, the levels are the roots that get bigger as you go up
    - eventually there is extra content, another pyramid that are the roots
        - can be accessed when you choose wish from tree
    - there is a flower on every level. These flowers were stolen from the tree a long time ago and must be returned to
        get your wish. There is a location on each level where the flower should be returned to.
            - complete quest to get flower
            - kill monster that stole it
            - solve a puzzle dungeon
            - it's just lost somewhere completely random

monsters
    - monsters respawn in the morning?? or at night or something
    - weak monster   drop 1
    - monster   drop 1 and 2
    - strong monster   drop 1, 2, and three
    - monster king     special drop
        - monster king is only summoned after a certain number of that monster is killed
        - king drop can be crafted into rings that repel or attract that kind of monster
    
    - monster following behavior
        - monsters should follow behind other monsters if chasing player. 
        - gargoyle should not follow if you go around a corner
        - minotaur should follow if you are within certain tiles, minotaurs will come if you get within certain distance

level system
    - each monster gives a stat when you kill it
    - somewhere displays total number of stats with or without inventory items

stats
    - health
        - some weapons require certain amount of health to use
    - strength
        - 1 strength = 1 attack power
        - some weapons require certain amount of strength to use
    - defense
        - defense negates enemy attack. if you have 2 defense and are attacked with 4 attack, you only take 2 damage
    - attack_speed
        - effects speed of attack
    - speed
        - effects walking speed

fighting
    - when you are adjacent to a monster you will automatically attack, monster will automatically attack you
    - entity attacks with attack power every certain number of seconds. (will also show damage per second)
    - crit attack??
    - if there are multiple enemies can choose which to attack first by clicking on them
    - can't attack if walking

inventory 
    - large inventory. gets bigger somehow
    - each spot can hold 999, weapons and armor maybe limited number of slots 9?
    - infinite amount of gold
    - equips
        - each slot can only have one
        - attack or defence or speed is added or subtracted to player attack or defence
        - weapon, head, chest, leg, boots, rings, necklaces, bracelet
    - feature to compare items
        - right click on item, compare
        - right click on second item, compare
        - in the description area both items will be shown, stacked on top of each other
        - button to stop comparing


map

    - starter map only shows very zoomed out and only shows landmarks
    - can buy maps of more detail in villages.
    - each map is on a new page of the journal. maps sometimes take up both sides of the journal. can't zoom in, have to
        move to the zoomed in map page
    

chalk
    - can draw arrows on stone
mirror
    - can see around corners if you are on the tile next to a corner
compass 
    - shows direction you are facing
hammer
    - allows you to craft simple items in your inventory

journal
    - stores information about items and monsters that you have seen
    - if you see a creature, then the picture and name is added to the journal along with location of sighting
    - if you kill a creature, the description, stats, and drops will be added to the journal
    - counts number of kills
    - types of creatures
        - aggressive | will attack on sight
        - passive | will only attack if attacked first
        - peaceful | will not attack
    - if you see a weapon in a shop or put a weapon in your inventory, weapon description, picture, name, stats are added
    - items are same as weapons, also have location info

    - has list of all current quests, all dialog lines for that quest, location of quest given
    - has all npcs that you have talked to. lists name, location, profession, and short description of them (maybe logs all conversation)
    - has alchemy recipes
    

alchemy
    - npc somewhere that says he is going to the city to learn alchemy, if you do quest he gives you book of recipes
    - create potions. different ways to process ingredients lead to slightly different potions or length of effects
    - maybe too many potions has negative side effect
    
maybe cooking?
    - cooking can have better effects but food must be eaten very quickly
    - some foods like jerky can last longer
    - must create a campfire with sticks and flint, flint is a key item that you get from centaurs

crafting
    - crafting tab accesses by hammer special item
 
random
    - karma is accumulated by quests and doing good things, bad things give negative karma
    - in not pixel art version of game, drawings of items or monsters in inventory or journal should be sketches with light coloring
    - note keeping section
    - there are rune things scattered throughout the map that give you stats or other benefits (increase inventory size
    - some armor makes you take extra damage
        - taking fire attacks with grass armor makes the armor catch on fire and deal extra damage
        - being in really hot place with metal armor eventually makes you take damage
        - mom's idea from alone when that guy used grass gloves to pick up pot and burned himself


levels
    0. Villages
        - somewhere there is an ocean
            - charybdis
        - possible biomes (not all will generate)
            - plains
            - forest
            - jungle 
            - frozen
            - desert
            - swamp
            - mountains

    1. Maze
        - certain number of entrances.
            - most have villages around them
        - inside of maze corresponds to the biome on the top
            - all, gargoyles
            - plains
            - forest
            - jungle 
            - frozen, zombies
            - desert
            - swamp, slimes
            - mountains, minotaurs
        - can only see a few tiles in front of you. cannot see past walls
        - maze shifts every certain amount of time. monsters respawn. being in the maze while its shifting is very dangerous
            - when maze shifts the entrances close until morning
        - maze does not take up the whole level
            - there is a hidden area around the outside of the maze that can only be found when the maze is shifting
                - some way to get back into the maze or back up to the surface

    2. Floating Islands
        - entrance is giant hole in center of the maze
            - if you have an item that lets you float down, people with wings fly around you and observe you as you fall
            - if you don't have item, death screen, but then it says "just kidding". You wake up in a village
        - floor is blessed and that allows people to have wings. When they become an adult they kill a griffin or
            something and get the wings. The wings only work on this floor.
        - if player gets wings they can fly from island to island or fly back up to the maze. if they don't have
            wings they have to use bridges to get to some islands or pay npc to carry them back to maze
        - bottom of the floor is filled with black smoke. It slowly damages you if you touch it. after certain amount of
            time it makes wings stop working
        - charon will ferry you to the bottom
    
    3. Volcano?

    forest floor (roots of the world tree)

    final floor
        - world tree grants you a wish. cutscenes play based on your choice and your stats gold and karma
            - general 
                - evil karma become a villain, depending on stats and gold you could destroy the world
                - bad karma become the ruler of the underground
                - neutral karma live peacefully with your friends, no one bother you again
                - good karma become king, kingdom is very prosperous
                - Righteous karma become ruler of the continent and lead humanity to an unprecedented era of peace 

            - power
                - if strength stat is at max, you become a god
                - if strength stat is really low, something else happens thats funny

            - wealth
                - if strength stat is low enough you attract a dragon and are not able to kill it, so it takes your gold
                - if money is above certain amount you build a castle out of solid gold
                - if money = 0, something
                - if money is low, "you no longer have to beg for scraps"

            - fame
            - eternal life
            - nothing
            - more adventure
                - unlocks next part
                - option after you make a wish when you enter the save, something about being able to choose the more adventure option


npcs
    any
        - mermaid
        - satyrs
    0. Villages
        - centaurs wandering merchants

creatures
    any
        - pegasus
        - hippocampi
        - dragon
        - fairy
        - dryad

other (nature, not meant to fight)
    any
        - charybdis
            - creates whirlpools, meant to be undefeatable
        - phoenix
            - large fire, some other creature summons rain to put it out. When the fire goes out, the still burning
                phoenix streaks across the sky leaving behind a rainbow. the phoenix is very colorful and the flames
monsters
    any
        - sirens
            - drops: scale

        - unicorns
            - drops: horn

        - vampires
        - golems
        - chupacraba??
        - wyvern
        - cu sith???
        - bunyip??
        - imp
        - Quetzalcoatl 
        - ladon (serpent guarding golden apple)


    0. The Open Sky
        Beginner
            - grass/weed
            - stumpling
            - rat
            - blue birds
            - porcupine
                - spine sword
            
        Intermediate
            - werewolves
            - scare crow
            - rock
                - cannot be damaged by cutting
            
        Difficult
            - frog ground trap
            - 
        
        
            - will o the wisp
                - king drop: wisp or "will" which allows you to create golems or something
            
        
    1. Maze
        - minotaur
            - mountain goats
            - drops: horn, hoof
            - king drop: minotaur hide

        - gargoyles
            - blend into the walls/floor, don't know they are there until you are right in front of them
            - drops: living stone

        - zombies in frozen area
            - drops: ice essence
            - king drop: frozen or rotting heart

        - slimes in slime area
            - slime core
        
        - vine monster
            - stops you from walking


    2. Floating Islands
        - griffin
            - drops: talons, beak, feathers

        - thunderbird
            - rare monsters
            - creates lighting storms around the area
            - drops: wings that you can equip

        - harpies
            - drops: corrupted wings, talons, teeth
            
            
            
            
"""

