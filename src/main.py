import random
import sys
import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SHIP_WIDTH = 40
SHIP_HEIGHT = 30
ASTEROID_MIN_RADIUS = 12
ASTEROID_MAX_RADIUS = 32
ASTEROID_SPAWN_MS = 700
SHIP_SPEED = 320
BACKGROUND_COLOR = (10, 12, 20)
SHIP_COLOR = (80, 200, 255)
ASTEROID_COLOR = (200, 140, 80)
TEXT_COLOR = (240, 240, 240)
ACCENT_COLOR = (120, 255, 180)


def spawn_asteroid():
    radius = random.randint(ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS)
    x = random.randint(radius, SCREEN_WIDTH - radius)
    y = -radius
    speed = random.randint(160, 260)
    return {
        "x": x,
        "y": y,
        "radius": radius,
        "speed": speed,
    }


def reset_game():
    ship_rect = pygame.Rect(
        SCREEN_WIDTH // 2 - SHIP_WIDTH // 2,
        SCREEN_HEIGHT - SHIP_HEIGHT - 40,
        SHIP_WIDTH,
        SHIP_HEIGHT,
    )
    asteroids = []
    score = 0.0
    return ship_rect, asteroids, score


def draw_ship(surface, ship_rect):
    tip = (ship_rect.centerx, ship_rect.top)
    left = (ship_rect.left, ship_rect.bottom)
    right = (ship_rect.right, ship_rect.bottom)
    pygame.draw.polygon(surface, SHIP_COLOR, [tip, left, right])


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Space Dodger")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont(None, 32)
    big_font = pygame.font.SysFont(None, 56)

    ship_rect, asteroids, score = reset_game()
    game_over = False
    spawn_timer = 0

    while True:
        dt = clock.tick(60) / 1000
        spawn_timer += clock.get_time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_r:
                    ship_rect, asteroids, score = reset_game()
                    game_over = False
                    spawn_timer = 0

        keys = pygame.key.get_pressed()
        if not game_over:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                ship_rect.x -= int(SHIP_SPEED * dt)
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                ship_rect.x += int(SHIP_SPEED * dt)
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                ship_rect.y -= int(SHIP_SPEED * dt)
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                ship_rect.y += int(SHIP_SPEED * dt)

            ship_rect.x = max(0, min(SCREEN_WIDTH - ship_rect.width, ship_rect.x))
            ship_rect.y = max(0, min(SCREEN_HEIGHT - ship_rect.height, ship_rect.y))

            if spawn_timer >= ASTEROID_SPAWN_MS:
                spawn_timer = 0
                asteroids.append(spawn_asteroid())

            for asteroid in asteroids:
                asteroid["y"] += asteroid["speed"] * dt

            asteroids = [a for a in asteroids if a["y"] < SCREEN_HEIGHT + a["radius"]]

            score += dt * 10

            for asteroid in asteroids:
                dx = ship_rect.centerx - asteroid["x"]
                dy = ship_rect.centery - asteroid["y"]
                if dx * dx + dy * dy <= (asteroid["radius"] + 16) ** 2:
                    game_over = True
                    break

        screen.fill(BACKGROUND_COLOR)

        for asteroid in asteroids:
            pygame.draw.circle(
                screen,
                ASTEROID_COLOR,
                (int(asteroid["x"]), int(asteroid["y"])),
                asteroid["radius"],
            )

        draw_ship(screen, ship_rect)

        score_text = font.render(f"Score: {int(score)}", True, TEXT_COLOR)
        screen.blit(score_text, (16, 16))
        hint_text = font.render(
            "Arrows/WASD move  |  R restart",
            True,
            ACCENT_COLOR,
        )
        screen.blit(hint_text, (16, SCREEN_HEIGHT - 32))

        if game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))

            title = big_font.render("Game Over", True, TEXT_COLOR)
            prompt = font.render("Press R to restart", True, TEXT_COLOR)
            screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 220))
            screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 300))

        pygame.display.flip()


if __name__ == "__main__":
    main()
