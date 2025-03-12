import pygame
import random
import os

pygame.init()

WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

font = pygame.font.Font(None, 36)

RECORD_FILE = "recorde.txt"

def carregar_recorde():
    """Lê o recorde do arquivo, se existir."""
    if os.path.exists(RECORD_FILE):
        with open(RECORD_FILE, "r") as f:
            return int(f.read().strip())
    return 0

def salvar_recorde(recorde):
    with open(RECORD_FILE, "w") as f:
        f.write(str(recorde))

def random_position():
    x = random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE
    y = random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
    return x, y

def show_game_over(score, recorde):
    screen.fill(BLACK)
    if score > recorde:
        recorde = score
        salvar_recorde(recorde)
        mensagem_recorde = "Novo Recorde!"
    else:
        mensagem_recorde = f"Recorde: {recorde} pontos"

    text1 = font.render("Game Over!", True, WHITE)
    text2 = font.render(f"Pontuação: {score} pontos", True, WHITE)
    text3 = font.render(mensagem_recorde, True, WHITE)
    text4 = font.render("Pressione R para reiniciar ou Q para sair", True, WHITE)

    screen.blit(text1, (WIDTH // 2 - text1.get_width() // 2, HEIGHT // 2 - 60))
    screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, HEIGHT // 2 - 30))
    screen.blit(text3, (WIDTH // 2 - text3.get_width() // 2, HEIGHT // 2))
    screen.blit(text4, (WIDTH // 2 - text4.get_width() // 2, HEIGHT // 2 + 40))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    exit()
    
    return recorde 

def main():
    """Loop principal do jogo."""
    snake = [(100, 100), (90, 100), (80, 100)]
    direction = (CELL_SIZE, 0)
    food = random_position()
    clock = pygame.time.Clock()

    score = 0
    recorde = carregar_recorde()

    running = True
    while running:
        screen.fill(BLACK)
        next_direction = direction  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                    next_direction = (0, -CELL_SIZE)
                elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                    next_direction = (0, CELL_SIZE)
                elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                    next_direction = (-CELL_SIZE, 0)
                elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                    next_direction = (CELL_SIZE, 0)

        direction = next_direction

        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        if new_head in snake or not (0 <= new_head[0] < WIDTH and 0 <= new_head[1] < HEIGHT):
            recorde = show_game_over(score, recorde)
            main() 

        snake.insert(0, new_head)

        if new_head == food:
            food = random_position()
            score += 5 
        else:
            snake.pop()


        for segment in snake:
            pygame.draw.rect(screen, GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))

        pygame.draw.rect(screen, RED, (food[0], food[1], CELL_SIZE, CELL_SIZE))

        score_text = font.render(f"Pontos: {score}", True, WHITE)
        record_text = font.render(f"Recorde: {recorde}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(record_text, (WIDTH - 150, 10))

        pygame.display.flip()
        clock.tick(10)

main()
