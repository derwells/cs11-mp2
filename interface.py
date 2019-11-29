import pyglet, time
import engine as e
from pyglet.window import key

class Interface():
	def __init__(self):
		self.window = pyglet.window.Window(width = 800, height = 800)
		self.engine = e.Engine()
		self.game_board_view = None
		self.active_buttons = []
		self.menu_is_running = True
		self.game_is_running = False
		self.lb_is_running = False
		self.game_user_input = None
		self.game_time_start = None
		self.end_is_running = False
		self.init_menu = False
		self.diff_is_running = False
		self.diff_value = None
		self.curr_button = 0
		pyglet.resource.path = ['resources/']
		pyglet.font.add_file('SourceCodePro-Black.ttf')
		pyglet.font.add_file('SourceCodePro-Bold.ttf')
		self.scp_regular = pyglet.font.load('Source Code Pro', bold = False, italic = False)
		self.scp_bold = pyglet.font.load('Source Code Pro Bold', bold = True, italic = False)
		pyglet.resource.reindex()

	def points(self, word):
		word_length = len(word)
		for letter in word:
			if letter == "$":
				word_length += 1
		if word_length <= 4:
			score = 1
		elif word_length == 5:
			score = 2
		elif word_length == 6:
			score = 3
		elif word_length == 7:
			score = 5
		elif word_length >= 8:
			score = 11 
		return score

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
		return

	def difficulty(self):
		self.diff_is_running = True
		self.end_is_running = False
		self.menu_is_running = False
		self.game_is_running = False
		self.init_menu = False
		self.lb_is_running = False

		self.curr_button = None
		self.active_buttons = []
		self.active_buttons.append('normal')
		self.active_buttons.append('hard')
		return

	def boggle(self):
		self.game_is_running = True
		self.menu_is_running = False
		self.lb_is_running = False
		self.end_is_running = False
		self.diff_is_running = False
		self.init_menu = False
		self.menu_is_running = False

		self.answer_idx = 0
		self.answer_correct = False #for UI indicator
		self.curr_button = None
		self.game_points = 0
		self.active_buttons = []
		self.game_user_input = ""
		self.engine.make_board(4)
		self.engine.solve_boggle()
		self.start = time.time()
		self.max_time = len(self.engine.game_solutions)*5
		print(self.max_time)
		print(self.engine.game_solutions)
		return

	def game_end(self):
		self.end_is_running = True
		self.diff_is_running = False
		self.menu_is_running = False
		self.game_is_running = False
		self.lb_is_running = False
		self.init_menu = False
		self.diff_size_is_running = False

		self.game_user_input = ""
		self.curr_button = None
		self.active_buttons = []
		return


	def start_screen(self):
		if self.menu_is_running == True:
			pyglet.text.Label(">hacker.",
								font_name='Source Code Pro', bold = True,
								font_size=12,
								x=50, y=300,
								anchor_x='center', anchor_y='center').draw()
		return			

	def difficulty_screen(self):
		if self.diff_is_running == True:
			pyglet.text.Label("normal",
								font_name='Source Code Pro', bold = True,
								font_size=12,
								x=100, y=300,
								anchor_x='center', anchor_y='center').draw()
			pyglet.text.Label("hard",
								font_name='Source Code Pro', bold = True,
								font_size=12,
								x=100, y=200,
								anchor_x='center', anchor_y='center').draw()
		return


	def timer(self, current_time):
		minutes = int((self.max_time - current_time) // 60)
		seconds = int((self.max_time - current_time) % 60)
		seconds = "0" + str(seconds) if seconds < 10 else seconds
		print(minutes, seconds)
		pyglet.text.Label("{0}:{1}".format(minutes, seconds),
							font_name='Source Code Pro', bold = True,
							font_size=12,
							x=100, y=50,
							anchor_x='center', anchor_y='center').draw()
		return

	def game_screen(self):
		if self.game_is_running == True:
			current_time = time.time() - self.start
			self.timer(current_time)

			word = self.game_user_input

			for i in range(len(word)): # qu handle
					if word[i] == '$':
						word = word[:i] + 'qu' + word[i + 1:]

			pyglet.text.Label(word,
						font_name='Source Code Pro', bold = True,
						font_size=12,
						x=self.window.width//2 - 100, y=self.window.height//2 - 100,
						anchor_x='center', anchor_y='center').draw()
			
			if self.answer_correct:
				word = "correct"
			else:
				word = "wrong"
			pyglet.text.Label(word,
					font_name='Source Code Pro', bold = True,
					font_size=12,
					x=self.window.width//2, y=self.window.height//2,
					anchor_x='center', anchor_y='center').draw()


			if self.engine.game_answered != []:
				for i in range(min(len(self.engine.game_answered), 10)):
					len_answered = len(self.engine.game_answered) - 1
					word = self.engine.game_answered[len_answered - i]
					if '$' in word:
						for i in range(len(word)): # qu handle
							if word[i] == '$':
								word = word[:i] + 'qu' + word[i + 1:]
					pyglet.text.Label(word,
									font_name='Source Code Pro', bold = True,
									font_size=12,
									x=100, y=12*(i+1),
									anchor_x='center', anchor_y='center').draw()
			for i in range(4):
					for j in range(4):
						letter = self.engine.game_board[i][j]
						if self.engine.game_board[i][j] == '$':
							letter = 'qu'
						pyglet.text.Label(letter,
								font_name='Source Code Pro', bold = True,
								font_size=12,
								x=275-50*i, y=350-50*j,
								anchor_x='center', anchor_y='center').draw()
								
			if current_time >= self.max_time: #time
				self.game_end()
		return

	def game_end_screen(self):
		if self.end_is_running == True:
			if self.engine.curr_score >= int(self.engine.max_score*self.diff_value):
				pyglet.text.Label('Successful wordhack.',
									font_name='Source Code Pro', bold = True,
									font_size=12,
									x=100, y=100,
									anchor_x='center', anchor_y='center').draw()
				pass
			else:
				pyglet.text.Label('w0rdh@ck f@il3d...',
									font_name='Source Code Pro', bold = True,
									font_size=12,
									x=100, y=100,
									anchor_x='center', anchor_y='center').draw()



			pyglet.text.Label("back to menu",
								font_name='Source Code Pro', bold = True,
								font_size=12,
								x=100, y=200,
								anchor_x='center', anchor_y='center').draw()
			word = self.game_user_input
			for i in range(len(word)):
					if word[i] == '$':
						word = word[:i] + 'qu' + word[i + 1:]
			pyglet.text.Label(word,
						font_name='Source Code Pro', bold = True,
						font_size=12,
						x=self.window.width//2 - 100, y=self.window.height//2 - 100,
						anchor_x='center', anchor_y='center').draw()
		return


	def update(self, dt):
		@self.window.event
		def on_draw():
			self.window.clear()
			self.start_screen()
			self.difficulty_screen()
			self.game_screen()
			self.game_end_screen()
			return

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
							self.diff_value = 0.3
						else:
							self.diff_value = 0.7
						self.boggle()
				else:
					self.curr_button = 0

			if self.game_is_running == True or self.end_is_running == True:
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

				if (97 <= symbol <= 122):
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
					if self.game_is_running == True:
						if self.engine.verify(answer):
							self.engine.curr_score += self.engine.points(answer)
							self.engine.game_answered.append(answer)
							self.answer_idx = len(self.engine.game_answered)
							self.answer_correct = True
						else:
							self.answer_correct = False
					if self.end_is_running == True:
						leaderboard = open("leaderboard.txt", "a")
						leaderboard.write("{0},{1},{2}\n".format(answer, self.engine.curr_score, self.engine.max_score))
						leaderboard.close()
						self.active_buttons.append(self.start_menu)

			return
					
