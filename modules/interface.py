import pyglet, time
from modules import ascii_art as a
from modules import engine as e
from pyglet.window import key

class Interface():
	def __init__(self):
		self.window = pyglet.window.Window(width = 800, height = 600)
		self.engine = e.Engine()
		self.active_buttons = []
		self.menu_is_running = True
		self.game_is_running = False
		self.lb_is_running = False
		self.end_is_running = False
		self.init_menu = False
		self.diff_is_running = False
		self.ascii = a.Ascii()
		pyglet.resource.path = ['resources/']
		pyglet.font.add_directory('resources/')
		self.scp_regular = pyglet.font.load('Hack', bold = False, italic = False)
		self.scp_bold = pyglet.font.load('Source Code Pro Bold', bold = True, italic = False)
		self.game_layout = pyglet.image.load('resources/game_gui.png')
		pyglet.resource.reindex()

	def start_menu(self):
		self.menu_is_running = True
		self.game_is_running = False
		self.diff_is_running = False
		self.lb_is_running = False
		self.init_menu = False
		self.end_is_running = False

		self.game_user_input = ""
		self.curr_button = None
		self.active_buttons = []
		self.active_buttons.append(self.difficulty)

	def difficulty(self):
		self.diff_is_running = True
		self.end_is_running = False
		self.menu_is_running = False
		self.game_is_running = False
		self.init_menu = False
		self.lb_is_running = False

		self.select_board_size = None
		self.curr_button = None
		self.active_buttons = []
		self.active_buttons.append('normal')
		self.active_buttons.append('hard')

	def boggle(self):
		self.game_is_running = True
		self.menu_is_running = False
		self.lb_is_running = False
		self.end_is_running = False
		self.diff_is_running = False
		self.init_menu = False
		self.menu_is_running = False

		self.caret_idx = 0
		self.answer_idx = 0
		self.answer_correct = "n" #for UI indicator
		self.curr_button = None
		self.active_buttons = []
		self.game_user_input = ""
		self.engine.make_board(self.select_board_size)
		self.engine.solve_boggle()
		self.start = time.time()
		self.max_time = len(self.engine.game_solutions)*5
		print(self.engine.game_solutions)

	def game_end(self):
		self.end_is_running = True
		self.diff_is_running = False
		self.menu_is_running = False
		self.game_is_running = False
		self.lb_is_running = False
		self.init_menu = False
		self.diff_size_is_running = False

		self.caret_idx = 0
		self.game_user_input = ""
		self.curr_button = None
		self.active_buttons = []


	def start_screen(self):
		if self.menu_is_running == True:
			pyglet.text.Label(
				">wordhack",
				font_name='Hack', bold = True,
				font_size=12,
				x=50, y=300,
				anchor_x='center', anchor_y='center',
				color = (57,255,0,255)
				).draw()

	def difficulty_screen(self):
		if self.diff_is_running == True:
			pyglet.text.Label(
				"normal",
				font_name='Hack', bold = True,
				font_size=12,
				x=100, y=300,
				anchor_x='center', anchor_y='center',
				color = (57,255,0,255)
				).draw()

			pyglet.text.Label(
				"hard",
				font_name='Hack', bold = True,
				font_size=12,
				x=100, y=200,
				anchor_x='center', anchor_y='center',
				color = (57,255,0,255)
				).draw()

	def timer(self, current_time):
		minutes = int((self.max_time - current_time) // 60)
		seconds = int((self.max_time - current_time) % 60)
		seconds = "0" + str(seconds) if seconds < 10 else seconds

		pyglet.text.Label(
			"{0}:{1}".format(minutes, seconds),
			font_name='Hack', bold = True,
			font_size=12,
			x=408, y=580,
			anchor_x='center',
			color = (0,0,0,255)
			).draw()
	
	def view_as_qu(self, word):
		if '$' in word:
			for i in range(len(word)):
				if word[i] == '$':
					word = word[:i] + 'qu' + word[i + 1:]
		return word

	def input_box(self):
		current_input = self.view_as_qu(self.game_user_input)
		pyglet.text.Label(
			"root@terminal:~$ " + current_input,
			font_name='Hack', bold = True,
			font_size=10,
			x=415, y=35,
			color = (57,255,0,255)
			).draw()

		if self.engine.game_answered != []:
				for i in range(min(len(self.engine.game_answered), 25)):
					len_answered = len(self.engine.game_answered) - 1
					past_answer = self.engine.game_answered[len_answered - i]
					self.view_as_qu(past_answer)

					pyglet.text.Label(
						"root@terminal:~$ " + past_answer,
						font_name='Hack', bold = True,
						font_size=10,
						x=415, y=35 + 20*(i+1),
						color = (57,255,0,255)
						).draw()

		return
	
	def indicator(self):
		if self.answer_correct == "t":
			indicator = self.ascii.success
			for i in range(len(indicator)):
				pyglet.text.Label(
					indicator[i],
					font_name='Hack', bold = True,
					font_size=8,
					x=30, y=120 - 10*i,
					color = (57,255,0,255)
					).draw()
		else:
			indicator = self.ascii.error
			for i in range(len(indicator)):
				pyglet.text.Label(
					indicator[i],
					font_name='Hack', bold = True,
					font_size=8,
					x=80, y=120 - 10*i,
					color = (57,255,0,255)
					).draw()


	def stats(self, dt):
		self.answer_correct = "n"
		pyglet.text.Label(str(self.engine.curr_score),
					font_name='Hack', bold = True,
					font_size=8,
					x=35, y=120).draw()

	def game_screen(self):
		if self.game_is_running == True:

			self.game_layout.blit(0, 0)
			current_time = time.time() - self.start
			self.timer(current_time)

			self.input_box()
			if self.engine.game_answered != []:
				for i in range(min(len(self.engine.game_answered), 25)):
					len_answered = len(self.engine.game_answered) - 1
					past_answer = self.engine.game_answered[len_answered - i]
					self.view_as_qu(past_answer)

					pyglet.text.Label(
						"root@terminal:~$ " + past_answer,
						font_name='Hack', bold = True,
						font_size=10,
						x=415, y=35 + 20*(i+1),
						color = (57,255,0,255)
						).draw()

			if self.answer_correct != "n":
				pyglet.clock.schedule_once(self.stats, 1.0)
				self.indicator()
			else:
				self.stats(0)

			for i in range(self.select_board_size):
					for j in range(self.select_board_size):
						letter = self.engine.game_board[i][j]
						letter = self.view_as_qu(letter)
						pyglet.text.Label(
							letter,
							font_name='Hack', bold = True,
							font_size=12,
							x=275-50*i, y=350-50*j,
							anchor_x='center', anchor_y='center',
							color = (57,255,0,255)
							).draw()

			if current_time >= self.max_time: #time
				self.game_end()

	def game_end_screen(self):
		if self.end_is_running == True:
			if self.engine.curr_score >= int(self.engine.max_score*0.4):
				pyglet.text.Label(
					'Successful wordhack.',
					font_name='Hack', bold = True,
					font_size=12,
					x=100, y=100,
					anchor_x='center', anchor_y='center',
					color = (57,255,0,255)
					).draw()
			else:
				pyglet.text.Label(
					'w0rdh@ck f@il3d...',
					font_name='Hack', bold = True,
					font_size=12,
					x=100, y=100,
					anchor_x='center', anchor_y='center',
					color = (57,255,0,255)
					).draw()

			pyglet.text.Label(
				"back to menu",
				font_name='Hack', bold = True,
				font_size=12,
				x=100, y=200,
				anchor_x='center', anchor_y='center',
				color = (57,255,0,255)
				).draw()

			username = self.game_user_input
			pyglet.text.Label(
				username,
				font_name='Hack', bold = True,
				font_size=12,
				x=self.window.width//2 - 100, y=self.window.height//2 - 100,
				anchor_x='center', anchor_y='center',
				color = (57,255,0,255)
				).draw()


	def update(self, dt):
		@self.window.event
		def on_draw():
			self.window.clear()
			self.start_screen()
			self.difficulty_screen()
			self.game_screen()
			self.game_end_screen()

		@self.window.event
		def on_mouse_press(x,y,button,modifiers):
			print(x,y)

		@self.window.event
		def on_key_press(symbol, modifiers):
			if self.menu_is_running == True or self.end_is_running == True:
				if self.curr_button != None:
					if symbol == key.UP:
						if self.curr_button > 0:
							self.curr_button -= 1
					elif symbol == key.DOWN:
						if self.curr_button < len(self.active_buttons) - 1:
							self.curr_button += 1
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
						self.boggle()
				else:
					self.curr_button = 0


			if self.end_is_running == True:
				if (97 <= symbol <= 122):
					self.game_user_input += chr(symbol)
				if symbol == key.BACKSPACE:
					self.game_user_input = self.game_user_input[:len(self.game_user_input) - 1]
				if symbol == key.ENTER:
					username = self.game_user_input
					self.game_user_input = ""
					leaderboard = open("leaderboard.txt", "a")
					leaderboard.write("{0},{1},{2}\n".format(username, self.engine.curr_score, self.engine.max_score))
					leaderboard.close()
					self.active_buttons.append(self.start_menu)
						

			if self.game_is_running == True:
				if symbol == key.UP:
					if self.answer_idx > 0:
						self.answer_idx -= 1
						self.game_user_input = self.engine.game_answered[self.answer_idx]	
				if symbol == key.DOWN:
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
				if (97 <= symbol <= 122) and len(self.game_user_input) <= 26:
					self.answer_idx = len(self.engine.game_answered) #when a key is pressed, reset idx
					if symbol == 117:
						if self.game_is_running == True:
							word = self.game_user_input
							if word != "":
								if word[len(word) - 1] == 'q':
									self.game_user_input = self.game_user_input[:len(word) - 1]
									self.game_user_input += '$'
								else:
									self.game_user_input += 'u'
							else:
								self.game_user_input += "u"
						else:
							self.game_user_input += "u"
					else:
						self.game_user_input += chr(symbol)
				if symbol == key.BACKSPACE:
					self.game_user_input = self.game_user_input[:len(self.game_user_input) - 1]
					self.answer_idx = len(self.engine.game_answered) #when a key is pressed, reset idx
				if symbol == key.ENTER:
					self.answer_idx = len(self.engine.game_answered) #when a key is pressed, reset idx
					answer = self.game_user_input
					self.game_user_input = ""
					if answer and self.engine.verify(answer):
						self.engine.curr_score += self.engine.points(answer)
						self.engine.game_answered.append(answer)
						self.answer_idx = len(self.engine.game_answered)
						self.answer_correct = "t"
					elif answer:
						self.answer_correct = "f"
					
