import pyglet, time, random
from modules import ascii_art as a
from modules import engine as e
from pyglet.window import key

class Interface():
	"""Handles all of GUI work as well as updating leaderboard and some game logic.
	Utilizes one instance of :class:'Engine' throughout the whole program to prevent
	dictionary trie loading time.

	Refer to main.py for running program.

	Attribues
		active_buttons (list): List of buttons in a certain screen.
		lb_list (list): Leaderboard read from leaderboard.txt file (stored in 'resources/data/').
		start_is_running (bool): An indicator whether start menu is running.
		diff_is_running (bool): An indicator whether difficulty menu is running.
		game_is_running (bool): An indicator whether main game is running.
		lb_is_running (bool): An indicator whether leaderboard is running.
		end_is_running (bool): An indicator whether game end (game over) is running.
		ascii (Ascii): An instance of :class:`Ascii`.
		engine (Engine): An instance of :class:`Engine` to be active throughout program instance.
		scp_regular (pyglet.font): A font container for labels.
		scp_bold (pyglet.font): A font container for labels.
		lb_layout (pyglet.image): Image loaded in leaderboard screen.
		game_layout (pyglet.image): Image loaded in main game screen.
		grid_4x4 (pyglet.image): Part of 4x4 main game screen.
		grid_5x5 (pyglet.image): Part of 5x5 main game screen.
		show_idx (int): Tracks leaderboard index in leaderboard screen.
		curr_button (int): Tracks current selected button id.
		select_board_size (int): Represents user choice of 4x4 or 5x5.
		game_user_input (string): Contains user input for main game screen and 
			end game screen.
		start (float): Time game started. For game timer.
		max_time (float): Maximum amount of time (in seconds) game instance will last.
		answer_correct (string): For calling ASCII indicator label. Set to 'n' 
			to clear indicator label.
	"""


	def __init__(self):
		"""Constructor method"""

		self.window = pyglet.window.Window(width = 800, height = 600)
		self.active_buttons = []
		self.lb_list = []
		self.start_is_running = True
		self.diff_is_running = False
		self.game_is_running = False
		self.lb_is_running = False
		self.end_is_running = False

		self.ascii = a.Ascii()
		self.engine = e.Engine()
		
		pyglet.font.add_directory('resources/fonts')
		self.lb_layout = pyglet.image.load('resources/images/leaderboard.png')
		self.game_layout = pyglet.image.load('resources/images/game_gui.png')
		self.grid_4x4 = pyglet.image.load('resources/images/letter_box_4x4.png')
		self.grid_5x5 = pyglet.image.load('resources/images/letter_box_5x5.png')

	def start_menu(self):
		"""Sets start menu state"""

		self.start_is_running = True
		self.game_is_running = False
		self.diff_is_running = False
		self.lb_is_running = False
		self.end_is_running = False

		self.game_user_input = ""
		self.curr_button = None
		self.active_buttons = [self.difficulty, self.leaderboard]

	def leaderboard(self):
		"""Sets leaderboard menu state"""

		self.lb_is_running = True
		self.diff_is_running = False
		self.end_is_running = False
		self.start_is_running = False
		self.game_is_running = False

		self.show_idx = 0
		self.curr_button = None
		self.active_buttons = [self.start_menu]
		lb_file = open("resources/data/leaderboard.txt","r")
		lb_list = [i.split(',') for i in lb_file.read().split()]
		lb_file.close()
		lb_list = sorted(lb_list, key = lambda x: int(x[1])/int(x[2]), reverse = True)
		self.lb_list = lb_list

	def difficulty(self):
		"""Sets difficulty-choice menu state"""

		self.diff_is_running = True
		self.end_is_running = False
		self.start_is_running = False
		self.game_is_running = False
		self.lb_is_running = False

		self.select_board_size = None
		self.curr_button = None
		self.active_buttons = ['normal', 'hard']

	def game(self):
		"""Sets main game state"""

		self.game_is_running = True
		self.start_is_running = False
		self.lb_is_running = False
		self.end_is_running = False
		self.diff_is_running = False

		self.engine.max_score = None
		self.engine.curr_score = None
		self.engine.game_board_size = None
		self.engine.game_board = None
		self.engine.game_solutions = set()
		self.engine.game_answered = []

		self.answer_idx = 0
		self.answer_correct = "n" #for UI indicator
		self.curr_button = None
		self.active_buttons = []
		self.game_user_input = ""
		self.engine.make_board(self.select_board_size)
		for i in self.engine.game_board:
			print(i)
		self.engine.solve_board()
		self.start = time.time()
		self.max_time = len(self.engine.game_solutions)*5
		print(self.engine.game_solutions)

	def game_end(self):
		"""Sets game end (game over) menu state"""

		self.end_is_running = True
		self.diff_is_running = False
		self.start_is_running = False
		self.game_is_running = False
		self.lb_is_running = False
		self.diff_size_is_running = False

		self.game_user_input = ""
		self.curr_button = None
		self.active_buttons = []


	def start_screen(self):
		"""Loads start menu assets onto window when called from update"""

		if self.start_is_running == True:
			for i in range(len(self.ascii.title)):
				pyglet.text.Label(
					self.ascii.title[i],
					font_name='Source Code Pro', bold = True,
					font_size=12,
					x=160, y=380-14*i,
					color = (57, 255, 20, 255)
				).draw()

			caret1, caret2 = '',''
			if self.curr_button == 0:
				caret1, caret2 = '>',''
			elif self.curr_button == 1:
				caret1, caret2 = '','>'
			pyglet.text.Label(
				caret1 + "start",
				font_name='Source Code Pro', bold = True,
				font_size=11,
				x=380, y=300,
				color = (57, 255, 20, 255)
			).draw()
			pyglet.text.Label(
				caret2 + "leaderboard",
				font_name='Source Code Pro', bold = True,
				font_size=11,
				x=380, y=260,
				color = (57, 255, 20, 255)
			).draw()
			
	def leaderboard_screen(self):
		"""Loads leaderboard menu assets onto window when called from update"""

		if self.lb_is_running == True:
			self.lb_layout.blit(0,0)
			pyglet.text.Label(
				"past hacks",
				font_name='Source Code Pro', bold = True,
				font_size=11,
				x=408, y=580,
				anchor_x='center',
				color = (0,0,0,255)
			).draw()

			for i in range(min(len(self.lb_list), 37)):
				log = self.lb_list[i + self.show_idx]
				pyglet.text.Label(
					log[0] + "."*(45 - len(log[0]) - len(log[1])
						- len(log[2]) - 1) + "{0}/{1}".format(log[1],log[2]),
					font_name='Source Code Pro', bold = True,
					font_size=10,
					x=220, y=540 - 14*i,
					color = (57, 255, 20, 255)
				).draw()

			if self.curr_button == 0:
				caret1 = '>'
			else:
				caret1 = ''

			pyglet.text.Label(
					caret1 + "back",
					font_name='Source Code Pro', bold = True,
					font_size=11,
					x=725, y=26,
					color = (57, 255, 20, 255)
				).draw()

	def difficulty_screen(self):
		"""Loads difficulty menu assets onto window when called from update"""

		if self.diff_is_running == True:
			for i in range(len(self.ascii.title)):
				pyglet.text.Label(
					self.ascii.title[i],
					font_name='Source Code Pro', bold = True,
					font_size=12,
					x=160, y=380-14*i,
					color = (57, 255, 20, 255)
				).draw()
			caret1, caret2 = '',''
			if self.curr_button == 0:
				caret1, caret2 = '>',''
			elif self.curr_button == 1:
				caret1, caret2 = '','>'
			pyglet.text.Label(
				caret1 + "4x4",
				font_name='Source Code Pro', bold = True,
				font_size=11,
				x=380, y=300,
				color = (57, 255, 20, 255)
			).draw()
			pyglet.text.Label(
				caret2 + "5x5",
				font_name='Source Code Pro', bold = True,
				font_size=11,
				x=380, y=260,
				color = (57, 255, 20, 255)
			).draw()

	def timer(self, current_time):
		"""Loads timer label onto window during the main game

		Args:
			current_time (int): From time.time() called in :meth:`game_screen`.
				Time (in seconds)
		"""

		minutes = int((self.max_time - current_time) // 60)
		seconds = int((self.max_time - current_time) % 60)
		seconds = "0" + str(seconds) if seconds < 10 else seconds

		pyglet.text.Label(
			"{0}:{1}".format(minutes, seconds),
			font_name='Source Code Pro', bold = True,
			font_size=11,
			x=408, y=580,
			anchor_x='center',
			color = (0,0,0,255)
		).draw()
	
	def view_as_qu(self, word):
		"""Helper function to convert '$' char in string to
		user-friendly 'qu'
		
		Args:
			word (string): Word to convert.
		"""	

		if '$' in word:
			for i in range(len(word)):
				if word[i] == '$':
					word = word[:i] + 'qu' + word[i + 1:]
		return word
	
	def indicator(self):
		"""Loads indicator label ("success"/"error") onto
		window during main game when answer is entered.
		"""

		if self.answer_correct == "t":
			indicator = self.ascii.success
			for i in range(len(indicator)):
				pyglet.text.Label(
					indicator[i],
					font_name='Hack', bold = True,
					font_size=12,
					x=45, y=120 - 14*i,
					color = (255,255,255,255)
				).draw()
		else:
			indicator = self.ascii.error
			for i in range(len(indicator)):
				pyglet.text.Label(
					indicator[i],
					font_name='Hack', bold = True,
					font_size=12,
					x=80, y=120 - 14*i,
					color = (216,0,12,255)
				).draw()

	def set_to_n(self, dt):
		"""Helper function for :meth:`indicator` animation.
		
		Args:
			dt (int): Used by pyglet.clock.schedule(). Indicates delay in seconds.
		"""
		self.answer_correct = "n"

	def stats(self):
		"""Loads current game statistics as labels  and decorative
		ASCII art from :class:`Ascii` onto window during main game.
		"""

		calc = int(100*self.engine.curr_score/(self.engine.max_score*0.5))
		info = [
			"hacking............................{0}%".format(100 if calc >= 100 else calc),
			"words..............................{0}".format(len(self.engine.game_solutions) - len(self.engine.game_answered)),
		]

		for i in range(2):
			pyglet.text.Label(
				info[i],
				font_name='Source Code Pro', bold = True,
				font_size=11,
				x=35, y=150-(15*i),
				color = (57, 255, 20, 255)
				).draw()
		
		for i in range(5):
			pyglet.text.Label(
				self.ascii.binary_sm[random.randint(0,3)],
				font_name='Source Code Pro', bold = True,
				font_size=11,
				x=35, y=120-(15*(i+1)),
				color = (57, 255, 20, 255)
				).draw()


	def game_screen(self):
		"""Loads main game assets onto window when called from update"""

		if self.game_is_running == True:
			self.game_layout.blit(0, 0)
			if self.select_board_size == 4:
				self.grid_4x4.blit(22, 183)
			else:
				self.grid_5x5.blit(22, 183)

			current_time = time.time() - self.start
			self.timer(current_time)

			if self.answer_correct != "n":
				self.indicator()
				pyglet.clock.schedule_once(self.set_to_n, 0.5)
			else:
				self.stats()

			for i in range(self.select_board_size):
					for j in range(self.select_board_size):
						letter = self.engine.game_board[i][j]
						letter = "Qu" if "$" == letter else letter.capitalize()
						if self.select_board_size == 4:
							idx = 68+95*j+1
							idy = 512-95*i
							fs = 32
						else:
							idx = 60+75*j+1
							idy = 522-75*i
							fs = 24
						pyglet.text.Label(
							letter,
							font_name='Subway Ticker', bold = True,
							font_size=fs,
							x=idx, y=idy,
							anchor_x='center', anchor_y='center',
							color = (57, 255, 20, 255)
						).draw()
			

			if self.engine.game_answered != []:
					for i in range(min(len(self.engine.game_answered), 25)):
						len_answered = len(self.engine.game_answered) - 1

						pyglet.text.Label(
							"root@terminal:~$ " + self.view_as_qu(self.engine.game_answered[len_answered - i]),
							font_name='Source Code Pro', bold = True,
							font_size=10,
							x=415, y=35 + 20*(i+1),
							color = (57, 255, 20, 255)
						).draw()

			pyglet.text.Label(
				"> " + self.game_user_input,
				font_name='Source Code Pro', bold = True,
				font_size=10,
				x=415, y=35,
				color = (57, 255, 20, 255)
			).draw()

			if (
				current_time >= self.max_time
			) or (
				self.engine.curr_score == self.engine.max_score
			):
				self.game_end()

	def end_screen(self):
		"""Loads game end menu (game over) assets onto window when called from update"""

		if self.end_is_running == True:
			self.game_layout.blit(0, 0)
			
			pyglet.text.Label(
				"enter username:",
				font_name='Source Code Pro', bold = True,
				font_size=10,
				x=415, y=49,
				color = (57, 255, 20, 255)
			).draw()

			pyglet.text.Label(
				"> " + self.game_user_input,
				font_name='Source Code Pro', bold = True,
				font_size=10,
				x=415, y=35,
				color = (57, 255, 20, 255)
			).draw()

			# win-condition is set to 50% of maximum possible score
			if self.engine.curr_score >= self.engine.max_score*0.5:
				message = "SUCCESS"
			else:
				message = "FAIL"

			pyglet.text.Label(
				message,
				font_name='Source Code Pro', bold = True,
				font_size=11,
				x=408, y=580,
				anchor_x='center',
				color = (0,0,0,255)
			).draw()

			for i in range(8):
				pyglet.text.Label(
					self.ascii.binary_sm[random.randint(0,3)],
					font_name='Source Code Pro', bold = True,
					font_size=11,
					x=35, y=150-(15*i),
					color = (57, 255, 20, 255)
				).draw()

			for i in range(23):
				pyglet.text.Label(
					self.ascii.jumbled_char[random.randint(0,19)],
					font_name='Source Code Pro', bold = True,
					font_size=11,
					x=35, y=535-(15*i),
					color = (57, 255, 20, 255)
				).draw()

	def update(self, dt):
		"""Contains main event loops"""

		@self.window.event
		def on_draw():
			self.window.clear()
			self.start_screen()
			self.leaderboard_screen()
			self.difficulty_screen()
			self.game_screen()
			self.end_screen()

		@self.window.event
		def on_key_press(symbol, modifiers):
			if self.start_is_running == True or self.lb_is_running == True:
				if self.curr_button != None:
					if symbol == key.UP:
						if self.curr_button > 0:
							self.curr_button -= 1
						if self.lb_is_running == True:
							if self.show_idx > 0:
								self.show_idx -= 1
					elif symbol == key.DOWN:
						if self.curr_button < len(self.active_buttons) - 1:
							self.curr_button += 1
						if self.lb_is_running == True:
							if self.show_idx < len(self.lb_list) - 37:
								self.show_idx += 1
					elif symbol == key.ENTER:
						if self.curr_button <= len(self.active_buttons) - 1 and self.curr_button >= 0:
							self.active_buttons[self.curr_button]()
				else:
					self.curr_button = 0


			if self.diff_is_running == True:
				if self.curr_button != None:
					if symbol == key.UP:
						if self.curr_button > 0:
							self.curr_button -= 1
					elif symbol == key.DOWN:
						if self.curr_button < len(self.active_buttons) - 1:
							self.curr_button += 1
					elif symbol == key.ENTER:
						value = self.active_buttons[self.curr_button]
						if value == "normal":
							self.select_board_size = 4
						else:
							self.select_board_size = 5
						self.game()
				else:
					self.curr_button = 0


			if self.end_is_running == True:
				if (97 <= symbol <= 122):
					self.game_user_input += chr(symbol)
				if symbol == key.BACKSPACE:
					self.game_user_input = self.game_user_input[:len(self.game_user_input) - 1]
				if symbol == key.ENTER:
					if self.game_user_input == "":
						self.game_user_input = "(n/a)"
					leaderboard = open("resources/data/leaderboard.txt", "a")
					leaderboard.write("{0},{1},{2}\n".format(self.game_user_input, self.engine.curr_score, self.engine.max_score))
					leaderboard.close()
					self.start_menu()
						

			if self.game_is_running == True:
				if symbol == key.UP:
					if self.answer_idx > 0:
						self.answer_idx -= 1
						self.game_user_input = self.engine.game_answered[self.answer_idx]	
				elif symbol == key.DOWN:
					len_answered = len(self.engine.game_answered)
					if self.answer_idx <= len_answered:
						if self.answer_idx == len_answered:
							self.game_user_input = ""
						else:
							self.answer_idx += 1
						if self.answer_idx == len_answered:
							self.game_user_input = ""
						else:
							self.game_user_input = self.engine.game_answered[self.answer_idx]
				else:
					# resets terminal navigation index
					self.answer_idx = len(self.engine.game_answered)

					if (97 <= symbol <= 122) and len(self.game_user_input) <= 25:
						self.game_user_input += chr(symbol)

					if symbol == key.BACKSPACE:
						self.game_user_input = self.game_user_input[:len(self.game_user_input) - 1]

					if symbol == key.ENTER:
						answer = self.game_user_input
						self.game_user_input = ""
						while "qu" in answer:
							qu_idx = answer.find("qu")
							answer = answer[:qu_idx] + "$" + answer[qu_idx + 2:] 
						if answer and self.engine.verify(answer):
							self.engine.curr_score += self.engine.points(answer)
							self.engine.game_answered.append(answer)
							self.answer_idx = len(self.engine.game_answered)
							self.answer_correct = "t"
						elif answer:
							self.answer_correct = "f"
					
