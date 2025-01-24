import pygame, random, os

pygame.init()
pygame.mixer.init()

# --- Screen Setup ---
SCREEN_WIDTH, SCREEN_HEIGHT = 1250, 640
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hangman with Audience")

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0,   0,   0)
RED   = (220, 20,  60)
GREEN = (50,  205, 50)
BLUE  = (70,  130, 180)

# --- Fonts ---
FONT       = pygame.font.SysFont('Arial', 50)
SMALL_FONT = pygame.font.SysFont('Arial', 35)

# --- Sound files (optional) ---
win_sound_file  = "win_sound.mp3"
lose_sound_file = "lose_sound.mp3"

# --- Background & Animation Sprites ---
# Provide your own images for these
try:
    background_img = pygame.image.load("background.jpg").convert()
except:
    background_img = None  # fallback if no file found

# Load a few frames for the crowd animation, e.g. crowd_0.png, crowd_1.png, crowd_2.png
crowd_frames = []
for i in range(3):  # Adjust to however many frames you have
    fname = f"crowd_{i}.png"
    if os.path.isfile(fname):
        img = pygame.image.load(fname).convert_alpha()
        crowd_frames.append(img)

# If you have no images, crowd_frames stays empty. We'll handle that gracefully.

# -----------------------
#  Loading & Saving
# -----------------------
def load_words():
    with open("mots.txt", "r") as f:
        return [line.strip() for line in f]

def save_score(name, score):
    with open("scores.txt", "a") as f:
        f.write(f"{name} {score}\n")

def show_scores():
    win.fill(WHITE)
    y = 50
    try:
        with open("scores.txt", "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = []
    scores = []
    for ln in lines:
        parts = ln.split()
        if len(parts) == 2 and parts[1].isdigit():
            scores.append((parts[0], int(parts[1])))
    scores.sort(key=lambda x: x[1], reverse=True)
    for name, val in scores[:5]:
        txt = SMALL_FONT.render(f"{name}: {val}", True, BLACK)
        win.blit(txt, (SCREEN_WIDTH // 2 - 80, y))
        y += 30
    pygame.display.update()
    pygame.time.wait(2000)

# -----------------------
#  Drawing Helpers
# -----------------------
def draw_text(text, font, color, x, y):
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(x, y))
    win.blit(surf, rect)

def draw_hangman(errors):
    # Base
    if errors >= 1:
        pygame.draw.line(win, RED, (150, 550), (250, 550), 5)  # ground
        pygame.draw.line(win, RED, (200, 550), (200, 150), 5)  # vertical
        pygame.draw.line(win, RED, (200, 150), (350, 150), 5)  # top horizontal
        pygame.draw.line(win, RED, (350, 150), (350, 200), 5)  # rope
    # Body
    if errors >= 2: pygame.draw.circle(win, WHITE, (350, 230), 30, 3)       # head
    if errors >= 3: pygame.draw.line(win, WHITE, (350, 260), (350, 340), 3) # torso
    if errors >= 4: pygame.draw.line(win, WHITE, (350, 280), (310, 320), 3) # left arm
    if errors >= 5: pygame.draw.line(win, WHITE, (350, 280), (390, 320), 3) # right arm
    if errors >= 6: pygame.draw.line(win, WHITE, (350, 340), (380, 400), 3) # right leg
    if errors >= 6: pygame.draw.line(win, WHITE, (350, 340), (380, 400), 3) # left leg

def draw_missed_letters(missed):
    txt = SMALL_FONT.render("Lettres ratées: " + " ".join(missed), True, RED)
    win.blit(txt, (20, SCREEN_HEIGHT - 50))

def draw_background():
    # If we have a background image, draw it first
    if background_img:
        win.blit(background_img, (0, 0))
    else:
        # Fallback: just fill with a color if no background
        win.fill((235, 235, 235))

# -----------------------
#  Crowd Animation
# -----------------------
def draw_crowd_animation(frame_index):
    """
    Draw the current frame of the crowd animation.
    We'll place them near the bottom or sides, whichever you prefer.
    """
    if crowd_frames:
        # Use modulo to cycle through frames
        idx = frame_index % len(crowd_frames)
        frame = crowd_frames[idx]

        # Example: draw crowd at the bottom-left
        # Adjust the position as needed
        win.blit(frame, (50, SCREEN_HEIGHT - frame.get_height() - 50))

# -----------------------
#  Player Name Input
# -----------------------
def get_player_name():
    name = ""
    active = True
    while active:
        draw_background()
        draw_text("Entrez votre nom et appuyez sur Entrée:", SMALL_FONT, RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
        draw_text(name, FONT, BLUE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    active = False
                elif e.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += e.unicode
    return name if name else "Player"

# -----------------------
#  Game Logic
# -----------------------
def start_game():
    word = random.choice(load_words())
    return word, ["_"] * len(word), 0, [], []

def game_loop(player_name):
    clock = pygame.time.Clock()
    word, guessed, errors, guessed_letters, missed_letters = start_game()

    # We'll animate the crowd by cycling frames
    crowd_frame = 0

    while True:
        # 1) Draw the background
        draw_background()

        # 2) Draw the crowd with current frame
        draw_crowd_animation(crowd_frame)

        # 3) Then proceed with hangman + UI
        draw_text("PENDU", FONT, RED, SCREEN_WIDTH // 2, 70)
        draw_text(" ".join(guessed), FONT, RED, SCREEN_WIDTH // 2, 300)
        draw_text(f"Joueur: {player_name}", SMALL_FONT, RED, SCREEN_WIDTH // 2, 130)
        draw_hangman(errors)
        draw_missed_letters(missed_letters)

        # Check lose condition
        if errors >= 7:
            draw_text("Perdu!", FONT, RED, SCREEN_WIDTH // 2, 420)
            pygame.display.update()
            if os.path.isfile(lose_sound_file):
                pygame.mixer.music.load(lose_sound_file)
                pygame.mixer.music.play()
            save_score(player_name, 0)
            pygame.time.wait(1500)
            break

        # Check win condition
        if "_" not in guessed:
            draw_text("Gagné!", FONT, GREEN, SCREEN_WIDTH // 2, 420)
            pygame.display.update()
            if os.path.isfile(win_sound_file):
                pygame.mixer.music.load(win_sound_file)
                pygame.mixer.music.play()
            score = len([g for g in guessed if g != "_"])
            save_score(player_name, score)
            pygame.time.wait(1500)
            break

        # Handle events
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return
                letter = pygame.key.name(e.key)
                if letter.isalpha() and letter not in guessed_letters:
                    guessed_letters.append(letter)
                    if letter in word:
                        for i, char in enumerate(word):
                            if char == letter:
                                guessed[i] = letter
                    else:
                        errors += 1
                        missed_letters.append(letter)

        # Update the crowd animation index
        crowd_frame += 1

        pygame.display.update()
        clock.tick(10)

def main_menu():
    while True:
        draw_background()
        draw_text("Hangman Du 13", FONT, RED, SCREEN_WIDTH // 2, 150)
        draw_text("1. Jouer", SMALL_FONT, RED, SCREEN_WIDTH // 2, 420)
        draw_text("2. Scores", SMALL_FONT, RED, SCREEN_WIDTH // 2, 470)
        draw_text("3. Quitter", SMALL_FONT, RED, SCREEN_WIDTH // 2, 520)
        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_1:
                    name = get_player_name()
                    game_loop(name)
                elif e.key == pygame.K_2:
                    show_scores()
                elif e.key == pygame.K_3:
                    pygame.quit()
                    quit()

if __name__ == "__main__":
    main_menu()
