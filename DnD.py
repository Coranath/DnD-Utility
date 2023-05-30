import os
from sys import stderr
import sqlite3
from random import randint
from time import sleep
import pickle
import flask
import logging
# import pygame

class dice:

    def __init__(self, dice_string) -> None:
        num,sides = dice_string.split('d')

        if num != '':
            self.num = int(num)
        self.sides = int(sides)

        

    def roll(self):
        tot = 0

        for _ in range(self.num):
            tot += randint(1,self.sides)

        return tot

class attack:

    def __init__(self, atk, reach, damage, comments) -> None:
        try:
            self.atk = int(atk)
            self.reach = int(reach)
            self.damage = dice(damage)
            self.comments = comments
        except:
            print('Failed to parse input and create attack object. Data dump: atk={atk} reach={reach} damage={damage} comments={comments}', file=stderr)

    def roll(self):
        return self.atk+self.damage.roll()
    
class monster:

    def __init__(self, name, ac, hp, attacks) -> None:
        self.name = name
        self.ac = ac
        self.hp = hp
        self.attacks = attacks

    def attack():
        """This function makes an attack
        ```python
        print(1+str)
        ```
        @TODO: Pull a list of players to attack or maybe do it randomly!
        """
        pass

class player:

    def __init__(self, name, ac, hp) -> None:
        self.name = name
        self.ac = ac
        self.hp = hp
        monster.attack()



def dots():
    sleep(1)
    print('.', end='', flush=True)
    sleep(1)
    print('.', end='', flush=True)
    sleep(1)

def addMonster():

    os.system('cls')

    # con = sqlite3.connect("DM_Toolbox.db")

    # db = con.cursor()

    db.execute('create table if not exists monsters(name, ac, hp, pickled)')

    name = input('Please enter the name of the monster: ')
    ac = input('Please enter the armor class of the monster: ')
    hp = input('Please enter the hp of the monster: ')
    atkNum = input('Please enter how many attacks you wish to enter for the monster: ')

    attacks = []

    for i in range(int(atkNum)):
        os.system('cls')
        atk = input(f'Please enter the attack modifier for attack #{i}: ')
        atk = atk.strip('+')
        reach = input('Please enter the range of the attack: ')
        damage = input('Please enter the damage of the attack: ')
        comments = input('Please add any comments pertaining to the attack here: ')

        attacks.append(attack(atk, reach, damage, comments))

    mon = monster(name, ac, hp, attacks)

    db.execute('insert into monsters values(?, ?, ?, ?)', [name, ac, hp, pickle.dumps(mon)])
    con.commit() # You must commit after inserting for some reason. This is a function of con, not db.

    # con.close()

def addPlayer():

    os.system('cls')

    db.execute('create table if not exists players(name, ac, hp)')

    name = input('Please enter the name of the player: ')
    ac = input('Please enter the armor class of the player: ')
    hp = input('Please enter the hp of the player: ')

    p1 = player(name,ac,hp)

    db.execute('INSERT INTO players VALUES(?,?,?)', [name, ac, hp])
    con.commit()

    # con.close()

def encounter():

    os.system('cls')

    print('Welcome to the enounter screen! Please choose which players you would like to include!')

    players = []
    
    for i, name in enumerate(db.execute('SELECT name FROM players').fetchall()):
        
        players.append(name) # We do this so that when they pick players by number we can easily find the name

        print(f'{i}. {name[0]}')

    res = input('Just press enter to include all of them: ')

    if res == '':

        players = []

        for p in db.execute('SELECT * FROM players').fetchall():

            players.append(player(p[0], p[1], p[2]))

    #TODO Add ability to pick only certain players

    os.system('cls')

    print('Please choose which monsters you would like to include!')

    monsterNames = []

    for i, name in enumerate(db.execute('SELECT name FROM monsters').fetchall()):

        monsterNames.append(name) # Same reason as why we did it for players

        print(f'{i}. {name[0]}')

    res = input("You may separate numbers by commas to choose more than one: ")

    res = res.split(',')

    monsters = []

    for num in res:

        for m in db.execute('SELECT pickled FROM monsters WHERE name = ?', monsters[num]):

            monsters.append(pickle.loads(m[0]))


        

if __name__ == '__main__':

    choice = -1
    

    while choice != 0:

        os.system('cls')

        con = sqlite3.connect('DM_Toolbox.db')
        db = con.cursor()

        print('''
        Welcome to the DM's toolbag!
        
        Please select one of the following options by entering the cooresponding number and pressing enter!
        
        1. Start a new encounter
        2. Add a player
        3. Add a monster
        0. Quit
        
        Please make your choice: ''', end='', flush=True)

        choice = input()

        try:
            choice = int(choice)

            match choice:
                case 0:
                    print('\nThank you for utilizing the DM\'s toolbag! Godspeed and may the dice be ever in your favor!')
                case 1:
                    encounter()
                case 2:
                    addPlayer()
                case 3:
                    addMonster()
                case 7:
                    print(db.execute('SELECT * from players').fetchall())
                    input("Press enter to continue")
                    print(db.execute('SELECT * from monsters').fetchall())
                    input("Press enter to continue")
                case _:
                    print(f'{choice} was not one of the available options. Please try again.', end='', flush=True)
                    dots()
        except ValueError:
            choice = -1
            print("I'm sorry but that input was invalid, please try again.", end='', flush=True)
            dots()

    con.close()
        

    
        
