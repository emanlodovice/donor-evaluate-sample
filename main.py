# Simple pygame program

# Import and initialize the pygame library
import pygame
import time
import random
from blood import Blood
from avatar import Avatar


SCREEN_HEIGHT = 700
SCREEN_WIDTH = 700
SPACING = 170
MAX_SCORE = 10
AVATARS = ["avatar1.webp", "avatar2.webp", "avatar3.png", "avatar4.png"]
BLOODS_IMAGES = ["blood1", "blood2", "blood3"]


def game(screen):
    score = 0
    life = 4
    min_speed = 3
    donor = AVATARS[random.randint(0, len(AVATARS) - 1)]

    screen.fill((255, 255, 255))
    donor_image = Avatar(donor, 300)
    donor_image.draw(screen, SCREEN_HEIGHT // 2 - (300 // 2), SCREEN_WIDTH // 2 - (300 // 2))
    pygame.display.flip()
    time.sleep(2)  # display the donor for 2 secs

    running = True
    ticker = 0
    donors = []
    bloods = []
    while running:
        # Fill the background with white
        screen.fill((255, 255, 255))

        if ticker % 50 == 0:
            donors, young_bloods = get_donors_and_bloods(donor, min_speed)
            bloods += young_bloods
            min_speed += 1
        
        donor_x = 50
        for _donor in donors:
            _donor.draw(screen, donor_x, 50)
            donor_x += SPACING


        display_score(screen, score, life)
        for blood in bloods:
            blood.draw(screen)
            blood.move()

        # Flip the display
        pygame.display.flip()
        time.sleep(0.05)

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Set the x, y postions of the mouse click
                x, y = event.pos
                has_hit = False
                for blood in bloods:
                    hit = blood.check_hit(x, y)
                    if not hit:
                        continue
                    has_hit = True
                    if blood.from_right_donor:
                        score += 1
                    else:
                        life -= 1
                if not has_hit:
                    life -= 1
                if life == 0 or score == MAX_SCORE:
                    running = False
        
        bloods = [blood for blood in bloods if not blood.has_left_screen(SCREEN_HEIGHT) and not blood.is_clicked]
        ticker += 1
    
    if life == 0:
        draw_loser(screen)
    elif score == MAX_SCORE:
        draw_winner(screen)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return True


def main():
    pygame.init()

    # Set up the drawing window
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption('Donor Evaluate Sample')

    cont = True
    while cont:
        cont = game(screen)

    # Done! Time to quit.
    pygame.quit()


def display_score(screen, score, life):
    font = pygame.font.Font('assets/creepster-regular.ttf', 32)
    score = font.render(f'Score: {score}', True, (0, 255, 0), (255, 255, 255))
    life = font.render(f'Life: {life}', True, (255, 0, 0), (255, 255, 255))
    score_rect = score.get_rect()
    score_rect.center = (620, 30)
    screen.blit(score, score_rect)
    life_rect = life.get_rect()
    score_rect.center = (500, 30)
    screen.blit(life, score_rect)


def draw_loser(screen):
    screen.fill((255, 255, 255))
    font = pygame.font.Font('assets/creepster-regular.ttf', 100)
    loser = font.render(f'What a loser', True, (255, 0, 0), (255, 255, 255))
    loser_rect = loser.get_rect()
    loser_rect.center = (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2)
    screen.blit(loser, loser_rect)
    pygame.display.flip()


def draw_winner(screen):
    screen.fill((255, 255, 255))
    font = pygame.font.Font('assets/creepster-regular.ttf', 70)
    text = "You're a great singer,\naw clicker diay!"
    for idx, t in enumerate(text.split('\n')):
        loser = font.render(t, True, (0, 255, 0), (255, 255, 255))
        loser_rect = loser.get_rect()
        loser_rect.center = (SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT // 2 - 70 + (idx * 100))
        screen.blit(loser, loser_rect)
    pygame.display.flip()


def get_donors_and_bloods(donor, min_speed):
    donor_images = list(AVATARS)  # create copy of the list
    random.shuffle(donor_images)
    cur_x = 80
    donors = []
    bloods = []
    for idx, image in enumerate(donor_images):
        donors.append(
            Avatar(
                image=image,
                size=50
            )
        )
        bloods.append(
            Blood(
                cur_x,
                speed=random.randint(min_speed, min_speed + 3),
                image=BLOODS_IMAGES[random.randint(0, len(BLOODS_IMAGES) - 1)],
                from_right_donor=image == donor
            )
        )
        cur_x += SPACING

    return donors, bloods


if __name__ == "__main__":
    main()
