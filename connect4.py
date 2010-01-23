#!/usr/bin/env python
#
#       Connect4 
#
#       Just did this for the fun. Have fun like i did. :) 
#       I did this in Geany, a small and fast IDE. http://www.geany.org/
#
#       Copyright 2009 Diogo Nuno dos Santos Silva <promzao@gmail.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 3 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

connect4_version = "0.51"
last_update = "10 Oct/2009"

import random
import curses
from sys import exit

def InitCurses():
	'''Curses related stuff'''
	global screen
	screen = curses.initscr()
	curses.noecho()
	curses.start_color()
	screen.keypad(1)
	curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK) # Create the colors
	curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_RED)
	curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
	curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)

# Screen information message position
info_x = 0
info_y = 1

def ScreenInfo(info_msg, info_color):
	'''Prints an information message in the position given up there'''
	last_pos = curses.getsyx()
	screen.move(info_x,info_y)
	screen.addstr("%s" % info_msg , curses.color_pair(info_color) | curses.A_BOLD)
	screen.move(last_pos[0],last_pos[1])

def Quit():
	'''Quiiiiiiiit!!!'''
	curses.endwin()
	quit()

class MoveCursor:
	'''
	An object to move the cursor with rules 
	Usage: MoveCursor(initial x position, initial y position, move left jump size, move right jump size, go up jump size, go down jump size, up limit size, down limit size, left limit size, right limit size) 
	'''
	def __init__(self,initial_x,initial_y,left,right,up,down,x_up_max,x_down_max,y_left_max,y_right_max):
		self.x = initial_x
		self.y = initial_y
		self.initial_x = initial_x
		self.initial_y = initial_x
		self.move_left = left
		self.move_right = right
		self.move_up = up
		self.move_down = down
		self.x_up_max = x_up_max
		self.y_left_max = y_left_max
		self.x_down_max = x_down_max
		self.y_right_max = y_right_max
	
	def MoveLeft(self):
		self.y = self.y-self.move_left
		if self.y < self.y_left_max:
			self.y = self.y_right_max

	def MoveRight(self):
		self.y = self.y+self.move_right
		if self.y > self.y_right_max:
			self.y = self.y_left_max

	def MoveUp(self):
		self.x = self.x-self.move_up
		if self.x < self.x_up_max:
			self.x = self.x_down_max

	def MoveDown(self):
		self.x = self.x+self.move_down
		if self.x > self.x_down_max:
			self.x = self.x_up_max
		
	def MoveInitial(self):
		self.x = self.initial_x
		self.y = self.initial_x

	def MoveActual(self):
		screen.move(self.x,self.y)
		
	def Move(self,option):
		if option == 'left':
			self.MoveLeft()
		elif option == 'right':
			self.MoveRight()
		elif option == 'up':
			self.MoveUp()
		elif option == 'down':
			self.MoveDown()
		elif option == 'initial':
			self.MoveInitial()
		elif option == 'actual':
			self.MoveActual()
		else:
			Quit()
	
	def get_x(self):
		'''Return X position'''
		return self.x
		
	def get_y(self):
		'''Return Y position'''
		return self.y

def About():
	'''About Connect4'''	
	screen.clear()
	screen.move(0,0)
	screen.addstr(" Connect 4 \n\n", curses.color_pair(3))
	screen.addstr(" Started in 2009/08/18, a hot day\n");
	screen.addstr(" Version %s ( last update: %s )\n\n" % (connect4_version,last_update));
	screen.addstr(" Made by Diogo Nuno\n Visit")
	screen.addstr(" http://www.diogonuno.com\n\n ", curses.color_pair(1))
	event = screen.getch()

def Help():
	'''Help me dear Connect4'''	
	screen.clear()
	screen.move(0,0)
	screen.addstr(" Connect 4 \n\n", curses.color_pair(3))
	screen.addstr(" Just get 4 in a row in horizontal or in diagonal and everything will be fine.\n")
	screen.addstr(" Use \"Q\" in game to quit.\n\n ")
	event = screen.getch()

class Board():
	'''The game board'''
	def __init__(self,y,x):
		self.Board = [] # create the Board
		self.Board_x = x # lines
		self.Board_y = y # columns
		for i in range(y): # create the Board columns
			self.Board.append([])
		self.Fill()
		
	def Fill(self):
		'''Fill the board with ghost Coins'''
		for y in range(0,self.Board_y):
			for x in range(0,self.Board_x):
				self.Board[y].append(Coin('G')) # the ghost coin

	def Print(self):
		'''Method to print our game board'''
		screen.addstr("\n\n"); # get a space for the information message  
		for x in reversed(range(0,self.Board_x)):
			screen.addstr(" | ", curses.color_pair(4) | curses.A_BOLD)
			for y in range(0,self.Board_y):
				self.Board[y][x].printCoin()
			screen.addstr(" | \n", curses.color_pair(4) | curses.A_BOLD)
	
	def SomebodyWonPopcorn(self):
		'''Method to check if somebody has won and give its deserved price'''
		for x in range(0,self.Board_x-3): # check vertical
			for y in range(0,self.Board_y):
				if self.Board[y][x].getCoin() != 'G' and self.Board[y][x].getCoin() == self.Board[y][x+1].getCoin() and self.Board[y][x+1].getCoin() == self.Board[y][x+2].getCoin() and self.Board[y][x+2].getCoin() == self.Board[y][x+3].getCoin():
					self.Board[y][x].changeColor() ; self.Board[y][x+1].changeColor() ; self.Board[y][x+2].changeColor() ; self.Board[y][x+3].changeColor()
					return True
		for x in range(0,self.Board_x): # check horizontal
			for y in range(0,self.Board_y-3):
				if self.Board[y][x].getCoin() != 'G' and self.Board[y][x].getCoin() == self.Board[y+1][x].getCoin() and self.Board[y+1][x].getCoin() == self.Board[y+2][x].getCoin() and self.Board[y+2][x].getCoin() == self.Board[y+3][x].getCoin():
					self.Board[y][x].changeColor() ; self.Board[y+1][x].changeColor() ; self.Board[y+2][x].changeColor() ; self.Board[y+3][x].changeColor()
					return True
		for x in range(0,self.Board_x-3): # check diagonal
			for y in range(0,self.Board_y-3):
				if (self.Board[y][x].getCoin() == 'X' and self.Board[y+1][x+1].getCoin() == 'X' and self.Board[y+2][x+2].getCoin() == 'X' and self.Board[y+3][x+3].getCoin() == 'X') or (self.Board[y][x].getCoin() == 'O' and self.Board[y+1][x+1].getCoin() == 'O' and self.Board[y+2][x+2].getCoin() == 'O' and self.Board[y+3][x+3].getCoin() == 'O'):
					self.Board[y][x].changeColor() ; self.Board[y+1][x+1].changeColor() ; self.Board[y+2][x+2].changeColor() ; self.Board[y+3][x+3].changeColor()
					return True
		for x in range(self.Board_x-3,self.Board_x): # check diagonal
			for y in range(0,self.Board_y-3):
				if (self.Board[y][x].getCoin() == 'X' and self.Board[y+1][x-1].getCoin() == 'X' and self.Board[y+2][x-2].getCoin() == 'X' and self.Board[y+3][x-3].getCoin() == 'X') or (self.Board[y][x].getCoin() == 'O' and self.Board[y+1][x-1].getCoin() == 'O' and self.Board[y+2][x-2].getCoin() == 'O' and self.Board[y+3][x-3].getCoin() == 'O'):
					self.Board[y][x].changeColor() ; self.Board[y+1][x-1].changeColor() ; self.Board[y+2][x-2].changeColor() ; self.Board[y+3][x-3].changeColor()
					return True	
		return False			
					
	def Play(self, Player, Column):
		'''We get the player and the column, check if everything is all right and play'''
		if self.Board[Column][self.Board_x-1].getCoin() == 'G': # check if the last position is clean if so, put the Coin, if not its full.
			CoinID=0
			del self.Board[Column][self.Board_x-1] # delete the clean position
			if not self.Board[Column][0].getCoin() == 'G': # if its not the first play lets check for the last Coin position index
				LastCoinID=0
				for i in range(0,self.Board_x-1):
					if self.Board[Column][LastCoinID].getCoin() == 'X' or self.Board[Column][LastCoinID].getCoin() == 'O':
						LastCoinID+=1
				CoinID=LastCoinID
			if Player == 1:
				self.Board[Column].insert(CoinID,Coin('X'))
			else:
				self.Board[Column].insert(CoinID,Coin('O'))
			return True
		else:
			return False

class Coin:
	'''Object to play'''		
	def __init__(self, suit):
		self.suit = suit
		if suit == 'X': # give the fashion color to the coin
			self.color = 1
		elif suit == 'O':
			self.color = 2

	def getCoin(self):
		'''Return the coin'''
		return self.suit

	def changeColor(self):
		'''Change my fashion color to the winner color'''
		self.color = 5
	
	def printCoin(self):
		'''Print me'''
		if self.getCoin() == 'G': # if its not a ghost coin, show it :)
			screen.addstr("   ")
		elif self.getCoin() == 'X': # X Coin
			screen.addstr(" %s " % self.getCoin(), curses.color_pair(self.color) | curses.A_BOLD)
		else: # O Coin
			screen.addstr(" %s " % self.getCoin(), curses.color_pair(self.color) | curses.A_BOLD)	

class Player:
	'''The player 1 or 2'''
	def __init__(self, Opponent):
		self.CurrentPlayer = 1
		self.Opponent = Opponent
				
	def ChangePlayer(self):
		''''Change player's turn'''
		if self.CurrentPlayer == 1:
			self.CurrentPlayer = 2
		else:
			self.CurrentPlayer = 1
				
	def TheHand(self, Board, ChosenColumn):
		'''Player's Hand'''
		if (Board.Play(self.getPlayerTurn(),ChosenColumn)): # If he plays
			if not Board.SomebodyWonPopcorn(): # checks if he won, if so he celebrates if not changes turn
				self.ChangePlayer()
				if self.Opponent == 'CPU':
					if (Board.Play(self.getPlayerTurn(),random.randint(0,Board.Board_x))):
						if Board.SomebodyWonPopcorn():
							return
					self.CurrentPlayer = 1

	def getPlayerTurn(self):
		'''Return the current Player'''
		return self.CurrentPlayer
		
class Table:
	'''Table where we play. The board is in the table and the players are sitting right next to it :)'''	
	def __init__(self, opponent):
		self.player = Player(opponent)
		self.Board = Board(7,6)
		self.Cursor = MoveCursor(9,4,3,3,0,0,0,0,4,22) # give the rules to MoveCursor Object
		self.ChosenColumn = 0 # my chosen column
		self.Think() # The main
		
	def ColumnColumnCursor(self, column):
		'''A method to get the right Column to play from the Y position of the cursor'''		
		if self.Cursor.get_y() > 22:
			self.ChosenColumn = 0
		elif self.Cursor.get_y()  < 4:
			self.ChosenColumn = 6
		else:
			self.ChosenColumn = column
	
	def Think(self):
		'''Method where we read the keyboard keys and think in the game :P'. We think then we use the hands'''
		while True:
			screen.clear()
			self.Board.Print()
			if self.Board.SomebodyWonPopcorn(): # checks if he won :P
				ScreenInfo("YOU WIIIIIIIIN!!! :)",self.player.getPlayerTurn())
				screen.getch()
				break
			else:
				ScreenInfo("Player's turn\n\n",self.player.getPlayerTurn())
			self.Cursor.Move('actual')
			event = screen.getch()
			if event == ord("q"): 
				break
			elif event == curses.KEY_LEFT:
				self.Cursor.Move('left')
				self.ColumnColumnCursor(self.ChosenColumn-1)
			elif event == curses.KEY_RIGHT:
				self.Cursor.Move('right')
				self.ColumnColumnCursor(self.ChosenColumn+1)
			elif event == 10:
				self.player.TheHand(self.Board,self.ChosenColumn)

class Menu:
	''''Where everything begins, the Menu (main too)'''	
	def __init__(self):
		self.Cursor = MoveCursor(2,0,0,0,1,1,2,6,0,0) # give the rules to MoveCursor Object
		self.main()

	def henshin_a_gogo_baby(self):
		'''A name inspired in Viewtiful Joe game, lol. It checks the cursor position and HENSHIN A GOGO BABY'''
		if self.Cursor.get_x() == 2:
			gogo = Table('CPU')
		if self.Cursor.get_x() == 3:
			gogo = Table('Player')
		elif self.Cursor.get_x() == 4:
			Help()
		elif self.Cursor.get_x() == 5:
			About()
		elif self.Cursor.get_x() == 6:
			Quit()
	
	def main(self):
		'''The main :|'''
		while True:
			screen.clear()
			screen.addstr(" Connect 4 \n\n", curses.color_pair(3))
			screen.addstr("  Play against dumb CPU\n")
			screen.addstr("  Play against Player\n")
			screen.addstr("  Help\n")
			screen.addstr("  About\n")
			screen.addstr("  Quit\n")
			self.Cursor.Move('actual')
			event = screen.getch()
			if event == ord("q"): 
				Quit()
			elif event == curses.KEY_UP:
				self.Cursor.Move('up')
			elif event == curses.KEY_DOWN:
				self.Cursor.Move('down')
			elif event == 10:
				self.henshin_a_gogo_baby()

if __name__ == '__main__': 
	try:
		InitCurses()
		run_for_your_life = Menu() # The menu
	except:
		Quit()
else:
	print "Connect4 - ??"

