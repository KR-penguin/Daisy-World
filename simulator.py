"""
Daisyworld 시뮬레이션 코어 모듈
"""
import numpy as np
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

# 시각화 설정
NUM_DAISIES = 300                  # 화면에 표시할 데이지 개수


class DaisyworldSimulator:
    """데이지 월드 시뮬레이션 클래스"""
    
    def __init__(self, planet_radius_px=350, center_x=400, center_y=400):
        """
        시뮬레이터 초기화
        
        Args:
            planet_radius_px: 행성 반지름 (픽셀)
            center_x: 중심 X 좌표
            center_y: 중심 Y 좌표
        """
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
        self.planet_radius_px = planet_radius_px
        self.center_x = center_x
        self.center_y = center_y
        self.daisy_positions = self._generate_daisy_positions()
    
    def _generate_daisy_positions(self):
        """데이지들의 랜덤 위치 생성 (픽셀 좌표)"""
        positions = []
        for _ in range(NUM_DAISIES):
            # 원 내부의 랜덤 위치 생성
            theta = np.random.uniform(0, 2 * np.pi)
            r = np.random.uniform(0, self.planet_radius_px * 0.95)
            x = self.center_x + r * np.cos(theta)
            y = self.center_y + r * np.sin(theta)
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
    
    def get_daisy_colors(self, color_black, color_white, color_bare):
        """
        현재 데이지 색상 배열 반환
        
        Args:
            color_black: 검은 데이지 색상
            color_white: 흰 데이지 색상
            color_bare: 빈 땅 색상
            
        Returns:
            색상 리스트
        """
        num_black = int(NUM_DAISIES * self.area_black_daisy)
        num_white = int(NUM_DAISIES * self.area_white_daisy)
        num_bare = NUM_DAISIES - num_black - num_white
        
        colors = [color_black] * num_black + [color_white] * num_white + [color_bare] * num_bare
        np.random.shuffle(colors)
        return colors
