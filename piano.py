import pygame
import sys

# 初始化
pygame.init()
pygame.mixer.init()

# 視窗設定
WIDTH, HEIGHT = 700, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🎹 鋼琴（每次按鍵都播放音）")

# 顏色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 149, 237)
GRAY = (200, 200, 200)

# 鍵位對應表：鍵 → (音檔, 唱名)
key_info = {
    pygame.K_q: ("C3.wav", "do"),
    pygame.K_w: ("D3.wav", "re"),
    pygame.K_e: ("E3.wav", "mi"),
    pygame.K_r: ("F3.wav", "fa"),
    pygame.K_t: ("G3.wav", "so"),
    pygame.K_y: ("A3.wav", "la"),
    pygame.K_u: ("B3.wav", "si"),
    pygame.K_a: ("C4.wav", "do"),
    pygame.K_s: ("D4.wav", "re"),
    pygame.K_d: ("E4.wav", "mi"),
    pygame.K_f: ("F4.wav", "fa"),
    pygame.K_g: ("G4.wav", "so"),
    pygame.K_h: ("A4.wav", "la"),
    pygame.K_j: ("B4.wav", "si"),
}

# 載入聲音
sounds = {}
for key, (filename, _) in key_info.items():
    try:
        sounds[key] = pygame.mixer.Sound(f'sounds/{filename}')
    except Exception as e:
        print(f"❌ 無法載入 sounds/{filename}: {e}")

# 建立單一播放通道
channel = pygame.mixer.Channel(0)

# 建立每個按鍵的矩形
keys_order = list(key_info.keys())
key_width = WIDTH // len(keys_order)
key_height = 200
key_rects = {}
for i, key in enumerate(keys_order):
    rect = pygame.Rect(i * key_width, HEIGHT - key_height, key_width, key_height)
    key_rects[key] = rect

# 字型
font = pygame.font.SysFont(None, 28)
current_key = None  # 記錄正在按下的按鍵

# 主迴圈
running = True
while running:
    screen.fill(GRAY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key in sounds:
                channel.stop()  # 停止前一個音
                channel.play(sounds[event.key])  # 播放目前音
                current_key = event.key

    # 畫鋼琴鍵
    for key, rect in key_rects.items():
        color = BLUE if key == current_key else WHITE
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

        # 顯示唱名
        _, note_name = key_info[key]
        text = font.render(note_name, True, BLACK)
        screen.blit(text, text.get_rect(center=rect.center))

    pygame.display.flip()

pygame.quit()
sys.exit()
