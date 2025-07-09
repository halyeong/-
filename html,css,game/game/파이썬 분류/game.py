import pygame
import random
import sys

pygame.init()

# 화면 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("재활용 분리배출 게임")

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 한글 폰트 (Windows 전용)
font = pygame.font.Font("C:/Windows/Fonts/malgun.ttf", 28)

# 쓰레기 종류
waste_types = ["플라스틱", "종이", "비닐", "유리", "일반"]

# 이미지 맵핑 (파일명은 꼭 맞춰서 준비해야 해!)
waste_images = {
    "플라스틱": pygame.image.load("plastic.png"),
    "종이": pygame.image.load("paper.png"),
    "비닐": pygame.image.load("vinyl.png"),
    "유리": pygame.image.load("glass.png"),
    "일반": pygame.image.load("general.png"),
}

# 쓰레기통 이미지
bin_image = pygame.image.load("bin.png")
bin_image = pygame.transform.scale(bin_image, (100, 80))

# 쓰레기통 위치 설정
trash_bin_positions = {}
for i, category in enumerate(waste_types):
    trash_bin_positions[category] = pygame.Rect(50 + i * 140, 500, 100, 80)

# 쓰레기 클래스
class Trash:
    def __init__(self, name):
        self.name = name
        self.image = pygame.transform.scale(waste_images[name], (100, 50))
        self.rect = self.image.get_rect(topleft=(random.randint(100, 600), 50))
        self.dragging = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        label = font.render(self.name, True, BLACK)
        screen.blit(label, (self.rect.x + 5, self.rect.y + 55))

# 게임 상태 초기화
current_trash = Trash(random.choice(waste_types))
score = 0
clock = pygame.time.Clock()
time_limit = 60
start_ticks = pygame.time.get_ticks()

# 게임 루프
running = True
while running:
    screen.fill(WHITE)

    # 시간 계산
    seconds = (pygame.time.get_ticks() - start_ticks) / 1000
    if seconds > time_limit:
        break

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if current_trash.rect.collidepoint(event.pos):
                current_trash.dragging = True
                offset_x = current_trash.rect.x - event.pos[0]
                offset_y = current_trash.rect.y - event.pos[1]

        elif event.type == pygame.MOUSEBUTTONUP:
            if current_trash.dragging:
                current_trash.dragging = False
                for category, bin_rect in trash_bin_positions.items():
                    if bin_rect.collidepoint(current_trash.rect.center):
                        if category == current_trash.name:
                            score += 1
                        else:
                            score -= 1
                        current_trash = Trash(random.choice(waste_types))

        elif event.type == pygame.MOUSEMOTION:
            if current_trash.dragging:
                mouse_x, mouse_y = event.pos
                current_trash.rect.x = mouse_x + offset_x
                current_trash.rect.y = mouse_y + offset_y

    # 쓰레기통 그리기
    for category, bin_rect in trash_bin_positions.items():
        screen.blit(bin_image, bin_rect)
        label = font.render(category, True, BLACK)
        screen.blit(label, (bin_rect.x + 10, bin_rect.y + -40)   )

    # 쓰레기와 상태 그리기
    current_trash.draw(screen)

    score_text = font.render(f"점수: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    timer_text = font.render(f"남은 시간: {int(time_limit - seconds)}초", True, BLACK)
    screen.blit(timer_text, (600, 10))

    pygame.display.flip()
    clock.tick(60)

# 게임 종료 화면
screen.fill(WHITE)
end_text = font.render(f"게임 종료! 최종 점수는 {score}점입니다.", True, BLACK)
screen.blit(end_text, (200, 250))
pygame.display.flip()
pygame.time.delay(3000)

pygame.quit()
print(f"게임 종료! 최종 점수는 {score}점입니다.")
