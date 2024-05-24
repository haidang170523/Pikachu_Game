import random, collections, time, sys, copy
import pygame as pg
from BFS import bfs

pg.init()
pg.font.init()
pg.mixer.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
FPS = 60
Time = pg.time.Clock()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

LIST_BACKGROUND = [pg.transform.scale(pg.image.load("assets/images/background/" + str(i) + ".jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT)) for i in range(10)]

BOARD_ROW = 9 #7
BOARD_COLUMN = 14 #12
NUM_TILE_ON_BOARD = 21
NUM_SAME_TILE = 4

TILE_WIDTH = 50
TILE_HEIGHT = 55                                                                                           
MARGIN_X = (SCREEN_WIDTH - TILE_WIDTH * BOARD_COLUMN) // 2
MARGIN_Y = (SCREEN_HEIGHT - TILE_HEIGHT * BOARD_ROW) // 2 + 15
NUM_TILE = 33
LIST_TILE = [0] * (NUM_TILE + 1)
for i in range(1, NUM_TILE + 1): LIST_TILE[i] = pg.transform.scale(pg.image.load("assets/images/tiles/section" + str(i) + ".png"), (TILE_WIDTH, TILE_HEIGHT))

GAME_TIME = 180
HINT_TIME = 20

#time bar
TIME_BAR_WIDTH = 500
TIME_BAR_HEIGHT = 30
TIME_BAR_POS = ((SCREEN_WIDTH - TIME_BAR_WIDTH) // 2, (MARGIN_Y - TIME_BAR_HEIGHT) // 2)
TIME_ICON = pg.transform.scale(pg.image.load("assets/images/tiles/section1.png"), (TILE_WIDTH, TILE_HEIGHT))

MAX_LEVEL = 5

LIVES_IMAGE = pg.transform.scale(pg.image.load("assets/images/heart.png"), (50, 50))

FONT_COMICSANSMS = pg.font.SysFont('dejavusans', 40)
FONT_TUROK = pg.font.SysFont('timesnewroman', 60)
FONT_PIKACHU = pg.font.Font("assets/font/pikachu.otf", 50)
FONT_ARIAL = pg.font.Font('assets/font/Folty-Bold.ttf', 50)

# start screen
START_SCREEN_BACKGOUND = pg.transform.scale(pg.image.load("assets/images/background/b1g.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT))

LIST_LEVEL = [pg.transform.scale(pg.image.load("assets/images/level/" + str(i) + ".png"), (50, 50)) for i in range(1, 10)]

# assets button
LOGO_IMAGE = pg.transform.scale(pg.image.load("assets/images/logo/logo_home.png"), (600, 200))
# PLAY_IMAGE = pg.transform.scale(pg.image.load("assets/images/button/play.png"), (144, 48))
PLAY_IMAGE = pg.image.load("assets/images/button/play.png")

SOUND_IMAGE = pg.transform.scale(pg.image.load("assets/images/button/sound.png"), (50, 50))
INFO_IMAGE = pg.transform.scale(pg.image.load("assets/images/button/info.png"), (50, 50))
EXIT_IMAGE = pg.transform.scale(pg.image.load("assets/images/button/close.png"), (60, 60))
PAUSE_PANEL_IMAGE = pg.transform.scale(pg.image.load("assets/images/button/panel_pause.png"), (300, 200))
REPLAY_BUTTON = pg.image.load("assets/images/button/replay.png")
HOME_BUTTON = pg.image.load("assets/images/button/exit.png").convert_alpha()
PAUSE_BUTTON = pg.transform.scale(pg.image.load("assets/images/button/pause.png").convert_alpha(), (50, 50))
CONTINUE_BUTTON = pg.image.load("assets/images/button/continue.png").convert_alpha()
GAMEOVER_BACKGROUND = pg.image.load("assets/images/button/gameover.png").convert_alpha()
WIN_BACKGROUND = pg.image.load("assets/images/button/win1.png").convert_alpha()
INSTRUCTION_PANEL = pg.transform.scale(pg.image.load("assets/images/button/instruction.png"), (700, 469)).convert_alpha()
TIME_END = 6
show_instruction = False

#load background music
pg.mixer.music.load("assets/music/background1.mp3")
pg.mixer.music.set_volume(0.1)
pg.mixer.music.play(-1, 0.0, 5000)
sound_on = True

#load sound
click_sound = pg.mixer.Sound("assets/sound/click_sound.mp3")
click_sound.set_volume(0.2)
success_sound = pg.mixer.Sound("assets/sound/success.mp3")
success_sound.set_volume(0.2)
fail_sound = pg.mixer.Sound("assets/sound/fail.mp3")
fail_sound.set_volume(0.2)
win_sound = pg.mixer.Sound("assets/sound/win.mp3")
win_sound.set_volume(0.2)
game_over_sound = pg.mixer.Sound("assets/sound/gameover.wav")
game_over_sound.set_volume(0.2)
def main():
	#init pygame and module
	global level, lives
	
	while True:
		level = 1
		lives = 3
		start_screen()
		while level <= MAX_LEVEL:
			random.shuffle(LIST_BACKGROUND)
			playing()
			level += 1
			pg.time.wait(300)
			pg.mixer.music.play()
			#end

def start_screen():
	global sound_on, music_on, show_instruction
	while True:
		
		Time.tick(FPS)
		screen.blit(START_SCREEN_BACKGOUND, (0, 0))
		# blit logo text
		image_width, image_height = LOGO_IMAGE.get_size()
		screen.blit(LOGO_IMAGE, ((SCREEN_WIDTH - image_width) // 2 - 20, (SCREEN_HEIGHT - image_height) // 2 - 150))
		mouse_x, mouse_y = pg.mouse.get_pos()

		# blit play button
		image_width, image_height = PLAY_IMAGE.get_size()
		play_rect = pg.Rect((SCREEN_WIDTH - image_width) // 2, (SCREEN_HEIGHT - image_height) // 2 + 100, image_width, image_height)
		screen.blit(PLAY_IMAGE, play_rect)

		#blit sound on button
		image_width, image_height = SOUND_IMAGE.get_size()
		sound_rect = pg.Rect(15, SCREEN_HEIGHT - 15 - image_height, image_width, image_height)
		if sound_on:
			screen.blit(SOUND_IMAGE, sound_rect)
		else: draw_dark_image(SOUND_IMAGE, sound_rect, (120, 120, 120))

		# blit info button
		image_width, image_height = INFO_IMAGE.get_size()
		info_rect = pg.Rect(SCREEN_WIDTH - 15 - image_width, SCREEN_HEIGHT - 15 - image_height, image_width, image_height)
		screen.blit(INFO_IMAGE, info_rect)

		# blit exit button
		image_width, image_height = EXIT_IMAGE.get_size()
		exit_rect = pg.Rect(SCREEN_WIDTH - 220, 105, image_width, image_height)

		

		if show_instruction:
			show_dim_screen()
			draw_instruction()
			screen.blit(EXIT_IMAGE, exit_rect)

		#check collide with mouse
		if play_rect.collidepoint(mouse_x, mouse_y) and not show_instruction:
			draw_dark_image(PLAY_IMAGE, play_rect, (60, 60, 60))
		
		if sound_rect.collidepoint(mouse_x, mouse_y) and not show_instruction:
			if sound_on:
				draw_dark_image(SOUND_IMAGE, sound_rect, (60, 60, 60))

		if info_rect.collidepoint(mouse_x, mouse_y) and not show_instruction:
				draw_dark_image(INFO_IMAGE, info_rect, (60, 60, 60))

		if exit_rect.collidepoint(mouse_x, mouse_y) and show_instruction:
				draw_dark_image(EXIT_IMAGE, exit_rect, (60, 60, 60))

		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				sys.exit()
			if event.type == pg.MOUSEBUTTONDOWN:
				mouse_x, mouse_y = event.pos
				if play_rect.collidepoint((mouse_x, mouse_y)):
					click_sound.play()
					draw_dark_image(PLAY_IMAGE, play_rect, (120, 120, 120))
					pg.display.flip()
					pg.time.wait(200)
					return
				if sound_rect.collidepoint(mouse_x, mouse_y):
					if sound_on:
						sound_on = False
						pg.mixer.music.set_volume(0)
						success_sound.set_volume(0)
						fail_sound.set_volume(0)
						click_sound.set_volume(0)
						
					else:
						sound_on = True
						pg.mixer.music.set_volume(0.1)
						success_sound.set_volume(0.2)
						fail_sound.set_volume(0.2)
						click_sound.set_volume(0.2)

						
				if info_rect.collidepoint(mouse_x, mouse_y):
					show_instruction = True
					click_sound.play()
				if exit_rect.collidepoint(mouse_x, mouse_y):
					show_instruction = False
					click_sound.play()
					

						
		pg.display.flip()

def playing():
	global level, lives, paused, time_start_paused, last_time_get_point, time_paused
	paused = False
	time_start_paused = 0
	time_paused = 0

	background = LIST_BACKGROUND[0] # get random background
	board = get_random_board() # get ramdom board of game

	mouse_x, mouse_y = 0, 0
	clicked_tiles = [] # store index cards clicked
	hint = get_hint(board)

	last_time_get_point = time.time()
	start_time = time.time()
	bouns_time = 0

	while True:
		Time.tick(FPS)

		screen.blit(background, (0, 0)) # set background
		dim_screen = pg.Surface(screen.get_size(), pg.SRCALPHA)
		pg.draw.rect(dim_screen, (0, 0, 0, 150), dim_screen.get_rect())
		screen.blit(dim_screen, (0, 0))
		draw_board(board)
		draw_lives(lives, level)
		draw_time_bar(start_time, bouns_time)
		draw_clicked_tiles(board, clicked_tiles)

		mouse_clicked = False

		if lives == 0:
			show_dim_screen()
			level = MAX_LEVEL + 1
			game_over_sound.play()
			pg.mixer.music.pause()
			start_end = time.time()
			while time.time() - start_end <= TIME_END:
				screen.blit(GAMEOVER_BACKGROUND, (0, 0))
				pg.display.flip()
			return

		# check event
		for event in pg.event.get():
			if event.type == pg.QUIT: pg.quit(), sys.exit()
			if event.type == pg.MOUSEMOTION:
				mouse_x, mouse_y = event.pos
			if event.type == pg.MOUSEBUTTONDOWN:
				mouse_x, mouse_y = event.pos
				mouse_clicked = True
			if event.type == pg.KEYUP:
				if event.key == pg.K_k: # use key k to hack game
					tile1_i, tile1_j = hint[0][0], hint[0][1]
					tile2_i, tile2_j = hint[1][0], hint[1][1]
					board[tile1_i][tile1_j] = 0
					board[tile2_i][tile2_j] = 0
					bouns_time += 1
					update_difficulty(board, level, tile1_i, tile1_j, tile2_i, tile2_j)

					if is_level_complete(board): return

					if not(board[tile1_i][tile1_j] != 0 and bfs(board, tile1_i, tile1_j, tile2_i, tile2_j)):
						hint = get_hint(board)
						while not hint:
							pg.time.wait(100)
							reset_board(board)
							hint = get_hint(board)

		draw_pause_button(mouse_x, mouse_y, mouse_clicked)

		is_time_up = check_time(start_time, bouns_time) # 0 if game over, 1 if lives -= 1, 2 if nothing
		if paused:
			show_dim_screen()
			if is_time_up == 0: #game over
				lives -= 1
			elif is_time_up == 1:
				lives -= 1
				level -= 1
				return
					 
			select = panel_pause(mouse_x, mouse_y, mouse_clicked) # 0 if click replay, 1 if click home, 2 if continue, 3 if nothing
			if select == 0: 
				lives -= 1
				if lives > 0:
					level -= 1
					return
			elif select == 1:
				level = MAX_LEVEL + 1
				return 
			elif select == 2: mouse_clicked = False # continue

		# check time get hint
		if time.time() - last_time_get_point - time_paused > HINT_TIME and not paused: draw_hint(hint)			
		#update
		try:
			tile_i, tile_j = get_index_at_mouse(mouse_x, mouse_y)
			if board[tile_i][tile_j] != 0 and not paused:
				draw_border_tile(board, tile_i, tile_j)
				if mouse_clicked:
					mouse_clicked = False
					clicked_tiles.append((tile_i, tile_j))
					draw_clicked_tiles(board, clicked_tiles)
					if len(clicked_tiles) > 1: # 2 cards was clicked 
						path = bfs(board, clicked_tiles[0][0], clicked_tiles[0][1], tile_i, tile_j)
						if path:
							# delete the same card
							board[clicked_tiles[0][0]][clicked_tiles[0][1]] = 0
							board[tile_i][tile_j] = 0
							success_sound.play(maxtime = 1500)
							draw_path(path)

							bouns_time += 1
							last_time_get_point = time.time() # count time hint
							# if level > 1, upgrade difficulty by moving cards 
							update_difficulty(board, level, clicked_tiles[0][0], clicked_tiles[0][1], tile_i, tile_j)
							if is_level_complete(board):
								if level == 5:
									pg.mixer.music.pause()
									fade_speed = 2
									alpha = 0
									time_win = 10
									tmp = time.time()
									win_sound.play(maxtime = 10000)
									show_dim_screen()
									while time.time() - tmp < 10:
										alpha += fade_speed
										if alpha > 255: alpha = 255
										tmp_image = WIN_BACKGROUND.copy()
										tmp_image.set_alpha(alpha)
										screen.blit(tmp_image, (180, 70))
										pg.display.flip()
								return
							# if hint got by player
							if not(board[hint[0][0]][hint[0][1]] != 0 and bfs(board, hint[0][0], hint[0][1], hint[1][0], hint[1][1])):
								hint = get_hint(board)
								while not hint:
									pg.time.wait(100)
									reset_board(board)
									hint = get_hint(board)
						else:
							if not (clicked_tiles[0][0] == clicked_tiles[1][0] and clicked_tiles[0][1] == clicked_tiles[1][1]):
								fail_sound.play(maxtime = 500)

						#reset
						clicked_tiles = []
		except: pass
		pg.display.flip()

def get_random_board():
	list_index_tiles = list(range(1, NUM_TILE + 1)) #21
	random.shuffle(list_index_tiles)
	list_index_tiles = list_index_tiles[:NUM_TILE_ON_BOARD] * NUM_SAME_TILE #84
	random.shuffle(list_index_tiles)
	board = [[0 for _ in range(BOARD_COLUMN)]for _ in range(BOARD_ROW)]
	k = 0
	for i in range(1, BOARD_ROW - 1):
		for j in range(1, BOARD_COLUMN - 1):
			board[i][j] = list_index_tiles[k]
			k += 1
	return board

def get_left_top_coords(i, j): # get left top coords of card from index i, j
	x = j * TILE_WIDTH + MARGIN_X
	y = i * TILE_HEIGHT + MARGIN_Y
	return x, y

def get_center_coords(i, j): # get center coords of card from index i, j
	x, y = get_left_top_coords(i, j)
	return x + TILE_WIDTH // 2, y + TILE_HEIGHT // 2

def get_index_at_mouse(x, y): # get index of card at mouse clicked from coords x, y
	if x < MARGIN_X or y < MARGIN_Y: return None, None
	return (y - MARGIN_Y) // TILE_HEIGHT, (x - MARGIN_X) // TILE_WIDTH

def draw_board(board):
	for i in range(1, BOARD_ROW - 1):
		for j in range(1, BOARD_COLUMN - 1):
			if board[i][j] != 0:
				screen.blit(LIST_TILE[board[i][j]], get_left_top_coords(i, j))

def draw_dark_image(image, image_rect, color):
	dark_image = image.copy()
	dark_image.fill(color, special_flags = pg.BLEND_RGB_SUB)
	screen.blit(dark_image, image_rect)

def draw_clicked_tiles(board, clicked_tiles):
	for i, j in clicked_tiles:
		x, y = get_left_top_coords(i, j)
		try:
			darkImage = LIST_TILE[board[i][j]].copy()
			darkImage.fill((60, 60, 60), special_flags = pg.BLEND_RGB_SUB)
			screen.blit(darkImage, (x, y))
		except: pass

def draw_border_tile(board, i, j):
	x, y = get_left_top_coords(i, j)
	pg.draw.rect(screen, (0, 0, 255),(x - 1, y - 3, TILE_WIDTH + 4, TILE_HEIGHT + 4), 2)

def draw_path(path):
	for i in range(len(path) - 1):
		start_pos = (get_center_coords(path[i][0], path[i][1]))
		end_pos = (get_center_coords(path[i + 1][0], path[i + 1][1]))
		pg.draw.line(screen, 'red', start_pos, end_pos, 4)
		pg.display.update()
	pg.time.wait(400)

def get_hint(board):
	hint = [] # stories two tuple
	tiles_location = collections.defaultdict(list)
	for i in range(BOARD_ROW):
		for j in range(BOARD_COLUMN):
			if board[i][j]:
				tiles_location[board[i][j]].append((i, j))
	for i in range(BOARD_ROW):
		for j in range(BOARD_COLUMN):
			if board[i][j]:
				for o in tiles_location[board[i][j]]:	
					if o != (i, j) and bfs(board, i, j, o[0], o[1]):
						hint.append((i, j))
						hint.append(o)
						return hint
	return []

def draw_hint(hint):
	for i, j in hint:
		x, y = get_left_top_coords(i, j)
		pg.draw.rect(screen, (0, 255, 0),(x - +1, y - 2, TILE_WIDTH + 4, TILE_HEIGHT + 4), 2)

def draw_time_bar(start_time, bouns_time):
	global time_start_paused, time_paused
	pg.draw.rect(screen, (255,255,255,5), (TIME_BAR_POS[0], TIME_BAR_POS[1], TIME_BAR_WIDTH, TIME_BAR_HEIGHT), 2, border_radius = 20)
	timeOut = 1 - (time.time() - start_time - bouns_time - time_paused) / GAME_TIME # ratio between remaining time and total time
	if paused:
		if not time_start_paused: time_start_paused = time.time()
		timeOut = 1 - (time_start_paused - start_time - bouns_time - time_paused) / GAME_TIME
	else:
		if time_start_paused:
			time_paused += time.time() - time_start_paused
			timeOut = 1 - (time.time() - start_time - bouns_time - time_paused) / GAME_TIME
		time_start_paused = 0

	innerPos = (TIME_BAR_POS[0] + 2, TIME_BAR_POS[1] + 2)
	innerSize = (TIME_BAR_WIDTH * timeOut - 4, TIME_BAR_HEIGHT - 4)
	pg.draw.rect(screen, 'green', (innerPos, innerSize), border_radius = 20)

def is_level_complete(board):
	for i in range(len(board)):
		for j in range(len(board[0])):
			if board[i][j] != 0: return False
	return True

def update_difficulty(board, level, tile1_i, tile1_j, tile2_i, tile2_j):
	if level == 2: #all card move up
		for j in (tile1_j, tile2_j):
			new_column = [0]
			for i in range(BOARD_ROW):
				if board[i][j] != 0:
					new_column.append(board[i][j])
			while(len(new_column) < BOARD_ROW): new_column.append(0)
			for k in range(BOARD_ROW):
				board[k][j] = new_column[k]
	if level == 3: #all card move down
		for j in (tile1_j, tile2_j):
			new_column = []
			for i in range(BOARD_ROW):
				if board[i][j] != 0:
					new_column.append(board[i][j])
			while(len(new_column) < BOARD_ROW - 1): new_column = [0] + new_column
			new_column.append(0)
			for k in range(BOARD_ROW):
				board[k][j] = new_column[k]
	if level == 4: #all card move left
		for i in (tile1_i, tile2_i):
			new_row = [0]
			for j in range(BOARD_COLUMN):
				if board[i][j] != 0:
					new_row.append(board[i][j])
			while(len(new_row) < BOARD_COLUMN): new_row.append(0)
			for k in range(BOARD_COLUMN):
				board[i][k] = new_row[k]
	if level == 5: #all card move right
		for i in (tile1_i, tile2_i):
			new_row = []
			for j in range(BOARD_COLUMN):
				if board[i][j] != 0:
					new_row.append(board[i][j])
			while len(new_row) < BOARD_COLUMN - 1: new_row = [0] + new_row
			new_row.append(0)
			for k in range(BOARD_COLUMN):
				board[i][k] = new_row[k]

def draw_lives(lives, level):
	screen.blit(LIVES_IMAGE, (10, 12))
	lives_count = FONT_PIKACHU.render(str(lives), True, 'white')
	screen.blit(lives_count, (60, 13))

	screen.blit(LIST_LEVEL[level - 1], (SCREEN_WIDTH - 70, 12))

def reset_board(board):
	current_tiles = []
	for i in range(BOARD_ROW):
		for j in range(BOARD_COLUMN):
			if board[i][j]: current_tiles.append(board[i][j])
	tmp = current_tiles[:]
	while tmp == current_tiles:
		random.shuffle(current_tiles)
	k = 0
	for i in range(BOARD_ROW):
		for j in range(BOARD_COLUMN):
			if board[i][j]:
				board[i][j] = current_tiles[k]
				k += 1
	return board

def check_time(start_time, bouns_time):
	global lives, level, paused, time_start_paused, time_paused
	if paused: return 2	
	# check game lost
	if time.time() - start_time - time_paused > GAME_TIME + bouns_time: # time up
		paused = True
		if lives <= 1: return 0
		return 1
	return 2

def show_dim_screen():
	dim_screen = pg.Surface(screen.get_size(), pg.SRCALPHA)
	pg.draw.rect(dim_screen, (0, 0, 0, 220), dim_screen.get_rect())
	screen.blit(dim_screen, (0, 0))
	
def panel_pause(mouse_x, mouse_y, mouse_clicked):
	global lives, paused
	panel_rect = pg.Rect(0, 0, *PAUSE_PANEL_IMAGE.get_size())
	panel_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
	screen.blit(PAUSE_PANEL_IMAGE, panel_rect)

	continue_rect = pg.Rect(0, 0, *CONTINUE_BUTTON.get_size())
	continue_rect.center = (panel_rect.centerx, panel_rect.centery)
	screen.blit(CONTINUE_BUTTON, continue_rect)
	if continue_rect.collidepoint(mouse_x, mouse_y):
		draw_dark_image(CONTINUE_BUTTON, continue_rect, (60, 60, 60))
		if mouse_clicked:
			draw_dark_image(CONTINUE_BUTTON, continue_rect, (120, 120, 120))
			paused = False
			click_sound.play()
			return 2

	replay_rect = pg.Rect(0, 0, *REPLAY_BUTTON.get_size())
	replay_rect.center = (panel_rect.centerx - 80, panel_rect.centery)
	screen.blit(REPLAY_BUTTON, replay_rect)
	if replay_rect.collidepoint(mouse_x, mouse_y):
		draw_dark_image(REPLAY_BUTTON, replay_rect, (60, 60, 60))
		if mouse_clicked:
			draw_dark_image(REPLAY_BUTTON, replay_rect, (120, 120, 120))
			click_sound.play()
			return 0

	home_rect = pg.Rect(0, 0, *HOME_BUTTON.get_size())
	home_rect.center = (panel_rect.centerx + 80, panel_rect.centery)
	screen.blit(HOME_BUTTON, home_rect)
	if home_rect.collidepoint(mouse_x, mouse_y):
		draw_dark_image(HOME_BUTTON, home_rect, (60, 60, 60))
		if mouse_clicked:
			draw_dark_image(HOME_BUTTON, home_rect, (120, 120, 120))
			click_sound.play()
			return 1

	return 3

def draw_pause_button(mouse_x, mouse_y, mouse_clicked):
	global paused
	pause_rect = pg.Rect(0, 0, *PAUSE_BUTTON.get_size())
	pause_rect.center = (SCREEN_WIDTH - 220, 35)
	screen.blit(PAUSE_BUTTON, pause_rect)
	if pause_rect.collidepoint(mouse_x, mouse_y):
		if not paused: draw_dark_image(PAUSE_BUTTON, pause_rect, (60, 60, 60))
		if mouse_clicked:
			mouse_clicked = False
			paused = True
			click_sound.play()

def draw_instruction():
	panel_rect = pg.Rect(0, 0, *INSTRUCTION_PANEL.get_size())
	panel_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
	screen.blit(INSTRUCTION_PANEL, panel_rect)

if __name__ == '__main__':
	main()