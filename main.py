import pygame
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import threading
from collections import deque
from datetime import datetime
import os

# ========== 상수 정의 ==========
# 물리 상수
STEFAN_BOLTZMANN_CONSTANT = 5.6696e-8  # 슈테판-볼츠만 상수 (W m^-2 K^-4)

# 알베도 상수 (반사율)
ALBEDO_BARE_GROUND = 0.5   # 빈 땅의 알베도
ALBEDO_BLACK_DAISY = 0.25  # 검은 데이지 알베도 (더 많은 열 흡수)
ALBEDO_WHITE_DAISY = 0.75  # 흰 데이지 알베도 (더 많은 열 반사)

# 시뮬레이션 상수
TEMPERATURE_FEEDBACK_FACTOR = 20  # 온도 피드백 계수
DEATH_RATE = 0.3                  # 데이지 사망률
OPTIMAL_TEMPERATURE = 295.5        # 최적 성장 온도 (K)
GROWTH_RATE_COEFFICIENT = 0.003265 # 성장률 계산 계수
MIN_AREA_THRESHOLD = 0.0001        # 최소 면적 임계값

# 태양 광도 관련
INITIAL_SOLAR_LUMINOSITY = 550     # 초기 태양 광도
SOLAR_LUMINOSITY_INCREASE_RATE = 5.5  # 시간당 태양 광도 증가율

# 시뮬레이션 시간
SIMULATION_TIME_STEPS = None          # 무한 시뮬레이션 (None = 무한)

# Pygame 시각화 설정
SCREEN_WIDTH = 800                 # 화면 너비
SCREEN_HEIGHT = 800                # 화면 높이
PLANET_RADIUS_PX = 350             # 행성 반지름 (픽셀)
CENTER_X = SCREEN_WIDTH // 2       # 중심 X 좌표
CENTER_Y = SCREEN_HEIGHT // 2      # 중심 Y 좌표
NUM_DAISIES = 300                  # 화면에 표시할 데이지 개수
FPS = 20                           # 초당 프레임 수

# 색상 정의 (RGB)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_SPACE = (8, 8, 20)           # 우주 배경색
COLOR_PLANET = (139, 115, 85)      # 행성 기본 색상
COLOR_BLACK_DAISY = (20, 20, 20)   # 검은 데이지
COLOR_WHITE_DAISY = (240, 240, 240) # 흰 데이지
COLOR_BARE_GROUND = (139, 115, 85) # 빈 땅
COLOR_TEXT = (255, 255, 255)       # 텍스트 색상


# ========== 시뮬레이션 클래스 ==========
class DaisyworldSimulator:
    def __init__(self):
        # 면적 변수
        self.area_black_daisy = 0.01  # 검은 데이지가 차지하는 면적
        self.area_white_daisy = 0.01  # 흰 데이지가 차지하는 면적
        self.area_bare_ground = 0.0   # 빈 땅의 면적
        
        # 온도 변수
        self.temperature_planet = 0.0       # 행성 전체 온도
        self.temperature_black_daisy = 0.0  # 검은 데이지 영역 온도
        self.temperature_white_daisy = 0.0  # 흰 데이지 영역 온도
        
        # 성장률 변수
        self.growth_factor_black = 0.0  # 검은 데이지 성장률
        self.growth_factor_white = 0.0  # 흰 데이지 성장률
        
        # 기타 변수
        self.solar_luminosity = 0.0    # 현재 태양 광도
        self.planetary_albedo = 0.0    # 행성 평균 알베도
        self.current_time = 0
        
        # 데이터 기록용 리스트
        self.history_black_daisy = []
        self.history_white_daisy = []
        self.history_temperature = []
        self.history_time = []
        
        # 데이지 위치 생성 (극좌표 사용)
        self.daisy_positions = self._generate_daisy_positions()
    
    def _generate_daisy_positions(self):
        """데이지들의 랜덤 위치 생성 (픽셀 좌표)"""
        positions = []
        for _ in range(NUM_DAISIES):
            # 원 내부의 랜덤 위치 생성
            theta = np.random.uniform(0, 2 * np.pi)
            r = np.random.uniform(0, PLANET_RADIUS_PX * 0.95)
            x = CENTER_X + r * np.cos(theta)
            y = CENTER_Y + r * np.sin(theta)
            positions.append((int(x), int(y)))
        return positions
    
    def step(self):
        """시뮬레이션 한 스텝 실행"""
        # 무한 시뮬레이션 (시간 제한 없음)
        
        # 태양 광도 계산
        self.solar_luminosity = INITIAL_SOLAR_LUMINOSITY + (SOLAR_LUMINOSITY_INCREASE_RATE * self.current_time)
        
        # 빈 땅 면적 계산
        self.area_bare_ground = 1 - self.area_black_daisy - self.area_white_daisy
        
        # 최소 면적 보장
        if self.area_black_daisy < MIN_AREA_THRESHOLD:
            self.area_black_daisy = MIN_AREA_THRESHOLD
        if self.area_white_daisy < MIN_AREA_THRESHOLD:
            self.area_white_daisy = MIN_AREA_THRESHOLD
        
        # 행성 평균 알베도 계산
        self.planetary_albedo = (
            (self.area_bare_ground * ALBEDO_BARE_GROUND) +
            (self.area_black_daisy * ALBEDO_BLACK_DAISY) +
            (self.area_white_daisy * ALBEDO_WHITE_DAISY)
        )
        
        # 행성 전체 온도 계산
        self.temperature_planet = (self.solar_luminosity * (1 - self.planetary_albedo) / STEFAN_BOLTZMANN_CONSTANT) ** 0.25
        
        # 각 데이지 영역의 온도 계산
        self.temperature_white_daisy = TEMPERATURE_FEEDBACK_FACTOR * (self.planetary_albedo - ALBEDO_WHITE_DAISY) + self.temperature_planet
        self.temperature_black_daisy = TEMPERATURE_FEEDBACK_FACTOR * (self.planetary_albedo - ALBEDO_BLACK_DAISY) + self.temperature_planet
        
        # 성장률 계산
        self.growth_factor_black = 1 - (GROWTH_RATE_COEFFICIENT * (OPTIMAL_TEMPERATURE - self.temperature_black_daisy) ** 2)
        self.growth_factor_white = 1 - (GROWTH_RATE_COEFFICIENT * (OPTIMAL_TEMPERATURE - self.temperature_white_daisy) ** 2)
        
        # 성장률 제한
        if self.growth_factor_black < 0:
            self.growth_factor_black = 0
        if self.growth_factor_white < 0:
            self.growth_factor_white = 0
        
        # 면적 변화량 계산
        delta_area_black = self.area_black_daisy * (self.area_bare_ground * self.growth_factor_black - DEATH_RATE)
        delta_area_white = self.area_white_daisy * (self.area_bare_ground * self.growth_factor_white - DEATH_RATE)
        
        # 면적 업데이트
        self.area_black_daisy += delta_area_black
        self.area_white_daisy += delta_area_white
        
        # 데이터 기록
        self.history_time.append(self.current_time)
        self.history_temperature.append(self.temperature_planet)
        self.history_black_daisy.append(self.area_black_daisy)
        self.history_white_daisy.append(self.area_white_daisy)
        
        self.current_time += 1
        return True
    
    def get_daisy_colors(self):
        """현재 데이지 색상 배열 반환"""
        num_black = int(NUM_DAISIES * self.area_black_daisy)
        num_white = int(NUM_DAISIES * self.area_white_daisy)
        num_bare = NUM_DAISIES - num_black - num_white
        
        colors = [COLOR_BLACK_DAISY] * num_black + [COLOR_WHITE_DAISY] * num_white + [COLOR_BARE_GROUND] * num_bare
        np.random.shuffle(colors)
        return colors
    
    def save_graphs(self, output_dir='results'):
        """시뮬레이션 결과 그래프를 파일로 저장"""
        # 결과 디렉토리 생성
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 타임스탬프로 파일명 생성
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Figure 생성
        fig, (ax_population, ax_temperature) = plt.subplots(2, 1, figsize=(12, 10))
        fig.suptitle(f'Daisyworld Simulation Results\n{timestamp}', fontsize=16, fontweight='bold')
        
        # 개체수 그래프
        ax_population.plot(self.history_time, self.history_black_daisy, 'k-', linewidth=2, label='Black Daisy')
        ax_population.plot(self.history_time, self.history_white_daisy, color='lightblue', linewidth=2, label='White Daisy')
        ax_population.set_xlabel('Time (steps)', fontsize=12)
        ax_population.set_ylabel('Population Area', fontsize=12)
        ax_population.set_title('Daisy Population Over Time', fontsize=13, fontweight='bold')
        ax_population.grid(True, alpha=0.3)
        ax_population.legend(loc='best')
        
        # 온도 그래프
        ax_temperature.plot(self.history_time, self.history_temperature, 'r-', linewidth=2, label='Planet Temp')
        ax_temperature.axhline(y=OPTIMAL_TEMPERATURE, color='green', linestyle='--', alpha=0.5, linewidth=2, label='Optimal Temp')
        ax_temperature.set_xlabel('Time (steps)', fontsize=12)
        ax_temperature.set_ylabel('Temperature (K)', fontsize=12)
        ax_temperature.set_title('Planetary Temperature Over Time', fontsize=13, fontweight='bold')
        ax_temperature.grid(True, alpha=0.3)
        ax_temperature.legend(loc='best')
        
        plt.tight_layout()
        
        # 파일 저장
        filename = os.path.join(output_dir, f'daisyworld_simulation_{timestamp}.png')
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"\n{'='*60}")
        print(f"Graph saved: {filename}")
        print(f"Total simulation steps: {self.current_time}")
        print(f"Final temperature: {self.temperature_planet:.2f} K")
        print(f"Final black daisy area: {self.area_black_daisy:.4f}")
        print(f"Final white daisy area: {self.area_white_daisy:.4f}")
        print(f"{'='*60}\n")
        
        return filename


# ========== Pygame 시각화 ==========
def run_pygame_visualization(simulator):
    """Pygame으로 행성 시각화"""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Daisyworld Planet Simulator')
    clock = pygame.time.Clock()
    
    # 폰트 설정
    font_large = pygame.font.Font(None, 48)
    font_small = pygame.font.Font(None, 32)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # 시뮬레이션 스텝 실행
        simulator.step()
        
        # 화면 그리기
        screen.fill(COLOR_SPACE)
        
        # 행성 그리기
        pygame.draw.circle(screen, COLOR_PLANET, (CENTER_X, CENTER_Y), PLANET_RADIUS_PX)
        
        # 데이지 그리기
        colors = simulator.get_daisy_colors()
        for pos, color in zip(simulator.daisy_positions, colors):
            pygame.draw.circle(screen, color, pos, 4)
        
        # 정보 텍스트 그리기
        title_text = font_large.render('Daisyworld Planet', True, COLOR_TEXT)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 30))
        
        info_lines = [
            f'Time: {simulator.current_time}',
            f'Temperature: {simulator.temperature_planet:.2f} K',
            f'Black Daisy: {simulator.area_black_daisy:.3f}',
            f'White Daisy: {simulator.area_white_daisy:.3f}',
            f'Solar Luminosity: {simulator.solar_luminosity:.1f}'
        ]
        
        y_offset = SCREEN_HEIGHT - 180
        for line in info_lines:
            text = font_small.render(line, True, COLOR_TEXT)
            screen.blit(text, (20, y_offset))
            y_offset += 35
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()


# ========== Matplotlib 그래프 ==========
def run_matplotlib_graphs(simulator):
    """Matplotlib으로 실시간 그래프 표시"""
    fig, (ax_population, ax_temperature) = plt.subplots(2, 1, figsize=(10, 8))
    fig.suptitle('Daisyworld Real-time Statistics', fontsize=16, fontweight='bold')
    
    # 개체수 그래프 설정
    ax_population.set_xlim(0, 200)
    ax_population.set_ylim(0, 1)
    ax_population.set_xlabel('Time (steps)', fontsize=11)
    ax_population.set_ylabel('Population Area', fontsize=11)
    ax_population.set_title('Daisy Population Over Time', fontsize=12, fontweight='bold')
    ax_population.grid(True, alpha=0.3)
    line_black, = ax_population.plot([], [], 'k-', linewidth=2, label='Black Daisy')
    line_white, = ax_population.plot([], [], color='lightblue', linewidth=2, label='White Daisy')
    ax_population.legend(loc='upper right')
    
    # 온도 그래프 설정
    ax_temperature.set_xlim(0, 200)
    ax_temperature.set_ylim(250, 350)
    ax_temperature.set_xlabel('Time (steps)', fontsize=11)
    ax_temperature.set_ylabel('Temperature (K)', fontsize=11)
    ax_temperature.set_title('Planetary Temperature Over Time', fontsize=12, fontweight='bold')
    ax_temperature.grid(True, alpha=0.3)
    ax_temperature.axhline(y=OPTIMAL_TEMPERATURE, color='green', linestyle='--', alpha=0.5, label='Optimal Temp')
    line_temp, = ax_temperature.plot([], [], 'r-', linewidth=2, label='Planet Temp')
    ax_temperature.legend(loc='upper right')
    
    plt.tight_layout()
    
    def init():
        """애니메이션 초기화"""
        line_black.set_data([], [])
        line_white.set_data([], [])
        line_temp.set_data([], [])
        return line_black, line_white, line_temp
    
    def animate(frame):
        """애니메이션 업데이트"""
        if len(simulator.history_time) > 0:
            # X축 범위 동적 조정
            current_max = max(simulator.history_time) if simulator.history_time else 200
            if current_max > 200:
                ax_population.set_xlim(0, current_max + 10)
                ax_temperature.set_xlim(0, current_max + 10)
                # X축 범위가 변경되었으므로 figure를 다시 그림
                fig.canvas.draw_idle()
            
            line_black.set_data(simulator.history_time, simulator.history_black_daisy)
            line_white.set_data(simulator.history_time, simulator.history_white_daisy)
            line_temp.set_data(simulator.history_time, simulator.history_temperature)
        return line_black, line_white, line_temp
    
    anim = animation.FuncAnimation(
        fig, 
        animate, 
        init_func=init,
        interval=50,  # 50ms마다 업데이트
        blit=False,  # blit=False로 변경하여 X축 업데이트 가능하게
        cache_frame_data=False
    )
    
    plt.show()


# ========== 메인 실행 ==========
if __name__ == "__main__":
    print("=" * 60)
    print("Daisyworld Simulation Starting...")
    print("=" * 60)
    print("Two windows will open:")
    print("  1. Pygame window: Visual planet with daisies")
    print("  2. Matplotlib window: Real-time graphs")
    print("\nSimulation runs indefinitely until you close the window.")
    print("Graphs will be saved automatically when you exit.")
    print("=" * 60)
    
    # 시뮬레이터 생성
    simulator = DaisyworldSimulator()
    
    # Matplotlib을 별도 스레드에서 실행
    graph_thread = threading.Thread(target=run_matplotlib_graphs, args=(simulator,), daemon=True)
    graph_thread.start()
    
    # Pygame을 메인 스레드에서 실행
    run_pygame_visualization(simulator)
    
    # 시뮬레이션 종료 후 그래프 저장
    print("\nSaving simulation results...")
    saved_file = simulator.save_graphs()
    
    print("Simulation completed!")
    print("=" * 60)