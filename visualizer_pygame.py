"""
Pygame을 이용한 행성 시각화 모듈
"""
import pygame
import random
import math


# Pygame 시각화 설정
SCREEN_WIDTH = 800                 # 화면 너비
SCREEN_HEIGHT = 800                # 화면 높이
PLANET_RADIUS_PX = 350             # 행성 반지름 (픽셀)
CENTER_X = SCREEN_WIDTH // 2       # 중심 X 좌표
CENTER_Y = SCREEN_HEIGHT // 2      # 중심 Y 좌표
FPS = 20                           # 초당 프레임 수

# 색상 정의 (RGB)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_SPACE = (8, 8, 20)           # 우주 배경색
COLOR_OCEAN = (30, 80, 150)        # 바다 (진한 파란색)
COLOR_LAND = (100, 140, 70)        # 육지 (녹색/갈색)
COLOR_ATMOSPHERE = (150, 200, 255, 80)  # 대기층 (반투명 하늘색)
COLOR_BLACK_DAISY = (20, 20, 20)   # 검은 데이지
COLOR_WHITE_DAISY = (240, 240, 240) # 흰 데이지
COLOR_BARE_GROUND_OCEAN = (25, 70, 130)  # 바다 위 빈 땅
COLOR_BARE_GROUND_LAND = (100, 140, 70)  # 육지 위 빈 땅
COLOR_TEXT = (255, 255, 255)       # 텍스트 색상


def generate_terrain(num_points=500):
    """
    바다와 육지 지형 생성 (각 지점에 바다인지 육지인지 저장)
    
    Returns:
        list: 각 지점의 (x, y, is_ocean) 튜플 리스트
    """
    terrain_points = []
    for _ in range(num_points):
        # 원 안의 랜덤한 위치 생성
        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(0, PLANET_RADIUS_PX)
        x = CENTER_X + int(radius * math.cos(angle))
        y = CENTER_Y + int(radius * math.sin(angle))
        
        # 70% 확률로 바다, 30% 확률로 육지
        is_ocean = random.random() < 0.7
        terrain_points.append((x, y, is_ocean))
    
    return terrain_points


def run_pygame_visualization(simulator):
    """
    Pygame으로 행성 시각화
    
    Args:
        simulator: DaisyworldSimulator 인스턴스
    """
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Daisyworld Planet Simulator')
    clock = pygame.time.Clock()
    
    # 지형 생성 (게임 시작 시 한 번만)
    terrain_points = generate_terrain(800)
    
    # 폰트 설정
    font_large = pygame.font.Font(None, 48)
    font_small = pygame.font.Font(None, 32)
    
    # 현재 배경색 (점진적 변화를 위한 변수)
    current_bg_r = 255
    current_bg_g = 255
    current_bg_b = 255
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # 시뮬레이션 스텝 실행
        simulator.step()
        
        # 태양 강도에 따라 배경색과 텍스트 색상 점진적으로 변경
        # solar_intensity: 1.0 (낮, 흰색) → 0.0 (밤, 검은색)
        target_bg_value = int(255 * simulator.solar_intensity)
        
        # 배경색을 목표값으로 부드럽게 이동 (각 RGB 채널)
        transition_speed = 5  # 전환 속도 (값이 클수록 빠름)
        current_bg_r += (target_bg_value - current_bg_r) * 0.1
        current_bg_g += (target_bg_value - current_bg_g) * 0.1
        current_bg_b += (target_bg_value - current_bg_b) * 0.1
        
        background_color = (int(current_bg_r), int(current_bg_g), int(current_bg_b))
        
        # 텍스트 색상 (배경의 반전색으로 가독성 확보)
        text_brightness = int(current_bg_r)
        if text_brightness > 127:
            text_color = COLOR_BLACK  # 밝은 배경에는 검은 텍스트
        else:
            text_color = COLOR_WHITE  # 어두운 배경에는 흰 텍스트
        
        # 화면 그리기
        screen.fill(background_color)
        
        # 행성 기본 배경 (바다색)
        pygame.draw.circle(screen, COLOR_OCEAN, (CENTER_X, CENTER_Y), PLANET_RADIUS_PX)
        
        # 지형 그리기 (바다와 육지)
        for x, y, is_ocean in terrain_points:
            color = COLOR_OCEAN if is_ocean else COLOR_LAND
            pygame.draw.circle(screen, color, (x, y), 5)
        
        # 대기층 그리기 (반투명 원)
        atmosphere_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        atmosphere_radius = PLANET_RADIUS_PX + 30
        pygame.draw.circle(atmosphere_surface, COLOR_ATMOSPHERE, (CENTER_X, CENTER_Y), atmosphere_radius, 30)
        screen.blit(atmosphere_surface, (0, 0))
        
        # 데이지 그리기
        colors = simulator.get_daisy_colors(COLOR_BLACK_DAISY, COLOR_WHITE_DAISY, COLOR_BARE_GROUND_OCEAN)
        for pos, color in zip(simulator.daisy_positions, colors):
            pygame.draw.circle(screen, color, pos, 4)
        
        # 정보 텍스트 그리기
        title_text = font_large.render('Daisyworld Planet', True, text_color)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 30))
        
        info_lines = [
            f'Time: {simulator.current_time}',
            f'Day/Night: {"DAY" if simulator.is_daytime else "NIGHT"} ({simulator.day_night_timer}/{150})',
            f'Solar Intensity: {simulator.solar_intensity:.2f}',
            f'',
            f'=== Milankovitch Cycles ===',
            f'Eccentricity: {simulator.eccentricity:.4f}',
            f'Obliquity: {simulator.obliquity:.2f} deg',
            f'Precession: {simulator.precession_angle:.1f} deg',
            f'',
            f'=== Temperatures ===',
            f'Atmosphere: {simulator.temperature_atmosphere:.2f} K',
            f'Ocean: {simulator.temperature_ocean:.2f} K',
            f'Land: {simulator.temperature_land:.2f} K',
            f'',
            f'=== Daisies ===',
            f'Black: {simulator.area_black_daisy:.3f}',
            f'White: {simulator.area_white_daisy:.3f}',
            f'',
            f'=== Atmosphere ===',
            f'O2: {simulator.o2_concentration:.0f} ppm',
            f'CO2: {simulator.co2_concentration:.2f} ppm',
            f'CH4: {simulator.ch4_concentration:.3f} ppm',
            f'H2O: {simulator.h2o_concentration:.1f} ppm',
            f'GH Effect: {simulator.greenhouse_effect:.3f}'
        ]
        
        y_offset = SCREEN_HEIGHT - 750
        for line in info_lines:
            text = font_small.render(line, True, text_color)
            screen.blit(text, (20, y_offset))
            y_offset += 35
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
