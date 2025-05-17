import pygame
import random
import time
import sys
import math

# --- Game Settings ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TARGET_SIZE = 50
TARGET_COLOR = (255, 0, 0)
PLAYER_COLOR = (0, 0, 255)
BULLET_COLOR = (0, 255, 0)
BULLET_SPEED = 15
TARGET_SPEED_BASE = 2
TARGET_SPAWN_RATE_BASE = 1.0  # Targets per second
DIFFICULTY_SMOOTHING_INCREASE = 0.02  # Smaller increase step
DIFFICULTY_SMOOTHING_DECREASE = 0.02  # Slightly larger decrease step for more noticeable effect
MAX_DIFFICULTY = 5.0  # Increased maximum difficulty
MIN_DIFFICULTY = 1.0  # Minimum difficulty (starting point)
TARGET_MISS_PENALTY = 0.01  # Amount to decrease difficulty per missed target
MAX_TARGETS = 15
PLAYER_LIVES = 3  # New setting for game over

# --- Global Variables ---
lives = PLAYER_LIVES
game_over = False

# --- Player Performance Tracking ---
SHOTS_TRACKED = 15
hit_history = []
shot_times = []
last_target_spawn_time = time.time()
consecutive_hits = 0
consecutive_misses = 0

# --- Difficulty Parameters (Initial Values) ---
difficulty_level = 1.0
target_speed = TARGET_SPEED_BASE
target_spawn_interval = 1.0 / TARGET_SPAWN_RATE_BASE

# --- High Score ---
HIGH_SCORE_FILE = "highscore.txt"
try:
    with open(HIGH_SCORE_FILE, "r") as f:
        high_score = int(f.read())
except FileNotFoundError:
    high_score = 0
except ValueError:
    high_score = 0

# --- Pygame Initialization ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dynamic Difficulty Shooter")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)

# --- Game Objects ---
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT - 50
player_size = 40
bullets = []
targets = []
score = 0
lives = PLAYER_LIVES
game_over = False

# --- Difficulty Selection Screen ---
def show_difficulty_menu():
    while True:
        screen.fill((0, 0, 0))
        title_text = large_font.render("Select Difficulty", True, (255, 255, 255))
        easy_text = font.render("1. Easy", True, (0, 255, 0))
        medium_text = font.render("2. Medium", True, (255, 255, 0))
        hard_text = font.render("3. Hard", True, (255, 0, 0))

        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        easy_rect = easy_text.get_rect(center=(SCREEN_WIDTH // 2, 250))
        medium_rect = medium_text.get_rect(center=(SCREEN_WIDTH // 2, 300))
        hard_rect = hard_text.get_rect(center=(SCREEN_WIDTH // 2, 350))

        screen.blit(title_text, title_rect)
        screen.blit(easy_text, easy_rect)
        screen.blit(medium_text, medium_rect)
        screen.blit(hard_text, hard_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 1.0
                elif event.key == pygame.K_2:
                    return 2.0
                elif event.key == pygame.K_3:
                    return 3.0

initial_difficulty = show_difficulty_menu()
difficulty_level = initial_difficulty

class Target:
    def __init__(self, x, y, speed, difficulty):
        self.x = x
        self.y = y
        self.speed = speed
        self.initial_y = y
        self.movement_type = random.randint(0, min(2, int(difficulty))) # More complex movement at higher difficulty
        self.amplitude = 20 + difficulty * 5
        self.frequency = 0.02 + difficulty * 0.005
        self.time_offset = random.random() * math.pi * 2

    def update(self):
        if self.movement_type == 1: # Horizontal sine wave
            self.x += math.sin(pygame.time.get_ticks() * self.frequency + self.time_offset) * self.amplitude * 0.1
        elif self.movement_type == 2: # Diagonal movement
            self.x += self.speed * 0.3 * (1 if random.random() > 0.5 else -1)

        self.y += self.speed
        if self.y > SCREEN_HEIGHT + TARGET_SIZE // 2:
            return True
        return False

    def draw(self, surface):
        pygame.draw.rect(surface, TARGET_COLOR, (int(self.x) - TARGET_SIZE // 2, int(self.y) - TARGET_SIZE // 2, TARGET_SIZE, TARGET_SIZE))

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        self.y -= BULLET_SPEED
        return self.y < 0

    def draw(self, surface):
        pygame.draw.rect(surface, BULLET_COLOR, (self.x - 5, self.y - 10, 10, 20))

def update_difficulty():
    global difficulty_level, target_speed, target_spawn_interval

    hit_rate = sum(hit_history) / len(hit_history) if hit_history else 0
    avg_reaction_time = sum(shot_times) / len(shot_times) if shot_times else float('inf')

    difficulty_adjustment = 0

    # Adjust difficulty based on hit rate
    if hit_rate > 0.8:
        difficulty_adjustment += DIFFICULTY_SMOOTHING_INCREASE
    elif hit_rate < 0.4:
        difficulty_adjustment -= DIFFICULTY_SMOOTHING_DECREASE

    # Adjust difficulty based on reaction time
    if avg_reaction_time < 0.3 and hit_history:
        difficulty_adjustment += DIFFICULTY_SMOOTHING_INCREASE
    elif avg_reaction_time > 0.8:
        difficulty_adjustment -= DIFFICULTY_SMOOTHING_DECREASE

    # Adjust difficulty based on consecutive hits/misses from shots fired
    if consecutive_hits >= 5:
        difficulty_adjustment += 0.005 * consecutive_hits
    elif consecutive_misses >= 3:
        difficulty_adjustment -= 0.01 * consecutive_misses

    # Apply the calculated adjustment to the difficulty level
    difficulty_level += difficulty_adjustment

    # Ensure difficulty level stays within the defined bounds
    difficulty_level = max(MIN_DIFFICULTY, min(MAX_DIFFICULTY, difficulty_level))

    # Update game parameters based on the new difficulty level
    target_speed = TARGET_SPEED_BASE * difficulty_level
    target_spawn_interval = max(0.1, 1.0 / (TARGET_SPAWN_RATE_BASE * difficulty_level))

def reset_performance_metrics():
    global hit_history, shot_times, consecutive_hits, consecutive_misses
    hit_history = []
    shot_times = []
    consecutive_hits = 0
    consecutive_misses = 0

def display_info():
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    difficulty_text = font.render(f"Difficulty: {difficulty_level:.2f}", True, (255, 255, 255))
    screen.blit(difficulty_text, (10, 40))

def reset_game():
    global targets, bullets, score, lives, game_over, hit_history, shot_times, consecutive_hits, consecutive_misses, difficulty_level
    targets = []
    bullets = []
    score = 0
    lives = PLAYER_LIVES
    game_over = False
    hit_history = []
    shot_times = []
    consecutive_hits = 0
    consecutive_misses = 0
    difficulty_level = initial_difficulty # Reset to the initially chosen difficulty

# --- Game Over Screen ---
def show_game_over():
    global high_score
    if score > high_score:
        high_score = score
        try:
            with open(HIGH_SCORE_FILE, "w") as f:
                f.write(str(high_score))
        except IOError:
            print("Error saving high score!")

    while True:
        screen.fill((0, 0, 0))
        game_over_text = large_font.render("Game Over", True, (255, 0, 0))
        score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
        high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
        retry_text = font.render("Press 'R' to Retry", True, (255, 255, 255))
        quit_text = font.render("Press 'Q' to Quit", True, (255, 255, 255))

        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 250))
        high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, 300))
        retry_rect = retry_text.get_rect(center=(SCREEN_WIDTH // 2, 400))
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, 450))

        screen.blit(game_over_text, game_over_rect)
        screen.blit(score_text, score_rect)
        screen.blit(high_score_text, high_score_rect)
        screen.blit(retry_text, retry_rect)
        screen.blit(quit_text, quit_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                    return
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# --- Update and Draw Lives ---
def display_lives():
    lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
    screen.blit(lives_text, (SCREEN_WIDTH - 100, 10))
    
# --- Update and Draw High Score ---
def display_high_score():
    high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
    screen.blit(high_score_text, (10, SCREEN_HEIGHT - 40))

# --- Game Loop ---
running = True
while running:
    if not game_over:
        screen.fill((0, 0, 0))
        current_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                bullet = Bullet(player_x, player_y)
                bullets.append(bullet)
                shot_start_time = current_time

        # Player Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= 5
        if keys[pygame.K_RIGHT]:
            player_x += 5
        player_x = max(player_size // 2, min(SCREEN_WIDTH - player_size // 2, player_x))

        # Target Spawning
        if len(targets) < MAX_TARGETS and current_time - last_target_spawn_time > target_spawn_interval:
            target_x = random.randint(TARGET_SIZE // 2, SCREEN_WIDTH - TARGET_SIZE // 2)
            target_speed_adjusted = TARGET_SPEED_BASE * difficulty_level
            target = Target(target_x, -TARGET_SIZE // 2, target_speed_adjusted, difficulty_level)
            targets.append(target)
            last_target_spawn_time = current_time

        # Update and Draw Targets
        new_targets = []
        for target in targets:
            if not target.update():
                target.draw(screen)
                new_targets.append(target)
            else:
                # Target went off-screen (missed) - Decrease difficulty
                if len(hit_history) == SHOTS_TRACKED:
                    hit_history.pop(0)
                hit_history.append(0)
                consecutive_misses += 1
                consecutive_hits = 0
                difficulty_level -= TARGET_MISS_PENALTY
                difficulty_level = max(MIN_DIFFICULTY, min(MAX_DIFFICULTY, difficulty_level))
                update_difficulty()
        targets = new_targets

        # Update and Draw Bullets
        new_bullets = []
        for bullet in bullets:
            if not bullet.update():
                bullet.draw(screen)
                new_bullets.append(bullet)
        bullets = new_bullets

        # Collision Detection (Target hits Player)
        player_rect = pygame.Rect(player_x - player_size // 2, player_y - player_size // 2, player_size, player_size)
        for target in list(targets):
            target_rect = pygame.Rect(target.x - TARGET_SIZE // 2, target.y - TARGET_SIZE // 2, TARGET_SIZE, TARGET_SIZE)
            if player_rect.colliderect(target_rect):
                lives -= 1
                targets.remove(target) # Remove the hitting target
                if lives <= 0:
                    game_over = True

        # Collision Detection (Bullet hits Target)
        for target in list(targets):
            for bullet in list(bullets):
                if (bullet.x > target.x - TARGET_SIZE // 2 and bullet.x < target.x + TARGET_SIZE // 2 and
                        bullet.y > target.y - TARGET_SIZE // 2 and bullet.y < target.y + TARGET_SIZE // 2):
                    score += 1
                    targets.remove(target)
                    bullets.remove(bullet)
                    hit_history.append(1)
                    shot_times.append(current_time - shot_start_time)
                    consecutive_hits += 1
                    consecutive_misses = 0
                    if len(hit_history) > SHOTS_TRACKED:
                        hit_history.pop(0)
                        shot_times.pop(0)
                    update_difficulty()
                    break

        # Draw Player
        pygame.draw.rect(screen, PLAYER_COLOR, (player_x - player_size // 2, player_y - player_size // 2, player_size, player_size))

        # Display Game Information
        display_info()
        display_lives()
        display_high_score()

        pygame.display.flip()
        clock.tick(60)
    else:
        show_game_over()

pygame.quit()
sys.exit()