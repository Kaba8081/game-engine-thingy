# Kaba's engine for simple games made in python using pygame
# github: https://github.com/Kaba8081/game-engine-thingy
# Not much but it's honest work

from ast import literal_eval
from os import path
import random
import pygame
import time

class Text:
    def __init__(self, pos_x, pos_y, text, font, color):
        pass

class Color_Button:
    def __init__(self, pos_x, pos_y, width, height, color, text, text_x, text_y, value, font):
        self.pos_x, self.pos_y = pos_x, pos_y
        self.label_x, self.label_y = text_x, text_y
        self.width, self.height = width, height
        self.color = color
        self.text = text
        self.value = value
        self.font = font

        self.label = self.font.render(str(self.text),1,(255,255,255))
    def update(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.pos_x, self.pos_y, self.width, self.height))
        screen.blit(self.label, (self.pos_x + self.label_x, self.pos_y + self.label_y))

        keys = pygame.mouse.get_pressed()
        if keys[0]:
            pos = pygame.mouse.get_pos()
            if pos[0] - self.pos_x >= 0 and pos[0] - self.pos_x <= self.width and pos[1] - self.pos_y >= 0 and pos[1] - self.pos_y <= self.height:
                return self.value
            else:
                return 0
        else:
            return 0

class Button(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, *texture):
        if not texture:
            pass
        else:
            pygame.sprite.Sprite.__init__(self)
            self.image = texture
            
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = pos_x, pos_y
            
class Tile(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, texture_id, textures, OFFSET, tilesize):
        pygame.sprite.Sprite.__init__(self)
        try:
            self.image = textures[texture_id]
        except:
            self.image = textures[0]

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos_x + OFFSET[0],pos_y + OFFSET[1]
        self.pos = (pos_x, pos_y)
        self.collidable = True
        self.tilesize = tilesize

    def update(self, OFFSET):
        self.rect.x, self.rect.y = self.pos[0] + OFFSET[0],self.pos[1] + OFFSET[1]

    def draw_debug(self, screen):
        pygame.draw.line(screen, (0,0,255), (self.rect.x, self.rect.y), (self.rect.x + self.tilesize, self.rect.y))
        pygame.draw.line(screen, (0,0,255), (self.rect.x + self.tilesize, self.rect.y), (self.rect.x + self.tilesize, self.rect.y + self.tilesize))
        pygame.draw.line(screen, (0,0,255), (self.rect.x + self.tilesize, self.rect.y + self.tilesize), (self.rect.x, self.rect.y + self.tilesize))
        pygame.draw.line(screen, (0,0,255), (self.rect.x, self.rect.y + self.tilesize), (self.rect.x, self.rect.y))

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, textures, movement_speed = 3):
        pygame.sprite.Sprite.__init__(self)
        self.textures = textures
        self.image = self.textures[0]

        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = pos_x, pos_y

        self.pos = [pos_x, pos_y]

        self.speed = movement_speed
        self.tilesize = 32
        self.weapon = None
        self.pos_change = [0,0]
        self.total_change = [0,0]

        self.debug0 = DebugText(0,"player_center: ", (255,255,255), (0,48))
        self.debug1 = DebugText(0,"player_change: ", (255,255,255), (0,60))
    
    def movement(self, SpriteGroups, OFFSET):
        self.rect.centerx, self.rect.centery = self.pos[0], self.pos[1]# - OFFSET[0], self.pos[1] - OFFSET[1]
        keys = pygame.key.get_pressed()

        pos_change = [0, 0]

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            pos_change[0] = -self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            pos_change[0] = self.speed

        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            pos_change[1] = self.speed
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            pos_change[1] = -self.speed

        if self.colliding_on_x(SpriteGroups, pos_change):
            pos_change[0] = 0
        
        if self.colliding_on_y(SpriteGroups, pos_change):
            pos_change[1] = 0

        self.total_change[0] += pos_change[0]
        self.total_change[1] += pos_change[1]

        return pos_change

    def animation(self, pos_change):
        if pos_change[0] == 0: # only moving on y
            if pos_change[1] > 0: # down
                self.image = self.textures[0]
            elif pos_change[1] < 0 : # up
                self.image = self.textures[4]
        else:
            if pos_change[0] > 0: # right
                if pos_change[1] > 0: # down
                    self.image = self.textures[7]
                elif pos_change[1] < 0 : # up
                    self.image = self.textures[5]
                elif pos_change[1] == 0:
                    self.image = self.textures[6]

            elif pos_change[0] < 0: # left
                if pos_change[1] > 0: # down
                    self.image = self.textures[1]
                elif pos_change[1] < 0 : # up
                    self.image = self.textures[3]
                elif pos_change[1] == 0:
                    self.image = self.textures[2]
                
    def colliding_on_x(self, SpriteGroups, pos_change):
        for spriteGroup in SpriteGroups:
            for sprite in spriteGroup:
                if sprite.collidable:
                    if abs(self.rect.centery - sprite.rect.centery) <= sprite.tilesize/2 + self.tilesize/2:
                        if abs(self.rect.centerx + pos_change[0] - sprite.rect.centerx) <= sprite.tilesize/2 + self.tilesize/2:
                            return True
        return False
    def colliding_on_y(self, spriteGroups, pos_change):
        for spriteGroup in spriteGroups:
            for sprite in spriteGroup:
                if sprite.collidable:
                    if abs(self.rect.centerx - sprite.rect.centerx) <= sprite.tilesize/2 + self.tilesize/2:
                        if abs(self.rect.centery + pos_change[1] - sprite.rect.centery) <= sprite.tilesize/2 + self.tilesize/2:
                            return True
        return False

    def assign_weapon(self, weapon):
        self.weapon = weapon

    def shoot(self, bulletsGroup, mouse_pos, camera_offset):
        if self.weapon != None:
            self.weapon.shoot(bulletsGroup, mouse_pos, camera_offset)

    def draw_debug(self, screen):
        pygame.draw.line(screen, (0,255,0), (self.rect.x, self.rect.y), (self.rect.x + self.tilesize, self.rect.y))
        pygame.draw.line(screen, (0,255,0), (self.rect.x + self.tilesize, self.rect.y), (self.rect.x + self.tilesize, self.rect.y + self.tilesize))
        pygame.draw.line(screen, (0,255,0), (self.rect.x + self.tilesize, self.rect.y + self.tilesize), (self.rect.x, self.rect.y + self.tilesize))
        pygame.draw.line(screen, (0,255,0), (self.rect.x, self.rect.y + self.tilesize), (self.rect.x, self.rect.y))

        self.debug0.update(screen, (self.rect.centerx, self.rect.centery))
        self.debug1.update(screen, (self.total_change[0], self.total_change[1]))

class Camera:
    def __init__(self, player, width, height):
        self.player = player
        self.camera_offset = [0,0]

        self.left = (width/8)*2
        self.right = (width/8)*6
        self.top = (height/8)*2
        self.bottom = (height/8)*6

        self.WIDTH = width
        self.HEIGHT = height

        self.centerx = width/2
        self.centery = height/2

        self.debug0 = DebugText(0,"camera_offset: ", (255,255,255), (0,12))
        self.debug1 = DebugText(0,"pos_change: ", (255,255,255), (0,24))

    def update(self, OFFSET, SpriteGroups, playerGroup, screen):
        self.player.pos_change = self.player.movement(SpriteGroups, OFFSET)

        value = 0,0 # self.player_at_edge(pos_change)

        if value[0] != 0:
            if value[0] == 1:
                OFFSET[0] += self.player.speed
                self.player.pos[0] += self.player.speed
            else: 
                OFFSET[0] += -self.player.speed
                self.player.pos[0] += -self.player.speed
        else:
            self.player.pos[0] += self.player.pos_change[0]
        
        if value[1] != 0:
            if value[1] == 1:
                OFFSET[1] += self.player.speed
                self.player.pos[1] += self.player.speed
            else:
                OFFSET[1] += -self.player.speed
                self.player.pos[1] += -self.player.speed
        else:
            self.player.pos[1] += self.player.pos_change[1]

        self.player.animation(self.player.pos_change)

        self.player.rect.x += self.camera_offset[0]
        self.player.rect.y += self.camera_offset[1]

        for SpriteGroup in SpriteGroups:
            for sprite in SpriteGroup:
                sprite.rect.x += self.camera_offset[0]
                sprite.rect.y += self.camera_offset[1]
        
        SpriteGroups.append(playerGroup)

        for SpriteGroup in SpriteGroups:
            SpriteGroup.draw(screen)

        return OFFSET
    
    def mouse_update(self, OFFSET, mouse_pos):
        self.camera_offset[0] = -mouse_pos[0] - self.player.pos[0] + self.centerx * 2
        self.camera_offset[1] = -mouse_pos[1] - self.player.pos[1] + self.centery * 2

    def player_at_edge(self, pos_change): # 0 - None; 1 - left / top; 2 - right / bottom]
        if self.player.rect.left + pos_change[0] < self.left:
            if self.player.rect.top + pos_change[1] < self.top:
                pos_change[0] = 0 
                pos_change[1] = 0
                return 1,1
            elif self.player.rect.bottom + pos_change[1] > self.bottom:
                pos_change[0] = 0 
                pos_change[1] = 0
                return 1,2
            else:
                pos_change[0] = 0 
                return 1,0
        elif self.player.rect.right + pos_change[0]> self.right:
            if self.player.rect.top + pos_change[1] < self.top:
                pos_change[0] = 0 
                pos_change[1] = 0
                return 2,1
            elif self.player.rect.bottom + pos_change[1] > self.bottom:
                pos_change[0] = 0 
                pos_change[1] = 0
                return 2,2
            else:
                pos_change[0] = 0 
                return 2,0   
        else:
            if self.player.rect.top + pos_change[1] < self.top:
                pos_change[1] = 0
                return 0,1
            elif self.player.rect.bottom + pos_change[1] > self.bottom:
                pos_change[1] = 0
                return 0,2
            else:
                return 0,0   

    def draw_debug(self, screen):
        pygame.draw.line(screen, (255,0,0), (self.left + (self.player.rect.centerx - self.centerx), self.top + (self.player.rect.centery - self.centery)), (self.right + (self.player.rect.centerx  - self.centerx), self.top + (self.player.rect.centery - self.centery)))
        pygame.draw.line(screen, (255,0,0), (self.left + (self.player.rect.centerx  - self.centerx), self.top + (self.player.rect.centery - self.centery)), (self.left + (self.player.rect.centerx - self.centerx), self.bottom + (self.player.rect.centery - self.centery)))
        pygame.draw.line(screen, (255,0,0), (self.left + (self.player.rect.centerx - self.centerx), self.bottom + (self.player.rect.centery - self.centery)), (self.right + (self.player.rect.centerx - self.centerx), self.bottom + (self.player.rect.centery - self.centery)))
        pygame.draw.line(screen, (255,0,0), (self.right + (self.player.rect.centerx  - self.centerx), self.bottom + (self.player.rect.centery - self.centery)), (self.right + (self.player.rect.centerx - self.centerx), self.top + (self.player.rect.centery - self.centery)))

        self.debug0.update(screen,self.camera_offset)

class Weapon(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, weaponID, textures, BulletTexture, mounted_to_player, player=None):
        pygame.sprite.Sprite.__init__(self)
        self.weaponID = weaponID
        self.textures = textures
        self.image = self.textures[0]

        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = pos_x, pos_y

        self.pos = [pos_x, pos_y]

        self.mounted_to_player = mounted_to_player
        self.player = player
        self.pause = 0
        self.maxPause = 0
        self.BulletTexture = BulletTexture
        self.collidable = False

        if self.weaponID == 0:
            self.maxPause = 20
            
        self.debug0 = DebugText(0,"weapon_center: ", (255,255,255), (0,36))
        self.debug = debug_placeholder(0,0)

    def update(self):
        if self.mounted_to_player:
            self.rect.x = self.player.rect.centerx 
            self.rect.y = self.player.rect.centery

        if self.pause > 0:
            self.pause -= 1

    def shoot(self, bulletsGroup, mouse_pos, camera_offset):
        if self.pause == 0:
            if self.weaponID == 0:
                    self.pause = self.maxPause
                    dx = -camera_offset[0] - self.player.total_change[0] + random.randint(-8,8)
                    dy = -camera_offset[1] - self.player.total_change[1] + random.randint(-8,8)
                    if abs(dx) > 0 or abs(dy) > 0 :
                        b = Bullet(self.rect.centerx - camera_offset[0], self.rect.centery - camera_offset[1], dx, dy, random.randint(7,8), 0, self.BulletTexture)
                        bulletsGroup.add(b)

    def draw_debug(self, screen):
        pygame.draw.line(screen, (52, 235, 158), (self.rect.left, self.rect.top), (self.rect.right, self.rect.top))
        pygame.draw.line(screen, (52, 235, 158), (self.rect.left, self.rect.top), (self.rect.left, self.rect.bottom))
        pygame.draw.line(screen, (52, 235, 158), (self.rect.left, self.rect.bottom), (self.rect.right, self.rect.bottom))
        pygame.draw.line(screen, (52, 235, 158), (self.rect.right, self.rect.bottom), (self.rect.right, self.rect.top))
        pygame.draw.line(screen, (52, 235, 158), (self.rect.left, self.rect.top), (self.rect.right, self.rect.bottom))
        pygame.draw.line(screen, (52, 235, 158), (self.rect.left, self.rect.bottom), (self.rect.right, self.rect.top))

        self.debug0.update(screen, (self.rect.centerx, self.rect.centery))

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy, speed, WeaponId, texture):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        if WeaponId == 0:
            self.image = texture
            self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.pos = pygame.math.Vector2(x, y)
        self.dir = pygame.math.Vector2(dx, dy).normalize()
        self.collidable = False

    def update(self, player_change):
        self.pos += self.dir * self.speed
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def draw_debug(self, screen):
        pygame.draw.line(screen, (255,102,102), (self.rect.left, self.rect.top), (self.rect.right, self.rect.top))
        pygame.draw.line(screen, (255,102,102), (self.rect.left, self.rect.top), (self.rect.left, self.rect.bottom))
        pygame.draw.line(screen, (255,102,102), (self.rect.left, self.rect.bottom), (self.rect.right, self.rect.bottom))
        pygame.draw.line(screen, (255,102,102), (self.rect.right, self.rect.bottom), (self.rect.right, self.rect.top))

class DebugText:
    def __init__(self, fontID, text, color, position):
        self.text = text
        self.color = color
        self.pos = position
        self.font = None

        if fontID == 0:
            self.font = pygame.font.SysFont("Arial", 10,bold=False,italic=False)
        elif fontID == 1:
            self.font = pygame.font.SysFont("Arial", 15,bold=False,italic=False)

        if self.font != None:
            self.label = self.font.render(str(self.text), 1, self.color)

    def update(self, screen, value):
        if self.font != None:
            self.label = self.font.render(str(self.text) + str(value), 1, self.color)
            screen.blit(self.label, self.pos)
        
class Map:
    def __init__(self, levels_directory, tile_textures):
        self.directory = levels_directory
        self.tile_textures = tile_textures
        self.level = [] 

    def place_tiles(self, allTiles, OFFSET):
        for tile_data in self.level:
                t = Tile(tile_data[0], tile_data[1], tile_data[2], self.tile_textures, OFFSET, 64)
                allTiles.add(t)

        return allTiles

    def replace_tiles_from_generator(self, map, TILESIZE):
        newMap = []
        for indexx, x in enumerate(map):
            for indexy, y in enumerate(x):
                if y == 1:
                    pos_x, pos_y = indexx * TILESIZE, indexy * TILESIZE
                    value = 1
                    emptyList = []
                    emptyList.append(pos_y)
                    emptyList.append(pos_x)
                    emptyList.append(value)
                    newMap.append(emptyList)
        return newMap

    def load_level(self, level_name):
        level = []

        with open(path.join(self.directory, level_name), "rb") as file:
            level = literal_eval(file.read().decode("utf-8"))

        return level
    
    def set_level(self, new_level):
        self.level = new_level

class Map_editor:
    def __init__(self, levels_directory):
        self.levels_directory = levels_directory
    
    def save_level(self, level, level_name):
        with open(path.join(self.levels_directory, level_name), "wb") as file:
            file.write(level)

    def load_level(self, level_name):
        with open(path.join(self.levels_directory, level_name), "wb") as file:
            return literal_eval(file.read().decode("utf-8"))

class Cave_Generator:
    def __init__(self, width, height, BirthChance, Death_limit, BirthLimit, NumberOfSteps):
        self.width, self.height = width, height
        self.birth_chance = BirthChance
        self.birth_limit = BirthLimit
        self.death_limit = Death_limit
        self.number_of_steps = NumberOfSteps

    def create_map(self):
        map = []
        
        for y in range(self.height):
            empty_list = []
            for x in range(self.width):
                empty_list.append(False)
            map.append(empty_list)
        
        for index_y, y in enumerate(map):
            for index_x, x in enumerate(map[index_y]):
                if self.birth_chance < random.randint(0,100):
                    map[index_y][index_x] = True

        return map

    def count_alive_neighbours(self, x, y, oldMap):
        count = 0

        for i in range(3):
            for j in range(3):
                neighbour_x = (x-1) + i
                neighbour_y = (y-1) + j

                if i == 1 and j == 1:
                    pass
                elif neighbour_x < 0 or neighbour_y < 0 or neighbour_x >= self.width or neighbour_y >= self.height:    
                    count += 1
                elif oldMap[neighbour_y][neighbour_x]:
                    count += 1
        
        return count

    def do_simulation_step(self, oldMap):
        newMap = []

        for y in range(self.height):
            empty_list = []
            for x in range(self.width):
                empty_list.append(False)
            newMap.append(empty_list)

        for index_y, y in enumerate(oldMap):
            for index_x, x in enumerate(y):
                nbs = self.count_alive_neighbours(index_x, index_y, oldMap)
                
                if oldMap[index_y][index_x]:
                    if nbs < self.death_limit:
                        newMap[index_y][index_x] = False
                    else: 
                        newMap[index_y][index_x] = True
                else: 
                    if nbs > self.birth_limit:
                        newMap[index_y][index_x] = True
                    else:
                        newMap[index_y][index_x] = False
        
        return newMap

    def replace_values(self, oldMap):
        newMap = []

        for y in range(self.height):
            empty_list = []
            for x in range(self.width):
                empty_list.append(False)
            newMap.append(empty_list)

        for index_y, y in enumerate(oldMap):
            for index_x, x in enumerate(y):
                if oldMap[index_y][index_x]:
                    newMap[index_y][index_x] = 1
                else:
                    newMap[index_y][index_x] = 0
        return newMap

    def make_borders(self, oldMap):
        newMap = oldMap
        for index_y, y in enumerate(oldMap):
            for index_x,x in enumerate(y):
                if index_x == 0 or index_y == 0:
                    newMap[index_y][index_x] = 1
                elif index_x == self.width-1 or index_y == self.height-1:
                    newMap[index_y][index_x] = 1
        return newMap

    def pick_starting_point(self, map):
        while True:
            for indexy,y in enumerate(map):
                for indexx,x in enumerate(y):
                    if x == 0:
                        return indexy, indexx

    def list_rooms(self,map):
        pass

    def connect_rooms(self,map):
        pass

    def generate_cave(self):
        map = self.create_map()

        for i in range(self.number_of_steps):
            map = self.do_simulation_step(map)

        map = self.make_borders(map)
        map = self.replace_values(map)
        starting_point = self.pick_starting_point(map)

        return map, starting_point

class debug_placeholder:
    def __init__(self, pos_x, pos_y):
        self.image = pygame.Surface((5,5))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos_x, pos_y
    def update(self, pos_x, pos_y, screen):
        self.rect.x, self.rect.y = pos_x, pos_y
        pygame.draw.rect(screen, (255,0,0), self.rect)
