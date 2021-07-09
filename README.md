# Lab 4: Basic Tower Defense

## Intro
This week, we will be taking a different approach to commanding our characters. Instead of having them make decisions through conditionals, we will be giving them direct instructions. You will be organizing a team of up to 3 characters, trying to find the quickest way to get all the diamonds from the playing area to the goal.

For this lab we will be practicing our data structures. You will be using dictionaries and lists to organize actions for your characters to take.

This week, we will be taking our first steps into building our tower defense game! You will be starting off with basic towers, that can only do a set amount of damage. The challenge here is to implement the logic on which monsters should the towers target. 

There will be two types of monsters:
* fast monsters with low HP
* heavy monsters with high HP

For this lab we will be practicing our iteration skills. You will be creating functions that will iterate through all of the monsters in range of a tower. Depending on characteristics of each monster, you will need to decide how to prioritize your targets.

## Set Up
* Click the green 'Code' button on the top right of this section.
* Find 'Download ZIP' option and click it
* Unzip the file and move it over to your 'workspace' folder (or wherever you keep your files)

* Find the folder and open the entire folder in VSCode
    * You can find it in your Files and right click on it. Use the "Open with VSCode" option
    * You can also open VSCode, go to 'File' > 'Open' and then find the lab folder

* With VSCode open, go to the top of your window and find `Terminal`
* Click `Terminal`
* Click `New Terminal`

* In the new window that opens at the bottom of VSCode, type in
```
python run_small.py
```

* Hit enter
* You should see a game window open up, with a small grid and game objects.
* You are done with set up!

## Game Explanation
This is a base version of tower defense with 1 tower type and 2 monster types. The objective is to take down the monsters before they reach the destination flag.

If a monster reaches your flag, then you will lose a life. Lose all 3 lives, and you lose the game.

We are starting off with a simple magic tower:
* Cooldown: 2.5 seconds
* Attack Radius: 500 pixels
* Attack Damage: 10HP

You will be facing off against two monster types:
* Fast Monster
    * Total Health: 25HP
    * Speed: 80 pixels per second
* Heavy Monster
    * Total Health: 120HP
    * Speed: 35 pixels per second

## Lab Steps
* All the code you will need to edit is in `lab.py`
* `run_small.py`, `run_med.py`, and `run_big.py` are used to run the game. If you take a look inside, you can see how we set up the game to be played.
* Everything inside the `engine/` folder are the inner workings of the game. Feel free to take a look, but you won't need to change anything (unless you want to change your sprite speed)

### Small Map
Let's get started with the small horde scenario.

* Let's first see what happens when we don't write any code for our towers.
* Open up your terminal (if it isn't open already) and type in `python run_small.py` and hit enter.
* Notice how monsters spawn and walk over to the right side of the screen (where the flag is).
* Once 3 monsters reach the flag, our life counter goes to 0 and our terminal says game over.

Now let's try giving some basic instructions
* Go into `lab.py` and find the section:
```python
# ------------------ Lab Small ---------------------


def lab_run_small(monsters):
    pass

```
* Notice how we take in an argument called `monsters`
* This argument will be a list of all the monster objects that are in range of our tower.
* We just need to select a monster from this list for us to target
* Let's first get started by just selecting the first monster in the list and see what happens
* Replace the section with:
```python
# ------------------ Lab Small ---------------------


def lab_run_small(monsters):
    if len(monsters) == 0:
        return None
    return monsters[0]

```
* Notice how we are taking the first item in the list
* Also notice how we FIRST check if the monsters list actually has anything in it
* Save your file and run `python run_small.py`

When the game runs, you should see that our tower happens to randomly choose monsters to target. This is because we can't gurantee the order in which we process the monsters in the field.

You should get Game Over with this setting (but you could win if you're lucky)

* We can do better, so let's improve our function
* A good strategy would be to make sure we always target the monster closest to our flag.
    * With our helper function `get_distance_to_goal`, we can get the distance in pixels from a monster to a flag
* Let's try to iterate through all our monsters, measuring the distance of each to our flag. Let's use a variable to keep track of which one was closest
* Replace `lab_run_small` with
```python
def lab_run_small(monsters):
    closest = None
    for monster in monsters:
        if closest == None:
            closest = monster
        elif get_distance_to_goal(monster) < get_distance_to_goal(closest):
            closest = monster
    return closest

```
* Take a look at our code here.
    * Let's create a variable that will keep track of the closest monster to the goal. Set it to None for now.
        * PS: We don't need to check for empty list. If the `monsters` list is empty, then we actually do nothing, and just return None
    * Next we start our iterative loop. We are using a `for` loop, going through the list, one `monster` at a time.
    * If `closest` is equal to None, we know that this is the first time we run the loop, so let's set closest equal to the monster right now (since it IS the closest monster we've seen so far)
    * Otherwise, let's do a check. Let's calculate distance to goal of our CURRENT monster and the one we've set equal to closest
        * In other words, we are trying to see which one is closer to the goal. The monster we are checking right now, and the one we have encountered already that has been closest so far
    * If the above is true, we have found a monster that is CLOSER than the one we have been tracking so far
    * Let's set `closest` equal to the current monster now
* At the end of the loop, we should be guaranteed that the monster that the `closest` variable is pointing to, will be the monster that is closest to the goal
* Return whatever we have `closest` pointing to.

* Save your file and run `python run_small.py`

* Now you should see that we always target the monster that is closest to the goal (if its in range)

### Medium Map
Now let's try it out on a bigger horde.

* Let's first see what happens when we don't write any code for our towers.
* Open up your terminal (if it isn't open already) and type in `python run_med.py` and hit enter.
* Notice how we now have fast AND heavy monsters.

* Let's try using our strategy from earlier and seeing how it works:
* Replace `lab_run_med` with
```python
def lab_run_med(monsters):
    closest = None
    for monster in monsters:
        if closest == None:
            closest = monster
        elif get_distance_to_goal(monster) < get_distance_to_goal(closest):
            closest = monster
    return closest

```
* Save your file and run `python run_med.py` again

* Notice how the heavy monsters soaked up all our damage! This allowed a lot of the faster monsters to breeze right through our defense.
* Let's strategize here a bit. In order for us to win, we need to have at least 1 life, meaning we can let TWO monsters through.
* Since we can't change our tower damage or speed, we need to be smart about what to target.

* Instead of wasting our time on the heavys, we can focus down the fast monsters.
* Since there are only two heavys, then we just need to take down all the fast monsters to win!

* Remember that fast monsters have `25HP` while heavy monsters have `120HP`. 
* Let's add a conditional in our iteration, that will allow us to IGNORE the heavy monsters!

* Add this line right underneath the beginning of your `for` statement (make sure your indentation level is correct):
```python
    if get_remaining_monster_health(monster) > 100:
        continue
```

* What are we doing here?
    * We are running a conditional that asks whether the current monster we are checking has health greater than 100
    * If the health IS greater than 100, this monster is too big, and we shouldn't bother trying to take it down.
    * In order to do this, we use the `continue` line. This means that we want to SKIP this step of the loop and move on to the next monster
    * Since we are skipping the rest of the code block for this monster, we never compare its distance and can never assign it to `closest`
    * Effectively meaning that we can ignore it!

* Hit save and run `python run_med.py` again

* You should see that your towers completely ignore the heavy monsters, and now just focus down the fast ones!

* You should win now (though barely)


### Big Map
Alright, now that you have the basics of iteration practiced, let's see how you do against a large horde!

You should now have 4 towers, which you can write functions for individually. Each function goes in order from left to right. So `lab_run_big_1` will control the first tower on the left. `lab_run_big_4` will control the one all the way on the right.

See if you can get creative with targeting strategies! And see how long you last!

The spawner will send monsters at you randomly, so different runs might get different results.

You can run the big horde by using the command `python run_big.py`
