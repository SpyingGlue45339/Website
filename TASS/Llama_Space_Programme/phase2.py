
import asyncio
import json
import os
import pygame
import random
import math
import global_variables
import audio_manager

# Defines
standardResolution = [1280, 720]
TARGET_DISTANCE = 20000
GAME_FOLDER = os.path.dirname(os.path.abspath(__file__))

def asset_path(*parts):
    return os.path.join(GAME_FOLDER, *parts)

# Phase 2 death state.
game_over = False
death_reason = ""
explosion_sound = None


# --------------------------------------------------
# CHECK THE ITEMS PURCHASED IN PHASE 1
# --------------------------------------------------

def get_purchased_item_names():

    purchased_item_names = []

    # Phase 1 stores purchases in global_variables.inventory.
    # Each item is normally a list, with its name in position zero.

    for item in global_variables.inventory:

        if isinstance(item, (list, tuple)) and len(item) > 0:
            purchased_item_names.append(str(item[0]).strip().lower())

        elif isinstance(item, str):
            purchased_item_names.append(item.strip().lower())

    return purchased_item_names


def has_laser_blaster():
    """Lasers can only be fired after the Phase 1 Laser blaster is bought."""
    return "laser blaster" in get_purchased_item_names()


def check_launch_requirements():

    purchased_item_names = get_purchased_item_names()

    missing_requirements = []

    # Any item with "fuel" in its name counts as purchased rocket fuel.
    has_fuel = False

    for item_name in purchased_item_names:

        if "fuel" in item_name:
            has_fuel = True
            break

    if not has_fuel:
        missing_requirements.append(
            "You did not purchase any rocket fuel."
        )

    # Water storage equipment is not itself a supply of drinking water.
    # Count an actual water purchase, not a tank or recycling system.
    has_water = False

    for item_name in purchased_item_names:

        if item_name == "gallon of water" or "drinking water" in item_name:
            has_water = True
            break

    if not has_water:
        missing_requirements.append(
            "You did not purchase any water."
        )

    # Only a rocket engine counts. The Engine cooling system does not.
    has_rocket_engine = False

    for item_name in purchased_item_names:

        if "rocket engine" in item_name:
            has_rocket_engine = True
            break

    if not has_rocket_engine:
        missing_requirements.append(
            "You did not purchase a rocket engine."
        )

    if len(missing_requirements) == 0:
        return None

    # Put all missing requirements on the same death screen.
    death_message = "Your launch failed. "

    for missing_requirement in missing_requirements:
        death_message += missing_requirement + " "

    return death_message.strip()


# --------------------------------------------------
# STANDARD DEATH SCREEN
# --------------------------------------------------

async def show_death_screen(screen, reason):

    death_font_path = asset_path("ShareTechMono-Regular.ttf")

    title_font = pygame.font.Font(death_font_path, 64)
    reason_font = pygame.font.Font(death_font_path, 23)
    instruction_font = pygame.font.Font(death_font_path, 19)

    death_red = (235, 65, 65)
    background_colour = (8, 7, 10)
    muted_colour = (175, 165, 165)

    screen_width = screen.get_width()
    screen_height = screen.get_height()

    maximum_text_width = screen_width - 180

    # Split the reason into lines that fit the screen.
    reason_lines = []

    for paragraph in str(reason).split("\n"):

        words = paragraph.split()
        current_line = ""

        for word in words:

            if current_line == "":
                test_line = word
            else:
                test_line = current_line + " " + word

            if reason_font.size(test_line)[0] <= maximum_text_width:
                current_line = test_line

            else:
                if current_line != "":
                    reason_lines.append(current_line)

                current_line = word

        if current_line != "":
            reason_lines.append(current_line)

    if len(reason_lines) == 0:
        reason_lines.append("Your mission has ended.")

    clock = pygame.time.Clock()
    waiting_for_exit = True

    while waiting_for_exit:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                waiting_for_exit = False

            elif event.type == pygame.KEYDOWN:
                waiting_for_exit = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                waiting_for_exit = False

        screen.fill(background_colour)

        # Main death heading.
        title_surface = title_font.render(
            "YOU DIED",
            True,
            death_red
        )

        title_rect = title_surface.get_rect(
            center=(screen_width // 2, screen_height // 2 - 105)
        )

        screen.blit(title_surface, title_rect)

        # Red separator lines.
        pygame.draw.line(
            screen,
            death_red,
            (screen_width // 2 - 250, screen_height // 2 - 45),
            (screen_width // 2 + 250, screen_height // 2 - 45),
            2
        )

        # Display the reason beneath the title.
        line_height = reason_font.get_linesize() + 9
        reason_block_height = len(reason_lines) * line_height

        reason_y = (
            screen_height // 2
            - reason_block_height // 2
            + 15
        )

        for reason_line in reason_lines:

            reason_surface = reason_font.render(
                reason_line,
                True,
                death_red
            )

            reason_rect = reason_surface.get_rect(
                center=(screen_width // 2, reason_y)
            )

            screen.blit(reason_surface, reason_rect)

            reason_y += line_height

        instruction_surface = instruction_font.render(
            "PRESS ANY KEY TO EXIT",
            True,
            muted_colour
        )

        instruction_rect = instruction_surface.get_rect(
            center=(screen_width // 2, screen_height - 85)
        )

        screen.blit(instruction_surface, instruction_rect)

        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)

# Pygame groups
bulletGroup = pygame.sprite.Group()
asteroidGroup = pygame.sprite.Group()
explosionGroup = pygame.sprite.Group()

class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y, angle, offset):
        super().__init__()

        self.angle = angle

        self.image = pygame.image.load(asset_path("Images", "8_BitBullet.png"))
        self.image = pygame.transform.scale(self.image, (20, 10))
        self.image = pygame.transform.rotate(self.image, -(angle+90))

        self.rect = self.image.get_rect(center=(x, y))

        # Store the actual starting position
        self.position = pygame.Vector2(x+offset*math.sin(math.radians(angle)),
                                        y-offset*math.cos(math.radians(angle)))

        # Calculate direction
        self.direction = pygame.Vector2(
            math.sin(math.radians(angle)),
            -math.cos(math.radians(angle))
        )

        self.speed = 500

        self.lastTime = pygame.time.get_ticks() / 1000

    def evolve(self):

        currentTime = pygame.time.get_ticks() / 1000

        dt = currentTime - self.lastTime
        self.lastTime = currentTime

        # Update position
        self.position += self.direction * self.speed * dt

        self.rect.center = self.position

        # Detect if out of bounds
        if not pygame.Rect(0, 0, 1280, 720).colliderect(self.rect):
            self.kill()

    def render(self, surface):
        surface.blit(self.image, self.rect)

# NOTE: Time evolve before doing key positions.
class Rocket(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load(
            asset_path("Images", "Ship For movement.png")
        ).convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 200))

        self.unrotatedImage = self.image
        self.rect = self.image.get_rect(center=(640, 360))
        self.position = pygame.Vector2(self.rect.center)

        # Maximum rotation
        self.maxRotation = 70

        # Standard speed limits.
        self.minVelocity = 10
        self.maxVelocity = 500

        # The Heavy-duty rocket engine gives the rocket 20% more speed
        # at both the minimum and maximum ends of its speed range.
        purchased_item_names = get_purchased_item_names()

        if "heavy-duty rocket engine" in purchased_item_names:
            self.minVelocity = self.minVelocity * 1.2
            self.maxVelocity = self.maxVelocity * 1.2

        self.angle = 0

        self.velocity = self.minVelocity
        self.vx = 0
        self.vy = -self.minVelocity

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.rocketTime = pygame.time.get_ticks()/1000
        self.dt = 0

        self.dist_travelled = 0

        self.maxLives = 3
        self.lives = self.maxLives
        self.inVuln = False
        self.inVulnTime = 0
        self.inVulnDuration = 1.5

        self.mask = pygame.mask.from_surface(self.image)

    # -1 direction is left, 1 direction is right
    def increaseAngle(self, direction):

        self.angle += 50*direction*self.dt

        # NOTICE: this requires the increase to only happen in the violating direction
        # it is a bit hacky but shouldn't fail.
        if abs(self.angle) > self.maxRotation:
            self.angle = self.maxRotation * direction

        # Re-calculate the velocities in each direction.

        self.vx = self.velocity * math.sin(math.radians(self.angle))
        self.vy = -self.velocity * math.cos(math.radians(self.angle))


        self.image = pygame.transform.rotate(
            self.unrotatedImage,
            -self.angle
        )

        self.rect = self.image.get_rect(center=self.position)

        self.mask = pygame.mask.from_surface(self.image)

    def timeEvolve(self):

        newTime = pygame.time.get_ticks()/1000

        self.dt = newTime - self.rocketTime
        self.rocketTime = newTime

        #self.position.x += self.dt * self.vx
        #self.position.y += self.dt * self.vy

        self.rect.center = self.position

        self.dist_travelled += -self.vy * self.dt

    def accelerate(self, direction):
        self.velocity += 50*self.dt*direction

        if self.velocity < self.minVelocity:
            self.velocity = self.minVelocity
        elif self.velocity > self.maxVelocity:
            self.velocity = self.maxVelocity

        self.vx = self.velocity * math.sin(math.radians(self.angle))
        self.vy = -self.velocity * math.cos(math.radians(self.angle))

    def shootBullet(self):

        newBullet = Bullet(self.rect.centerx, self.rect.centery, self.angle, 100)
        bulletGroup.add(newBullet)


    def takeDamage(self):

        global game_over
        global death_reason

        if self.inVuln or game_over:
            return

        self.lives -= 1

        self.inVuln = True
        self.inVulnTime = 0

        if self.lives <= 0:

            game_over = True

            if "emergency escape system" in get_purchased_item_names():
                death_reason = (
                    "Your rocket was destroyed after taking too much "
                    "asteroid damage. You activated the emergency escape "
                    "system and escaped death by ejecting into the cold "
                    "vacuum of space. Unfortunately, the sudden "
                    "decompression caused the poo inside you to explode "
                    "your insides. What a dreadful way to go."
                )
            else:
                death_reason = (
                    "Your rocket was destroyed after taking too much "
                    "asteroid damage. You ran out of lives."
                )


    def updateInVuln(self, dt):

        if not self.inVuln:
            return

        self.inVulnTime += dt

        if self.inVulnTime >= self.inVulnDuration:
            self.inVuln = False
            self.inVulnTime = 0

    def renderRocket(self, surface):

        surface.blit(self.image, self.rect)


class Asteroid(pygame.sprite.Sprite):

    # Placeholders
    asteroidImgList = ["asteroid1.png", "asteroid2.png", "asteroid3.png", "asteroid4.png"]
    asteroidSizeList = [(60, 90), (70, 60), (55, 70), (62, 58)]

    def __init__(self, asteroidPos):
        super().__init__()

        randImg = random.randint(0,len(self.asteroidImgList)-1)

        self.image = pygame.image.load(
            asset_path("Images", self.asteroidImgList[randImg])
        ).convert_alpha()

        self.image = pygame.transform.scale(
            self.image,
            self.asteroidSizeList[randImg]
        )

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect(center=asteroidPos)
        self.position = pygame.Vector2(asteroidPos)

    def evolve(self, rocket, dt):

        self.position.x -= rocket.vx * dt
        self.position.y -= rocket.vy * dt

        self.rect.center = self.position

        if not pygame.Rect(-400, -400, 2080, 1520).colliderect(self.rect):
            self.kill()


    def explode():
        pass

    def render(self, surface):
        surface.blit(self.image, self.rect)

class GifAnimation:

    def __init__(self, frames_folder, scale=1):
        """Load pre-extracted PNG frames without a browser-incompatible dependency."""

        duration_path = os.path.join(frames_folder, "durations.json")

        with open(duration_path, "r", encoding="utf-8") as duration_file:
            frame_durations_ms = json.load(duration_file)

        frame_filenames = sorted(
            filename
            for filename in os.listdir(frames_folder)
            if filename.lower().endswith(".png")
        )

        if not frame_filenames:
            raise RuntimeError("No PNG animation frames found in: " + frames_folder)

        if len(frame_filenames) != len(frame_durations_ms):
            raise RuntimeError("Animation frame timings do not match the PNG frames in: " + frames_folder)

        self.frames = []
        self.durations = []

        for frame_index, frame_filename in enumerate(frame_filenames):
            frame_path = os.path.join(frames_folder, frame_filename)
            frame_surface = pygame.image.load(frame_path).convert_alpha()

            scaled_width = max(1, int(frame_surface.get_width() * scale))
            scaled_height = max(1, int(frame_surface.get_height() * scale))

            frame_surface = pygame.transform.scale(
                frame_surface,
                (scaled_width, scaled_height)
            )

            self.frames.append(frame_surface)
            self.durations.append(frame_durations_ms[frame_index] / 1000)
class Explosion(pygame.sprite.Sprite):

    def __init__(self, position, animation):
        super().__init__()

        self.position = pygame.Vector2(position)
        self.animation = animation

        self.currentFrame = 0
        self.frameTime = 0

        self.image = self.animation.frames[0]

        self.rect = self.image.get_rect(
            center=position
        )

    def evolve(self, dt):

        self.frameTime += dt

        while self.frameTime >= self.animation.durations[self.currentFrame]:

            self.frameTime -= self.animation.durations[self.currentFrame]

            self.currentFrame += 1

            if self.currentFrame >= len(self.animation.frames):
                self.kill()
                return

            self.image = self.animation.frames[self.currentFrame]

            self.rect = self.image.get_rect(
                center=self.position
            )

    def render(self, surface):
        surface.blit(self.image, self.rect)

class HUD:

    def __init__(self):

        pygame.font.init()

        self.font = pygame.font.Font(None, 36)
        self.smallFont = pygame.font.Font(None, 24)

        self.white = (255, 255, 255)
        self.grey = (180, 180, 180)

        self.heartFull = pygame.image.load(
            asset_path("Images", "fullHeart.jpg")
        ).convert_alpha()

        self.heartEmpty = pygame.image.load(
            asset_path("Images", "emptyHeart.jpg")
        ).convert_alpha()

        self.heartFull = pygame.transform.scale(
            self.heartFull, (35, 35)
        )

        self.heartEmpty = pygame.transform.scale(
            self.heartEmpty, (35, 35)
        )

    def renderLives(self, surface, rocket):

        for i in range(rocket.maxLives):

            if i < rocket.lives:
                heart = self.heartFull
            else:
                heart = self.heartEmpty

            x = surface.get_width() - 20 - (i + 1) * 45

            surface.blit(heart, (x, 20))

    def render(self, surface, rocket, laser_equipped=False):

        # Distance to the 25 km destination.
        distanceText = self.font.render(
            f"Distance: {int(rocket.dist_travelled)} /{TARGET_DISTANCE:,} m",
            True,
            self.white
        )

        # Velocity
        velocityText = self.smallFont.render(
            f"Velocity: {int(rocket.velocity)} m/s",
            True,
            self.grey
        )

        # Display in top-left corner
        surface.blit(distanceText, (20, 20))
        surface.blit(velocityText, (20, 60))

        if laser_equipped:
            laser_message = "LASER READY - SPACE TO FIRE"
            laser_colour = (130, 235, 170)
        else:
            laser_message = "NO LASER - BUY A LASER BLASTER IN ELECTRONICS"
            laser_colour = (255, 145, 110)

        laserText = self.smallFont.render(laser_message, True, laser_colour)
        surface.blit(laserText, (20, 94))

        controlsText = self.smallFont.render(
            "STEER: A/D OR LEFT/RIGHT   THRUST: W/UP   SLOW: S/DOWN",
            True,
            self.grey
        )
        surface.blit(controlsText, (20, 124))

        self.renderLives(surface, rocket)


def spawn_asteroids_initially(rocket):

    numAsteroids = random.randint(15, 25)

    maxAttempts = 1000

    for i in range(numAsteroids):

        asteroidSpawned = False

        for attempt in range(maxAttempts):

            asteroidPos = (
                random.randint(0, 1280),
                random.randint(0, 720)
            )

            newAsteroid = Asteroid(asteroidPos)

            # Check collision with rocket
            if newAsteroid.rect.colliderect(
                rocket.rect.inflate(20, 20)
            ):
                continue

            # Check collision with existing asteroids
            collidingWithAsteroid = False

            for asteroid in asteroidGroup:

                if newAsteroid.rect.colliderect(
                    asteroid.rect.inflate(10, 10)
                ):
                    collidingWithAsteroid = True
                    break

            if collidingWithAsteroid:
                continue

            # Valid position found!
            asteroidGroup.add(newAsteroid)
            asteroidSpawned = True
            break

def spawn_asteroids_ahead(rocket, targetCount=20):

    direction = pygame.Vector2(rocket.vx, rocket.vy)

    if direction.length() == 0:
        return

    direction = direction.normalize()
    perpendicular = pygame.Vector2(-direction.y, direction.x)

    centre = pygame.Vector2(640, 360)

    halfForward = (
        abs(direction.x) * 640 +
        abs(direction.y) * 360
    )

    halfPerpendicular = (
        abs(perpendicular.x) * 640 +
        abs(perpendicular.y) * 360
    )

    # Calculate how many asteroids need spawning
    missingAsteroids = targetCount - len(asteroidGroup)

    for i in range(missingAsteroids):

        for attempt in range(100):

            forwardDistance = halfForward + random.randint(80, 200)

            sideDistance = random.uniform(
                -halfPerpendicular,
                halfPerpendicular
            )

            asteroidPos = (
                centre +
                direction * forwardDistance +
                perpendicular * sideDistance
            )

            newAsteroid = Asteroid(asteroidPos)

            colliding = False

            for asteroid in asteroidGroup:

                if newAsteroid.rect.colliderect(
                    asteroid.rect.inflate(20, 20)
                ):
                    colliding = True
                    break

            if colliding:
                continue

            asteroidGroup.add(newAsteroid)
            break

async def graphics_init(screen):

    global game_over
    global death_reason
    global TARGET_DISTANCE

    # The display is supplied by main.py and is reused by every phase.

    # The navigational computer makes the journey shorter and easier.
    # Without it, the rocket must travel an extra 5,000 metres.
    purchased_item_names = get_purchased_item_names()

    if "navigational computer" in purchased_item_names:
        TARGET_DISTANCE = 20000
    else:
        TARGET_DISTANCE = 25000

    # Check the Phase 1 purchases before starting the flight.
    launch_failure_reason = check_launch_requirements()

    if launch_failure_reason is not None:

        # Store the failure state so run_phase2() displays the death screen.
        death_reason = launch_failure_reason
        game_over = True

        print("[PHASE 2] LAUNCH CHECK FAILED")
        print("[PHASE 2] Purchased items:", purchased_item_names)
        print("[PHASE 2] Reason:", launch_failure_reason)

        return False

    print("[PHASE 2] Launch requirements satisfied.")
    print("[PHASE 2] Purchased items:", purchased_item_names)

    # Only start the music once the launch requirements are met.
    audio_manager.start_music(
        asset_path("Audio", "bgMusic.ogg"),
        volume=0.60,
        loops=-1
    )

    # Load the impact sound once, not every time an asteroid is destroyed.
    global explosion_sound
    explosion_sound = audio_manager.load_sound(
        asset_path("Audio", "explosionSound.ogg"),
        volume=0.8
    )

    asteroidExplosionAnimations = [

    GifAnimation(asset_path("Images", "explosion1_frames"), 0.4),
    GifAnimation(asset_path("Images", "explosion3_frames"), 0.4)
    ]



    # Create base resolution surface
    baseScreen = pygame.Surface(standardResolution)

    # Load image ONCE
    player = pygame.image.load(
        asset_path("Images", "Ship For movement.png")
    ).convert_alpha()

    bullets=[]
    # Generate stars ONCE
    pixelWhite = []

    for i in range(1500):
        x = random.randrange(1280)
        y = random.randrange(720)

        colour = (
            random.randint(100, 255),
            random.randint(100, 255),
            random.randint(100, 255)
        )

        pixelWhite.append((x, y, colour))


        

    running = True
    window_closed = False

    clock = pygame.time.Clock()

    def speedscale(t):
        return 5 + 10*t

    moveStartTimeUp = None
    moveStartTimeDown = None
    moveStartTimeLeft = None
    moveStartTimeRight = None

    testRocketClass = Rocket()

    hud = HUD()
    laser_equipped = has_laser_blaster()

    shootCooldown = 0.5
    laserShotTime = 0

    spawn_asteroids_initially(testRocketClass)
    distanceSinceSpawn = 0
    spawnDistance = 350

    targetAsteroidCount = 20
    spawnDistance = 100
    distanceSinceSpawn = 0
    
    # Game loop
    # The loop ends when the player closes the window, reaches 25 km,
    # or loses all three lives.
    while running and not game_over:

        # Events
        # Events
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                window_closed = True
                running = False

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_n:
                    print("Phase 2 skipped.")
                    running = False

        # Keyboard input
        keys = pygame.key.get_pressed()



        # Get current window size
        viewportSize = screen.get_size()

        # Draw everything onto base surface
        baseScreen.fill((0, 0, 0))

        # Draw stars
        for x, y, colour in pixelWhite:
            baseScreen.set_at((x, y), colour)


        # Scale base surface to window size
        scaledSurface = pygame.transform.scale(
            baseScreen,
            viewportSize
        )

        # Both WASD and arrow keys control steering and throttle.
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            testRocketClass.increaseAngle(-1)

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            testRocketClass.increaseAngle(1)

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            testRocketClass.accelerate(1)

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            testRocketClass.accelerate(-1)

        testRocketClass.timeEvolve()

        testRocketClass.updateInVuln(testRocketClass.dt)


        if testRocketClass.dist_travelled >= TARGET_DISTANCE:
            running = False

        # Track how far the rocket has travelled
        distanceSinceSpawn += (
            testRocketClass.velocity * testRocketClass.dt
        )

        if distanceSinceSpawn >= spawnDistance:

            spawn_asteroids_ahead(
                testRocketClass,
                targetAsteroidCount
            )

            distanceSinceSpawn -= spawnDistance

        for asteroid in asteroidGroup:
            asteroid.evolve(testRocketClass, testRocketClass.dt)
            asteroid.render(scaledSurface)

        for bullet in bulletGroup:
            bullet.evolve()
            bullet.render(scaledSurface)

        for explosion in explosionGroup:

            explosion.evolve(testRocketClass.dt)
            explosion.render(scaledSurface)

        testRocketClass.renderRocket(scaledSurface)

        explodedAsteroids = pygame.sprite.groupcollide(
            bulletGroup,
            asteroidGroup,
            True,
            True
        )

        for bullet, asteroids in explodedAsteroids.items():

            for asteroid in asteroids:

                animation = random.choice(
                    asteroidExplosionAnimations
                )

                audio_manager.play_sound(explosion_sound)

                explosionGroup.add(
                    Explosion(
                        asteroid.position,
                        animation
                    )
                )

        if not testRocketClass.inVuln:
            rocketCollisions = pygame.sprite.spritecollide(
                testRocketClass,
                asteroidGroup,
                True,
                pygame.sprite.collide_mask
            )

            if rocketCollisions:
                testRocketClass.takeDamage()
        
        
        # Shooting
        currentTime = pygame.time.get_ticks() / 1000

        if laser_equipped and keys[pygame.K_SPACE]:

            if currentTime - laserShotTime >= shootCooldown:
                testRocketClass.shootBullet()
                laserShotTime = currentTime

        hud.render(scaledSurface, testRocketClass, laser_equipped)

        # Draw scaled surface onto display
        screen.blit(scaledSurface, (0, 0))

        # Update display
        pygame.display.flip()

        clock.tick(60)
        await asyncio.sleep(0)

    return not window_closed and not game_over


async def run_phase2(screen_surface):
    """Run rocket flight on the already-created shared Pygame display."""
    global game_over, death_reason

    game_over = False
    death_reason = ""
    bulletGroup.empty()
    asteroidGroup.empty()
    explosionGroup.empty()

    phase_completed = await graphics_init(screen_surface)

    if game_over:
        await show_death_screen(screen_surface, death_reason)
        return False

    if not phase_completed:
        return False

    audio_manager.stop_music(fade_ms=500)
    print("Phase 2 finished.")
    return True
