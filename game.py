#3rd party modules
import pygame
import libtcodpy as libtcod
import math
import random
#game files
import constants

class struc_Tile:
	def __init__(self,block_path):
		self.block_path = block_path
		self.explored = False

class struc_Assets:
	def __init__(self):
	

		#SPRITES
		self.S_WALL = pygame.image.load("data/wall.jpg")
		self.S_WALLEXPLORED = pygame.image.load("data/wallunseen2.png")
		self.S_FLOOR = pygame.image.load("data/floor.png")
		self.S_FLOOREXPLORED = pygame.image.load("data/floorunseen2.png")

		#ITEMS
		self.S_PISTOL = [pygame.transform.scale(pygame.image.load("data/pistol.png"), 
					   (constants.CELL_WIDTH, constants.CELL_HEIGHT))]

		self.S_GRENADE = [pygame.transform.scale(pygame.image.load("data/grenade.png"), 
					   (constants.CELL_WIDTH, constants.CELL_HEIGHT))]

		self.S_KEVLAR = [pygame.transform.scale(pygame.image.load("data/kevlar.png"), 
					   (constants.CELL_WIDTH, constants.CELL_HEIGHT))]

		#FONTS
		self.FONT_DEBUG_MESSAGE = pygame.font.Font("data\joystix.ttf", 16)
		self.FONT_MESSAGE_TEXT = pygame.font.Font("data\joystix.ttf", 12)


class damage_system:






class obj_Actor:
	def __init__(self, x, y,
				 name_object, 
				 animation,
				 animation_speed = .5, 
				 creature = None, 
				 ai = None,
				 container = None,
				 item = None,
				 equipment = None):

		self.x = x #map address
		self.y= y #map address
		self.name_object = name_object
		self.animation = animation
		self.animation_speed = animation_speed / 2.0 #in seconds

		#animation flicker speed
		self.flicker_speed = self.animation_speed / len(self.animation)
		self.flicker_timer = 0.0
		self.sprite_image = 0

		self.creature = creature
		if self.creature:
			self.creature.owner = self

		self.ai = ai
		if self.ai:
			self.ai.owner = self

		self.container = container
		if self.container:
			self.container.owner = self

		self.item = item
		if self.item:
			self.item.owner = self

		self.equipment = equipment
		if self.equipment:
			self.equipment.owner = self

			self.item = com_Item()
			self.item.owner = self

	@property
	def display_name(self):

		if self.creature:
			return(self.creature.name_instance + " the " + self.name_object)

		if self.item:
			if self.equipment and self.equipment.equipped:
				return (self.name_object + " (e)")

			else:
				return self.name_object

	def draw(self):
		is_visible = libtcod.map_is_in_fov(FOV_MAP, self.x, self.y)

		if is_visible:
			if len(self.animation) == 1:
				SURFACE_MAIN.blit(self.animation[0], (self.x*constants.CELL_WIDTH, self.y*constants.CELL_HEIGHT))

			elif len(self.animation) > 1:
				if CLOCK.get_fps() > 0.0:
					self.flicker_timer += 1 / CLOCK.get_fps()

				if self.flicker_timer >= self.animation_speed:
					self.flicker_timer = 0.0

					if self.sprite_image >= len(self.animation) - 1:
						self.sprite_image = 0

					else:
						self.sprite_image += 1

				SURFACE_MAIN.blit(self.animation[self.sprite_image], 
								 (self.x*constants.CELL_WIDTH, self.y*constants.CELL_HEIGHT))	

	def distance_to(self, other):

		dx = other.x - self.x
		dy = other.y - self.y

		return math.sqrt(dx ** 2 + dy ** 2)

	def move_towards(self, other):

		dx = other.x - self.x
		dy = other.y - self.y

		distance = math.sqrt(dx ** 2 + dy ** 2)

		dx = int(round(dx / distance))
		dy = int(round(dy / distance))

		self.creature.move(dx, dy)


class obj_Game:
	def __init__(self):
		self.current_map = map_create()
		self.current_objects = []
		self.message_history = []

class obj_Spritesheet:
	def __init__(self, file_name):
		self.sprite_sheet = pygame.image.load(file_name).convert()
		self.tiledict = {'a': 1, 'b': 2, 'c': 3, 'd': 4,
						 'e': 5, 'f': 6, 'g': 7, 'h': 8,
						 'i': 9, 'j': 10, 'k': 11, 'l': 12,
						 'm': 13, 'n': 14, 'o': 15, 'p': 16}

	def get_image(self, column, row, width = constants.CELL_WIDTH, height = constants.CELL_HEIGHT,
				  scale = None):

		image_list = []

		image = pygame.Surface([width, height]).convert()

		image.blit(self.sprite_sheet, (0, 0), (self.tiledict[column]*width, row*height, width, height))

		image.set_colorkey(constants.COLOR_BLACK)

		if scale:
			(new_w, new_h) = scale
			image = pygame.transform.scale(image, (new_w, new_h))

		image_list.append(image)

		return image_list

	def get_animation(self, column, row, width = constants.CELL_WIDTH, height = constants.CELL_HEIGHT,
				  	  num_sprites = 1, scale = None):

		image_list = []

		for i in range(num_sprites):
			
			image = pygame.Surface([width, height]).convert()

			
			image.blit(self.sprite_sheet, (0, 0), (self.tiledict[column]*width+(width*i), row*height, width, height))

			
			image.set_colorkey(constants.COLOR_BLACK)

			if scale:
				(new_w, new_h) = scale

				image = pygame.transform.scale(image, (new_w, new_h))

			image_list.append(image)

		return image_list



class com_Creature:

	def __init__(self, name_instance, base_atk = 2, base_def = 0, hp = 10, 
				 death_function = None):
		self.name_instance = name_instance
		self.base_atk = base_atk
		self.base_def = base_def
		self.maxhp = hp
		self.hp = hp
		self.death_function = death_function

	


	def move(self,dx,dy):


		tile_is_wall = (GAME.current_map[self.owner.x + dx][self.owner.y + dy].block_path == True)

		target = map_check_for_creature(self.owner.x + dx, self.owner.y + dy, self.owner)


		if target:
			self.attack(target)

		if not tile_is_wall and target is None:
			self.owner.x += dx
			self.owner.y += dy


	def attack(self, target):

		damage_delt = self.power - target.creature.defense

		game_message( self.name_instance + " attacks " + target.creature.name_instance + " for " + str(damage_delt) + 
			" damage!", constants.COLOR_WHITE)

		target.creature.take_damage(damage_delt)

	def take_damage(self, damage):
		self.hp -= damage
		game_message(self.name_instance + "'s health is " + str(self.hp) + "/" + str(self.maxhp), constants.COLOR_RED)

		if self.hp <= 0:
			if self.death_function is not None:
				self.death_function(self.owner)

	def heal(self, value):

		self.hp += value

		if self.hp > self.maxhp:
			self.hp = self.maxhp

	@property
	def power(self):

		total_power = self.base_atk

		if self.owner.container:
			object_bonuses = [obj.equipment.attack_bonus 
							  for obj in self.owner.container.equipped_items]

			for bonus in object_bonuses:
				if bonus:
					total_power += bonus

		return total_power

	@property
	def defense(self):

		total_defense = self.base_def

		if self.owner.container:
			object_bonuses = [obj.equipment.defense_bonus 
							  for obj in self.owner.container.equipped_items]

			for bonus in object_bonuses:
				if bonus:
					total_defense += bonus

		return total_defense

class com_Container:
	def __init__(self, volume = 10.0, inventory = []):
		self.inventory = inventory
		self.max_volume = volume

	

	
	@property
	def volume(self):
		return 0.0

	@property
	def equipped_items(self):

		list_of_equipped_items = [obj for obj in self.inventory 
								  if obj.equipment and obj.equipment.equipped]

		return list_of_equipped_items

	
class com_Item:
	def __init__(self, weight = 0.0, volume = 0.0, use_function = None,
		value = None):
		self.weight = weight
		self.volume = volume
		self.value = value
		self.use_function = use_function

	#Pick up this item
	def pick_up(self, actor):

		if actor.container:
			if actor.container.volume + self.volume > actor.container.max_volume:
				game_message("Not enough room to pick up")

			else:
				game_message("Picking up")
				actor.container.inventory.append(self.owner)
				GAME.current_objects.remove(self.owner)
				self.container = actor.container

	#Drop this item
	def drop(self, new_x, new_y):
		GAME.current_objects.append(self.owner)
		self.container.inventory.remove(self.owner)
		self.owner.x = new_x
		self.owner.y = new_y
		game_message("Item Dropped!") 

	#Use the item

	def use(self):

		if self.owner.equipment:

			self.owner.equipment.toggle_equip()
			return

		if self.use_function:
			result = self.use_function(self.container.owner, self.value)

			if result is not None:
				print("use_function failed")

			else:
				self.container.inventory.remove(self.owner)

class com_Equipment:

	def __init__(self, attack_bonus = None, defense_bonus = None, slot = None, has_grenade = False):

		self.attack_bonus = attack_bonus
		self.defense_bonus = defense_bonus
		self.slot = slot
		self.has_grenade = has_grenade
		self.equipped = False

	def toggle_equip(self):

		if self.equipped:
			self.unequip()
		else:
			self.equip()

	def equip(self):

		all_equipped_items = self.owner.item.container.equipped_items

		
		for item in all_equipped_items:
			if item.equipment.slot and (item.equipment.slot != self.slot):

				game_message("equipment slot is occupied", constants.COLOR_RED)
				return


		self.equipped = True

		game_message("item equipped")

	def unequip(self):

		self.equipped = False

		game_message("item unequipped")











class ai_Chase:



	def take_turn(self):

		monster = self.owner

		if libtcod.map_is_in_fov(FOV_MAP, monster.x, monster.y):

			if monster.distance_to(PLAYER) >= 2:
				self.owner.move_towards(PLAYER)


			elif PLAYER.creature.hp > 0:
				monster.creature.attack(PLAYER)








def death_monster(monster):

	game_message(monster.creature.name_instance + " is dead!", constants.COLOR_GREY)
	monster.creature = None
	monster.ai = None


def map_create():
	new_map=[[struc_Tile(False) for y in range(0,  constants.MAP_HEIGHT)] for x in range(0,constants.MAP_WIDTH) ]		

	new_map[10][10].block_path = True
	new_map[10][15].block_path = True
	for x in range(constants.MAP_WIDTH):
		new_map[x][0].block_path = True
		new_map[x][constants.MAP_HEIGHT-1].block_path = True
	for y in range(constants.MAP_HEIGHT):
		new_map[0][y].block_path = True
		new_map[constants.MAP_WIDTH-1][y].block_path = True


	map_make_fov(new_map)

	return new_map

def map_check_for_creature(x, y, exclude_object = None):

	target = None

	if exclude_object:

		for object in GAME.current_objects:
			if (object is not exclude_object and 
				object.x == x and
				object.y == y and 
				object.creature):

				target = object

			if target:
				return target

	else:

		for object in GAME.current_objects:
			if (object.x == x and
				object.y == y and 
				object.creature):

				target = object

			if target:
				return target

def map_check_for_wall(x, y):
	incoming_map[x][y].block_path


def map_make_fov(incoming_map):
	global FOV_MAP

	FOV_MAP = libtcod.map_new(constants.MAP_WIDTH, constants.MAP_HEIGHT)

	for y in range(constants.MAP_HEIGHT):
		for x in range(constants.MAP_WIDTH):
			libtcod.map_set_properties(FOV_MAP, x, y, 
				not incoming_map[x][y].block_path, not incoming_map[x][y].block_path)


def map_calculate_fov():
	global FOV_CALCULATE

	if FOV_CALCULATE:
		FOV_CALCULATE = False
		libtcod.map_compute_fov(FOV_MAP, PLAYER.x, PLAYER.y, constants.TORCH_RADIUS, constants.FOV_LIGHT_WALLS,
			constants.FOV_ALGO)

def map_objects_at_coords(coords_x, coords_y):
	
	object_options = [obj for obj in GAME.current_objects
						if obj.x == coords_x and obj.y == coords_y]

	return object_options

def map_find_line(coords1, coords2):

	x1, y1 = coords1

	x2, y2 = coords2

	libtcod.line_init(x1, y1, x2, y2)

	calc_x, calc_y = libtcod.line_step()

	coord_list = []

	if x1 == x2 and y1 == y2:
		return [(x1, y1)]

	while (not calc_x is None):

		coord_list.append((calc_x, calc_y))

		calc_x, calc_y = libtcod.line_step()

	return coord_list

def map_find_radius(coords, radius):

	center_x, center_y = coords

	tile_list = []

	start_x = (center_x - radius)
	end_x = (center_x + radius + 1)

	start_y = (center_y - radius)
	end_y = (center_y + radius + 1)

	for x in range(start_x, end_x):
		for y in range(start_y, end_y):
			tile_list.append((x, y))

	return tile_list			


def draw_game():
	global SURFACE_MAIN
	#clean the surface
	SURFACE_MAIN.fill(constants.COLOR_DEFAULT_BG)
	#draw the map
	draw_map(GAME.current_map)
	#draw all objects
	for obj in GAME.current_objects:
		obj.draw()

	draw_debug()
	draw_messages()

def draw_map(map_to_draw):
	for x in range(0,constants.MAP_WIDTH):
		for y in range(0,constants.MAP_HEIGHT):

			is_visible = libtcod.map_is_in_fov(FOV_MAP, x, y)


			if is_visible:

				map_to_draw[x][y].explored = True


				if map_to_draw[x][y].block_path == True:
					#draw wall
					SURFACE_MAIN.blit(ASSETS.S_WALL,(x*constants.CELL_WIDTH,y*constants.CELL_HEIGHT ))

				else:
					#draw floor
					SURFACE_MAIN.blit(ASSETS.S_FLOOR,(x*constants.CELL_WIDTH,y*constants.CELL_HEIGHT ))

			elif map_to_draw[x][y].explored:
				if map_to_draw[x][y].block_path == True:
					#draw wall
					SURFACE_MAIN.blit(ASSETS.S_WALLEXPLORED,(x*constants.CELL_WIDTH,y*constants.CELL_HEIGHT ))

				else:
					#draw floor
					SURFACE_MAIN.blit(ASSETS.S_FLOOREXPLORED,(x*constants.CELL_WIDTH,y*constants.CELL_HEIGHT ))

def draw_debug():

	draw_text(SURFACE_MAIN, "fps: " + str(int(CLOCK.get_fps())), (0, 0), constants.COLOR_WHITE, constants.COLOR_BLACK)

def draw_messages():

	if len(GAME.message_history) <= constants.NUM_MESSAGES:
		to_draw = GAME.message_history
	else:
		to_draw = GAME.message_history[-constants.NUM_MESSAGES:]

	text_height = helper_text_height(ASSETS.FONT_MESSAGE_TEXT)

	start_y = constants.MAP_HEIGHT*constants.CELL_HEIGHT - (constants.NUM_MESSAGES * text_height) - 10

	i = 0

	for message, color in to_draw:

		draw_text(SURFACE_MAIN, message, (0, start_y + (i * text_height)), color, constants.COLOR_BLACK)

		i += 1


def draw_text(display_surface, text_to_display, T_coords, text_color, back_color = None, center = False):
	#displays text on referenced surface
	text_surf, text_rect = helper_text_objects(text_to_display, text_color, back_color)
	if not center:
		text_rect.topleft = T_coords
	else:
		text_rect.center = T_coords

	display_surface.blit(text_surf, text_rect)


def draw_tile_rect(coords, tile_color = None, tile_alpha = None, mark = None):

	x, y = coords
	if tile_color:
		local_color = tile_color
	else:
		local_color = constants.COLOR_WHITE

	if tile_alpha:
		local_alpha = tile_alpha
	else:
		local_alpha = 200

	new_x = x * constants.CELL_WIDTH
	new_y = y * constants.CELL_WIDTH

	new_surface = pygame.Surface((constants.CELL_WIDTH, constants.CELL_HEIGHT))

	new_surface.fill(local_color)

	new_surface.set_alpha(local_alpha)

	if mark:
		draw_text(new_surface, mark, 
				  T_coords = (constants.CELL_WIDTH / 2, constants.CELL_HEIGHT / 2),
				  text_color = constants.COLOR_BLACK, center = True)

	SURFACE_MAIN.blit(new_surface, (new_x, new_y))









def helper_text_objects(incoming_text, incoming_color, incoming_bg):
	
	if incoming_bg:
		Text_surface = ASSETS.FONT_DEBUG_MESSAGE.render(incoming_text, False, incoming_color, incoming_bg)

	else:
		Text_surface = ASSETS.FONT_DEBUG_MESSAGE.render(incoming_text, False, incoming_color)

	return Text_surface, Text_surface.get_rect()

def helper_text_height(font):

	font_object = font.render("a", False, (0, 0, 0))
	font_rect = font_object.get_rect()

	return font_rect.height

def helper_text_width(font):

	font_object = font.render("a", False, (0, 0, 0))
	font_rect = font_object.get_rect()

	return font_rect.width








def cast_grenade():

	damage = 5 
	local_radius = 1
	max_r = 4
	player_location = (PLAYER.x, PLAYER.y)

	point_selected = menu_tile_select(coords_origin = player_location,
									  max_range = max_r, 
									  penetrate_walls = False, 
									  pierce_creature = False,
									  radius = local_radius)

	if point_selected:

		tiles_to_damage = map_find_radius(point_selected, local_radius)

		creature_hit = False

		for (x, y) in tiles_to_damage:
			creature_to_damage = map_check_for_creature(x, y)

			if creature_to_damage:
				creature_to_damage.creature.take_damage(damage)

				if creature_to_damage is not PLAYER:
					creature_hit = True

		if creature_hit:
			game_message("The enemy howls out in pain.", constants.COLOR_RED)




def menu_pause():


	menu_close = False

	window_width = constants.MAP_WIDTH*constants.CELL_WIDTH
	window_height = constants.MAP_HEIGHT*constants.CELL_HEIGHT

	menu_text = "PAUSED"
	menu_font = ASSETS.FONT_DEBUG_MESSAGE

	text_height = helper_text_height(menu_font)
	text_width = len(menu_text) * helper_text_width(menu_font)

	while not menu_close:

		events_list = pygame.event.get()

		for event in events_list:

			if event.type == pygame.KEYDOWN:

				if event.key == pygame.K_p:
					menu_close = True
				
		draw_text(SURFACE_MAIN, menu_text,
			((window_width / 2) - (text_width / 2), (window_height / 2) - (text_height / 2)),
			constants.COLOR_WHITE, constants.COLOR_BLACK)

		CLOCK.tick(constants.GAME_FPS)

		pygame.display.flip()

def menu_inventory():

	menu_close = False

	window_width = constants.MAP_WIDTH*constants.CELL_WIDTH
	window_height = constants.MAP_HEIGHT*constants.CELL_HEIGHT

	menu_width = 200
	menu_height = 200
	menu_x = (window_width / 2) - (menu_width / 2)
	menu_y = (window_height / 2) - (menu_height / 2)


	menu_text_font = ASSETS.FONT_MESSAGE_TEXT

	menu_text_height = helper_text_height(menu_text_font)

	menu_text_color = constants.COLOR_WHITE

	local_inventory_surface = pygame.Surface((menu_width, menu_height))

	while not menu_close:

		#Clear the menu
		local_inventory_surface.fill(constants.COLOR_BLACK)

		#Register Changes

		print_list = [obj.display_name for obj in PLAYER.container.inventory]

		events_list = pygame.event.get()
		mouse_x, mouse_y = pygame.mouse.get_pos()

		mouse_x_rel = mouse_x - menu_x
		mouse_y_rel = mouse_y - menu_y

		mouse_in_window = (mouse_x_rel > 0 and 
						   mouse_y_rel > 0 and
						   mouse_x_rel < menu_width and
						   mouse_y_rel < menu_height)

		mouse_line_selection = mouse_y_rel / menu_text_height

		for event in events_list:

			if event.type == pygame.KEYDOWN:

				if event.key == pygame.K_i:
					menu_close = True
			if event.type == pygame.MOUSEBUTTONDOWN:

				if event.button == 1:

					if (mouse_in_window and 
						mouse_line_selection <= len(print_list) - 1):

						PLAYER.container.inventory[mouse_line_selection].item.use()

		#Draw the list
		for line, (name) in enumerate(print_list):

			if line == mouse_line_selection and mouse_in_window:
				draw_text(local_inventory_surface,
				 	 	  name,
				 	 	  (0, 0 + (line * menu_text_height)), 
				 	 	  menu_text_color, constants.COLOR_GREY)
			else:
				draw_text(local_inventory_surface,
				 	 	  name,
				 	 	  (0, 0 + (line * menu_text_height)), 
				 	 	  menu_text_color)


		draw_game()

		#Display Menu
		SURFACE_MAIN.blit(local_inventory_surface, (menu_x, menu_y))


		CLOCK.tick(constants.GAME_FPS)

		pygame.display.update()


def menu_tile_select(coords_origin = None, max_range = None, penetrate_walls = True,
					 pierce_creature = True, radius = None):

	menu_close = False

	while not menu_close:

		#Get mouse position
		mouse_x, mouse_y = pygame.mouse.get_pos()
		#Get button clicks
		events_list = pygame.event.get()

		#Mouse map selection
		map_coord_x = mouse_x / constants.CELL_WIDTH
		map_coord_y = mouse_y / constants.CELL_HEIGHT

		valid_tiles = []


		if coords_origin:
			full_list_tiles = map_find_line(coords_origin, (map_coord_x, map_coord_y))

			for i, (x, y) in enumerate(full_list_tiles):

				valid_tiles.append((x, y))

				if max_range and i == max_range - 1:
					break

				if not penetrate_walls and GAME.current_map[x][y].block_path:
					break

				if not pierce_creature and map_check_for_creature(x, y):
					break


		else:
			valid_tiles = [(map_coord_x, map_coord_y)]

		for event in events_list:

			if event.type == pygame.KEYDOWN:

				if event.key == pygame.K_i:
					menu_close = True

			if event.type == pygame.MOUSEBUTTONDOWN:

				if event.button == 1:
					#Will turn to return
					return (valid_tiles[-1])

		#Draw game
		draw_game()

		#Draw rectangle at mouse position
		for (tile_x, tile_y) in valid_tiles:

			if (tile_x, tile_y) == valid_tiles[-1]:
				draw_tile_rect(coords = (tile_x, tile_y), mark = 'X')
			else:
				draw_tile_rect(coords = (tile_x, tile_y))

		if radius:
			area_effect = map_find_radius(valid_tiles[-1], radius)

			for (tile_x, tile_y) in area_effect:
				draw_tile_rect(coords = (tile_x, tile_y), 
							   tile_color = constants.COLOR_RED,
							   tile_alpha = 150)

		pygame.display.flip()
		CLOCK.tick(constants.GAME_FPS)

		








def game_main_loop(): 
	game_quit = False


	player_action = "no-action"
	while not game_quit:


		#handle player input
		player_action = game_handle_keys()

		map_calculate_fov()

		if player_action == "QUIT":
			game_quit = True

		elif player_action != "no-action":
			for obj in GAME.current_objects:
				if obj.ai:
					obj.ai.take_turn()	
		#draw the game
		draw_game()

		pygame.display.flip()
		CLOCK.tick(constants.GAME_FPS)

	#quit the game
	pygame.quit()
	exit()


def game_initialize():
	'''Initializes the main window and pygame'''
	global SURFACE_MAIN, GAME, CLOCK, FOV_CALCULATE, PLAYER, ENEMY, ASSETS


	#initialize pygame
	pygame.init()

	pygame.key.set_repeat(200, 70)

	SURFACE_MAIN = pygame.display.set_mode((constants.MAP_WIDTH*constants.CELL_WIDTH, 
											constants.MAP_HEIGHT*constants.CELL_HEIGHT))

	GAME = obj_Game()

	CLOCK = pygame.time.Clock()

	FOV_CALCULATE = True

	ASSETS = struc_Assets()

	container_com1 = com_Container()
	creature_com1 = com_Creature("martin", base_atk = 4)
	PLAYER = obj_Actor(1, 1, "gangster", 
					   ASSETS.A_PLAYER,
					   animation_speed = 1.0,
					   creature = creature_com1,
					   container = container_com1)


	item_com1 = com_Item(value = 4, use_function = cast_heal)
	creature_com2 = com_Creature("jack", death_function = death_monster)
	ai_com1 = ai_Chase()
	ENEMY = obj_Actor (15,15, "thug", ASSETS.A_ENEMY, animation_speed = 1.0, 
		creature = creature_com2, ai = ai_com1, item = item_com1)

	item_com2 = com_Item(value = 5, use_function = cast_heal)
	ai_com2 = ai_Chase()
	creature_com3 = com_Creature("bob", death_function = death_monster)
	ENEMY2 = obj_Actor (14,15, "bastard", ASSETS.A_ENEMY, animation_speed = 1.0, 
		creature = creature_com3, ai = ai_com2, item = item_com2)

	equipment_com1 = com_Equipment(attack_bonus = 2)
	PISTOL = obj_Actor(2, 2, "pistol", ASSETS.S_PISTOL, 
					  equipment = equipment_com1)

	equipment_com2 = com_Equipment(has_grenade = True)
	GRENADE = obj_Actor(2, 3, "shield", ASSETS.S_GRENADE, 
					  equipment = equipment_com2)


	equipment_com3 = com_Equipment(defense_bonus = 2)
	KEVLAR = obj_Actor(2, 4, "Short-sword", ASSETS.S_KEVLAR, 
					  equipment = equipment_com3)

	GAME.current_objects = [PLAYER, ENEMY, ENEMY2, PISTOL, GRENADE, KEVLAR]

def game_handle_keys():
	global FOV_CALCULATE
	#get player input
	events_list = pygame.event.get()
		#process input
	for event in events_list:
		if event.type == pygame.QUIT:
			return "QUIT"

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				PLAYER.creature.move(0, -1)
				FOV_CALCULATE = True
				return "player-moved"
			if event.key == pygame.K_DOWN:
				PLAYER.creature.move(0, 1)
				FOV_CALCULATE = True
				return "player-moved"
			if event.key == pygame.K_LEFT:
				PLAYER.creature.move(-1,0)
				FOV_CALCULATE = True
				return "player-moved"
			if event.key == pygame.K_RIGHT:
				PLAYER.creature.move(1,0)
				FOV_CALCULATE = True
				return "player-moved"

			if event.key == pygame.K_g:
				objects_at_player = map_objects_at_coords(PLAYER.x, PLAYER.y)

				for obj in objects_at_player:
					if obj.item:
						obj.item.pick_up(PLAYER)

			if event.key == pygame.K_d:
				if len(PLAYER.container.inventory) > 0:
					PLAYER.container.inventory[-1].item.drop(PLAYER.x, PLAYER.y)

			if event.key == pygame.K_p:
				menu_pause()

			if event.key == pygame.K_i:
				menu_inventory()

			if event.key == pygame.K_l:
				if has_grenade == True:
					cast_grenade()


	return "no-action"

def game_message(game_msg, msg_color = constants.COLOR_GREY):

	GAME.message_history.append((game_msg, msg_color))





game_initialize()
game_main_loop()