from kabanos_engine import engine

import pygame as pg
from os import path
import time

# overall init
pg.init()

global WIDTH, HEIGHT, TILESIZE, FPS, OFFSET, DEBUG
WIDTH = 1280 
HEIGHT = 720
TILESIZE = 64
FPS = 60
OFFSET = [WIDTH/2,HEIGHT/2]
DEBUG = False

clock = pg.time.Clock()

screen = pg.display.set_mode((WIDTH,HEIGHT))
pg.display.set_caption("Gameplay tests")

allSpriteGroups = []
allSprites = pg.sprite.Group()
allTiles = pg.sprite.Group()
playerGroup = pg.sprite.Group()

allSpriteGroups.append(playerGroup)
allSpriteGroups.append(allTiles)
allSpriteGroups.append(allSprites)


d1 = engine.DebugText(0, "OFFSET: ", (255,255,255), (0,0))

# Texture loading
img_dir = path.join(path.dirname(__file__),"textures")
lvl_dir = path.join(path.dirname(__file__),"levels")

player_textures = [] # N, E, S, W <- this order needs to be followed
tile_textures = []

for texture in range(8):
    player_textures.append(pg.transform.scale(pg.image.load(path.join(img_dir,"player_debug{0}.png".format(texture+1))).convert_alpha(),(int(TILESIZE/2),int(TILESIZE/2))))

tile_textures.append(pg.transform.scale(pg.image.load(path.join(img_dir,"missing_texture.png")).convert_alpha(),(TILESIZE,TILESIZE)))
tile_textures.append(pg.transform.scale(pg.image.load(path.join(img_dir,"placeholder64.png")).convert_alpha(),(TILESIZE,TILESIZE)))

p = engine.Player(WIDTH/2, HEIGHT/2, player_textures, 5)
playerGroup.add(p)

camera = engine.Camera(p, WIDTH, HEIGHT)

#map = engine.Map(lvl_dir, "1", tile_textures)
#allTiles = map.place_tiles(allTiles, OFFSET)

map = engine.Map(lvl_dir, tile_textures)
cave_generator = engine.Cave_Generator(50,50,60,3,4,15)
generated_level, starting_point = cave_generator.generate_cave()
map.set_level(map.replace_tiles_from_generator(generated_level, TILESIZE))

print(starting_point[0], starting_point[1])

OFFSET[0] -= starting_point[1] * TILESIZE + 32
OFFSET[1] -= starting_point[0] * TILESIZE + 32

allTiles = map.place_tiles(allTiles, OFFSET)

def game():
    global WIDTH, HEIGHT, TILESIZE, FPS, OFFSET, DEBUG
    while True:
        mouse_pos = pg.mouse.get_pos()
        screen.fill((0,0,0))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_1:
                    DEBUG = not DEBUG

        for sprite in allSprites:
            sprite.update(OFFSET)

        camera.mouse_update(OFFSET, [allSprites, allTiles], mouse_pos)
        OFFSET = camera.update(OFFSET, [allSprites, allTiles], playerGroup, screen)

        #for spriteGroup in allSpriteGroups:
        #    spriteGroup.draw(screen)

        if DEBUG:
            d1.update(screen, OFFSET)
            camera.draw_debug(screen)
            for spriteGroup in allSpriteGroups:
                for sprite in spriteGroup:
                    sprite.draw_debug(screen)
        pg.display.flip()
        clock.tick(60)

game()