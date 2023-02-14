import pygame as pg
import sys
import os
import math
from collections import deque
from random import randint, random


RES = WIGHT, HEIGHT = 1550, 800
FPS = 0
HALF_WIGHT = WIGHT // 2
HALF_HEIGHT = HEIGHT // 2

PLAYER_POS = 1.5, 15.5
PLAYER_ANGLE = 0
PLAYER_SPEED = 0.004
PLAYER_ROT_SPEED = 0.002
PLAYER_SIZE_SCALE = 60
PLAYER_MAX_HEALTH = 100
PLAYER_SCORE = 50

MOUSE_SENSITIVITY = 0.0003
MOUSE_MAX_REL = 20
MOUSE_BORDER_LEFT = 100
MOUSE_BORDER_RIGHT = WIGHT - MOUSE_BORDER_LEFT

FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = WIGHT // 2
HALF_NUM_RAYS = NUM_RAYS // 2
DELTA_ANGLE = FOV / NUM_RAYS
MAX_DEPTH = 20

SCREEN_DIST = HALF_WIGHT / math.tan(HALF_FOV)
SCALE = WIGHT // NUM_RAYS

TEXTURE_SIZE = 256
HALF_TEXTURE_SIZE = TEXTURE_SIZE // 2

FLOOR_COLOR = (30, 30, 30)


class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)
        self.new_game()

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.object_render = ObjectRender(self)
        self.raycasting = Raycasting(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.pathfinding = Pathfinding(self)
        pg.mixer.music.play(-1)

    def update(self):
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        self.weapon.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        #self.screen.fill('black')
        self.object_render.draw()
        self.weapon.draw()
        #self.map.draw()
        #self.player.draw()

    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True
            self.player.single_fire_event(event)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


q = False
mini_map = [
    [5, 5, 5, 5, 2, 2, 5, 2, 5, 5, 2, 5, 2, 2, 5, 5],
    [5, 2, q, q, q, q, q, q, 6, q, q, q, q, q, 5, 5],
    [5, 2, q, q, q, q, q, q, q, q, q, q, q, q, 2, 5],
    [5, 5, q, q, 2, 6, 5, q, q, q, 2, 6, q, q, 2, 5],
    [5, 5, q, q, q, q, q, q, q, q, q, q, q, q, 5, 5],
    [5, 2, q, q, q, q, q, q, q, q, q, q, q, q, 2, 5],
    [5, 5, q, 3, 1, 1, 3, q, q, q, 3, 1, 3, q, 5, 5],
    [5, 5, q, 1, 5, 5, 1, q, 3, q, 1, 5, 1, q, 2, 5],
    [5, 2, q, 3, 1, 1, 3, q, q, q, 3, 1, 3, q, 2, 5],
    [5, q, q, q, q, q, q, q, q, q, q, q, q, q, q, 5],
    [2, q, q, q, q, q, q, q, 6, q, q, q, q, q, q, 2],
    [2, q, q, 5, q, q, q, q, q, q, q, q, q, q, q, 5],
    [5, q, q, 2, q, q, q, q, q, q, 5, q, q, 3, q, 2],
    [2, q, q, 5, 2, 2, 5, q, q, q, 2, 2, 5, 2, 5, 5],
    [5, q, q, q, q, q, q, q, q, q, q, q, q, q, 6, 5],
    [2, q, q, q, q, q, q, q, 1, q, q, q, q, q, q, 4],
    [2, q, q, q, q, q, q, q, q, q, q, q, q, q, 6, 5],
    [2, q, q, 2, 5, 2, 5, q, q, q, 5, 2, 5, 2, 5, 5],
    [5, q, q, q, q, q, 5, q, q, q, 5, q, q, q, q, 2],
    [5, q, q, q, q, q, 2, q, 6, q, q, q, q, q, q, 5],
    [2, q, q, q, q, q, q, q, q, q, q, q, q, q, q, 2],
    [5, q, q, q, q, q, q, q, q, q, q, q, q, q, q, 2],
    [5, 2, q, 3, 1, 1, 3, q, q, q, 3, 1, 3, q, 5, 5],
    [5, 5, q, 1, 5, 5, 1, q, 3, q, 1, 5, 1, q, 2, 5],
    [5, 5, q, 3, 1, 1, 3, q, q, q, 3, 1, 3, q, 5, 5],
    [5, 2, q, q, q, q, q, q, q, q, q, q, q, q, 2, 5],
    [5, 2, q, q, q, q, q, q, q, q, q, q, q, q, 2, 5],
    [5, 5, q, q, 2, 6, 5, q, q, q, 2, 6, q, q, 5, 5],
    [5, 2, q, q, q, q, q, q, q, q, q, q, q, q, 5, 5],
    [5, 5, q, q, q, q, q, q, 6, q, q, q, q, q, 2, 5],
    [5, 5, 2, 5, 5, 2, 5, 2, 5, 5, 2, 2, 5, 5, 5, 5]
]


class Map:
    def __init__(self, game):
        self.game = game
        self.mini_map = mini_map
        self.world_map = {}
        self.get_map()

    def get_map(self):
        for j, row in enumerate(self.mini_map):
            for i, value in enumerate(row):
                if value:
                    self.world_map[(i, j)] = value

    def draw(self):
        [pg.draw.rect(self.game.screen, 'darkgray', (pos[0] * 100, pos[1] * 100, 100, 100), 20)
         for pos in self.world_map]


class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.nps_list = []
        self.nps_sprite_path = 'resources/sprites/nps'
        self.static_sprite_path = 'resources/sprites/static_sprites'
        self.anim_sprite_path = 'resources/sprites/animated_sprite'
        add_sprite = self.add_sprite
        add_nps = self.add_nps
        self.nps_position = {}

        add_sprite(SpriteObject(game))
        add_sprite(SpriteObject(game, pos=(7.5, 1.5)))
        add_sprite(SpriteObject(game, pos=(2.5, 1.5)))
        add_sprite(SpriteObject(game, pos=(13.5, 1.5)))
        add_sprite(SpriteObject(game, pos=(8.5, 6.5)))
        add_sprite(SpriteObject(game, pos=(7.5, 29.5)))
        add_sprite(SpriteObject(game, pos=(9.5, 29.5)))
        add_sprite(SpriteObject(game, pos=(2.5, 29.5)))
        add_sprite(SpriteObject(game, pos=(8.5, 24.5)))
        add_sprite(SpriteObject(game, pos=(13.5, 29.5)))
        add_sprite(AnimatedSprite(game))
        add_sprite(AnimatedSprite(game, pos=(13.7, 14.5)))
        add_sprite(AnimatedSprite(game, pos=(13.7, 16.5)))
        add_sprite(AnimatedSprite(game, pos=(12.2, 14.5)))
        add_sprite(AnimatedSprite(game, pos=(12.2, 16.5)))
        add_sprite(AnimatedSprite(game, pos=(10.7, 14.5)))
        add_sprite(AnimatedSprite(game, pos=(10.7, 16.5)))

        add_sprite(AnimatedSprite(game, pos=(14.5, 18.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 21.5)))
        add_sprite(AnimatedSprite(game, pos=(11.5, 18.5)))

        add_sprite(AnimatedSprite(game, pos=(14.5, 9.5)))
        add_sprite(AnimatedSprite(game, pos=(11.5, 12.5)))

        add_sprite(AnimatedSprite(game, pos=(1.5, 21.5)))
        add_sprite(AnimatedSprite(game, pos=(1.5, 9.5)))

        add_nps(NPS(game))
        add_nps(NPS(game, pos=(9.5, 1.5)))
        add_nps(NPS(game, pos=(13.5, 1.5)))
        add_nps(NPS(game, pos=(9.6, 1.6)))
        add_nps(NPS(game, pos=(9.7, 1.7)))
        add_nps(NPS(game, pos=(13, 14.5)))
        add_nps(NPS(game, pos=(13.5, 29.5)))
        add_nps(NPS(game, pos=(8.5, 24.5)))
        add_nps(NPS(game, pos=(8.6, 24.6)))
        add_nps(NPS(game, pos=(7.5, 29.5)))
        add_nps(NPS(game, pos=(7.7, 29.7)))

    def update(self):
        self.nps_position = {nps.map_pos for nps in self.nps_list if nps.alive}
        [sprite.update() for sprite in self.sprite_list]
        [nps.update() for nps in self.nps_list]

    def add_nps(self, nps):
        self.nps_list.append(nps)

    def check_win(self):
        if not len(self.nps_position) and 14.0 < self.game.player.pos[0] < 15:
            self.game.object_render.game_win()

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)


class ObjectRender:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_texture()
        self.sky_image = self.get_texture('resources/texture/sky.png', (WIGHT, HALF_HEIGHT))
        self.sky_offset = 0
        self.blood_screen = self.get_texture('resources/texture/blood_screen.png', RES)
        self.digit_size = 90
        self.digit_image = [self.get_texture(f'resources/texture/digits/{i}.png', [self.digit_size] * 2)
                            for i in range(11)]
        self.digits = dict(zip(map(str, range(11)), self.digit_image))
        self.scores = dict(zip(map(str, range(11)), self.digit_image))
        self.game_over_image = self.get_texture('resources/texture/game_over.png', RES)
        self.win_image = self.get_texture('resources/texture/win.png', RES)

    def draw(self):
        self.draw_backgroung()
        self.rander_game_objects()
        self.draw_player_health()
        self.draw_player_score()

    def game_over(self):
        self.screen.blit(self.game_over_image, (0, 0))

    def game_win(self):
        self.screen.blit(self.win_image, (0, 0))
        pg.display.flip()
        pg.mixer.music.stop()
        self.game.sound.win.play()
        pg.time.delay(10000)
        exit()

    def draw_player_score(self):
        score = str(self.game.player.score)
        for i, char in enumerate(score):
            self.screen.blit(self.scores[char], (i * self.digit_size + WIGHT - self.digit_size * 3, 0))

    def draw_player_health(self):
        health = str(self.game.player.health)
        for i, char in enumerate(health):
            self.screen.blit(self.digits[char], (i * self.digit_size, 0))
        self.screen.blit(self.digits['10'], ((i + 1) * self.digit_size, 0))

    def player_damage(self):
        self.screen.blit(self.blood_screen, (0, 0))

    def draw_backgroung(self):
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WIGHT
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIGHT, 0))

        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIGHT, HEIGHT))

    def rander_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda x: x[0], reverse=True)
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_wall_texture(self):
        return {1: self.get_texture('resources/texture/1.png'),
                2: self.get_texture('resources/texture/2.png'),
                3: self.get_texture('resources/texture/3.png'),
                4: self.get_texture('resources/texture/4.png'),
                5: self.get_texture('resources/texture/5.png'),
                6: self.get_texture('resources/texture/6.png')
                }


class Pathfinding:
    def __init__(self, game):
        self.game = game
        self.map = game.map.mini_map
        self.ways = [-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [1, -1], [1, 1], [-1, 1]
        self.graph = {}
        self.get_graph()

    def get_path(self, start, goal):
        self.visited = self.bfs(start, goal, self.graph)
        path = [goal]
        step = self.visited.get(goal, start)

        while step and step != start:
            path.append(step)
            step = self.visited[step]
        return path[-1]

    def bfs(self, start, goal, graph):
        queue = deque([start])
        visited = {start: None}

        while queue:
            cur_node = queue.popleft()
            if cur_node == goal:
                break
            next_nodes = graph[cur_node]

            for next_node in next_nodes:
                if next_node not in visited and next_node not in self.game.object_handler.nps_position:
                    queue.append(next_node)
                    visited[next_node] = cur_node
        return visited

    def get_next_nodes(self, x, y):
        return [(x + dx, y + dy) for dx, dy in self.ways if (x + dx, y + dy) not in self.game.map.world_map]

    def get_graph(self):
        for y, row in enumerate(self.map):
            for x, col in enumerate(row):
                if not col:
                    self.graph[(x, y)] = self.graph.get((x, y), []) + self.get_next_nodes(x, y)


class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.health = PLAYER_MAX_HEALTH
        self.score = PLAYER_SCORE
        self.rel = 0
        self.health_recovery_delay = 900
        self.time_prev = pg.time.get_ticks()
        self.shot = False

    def recover_health(self):
        if self.check_health_recovery_delay() and self.health < 30:
            self.health += 1

    def check_health_recovery_delay(self):
        time_now = pg.time.get_ticks()
        if time_now - self.time_prev > self.health_recovery_delay:
            self.time_prev = time_now
            return True

    def check_game_over(self):
        if self.health < 1:
            self.game.object_render.game_over()
            pg.display.flip()
            pg.time.delay(3500)
            self.game.new_game()

    def get_damage(self, damage):
        self.health -= damage
        self.game.object_render.player_damage()
        self.game.sound.player_pain.play()
        self.check_game_over()

    def get_score(self, lotting):
        self.score += lotting

    def single_fire_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.shot and not self.game.weapon.reloading:
                self.game.sound.shotgun.play()
                self.shot = True
                self.game.weapon.reloading = True

    def moment(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a
        dx, dy = 0, 0

        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            dx += -speed_cos
            dy += -speed_sin
        if keys[pg.K_a]:
            dx += speed_sin
            dy += -speed_cos
        if keys[pg.K_d]:
            dx += -speed_sin
            dy += speed_cos

        self.check_wall_collision(dx, dy)

        self.angle %= math.tau

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        scale = PLAYER_SIZE_SCALE / self.game.delta_time
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy

    def draw(self):
        pg.draw.line(self.game.screen, 'yellow', (self.x * 100, self.y * 100),
                     (self.x * 100 + WIGHT * math.cos(self.angle), self.y * 100 + WIGHT * math.sin(self.angle)), 2)
        pg.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15)

    def mouse_control(self):
        mx, my = pg.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIGHT, HALF_HEIGHT])
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time

    def update(self):
        self.moment()
        self.mouse_control()
        self.recover_health()

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)


class Raycasting:
    def __init__(self, game):
        self.game = game
        self.ray_casting_result = []
        self.object_to_render = []
        self.textures = self.game.object_render.wall_textures

    def get_objects_to_render(self):
        self.objects_to_render = []
        for ray, values in enumerate(self.ray_casting_result):
            depth, proj_height, texture, offset = values

            if proj_height < HEIGHT:
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, proj_height))
                wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)
            else:
                texture_height = TEXTURE_SIZE * HEIGHT / proj_height
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), HALF_TEXTURE_SIZE - texture_height // 2,
                    SCALE, texture_height
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, HEIGHT))
                wall_pos = (ray * SCALE, 0)

            self.objects_to_render.append((depth, wall_column, wall_pos))

    def ray_cast(self):
        self.ray_casting_result = []
        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        texture_vert, texture_hor = 1, 1

        ray_angle = self.game.player.angle - HALF_FOV + 0.0001
        for ray in range(NUM_RAYS):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)
            depth_hor = (y_hor - oy) / sin_a
            x_hor = ox + depth_hor * cos_a
            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            for i in range(MAX_DEPTH):
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in self.game.map.world_map:
                    texture_hor = self.game.map.world_map[tile_hor]
                    break
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)
            depth_vert = (x_vert - ox) / cos_a
            y_vert = oy + depth_vert * sin_a
            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            for i in range(MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in self.game.map.world_map:
                    texture_vert = self.game.map.world_map[tile_vert]
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            if depth_vert < depth_hor:
                depth, texture = depth_vert, texture_vert
                y_vert %= 1
                offset = y_vert if cos_a > 0 else(1 - y_vert)
            else:
                depth, texture = depth_hor, texture_hor
                x_hor %= 1
                offset = (1 - x_hor) if sin_a > 0 else x_hor

            depth *= math.cos(self.game.player.angle - ray_angle)

            proj_height = SCREEN_DIST / (depth + 0.0001)

            self.ray_casting_result.append((depth, proj_height, texture, offset))

            ray_angle += DELTA_ANGLE

    def update(self):
        self.ray_cast()
        self.get_objects_to_render()


class Sound:
    def __init__(self, game):
        self.game = game
        pg.mixer.init()
        self.path = 'resources/sound'
        self.shotgun = pg.mixer.Sound(self.path + '/shotgun.mp3')
        self.nps_pain = pg.mixer.Sound(self.path + '/nps_pain.mp3')
        self.nps_death = pg.mixer.Sound(self.path + '/nps_death.mp3')
        self.nps_shot = pg.mixer.Sound(self.path + '/nps_attack.mp3')
        self.player_pain = pg.mixer.Sound(self.path + '/player_pain.mp3')
        self.win = pg.mixer.Sound(self.path + '/jojo_win.mp3')
        self.theme = pg.mixer.music.load(self.path + '/theme.mp3')
        self.nps_shot.set_volume(0.8)
        pg.mixer.music.set_volume(0.4)


class SpriteObject:
    def __init__(self, game, path='resources/sprites/static_sprites/candlebra.png',
                 pos=(9.5, 1.5), scale=0.8, shift=0.2):
        self.game = game
        self.player = game.player
        self.x, self.y = pos
        self.image = pg.image.load(path).convert_alpha()
        self.IMAGE_WIDTH = self.image.get_width()
        self.IMAGE_HALF_WIDTH = self.image.get_width() // 2
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image.get_height()
        self.dx, self.dy, self.theta, self.screen_x, self.dist, self.norm_dist = 0, 0, 0, 0, 1, 1
        self.sprite_half_width = 0
        self.SPRITE_SCALE = scale
        self.SPRITE_HEIGHT_SHIFT = shift

    def get_sprite_projection(self):
        proj = SCREEN_DIST / self.norm_dist * self.SPRITE_SCALE
        proj_width, proj_height = proj * self.IMAGE_RATIO, proj

        image = pg.transform.scale(self.image, (proj_width, proj_height))
        self.sprite_half_wight = proj_width // 2
        height_shift = proj_height * self.SPRITE_HEIGHT_SHIFT
        pos = self.screen_x - self.sprite_half_wight, HALF_HEIGHT - proj_height // 2 + height_shift

        self.game.raycasting.objects_to_render.append((self.norm_dist, image, pos))

    def get_sprite(self):
        dx = self.x - self.player.x
        dy = self.y - self.player.y
        self.dx, self.dy = dx, dy
        self.theta = math.atan2(dy, dx)

        delta = self.theta - self.player.angle
        if (dx > 0 and self.player.angle > math.pi) or (dx < 0 and dy <0):
            delta += math.tau

        delta_rays = delta / DELTA_ANGLE
        self.screen_x = (HALF_NUM_RAYS + delta_rays) * SCALE
        self.dist = math.hypot(dx, dy)
        self.norm_dist = self.dist * math.cos(delta)
        if -self.IMAGE_HALF_WIDTH < self.screen_x < (WIGHT + self.IMAGE_HALF_WIDTH) and self.norm_dist > 0.5:
            self.get_sprite_projection()

    def update(self):
        self.get_sprite()


class AnimatedSprite(SpriteObject):
    def __init__(self, game, path='resources/sprites/animated_sprite/green_light/0.png', pos=(11.5, 3.5), scale=0.8,
                 shift=0.15, animation_time=120):
        super().__init__(game, path, pos, scale, shift)
        self.animation_time = animation_time
        self.path = path.rsplit('/', 1)[0]
        self.images = self.get_images(self.path)
        self.animation_time_prev = pg.time.get_ticks()
        self.animation_trigger = False

    def update(self):
        super().update()
        self.check_anuimation_time()
        self.animate(self.images)

    def animate(self, images):
        if self.animation_trigger:
            images.rotate(-1)
            self.image = images[0]

    def check_anuimation_time(self):
        self.animation_trigger = False
        time_now = pg.time.get_ticks()
        if time_now - self.animation_time_prev > self.animation_time:
            self.animation_time_prev = time_now
            self.animation_trigger = True

    def get_images(self, path):
        images = deque()
        for file_name in os.listdir(path):
            if os.path.isfile(os.path.join(path, file_name)):
                img = pg.image.load(path + '/' + file_name).convert_alpha()
                images.append(img)
        return images


class Weapon(AnimatedSprite):
    def __init__(self, game, path='resources/sprites/weapon/0.png', scale=0.4, animation_time=90):
        super().__init__(game=game, path=path, scale=scale, animation_time=animation_time)
        self.images = deque(
            [pg.transform.smoothscale(img, (self.IMAGE_WIDTH * scale, self.image.get_height() * scale))
             for img in self.images])
        self.weapon_pos = (HALF_WIGHT - self.images[0].get_width() // 2, HEIGHT - self.images[0].get_height())
        self.reloading = False
        self.num_images = len(self.images)
        self.frame_counter = 0
        self.damage = 50

    def animated_shot(self):
        if self.reloading:
            self.game.player.shot = False
            if self.animation_trigger:
                self.images.rotate(-1)
                self.image = self.images[0]
                self.frame_counter += 1
                if self.frame_counter == self.num_images:
                    self.reloading = False
                    self.frame_counter = 0

    def draw(self):
        self.game.screen.blit(self.images[0], self.weapon_pos)

    def update(self):
        self.check_anuimation_time()
        self.animated_shot()


class NPS(AnimatedSprite):
    def __init__(self, game, path='resources/sprites/nps/soldier/0.png', pos=(7.5, 1.5),
                 scale=0.8, shift=0.3, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_images = self.get_images(self.path + '/attack')
        self.death_images = self.get_images(self.path + '/death')
        self.idle_images = self.get_images(self.path + '/idle')
        self.pain_images = self.get_images(self.path + '/pain')
        self.walk_images = self.get_images(self.path + '/walk')

        self.attack_dist = randint(3, 6)
        self.speed = 0.03
        self.size = 10
        self.health = 100
        self.attack_damage = 15
        self.score_looting = 25
        self.accuracy = 0.15
        self.alive = True
        self.pain = False
        self.ray_cast_value = False
        self.player_search_trigger = False
        self.flag = False
        self.frame_counter = 0

    def update(self):
        self.check_anuimation_time()
        self.get_sprite()
        self.run_logic()
        #self.draw_ray_cast()

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        if self.check_wall(int(self.x + dx * self.size), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * self.size)):
            self.y += dy

    def movement(self):
        next_pos = self.game.pathfinding.get_path(self.map_pos, self.game.player.map_pos)
        next_x, next_y = next_pos

        #pg.draw.rect(self.game.screen, 'blue', (100 * next_x, 100 * next_y, 100, 100))
        if next_pos not in self.game.object_handler.nps_position:
            angle = math.atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x)
            dx = math.cos(angle) * self.speed
            dy = math.sin(angle) * self.speed
            self.check_wall_collision(dx, dy)

    def lotting(self):
        if self.animation_trigger:
            self.game.player.get_score(self.score_looting)
            self.flag = False

    def pick_up_lotting(self):
        if self.animation_trigger:
            self.game.player.get_score(-1)

    def attack(self):
        if self.animation_trigger:
            self.game.sound.nps_shot.play()
            if random() < self.accuracy:
                self.game.player.get_damage(self.attack_damage)
                self.pick_up_lotting()

    def animate_death(self):
        if not self.alive:
            if self.game.global_trigger and self.frame_counter < len(self.death_images) - 1:
                self.death_images.rotate(-1)
                self.image = self.death_images[0]
                self.frame_counter += 1

    def animate_pain(self):
        self.animate(self.pain_images)
        if self.animation_trigger:
            self.pain = False

    def check_hit_in_nps(self):
        if self.ray_cast_value and self.game.player.shot:
            if HALF_WIGHT - self.sprite_half_wight < self.screen_x < HALF_WIGHT + self.sprite_half_wight:
                self.game.sound.nps_pain.play()
                self.game.player.shot = False
                self.pain = True
                self.health -= self.game.weapon.damage
                self.check_health()

    def check_health(self):
        if self.health < 1:
            self.alive = False
            self.game.sound.nps_death.play()

    def run_logic(self):
        if self.alive:
            self.ray_cast_value = self.ray_cast_player_nps()
            self.check_hit_in_nps()
            if self.pain:
                self.animate_pain()
                self.lotting()
                self.flag = True
            elif self.ray_cast_value:
                self.player_search_trigger = True
                if self.dist < self.attack_dist:
                    self.animate(self.attack_images)
                    self.attack()
                else:
                    self.animate(self.walk_images)
                    self.movement()
            elif self.player_search_trigger:
                self.animate(self.walk_images)
                self.movement()
            else:
                self.animate(self.idle_images)

        else:
            if self.flag:
                self.lotting()
            self.animate_death()
            self.game.object_handler.check_win()



    @property
    def map_pos(self):
        return int(self.x), int(self.y)

    def ray_cast_player_nps(self):
        if self.game.player.map_pos == self.map_pos:
            return True

        wall_dist_v, wall_dist_h = 0, 0
        player_dist_v, player_dist_h = 0, 0

        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        ray_angle = self.theta

        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)
        depth_hor = (y_hor - oy) / sin_a
        x_hor = ox + depth_hor * cos_a
        delta_depth = dy / sin_a
        dx = delta_depth * cos_a

        for i in range(MAX_DEPTH):
            tile_hor = int(x_hor), int(y_hor)
            if tile_hor == self.map_pos:
                player_dist_h = depth_hor
                break
            if tile_hor in self.game.map.world_map:
                wall_dist_h = depth_hor
                break
            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth

        x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)
        depth_vert = (x_vert - ox) / cos_a
        y_vert = oy + depth_vert * sin_a
        delta_depth = dx / cos_a
        dy = delta_depth * sin_a

        for i in range(MAX_DEPTH):
            tile_vert = int(x_vert), int(y_vert)
            if tile_vert == self.map_pos:
                player_dist_v = depth_vert
                break
            if tile_vert in self.game.map.world_map:
                wall_dist_v = depth_vert
                break
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth

        player_dist = max(player_dist_v, player_dist_h)
        wall_dist = max(wall_dist_v, wall_dist_h)

        if 0 < player_dist < wall_dist or not wall_dist:
            return True
        return False

    def draw_ray_cast(self):
        pg.draw.circle(self.game.screen, 'red', (100 * self.x, 100 * self.y), 15)
        if self.ray_cast_player_nps():
            pg.draw.line(self.game.screen, 'orange', (100 * self.game.player.x, 100 * self.player.y),
                         (100 * self.x, 100 * self.y), 2)


class Okno:
    def __init__(self):
        pg.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.screen = pg.display.set_mode(RES)
        self.font = "other/text.ttf"
        self.first_image = pg.image.load('resources/texture/doom_image.png')
        self.clock = pg.time.Clock()

    def main_menu(self):

        menu = True
        selected = "start"

        while menu:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        selected = "start"
                    elif event.key == pg.K_DOWN:
                        selected = "quit"
                    if event.key == pg.K_RETURN:
                        if selected == "start":
                            game = Game()
                            game.run()
                        if selected == "quit":
                            pg.quit()
                            quit()

            self.screen.blit(self.first_image, (0, 0))
            if selected == "start":
                text_start = self.text_format("START", self.font, 75, (242, 0, 0))
            else:
                text_start = self.text_format("START", self.font, 75, (140, 0, 0))
            if selected == "quit":
                text_quit = self.text_format("QUIT", self.font, 75, (242, 0, 0))
            else:
                text_quit = self.text_format("QUIT", self.font, 75, (140, 0, 0))

            start_rect = text_start.get_rect()
            quit_rect = text_quit.get_rect()

            self.screen.blit(text_start, (WIGHT // 2 - (start_rect[2]/2), 430))
            self.screen.blit(text_quit, (WIGHT // 2 - (quit_rect[2]/2), 560))
            pg.display.update()
            self.clock.tick(FPS)
            pg.display.set_caption("My DOOM")

    def text_format(self, message, textFont, textSize, textColor):
        newFont = pg.font.Font(textFont, textSize)
        newText = newFont.render(message, 0, textColor)
        return newText


if __name__ == '__main__':
    okno = Okno()
    okno.main_menu()