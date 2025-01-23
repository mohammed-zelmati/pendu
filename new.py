import pygame, random, os

pygame.init()
pygame.mixer.init()

# --- Screen Setup ---
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hangman")

# --- Colors (brighter contrasts) ---
WHITE = (255, 255, 255)
BLACK = (0,   0,   0)
RED   = (220, 20,  60)
GREEN = (50,  205, 50)
BLUE  = (70,  130, 180)

# --- Fonts ---
FONT       = pygame.font.SysFont('Arial', 40)
SMALL_FONT = pygame.font.SysFont('Arial', 25)

# --- Sound files (optional) ---
win_sound_file  = "win_sound.mp3"
lose_sound_file = "lose_sound.mp3"

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
        win.blit(txt, (SCREEN_WIDTH//2 - 80, y))
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
    if errors >= 1:
        pygame.draw.line(win, BLACK, (150, 550), (250, 550), 5)
        pygame.draw.line(win, BLACK, (200, 550), (200, 150), 5)
        pygame.draw.line(win, BLACK, (200, 150), (350, 150), 5)
        pygame.draw.line(win, BLACK, (350, 150), (350, 200), 5)
    if errors >= 2: pygame.draw.circle(win, BLACK, (350, 230), 30, 3)
    if errors >= 3: pygame.draw.line(win, BLACK, (350, 260), (350, 340), 3)
    if errors >= 4: pygame.draw.line(win, BLACK, (350, 280), (310, 320), 3)
    if errors >= 5: pygame.draw.line(win, BLACK, (350, 280), (390, 320), 3)
    if errors >= 6: pygame.draw.line(win, BLACK, (350, 340), (380, 400), 3)
    if errors >= 7: pygame.draw.line(win, BLACK, (350, 340), (320, 400), 3)

def draw_missed_letters(missed):
    txt = SMALL_FONT.render("Lettres ratées: " + " ".join(missed), True, RED)
    win.blit(txt, (20, SCREEN_HEIGHT - 50))

# -----------------------
#  Player Name Input
# -----------------------
def get_player_name():
    name = ""
    active = True
    while active:
        win.fill(WHITE)
        draw_text("Entrez votre nom et appuyez sur Entrée:", SMALL_FONT, BLACK, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50)
        draw_text(name, FONT, BLUE, SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
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

    while True:
        win.fill(WHITE)
        draw_text("PENDU", FONT, BLACK, SCREEN_WIDTH//2, 70)
        draw_text(" ".join(guessed), FONT, BLACK, SCREEN_WIDTH//2, 300)
        draw_text(f"Joueur: {player_name}", SMALL_FONT, BLACK, SCREEN_WIDTH//2, 130)

        draw_hangman(errors)
        draw_missed_letters(missed_letters)

        if errors >= 7:
            draw_text("Perdu!", FONT, RED, SCREEN_WIDTH//2, 420)
            pygame.display.update()
            if os.path.isfile(lose_sound_file):
                pygame.mixer.music.load(lose_sound_file)
                pygame.mixer.music.play()
            save_score(player_name, 0)
            pygame.time.wait(1500)
            break

        if "_" not in guessed:
            draw_text("Gagné!", FONT, GREEN, SCREEN_WIDTH//2, 420)
            pygame.display.update()
            if os.path.isfile(win_sound_file):
                pygame.mixer.music.load(win_sound_file)
                pygame.mixer.music.play()
            score = len([g for g in guessed if g != "_"])
            save_score(player_name, score)
            pygame.time.wait(1500)
            break

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

        pygame.display.update()
        clock.tick(10)

# -----------------------
#  Main Menu
# -----------------------
def main_menu():
    while True:
        win.fill(WHITE)
        draw_text("Menu Principal", FONT, GREEN, SCREEN_WIDTH//2, 80)
        draw_text("1. Jouer", SMALL_FONT, BLACK, SCREEN_WIDTH//2, 220)
        draw_text("2. Scores", SMALL_FONT, BLACK, SCREEN_WIDTH//2, 270)
        draw_text("3. Quitter", SMALL_FONT, BLACK, SCREEN_WIDTH//2, 320)
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
