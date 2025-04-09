import pygame
import math
import random
import asyncio

async def main():
    pygame.init()
    pygame.mixer.init()

    WIDTH = 1200
    HEIGHT = 800
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Spaceship Meteor Dodge")

    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    GRAY = (100, 100, 100)
    GREEN = (0, 255, 0)
    FIRE_COLOR = (255, 100, 0)
    BLUE = (0, 0, 255)
    PURPLE = (255, 0, 255)
    # Image loading with fallbacks
    try:
        SHIP_IMAGE = pygame.image.load("ship_hd.png").convert_alpha()
        SHIP_IMAGE = pygame.transform.smoothscale(SHIP_IMAGE, (45, 45))
    except Exception as e:
        print(f"Ship load error: {e}")
        SHIP_IMAGE = pygame.Surface((45, 45), pygame.SRCALPHA)
        pygame.draw.polygon(SHIP_IMAGE, WHITE, [(22, 0), (44, 44), (0, 44)])

    try:
        SMALL_ASTEROID = pygame.image.load("small_asteroid.png").convert_alpha()
    except Exception as e:
        print(f"Small asteroid error: {e}")
        SMALL_ASTEROID = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.circle(SMALL_ASTEROID, GRAY, (25, 25), 25)

    try:
        MEDIUM_ASTEROID = pygame.image.load("medium_asteroid.png").convert_alpha()
    except Exception as e:
        print(f"Medium asteroid error: {e}")
        MEDIUM_ASTEROID = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.circle(MEDIUM_ASTEROID, GRAY, (25, 25), 25)

    try:
        ENGINE_FIRE = pygame.image.load("engine_fire.png").convert_alpha()
        ENGINE_FIRE = pygame.transform.smoothscale(ENGINE_FIRE, (30, 30))
    except Exception as e:
        print(f"Engine fire load error: {e}")
        ENGINE_FIRE = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.polygon(ENGINE_FIRE, FIRE_COLOR, [(15, 0), (30, 30), (0, 30)])
    try:
        BULLET_IMAGE = pygame.image.load("bullet.png").convert_alpha()
        BULLET_IMAGE = pygame.transform.smoothscale(BULLET_IMAGE, (10, 10))
    except Exception as e:
        print(f"Bullet load error: {e}")
        BULLET_IMAGE = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(BULLET_IMAGE, RED, (5, 5), 5)

    try:
        COIN_IMAGE = pygame.image.load("coin.png").convert_alpha()
        COIN_IMAGE = pygame.transform.smoothscale(COIN_IMAGE, (20, 20))
    except Exception as e:
        print(f"Coin load error: {e}")
        COIN_IMAGE = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(COIN_IMAGE, YELLOW, (10, 10), 10)

    try:
        POWERUP_IMAGE = pygame.image.load("powerup.png").convert_alpha()
        POWERUP_IMAGE = pygame.transform.smoothscale(POWERUP_IMAGE, (20, 20))
    except Exception as e:
        print(f"Power-up load error: {e}")
        POWERUP_IMAGE = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(POWERUP_IMAGE, PURPLE, (10, 10), 10)

    try:
        BACKGROUND_IMAGE = pygame.image.load("background.png").convert()
        BACKGROUND_IMAGE = pygame.transform.smoothscale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))
    except Exception as e:
        print(f"Background load error: {e}")
        BACKGROUND_IMAGE = pygame.Surface((WIDTH, HEIGHT))
        BACKGROUND_IMAGE.fill((0, 0, 0))
    # UI Images
    try:
        SUPERPOINTS_IMAGE = pygame.image.load("superpoints.png").convert_alpha()
        SUPERPOINTS_IMAGE = pygame.transform.smoothscale(SUPERPOINTS_IMAGE, (80, 20))
        AMMO_IMAGE = pygame.image.load("ammo.png").convert_alpha()
        AMMO_IMAGE = pygame.transform.smoothscale(AMMO_IMAGE, (80, 20))
        LEVEL_IMAGE = pygame.image.load("level.png").convert_alpha()
        LEVEL_IMAGE = pygame.transform.smoothscale(LEVEL_IMAGE, (80, 20))
        POWERUPREADY_IMAGE = pygame.image.load("powerupready.png").convert_alpha()
        POWERUPREADY_IMAGE = pygame.transform.smoothscale(POWERUPREADY_IMAGE, (80, 20))
        POWERUP_S_IMAGE = pygame.image.load("powerup_s.png").convert_alpha()
        POWERUP_S_IMAGE = pygame.transform.smoothscale(POWERUP_S_IMAGE, (20, 20))
        RUSHIN_IMAGE = pygame.image.load("rushin.png").convert_alpha()
        RUSHIN_IMAGE = pygame.transform.smoothscale(RUSHIN_IMAGE, (80, 20))
        MEGARUSH_IMAGE = pygame.image.load("megarush.png").convert_alpha()
        MEGARUSH_IMAGE = pygame.transform.smoothscale(MEGARUSH_IMAGE, (80, 20))
        MEGARUSH_INCOMING_IMAGE = pygame.image.load("megarush_incoming.png").convert_alpha()
        MEGARUSH_INCOMING_IMAGE = pygame.transform.smoothscale(MEGARUSH_INCOMING_IMAGE, (200, 50))
        GAMEOVER_IMAGE = pygame.image.load("gameover.png").convert_alpha()
        GAMEOVER_IMAGE = pygame.transform.smoothscale(GAMEOVER_IMAGE, (300, 100))
        START_BUTTON_IMAGE = pygame.image.load("start_button.png").convert_alpha()
        START_BUTTON_IMAGE = pygame.transform.smoothscale(START_BUTTON_IMAGE, (200, 200))
        NUMBER_IMAGES = {str(i): pygame.transform.smoothscale(pygame.image.load(f"number_{i}.png").convert_alpha(), (20, 20)) for i in range(10)}
    except Exception as e:
        print(f"Image load error: {e}")
    # Sound loading (delay music for web)
    try:
        BULLET_SOUND = pygame.mixer.Sound("bullet_sound.wav")
        ENGINE_SOUND = pygame.mixer.Sound("engine_sound.wav")
        ENGINE_SOUND.set_volume(0.5)
        pygame.mixer.music.load("background_music.mp3")
        pygame.mixer.music.set_volume(0.3)
    except Exception as e:
        print(f"Sound load error: {e}")
        BULLET_SOUND = ENGINE_SOUND = None

    # Game constants
    ship_x = WIDTH // 2
    ship_y = HEIGHT // 2
    ship_angle = 0
    ship_speed = 0
    MAX_SPEED = 3
    ACCELERATION = 0.0495
    FRICTION = 0.98
    STAMINA_MAX = 200
    stamina = STAMINA_MAX
    STAMINA_DRAIN = 0.5
    STAMINA_RECHARGE = 0.5

    meteors = []
    big_meteors = []
    coins = []
    bullets = []
    powerup = None
    powerup_held = False

    super_points = 0
    ammo = 0
    score_timer = 0
    rush_count = 0
    level = 1
    RUSH_INTERVAL = 20 * 60
    RUSH_DURATION = 10 * 60
    MEGARUSH_DURATION = 20 * 60
    rush_timer = RUSH_INTERVAL
    rush_countdown_active = True
    rush_active = False
    megarush_active = False
    rush_remaining = 0
    POWERUP_INTERVAL = 2
    POWERUP_DURATION = 3 * 60
    powerup_active = False
    powerup_remaining = 0

    font = pygame.font.Font(None, 36)
    class Meteor:
        def __init__(self, speed_multiplier=1.0):
            side = random.randint(0, 3)
            if side == 0:
                self.x, self.y, self.angle = random.randint(0, WIDTH), -50, random.uniform(math.pi / 4, 3 * math.pi / 4)
            elif side == 1:
                self.x, self.y, self.angle = WIDTH + 50, random.randint(0, HEIGHT), random.uniform(5 * math.pi / 4, 7 * math.pi / 4)
            elif side == 2:
                self.x, self.y, self.angle = random.randint(0, WIDTH), HEIGHT + 50, random.uniform(-3 * math.pi / 4, -math.pi / 4)
            else:
                self.x, self.y, self.angle = -50, random.randint(0, HEIGHT), random.uniform(math.pi / 4, -math.pi / 4)
            self.speed = random.uniform(2, 4) * speed_multiplier
            self.size = random.randint(20, 50)
            self.image = pygame.transform.smoothscale(SMALL_ASTEROID, (self.size, self.size))
        def move(self):
            self.x += math.cos(self.angle) * self.speed
            self.y -= math.sin(self.angle) * self.speed
            return self.x < -50 or self.x > WIDTH + 50 or self.y < -50 or self.y > HEIGHT + 50
        def draw(self):
            rect = self.image.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(self.image, rect)

    class BigMeteor:
        def __init__(self, speed_multiplier=1.0):
            side = random.randint(0, 3)
            if side == 0:
                self.x, self.y, self.angle = random.randint(0, WIDTH), -100, random.uniform(math.pi / 4, 3 * math.pi / 4)
            elif side == 1:
                self.x, self.y, self.angle = WIDTH + 100, random.randint(0, HEIGHT), random.uniform(5 * math.pi / 4, 7 * math.pi / 4)
            elif side == 2:
                self.x, self.y, self.angle = random.randint(0, WIDTH), HEIGHT + 100, random.uniform(-3 * math.pi / 4, -math.pi / 4)
            else:
                self.x, self.y, self.angle = -100, random.randint(0, HEIGHT), random.uniform(math.pi / 4, -math.pi / 4)
            self.speed = random.uniform(1, 3) * speed_multiplier
            self.size = random.randint(50, 100)
            self.image = pygame.transform.smoothscale(MEDIUM_ASTEROID, (self.size, self.size))
        def move(self):
            self.x += math.cos(self.angle) * self.speed
            self.y -= math.sin(self.angle) * self.speed
            return self.x < -100 or self.x > WIDTH + 100 or self.y < -100 or self.y > HEIGHT + 100
        def draw(self):
            rect = self.image.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(self.image, rect)

    class Coin:
        def __init__(self):
            side = random.randint(0, 3)
            if side == 0:
                self.x, self.y, self.angle = random.randint(0, WIDTH), -20, random.uniform(math.pi / 4, 3 * math.pi / 4)
            elif side == 1:
                self.x, self.y, self.angle = WIDTH + 20, random.randint(0, HEIGHT), random.uniform(5 * math.pi / 4, 7 * math.pi / 4)
            elif side == 2:
                self.x, self.y, self.angle = random.randint(0, WIDTH), HEIGHT + 20, random.uniform(-3 * math.pi / 4, -math.pi / 4)
            else:
                self.x, self.y, self.angle = -20, random.randint(0, HEIGHT), random.uniform(math.pi / 4, -math.pi / 4)
            self.speed = random.uniform(1, 3)
            self.image = COIN_IMAGE
        def move(self):
            self.x += math.cos(self.angle) * self.speed
            self.y -= math.sin(self.angle) * self.speed
            return self.x < -20 or self.x > WIDTH + 20 or self.y < -20 or self.y > HEIGHT + 20
        def draw(self):
            rect = self.image.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(self.image, rect)

    class Bullet:
        def __init__(self, x, y, angle):
            self.x, self.y = x, y
            self.speed = 6
            self.angle = angle
            self.image = pygame.transform.rotate(BULLET_IMAGE, math.degrees(-angle) - 90)
        def move(self):
            self.x += math.cos(self.angle) * self.speed
            self.y -= math.sin(self.angle) * self.speed
            return self.x < 0 or self.x > WIDTH or self.y < 0 or self.y > HEIGHT
        def draw(self):
            rect = self.image.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(self.image, rect)

    class PowerUp:
        def __init__(self):
            self.x, self.y = random.randint(0, WIDTH), random.randint(0, HEIGHT)
            self.image = POWERUP_IMAGE
        def draw(self):
            rect = self.image.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(self.image, rect)
    clock = pygame.time.Clock()

    # Start screen loop
    start_game = False
    while not start_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                button_rect = START_BUTTON_IMAGE.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                if button_rect.collidepoint(mouse_x, mouse_y):
                    start_game = True
                    pygame.mixer.music.play(-1)  # Start music on click
        screen.blit(BACKGROUND_IMAGE, (0, 0))
        screen.blit(START_BUTTON_IMAGE, (WIDTH // 2 - 100, HEIGHT // 2 - 100))
        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)

    # Main game loop
    running = True
    meteor_spawn_timer = 0
    coin_spawn_timer = 0
    big_meteor_timer = 0
    big_meteor_spawn_interval = random.randint(600, 900)
    engine_playing = False

    try:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and ammo >= 3:
                    for i in range(3):
                        angle = ship_angle + random.uniform(-0.2, 0.2)
                        bullets.append(Bullet(ship_x, ship_y, angle))
                        ammo -= 1
                        if BULLET_SOUND:
                            BULLET_SOUND.play()

            keys = pygame.key.get_pressed()
            boosting = False
            if keys[pygame.K_a] and stamina > 0:
                ship_speed += ACCELERATION
                ship_speed = min(ship_speed, MAX_SPEED)
                stamina -= STAMINA_DRAIN
                boosting = True
                if ENGINE_SOUND and not engine_playing:
                    ENGINE_SOUND.play(-1)
                    engine_playing = True
            else:
                stamina = min(STAMINA_MAX, stamina + STAMINA_RECHARGE)
                if ENGINE_SOUND and engine_playing:
                    ENGINE_SOUND.stop()
                    engine_playing = False
            if keys[pygame.K_s] and powerup_held and not powerup_active:
                powerup_active = True
                powerup_remaining = POWERUP_DURATION
                powerup_held = False

            ship_speed *= FRICTION
            mouse_x, mouse_y = pygame.mouse.get_pos()
            ship_angle = math.atan2(ship_y - mouse_y, mouse_x - ship_x)
            ship_x += math.cos(ship_angle) * ship_speed
            ship_y -= math.sin(ship_angle) * ship_speed
            ship_x = max(0, min(ship_x, WIDTH))
            ship_y = max(0, min(ship_y, HEIGHT))

            # Rush/Megarush logic
            if rush_active or megarush_active:
                rush_remaining -= 1
                if rush_remaining <= 0:
                    rush_active = megarush_active = False
                    rush_countdown_active = True
                    rush_timer = RUSH_INTERVAL
            elif rush_countdown_active:
                rush_timer -= 1
                if rush_timer <= 0:
                    rush_countdown_active = False
                    rush_count += 1
                    if rush_count % 5 == 0:
                        megarush_active = True
                        rush_remaining = MEGARUSH_DURATION
                        level += 1
                    else:
                        rush_active = True
                        rush_remaining = RUSH_DURATION

            # Power-up logic
            if rush_count % POWERUP_INTERVAL == 0 and rush_count > 0 and powerup is None and not powerup_held and not powerup_active:
                powerup = PowerUp()
            if powerup_active:
                powerup_remaining -= 1
                if powerup_remaining <= 0:
                    powerup_active = False
            if powerup and not powerup_held and not powerup_active and math.hypot(ship_x - powerup.x, ship_y - powerup.y) < 25:
                powerup_held = True
                powerup = None

            # Meteor spawning
            meteor_spawn_timer += 1
            speed_multiplier = 1.0 * (1.0105 ** (level - 1))
            spawn_threshold = 8 if not (rush_active or megarush_active) else (4 if rush_active else 2)
            meteor_count = 2 if not (rush_active or megarush_active) else (4 if rush_active else 8)
            if meteor_spawn_timer > spawn_threshold and len(meteors) < 100:
                for _ in range(meteor_count):
                    meteors.append(Meteor(speed_multiplier))
                meteor_spawn_timer = 0

            # Coin spawning
            coin_spawn_timer += 1
            if coin_spawn_timer > 120 and len(coins) < 20:
                coins.append(Coin())
                coin_spawn_timer = 0
            # Big meteor spawning
            big_meteor_timer += 1
            big_meteor_count = random.randint(2, 4) if not megarush_active else random.randint(3, 6)
            if big_meteor_timer >= big_meteor_spawn_interval and len(big_meteors) < 10:
                for _ in range(big_meteor_count):
                    big_meteors.append(BigMeteor(speed_multiplier))
                big_meteor_timer = 0
                big_meteor_spawn_interval = random.randint(600, 900)

            # Update game objects
            for meteor in meteors[:]:
                if meteor.move():
                    meteors.remove(meteor)
                elif not powerup_active and math.hypot(ship_x - meteor.x, ship_y - meteor.y) < meteor.size // 2 * 0.9:
                    running = False

            for big_meteor in big_meteors[:]:
                if big_meteor.move():
                    big_meteors.remove(big_meteor)
                elif not powerup_active and math.hypot(ship_x - big_meteor.x, ship_y - big_meteor.y) < big_meteor.size // 2 * 0.9:
                    running = False

            for coin in coins[:]:
                if coin.move():
                    coins.remove(coin)
                elif math.hypot(ship_x - coin.x, ship_y - coin.y) < 25:
                    coins.remove(coin)
                    super_points += 10
                    ammo += 3

            for bullet in bullets[:]:
                if bullet.move():
                    bullets.remove(bullet)
                else:
                    for meteor in meteors[:]:
                        if math.hypot(bullet.x - meteor.x, bullet.y - meteor.y) < meteor.size // 2:
                            meteors.remove(meteor)
                            bullets.remove(bullet)
                            super_points += 5
                            break
                    else:
                        for big_meteor in big_meteors[:]:
                            if math.hypot(bullet.x - big_meteor.x, bullet.y - big_meteor.y) < big_meteor.size // 2:
                                big_meteors.remove(big_meteor)
                                bullets.remove(bullet)
                                super_points += 20
                                break

            # Score update
            score_timer += 1
            if score_timer >= 60:
                super_points += 1
                score_timer = 0

            # Drawing
            screen.blit(BACKGROUND_IMAGE, (0, 0))
            rotated_ship = pygame.transform.rotozoom(SHIP_IMAGE, math.degrees(ship_angle) - 90, 1)
            ship_rect = rotated_ship.get_rect(center=(int(ship_x), int(ship_y)))
            if boosting:
                rotated_fire = pygame.transform.rotate(ENGINE_FIRE, math.degrees(ship_angle) - 90)
                fire_rect = rotated_fire.get_rect(center=(int(ship_x - 25 * math.cos(ship_angle)), int(ship_y + 25 * math.sin(ship_angle))))
                screen.blit(rotated_fire, fire_rect)
            rotated_ship.set_alpha(128 if powerup_active else 255)
            screen.blit(rotated_ship, ship_rect)

            for meteor in meteors: meteor.draw()
            for big_meteor in big_meteors: big_meteor.draw()
            for coin in coins: coin.draw()
            for bullet in bullets: bullet.draw()
            if powerup: powerup.draw()

            # UI Drawing
            try:
                screen.blit(SUPERPOINTS_IMAGE, (10, 10))
                for i, digit in enumerate(str(super_points)):
                    screen.blit(NUMBER_IMAGES[digit], (100 + i * 20, 10))
            except NameError:
                screen.blit(font.render(f"Super Points: {super_points}", True, WHITE), (10, 10))
            try:
                screen.blit(AMMO_IMAGE, (10, 40))
                for i, digit in enumerate(str(ammo)):
                    screen.blit(NUMBER_IMAGES[digit], (100 + i * 20, 40))
            except NameError:
                screen.blit(font.render(f"Ammo: {ammo}", True, WHITE), (10, 40))
            try:
                screen.blit(LEVEL_IMAGE, (10, 70))
                for i, digit in enumerate(str(level)):
                    screen.blit(NUMBER_IMAGES[digit], (100 + i * 20, 70))
            except NameError:
                screen.blit(font.render(f"Level: {level}", True, WHITE), (10, 70))
            try:
                screen.blit(POWERUPREADY_IMAGE if powerup_held else POWERUP_IMAGE, (10, 100))
                if powerup_held:
                    screen.blit(POWERUP_S_IMAGE, (90, 100))
            except NameError:
                screen.blit(font.render("Power-Up: Ready (S)" if powerup_held else "Power-Up: None", True, PURPLE), (10, 100))

            # Rush timer display
            if rush_countdown_active:
                try:
                    screen.blit(RUSHIN_IMAGE, (WIDTH - 200, 10))
                    seconds = str(rush_timer // 60)
                    for i, digit in enumerate(seconds):
                        screen.blit(NUMBER_IMAGES[digit], (WIDTH - 110 + i * 20, 10))
                except NameError:
                    screen.blit(font.render(f"Rush in: {rush_timer // 60}", True, WHITE), (WIDTH - 200, 10))

            # Stamina bar
            pygame.draw.rect(screen, GRAY, (10, 130, 62.5, 20))
            pygame.draw.rect(screen, GREEN, (10, 130, (stamina / STAMINA_MAX) * 62.5, 20))

            # Rush/Megarush indicators
            if rush_active or megarush_active:
                rush_bar_width = (rush_remaining / (MEGARUSH_DURATION if megarush_active else RUSH_DURATION)) * 100
                pygame.draw.rect(screen, GRAY, (WIDTH - 110, 40, 100, 10))
                pygame.draw.rect(screen, BLUE, (WIDTH - 110, 40, rush_bar_width, 10))
                try:
                    screen.blit(MEGARUSH_IMAGE if megarush_active else RUSHIN_IMAGE, (WIDTH - 150, 60))
                except NameError:
                    screen.blit(font.render("Mega Rush!" if megarush_active else "Rush!", True, WHITE), (WIDTH - 150, 60))
            elif rush_count > 0 and rush_count % 5 == 4 and rush_timer <= 5 * 60 and rush_countdown_active:
                try:
                    screen.blit(MEGARUSH_INCOMING_IMAGE, (WIDTH // 2 - 100, 10))
                except NameError:
                    screen.blit(font.render("Mega Rush Incoming!", True, WHITE), (WIDTH // 2 - 100, 10))

            pygame.display.flip()
            clock.tick(60)
            await asyncio.sleep(0)  # Pygbag needs this

    except Exception as e:
        print(f"Game crashed: {e}")

    # Game over screen with score display
    pygame.mixer.music.stop()
    screen.blit(BACKGROUND_IMAGE, (0, 0))
    try:
        # Game Over image
        screen.blit(GAMEOVER_IMAGE, (WIDTH // 2 - 150, HEIGHT // 2 - 120))  # Adjusted up for score
        # Super Points
        screen.blit(SUPERPOINTS_IMAGE, (WIDTH // 2 - 150, HEIGHT // 2 - 20))
        for i, digit in enumerate(str(super_points)):
            screen.blit(NUMBER_IMAGES[digit], (WIDTH // 2 - 50 + i * 20, HEIGHT // 2 - 20))
        # Level
        screen.blit(LEVEL_IMAGE, (WIDTH // 2 - 150, HEIGHT // 2 + 20))
        for i, digit in enumerate(str(level)):
            screen.blit(NUMBER_IMAGES[digit], (WIDTH // 2 - 50 + i * 20, HEIGHT // 2 + 20))
    except NameError:
        # Fallback text if images fail
        screen.blit(font.render("Game Over!", True, WHITE), (WIDTH // 2 - 70, HEIGHT // 2 - 120))
        screen.blit(font.render(f"Super Points: {super_points}", True, WHITE), (WIDTH // 2 - 100, HEIGHT // 2 - 20))
        screen.blit(font.render(f"Level: {level}", True, WHITE), (WIDTH // 2 - 50, HEIGHT // 2 + 20))
    pygame.display.flip()
    await asyncio.sleep(5)  # 5 seconds to view score
    pygame.quit()

asyncio.run(main())