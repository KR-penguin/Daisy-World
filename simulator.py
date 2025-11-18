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
INITIAL_SOLAR_LUMINOSITY = 450     # 초기 태양 광도 (낮춤)
SOLAR_LUMINOSITY_INCREASE_RATE = 0.0  # 태양 광도 증가율 (0.0 = 고정, 현실적)

# 시뮬레이션 시간
SIMULATION_TIME_STEPS = None          # 무한 시뮬레이션 (None = 무한)
TIME_STEP_SECONDS = 3600              # 1스텝 = 1시간 (3600초)

# 시각화 설정
NUM_DAISIES = 300                  # 화면에 표시할 데이지 개수

# 지형 관련 상수
OCEAN_RATIO = 0.7                  # 바다 비율 (지구는 약 71%)
LAND_RATIO = 0.3                   # 대륙 비율 (지구는 약 29%)

# 열용량 관련 상수 (현실적인 값)
ATMOSPHERE_HEAT_CAPACITY = 0.88    # 대기 열용량 (온도 변화 완만)
OCEAN_HEAT_CAPACITY = 0.96         # 바다 열용량 (매우 느리게 변화, 거대한 열 저장소)
LAND_HEAT_CAPACITY = 0.90          # 대륙 열용량 (느린 변화)

# 알베도 - 지형별
ALBEDO_OCEAN = 0.06                # 바다 알베도 (매우 낮음, 열 잘 흡수)
ALBEDO_LAND = 0.3                  # 대륙 알베도 (중간)

# 대기 및 온실효과 관련 상수
BASE_EARTH_EMISSIVITY = 1.0           # 기본 지구 복사 방출 효율 (온실효과 없을 때)
GREENHOUSE_EFFECT_COEFFICIENT = 0.38  # 온실효과 계수 (방출 효율 감소율, 균형 조정)

# 온실 기체 초기 농도 (ppm - parts per million)
INITIAL_CO2_CONCENTRATION = 400.0     # 초기 CO2 농도 (ppm)
INITIAL_O2_CONCENTRATION = 210000.0   # 초기 O2 농도 (ppm, ~21%)
INITIAL_CH4_CONCENTRATION = 1.8       # 초기 CH4 농도 (ppm)
INITIAL_H2O_CONCENTRATION = 10000.0   # 초기 H2O 농도 (ppm, ~1%)

# 광합성 및 호흡 상수
RESPIRATION_RATE = 0.5                # 호흡률 (일정하게 유지)
BASE_PHOTOSYNTHESIS_RATE = 1.2        # 기본 광합성률 (호흡보다 큼)
PHOTOSYNTHESIS_TEMP_COEFFICIENT = 0.005  # 온도에 따른 광합성 효율 증가

# 온실 기체별 온실효과 기여도 (상대적 강도)
CO2_GREENHOUSE_FACTOR = 1.0           # CO2 기준 (1배)
CH4_GREENHOUSE_FACTOR = 25.0          # CH4는 CO2 대비 25배 강력
H2O_GREENHOUSE_FACTOR = 0.1           # H2O는 농도가 높지만 효과는 약함


# 낮/밤 사이클 설정
DAY_NIGHT_CYCLE_DURATION = 100         # 낮/밤 전환 주기 (스텝 단위) - 24시간 = 1일
NIGHT_SOLAR_REDUCTION = 0.42          # 밤에 태양 광도 감소율 (42% 유지)
TRANSITION_SMOOTHNESS = 0.08          # 낮/밤 전환 부드러움 (더 부드럽게)

# 밀란코비치 주기 설정 (현실적인 천문학적 주기)
# 실제 주기를 1000배 축소하여 시뮬레이션에서 관찰 가능하게 조정
ECCENTRICITY_CYCLE = 10000            # 이심률 변화 주기 (실제: ~100,000년)
PRECESSION_CYCLE = 2600               # 세차운동 주기 (실제: ~26,000년)
OBLIQUITY_CYCLE = 4100                # 자전축 기울기 변화 주기 (실제: ~41,000년)

# 밀란코비치 변화 범위
ECCENTRICITY_MIN = 0.0                # 최소 이심률 (원형 궤도)
ECCENTRICITY_MAX = 0.06               # 최대 이심률 (실제 지구: 0~0.06)
OBLIQUITY_MIN = 22.1                  # 최소 기울기 (도)
OBLIQUITY_MAX = 24.5                  # 최대 기울기 (도) (실제 지구: 22.1~24.5도)
CURRENT_OBLIQUITY = 23.5              # 현재 기울기 (도)

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
        
        # 온도 변수 (초기값 250K)
        self.temperature_planet = 250.0       # 행성 전체 온도
        self.temperature_atmosphere = 250.0   # 대기 온도
        self.temperature_ocean = 250.0        # 바다 온도
        self.temperature_land = 250.0         # 대륙 온도
        self.temperature_black_daisy = 250.0  # 검은 데이지 영역 온도
        self.temperature_white_daisy = 250.0  # 흰 데이지 영역 온도
        
        # 성장률 변수
        self.growth_factor_black = 0.0  # 검은 데이지 성장률
        self.growth_factor_white = 0.0  # 흰 데이지 성장률
        
        # 기타 변수
        self.solar_luminosity = INITIAL_SOLAR_LUMINOSITY  # 현재 태양 광도 (고정)
        self.planetary_albedo = 0.0    # 행성 평균 알베도
        self.current_time = 0
        
        # 대기 및 온실효과 변수
        self.co2_concentration = INITIAL_CO2_CONCENTRATION    # CO2 농도 (ppm)
        self.o2_concentration = INITIAL_O2_CONCENTRATION      # O2 농도 (ppm)
        self.ch4_concentration = INITIAL_CH4_CONCENTRATION    # CH4 농도 (ppm)
        self.h2o_concentration = INITIAL_H2O_CONCENTRATION    # H2O 농도 (ppm)
        self.greenhouse_effect = 0.0                          # 총 온실효과
        self.earth_emissivity = BASE_EARTH_EMISSIVITY         # 현재 지구 복사 방출 효율
        
        # 낮/밤 사이클 변수
        self.is_daytime = True                                # 현재 낮인지 밤인지
        self.day_night_timer = 0                              # 낮/밤 전환 타이머
        self.solar_intensity = 1.0                            # 현재 태양 강도 (0.0 ~ 1.0, 점진적 변화)
        
        # 밀란코비치 주기 변수
        self.eccentricity = 0.0167                            # 현재 이심률 (지구 현재값)
        self.obliquity = CURRENT_OBLIQUITY                    # 현재 자전축 기울기 (도)
        self.precession_angle = 0.0                           # 세차운동 각도 (도)
        
        # 데이터 기록용 리스트
        self.history_black_daisy = []
        self.history_white_daisy = []
        self.history_temperature = []
        self.history_atmosphere_temp = []
        self.history_ocean_temp = []
        self.history_land_temp = []
        self.history_time = []
        self.history_co2 = []
        self.history_o2 = []
        self.history_ch4 = []
        self.history_h2o = []
        self.history_greenhouse_effect = []
        self.history_emissivity = []
        
        # 데이지 위치 생성 (극좌표 사용)
        self.planet_radius_px = planet_radius_px
        self.center_x = center_x
        self.center_y = center_y
        self.daisy_positions = self._generate_daisy_positions()
    
        self.solar_luminosity = INITIAL_SOLAR_LUMINOSITY

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
    
    def _calculate_greenhouse_effect(self):
        """
        온실 기체 농도를 바탕으로 온실효과 계산
        
        Returns:
            총 온실효과 값 (0 ~ 1 범위로 정규화)
        """
        # 각 온실 기체의 기여도 계산 (초기 농도 대비 비율)
        co2_contribution = (self.co2_concentration / INITIAL_CO2_CONCENTRATION) * CO2_GREENHOUSE_FACTOR
        ch4_contribution = (self.ch4_concentration / INITIAL_CH4_CONCENTRATION) * CH4_GREENHOUSE_FACTOR
        h2o_contribution = (self.h2o_concentration / INITIAL_H2O_CONCENTRATION) * H2O_GREENHOUSE_FACTOR
        
        # 총 온실효과 (가중 평균)
        total_effect = (co2_contribution + ch4_contribution + h2o_contribution) / 3.0
        
        # 0과 1 사이로 정규화 (너무 커지지 않도록)
        normalized_effect = min(total_effect, 3.0) / 3.0
        
        return normalized_effect
    
    def _update_earth_emissivity(self):
        """
        온실효과에 따라 지구 복사 방출 효율 업데이트
        온실효과가 증가하면 → 대기가 열을 가두므로 → 방출 효율 감소
        """
        # 온실효과가 클수록 방출 효율이 감소
        # emissivity = base_emissivity * (1 - greenhouse_effect * coefficient)
        self.earth_emissivity = BASE_EARTH_EMISSIVITY * (1.0 - self.greenhouse_effect * GREENHOUSE_EFFECT_COEFFICIENT)
        
        # 최소값 보장 (완전히 0이 되지 않도록)
        self.earth_emissivity = max(self.earth_emissivity, 0.3)
    
    def _update_greenhouse_gases(self):
        """
        시간에 따른 온실 기체 농도 업데이트
        광합성과 호흡을 통한 CO2/O2 순환 포함
        """
        total_daisy_area = self.area_black_daisy + self.area_white_daisy
        
        # === 광합성 및 호흡 시스템 ===
        # 호흡: 항상 일정하게 발생 (O2 소비, CO2 생성)
        respiration_co2 = total_daisy_area * RESPIRATION_RATE
        respiration_o2 = -total_daisy_area * RESPIRATION_RATE  # O2 소비 (음수)
        
        # 광합성: 낮에만 발생 (CO2 소비, O2 생성)
        # 온도가 높을수록 광합성 효율 증가
        if self.is_daytime:
            temp_celsius = self.temperature_planet - 273.15
            temp_boost = 1.0 + (temp_celsius * PHOTOSYNTHESIS_TEMP_COEFFICIENT)  # 온도에 따른 효율 증가
            temp_boost = max(0.5, min(temp_boost, 2.0))  # 0.5~2.0 범위로 제한
            
            photosynthesis_rate = BASE_PHOTOSYNTHESIS_RATE * temp_boost * self.solar_intensity
            photosynthesis_co2 = -total_daisy_area * photosynthesis_rate  # CO2 소비 (음수)
            photosynthesis_o2 = total_daisy_area * photosynthesis_rate    # O2 생성 (양수)
        else:
            # 밤: 광합성 없음
            photosynthesis_co2 = 0.0
            photosynthesis_o2 = 0.0
        
        # 순 변화량 계산
        # 낮: 광합성 > 호흡 → 순 O2 생성, CO2 소비
        # 밤: 호흡만 → O2 소비, CO2 생성 (낮의 축적량보다 적음)
        net_co2_change = respiration_co2 + photosynthesis_co2
        net_o2_change = respiration_o2 + photosynthesis_o2
        
        self.co2_concentration += net_co2_change
        self.o2_concentration += net_o2_change
        
        # CH4: 습지(바다 근처)와 생물 활동에 따라 변화
        ch4_production = total_daisy_area * 0.001  # 생물 활동
        ch4_decay = self.ch4_concentration * 0.001  # 자연 분해
        self.ch4_concentration += ch4_production - ch4_decay
        
        # H2O: 온도와 바다 면적에 따라 증발/응결
        temp_factor = (self.temperature_ocean - 273.15) / 100.0  # 섭씨 기준
        evaporation = max(0, temp_factor * 30.0)  # 증발 속도 감소 (50.0 → 30.0)
        condensation = self.h2o_concentration * 0.002  # 응결 속도 증가 (0.001 → 0.002)
        self.h2o_concentration += evaporation - condensation
        
        # 농도 상한선 및 하한선 설정 (폭주 방지)
        self.co2_concentration = max(50.0, min(self.co2_concentration, 800.0))  # 50~800 ppm
        self.o2_concentration = max(100000.0, min(self.o2_concentration, 300000.0))  # 100000~300000 ppm (10~30%)
        self.ch4_concentration = max(0.5, min(self.ch4_concentration, 5.0))     # 0.5~5 ppm
        self.h2o_concentration = max(1000.0, min(self.h2o_concentration, 25000.0))  # 1000~25000 ppm
    
    def _calculate_terrain_temperatures(self, effective_solar_luminosity):
        """
        지형별 온도 계산 (열용량 고려)
        
        Args:
            effective_solar_luminosity: 유효 태양 광도
        """
        # 지형별 기본 온도 계산 (열용량 없이)
        base_temp_ocean = (
            effective_solar_luminosity * (1 - ALBEDO_OCEAN) /
            (self.earth_emissivity * STEFAN_BOLTZMANN_CONSTANT)
        ) ** 0.25
        
        base_temp_land = (
            effective_solar_luminosity * (1 - ALBEDO_LAND) /
            (self.earth_emissivity * STEFAN_BOLTZMANN_CONSTANT)
        ) ** 0.25
        
        # 대기 온도는 해양과 육지의 가중 평균
        base_temp_atmosphere = (
            base_temp_ocean * OCEAN_RATIO +
            base_temp_land * LAND_RATIO
        )
        
        # 열용량 적용 (이전 온도와 새 온도의 가중 평균)
        # 열용량이 클수록 이전 온도를 더 많이 유지
        self.temperature_atmosphere = (
            self.temperature_atmosphere * ATMOSPHERE_HEAT_CAPACITY +
            base_temp_atmosphere * (1 - ATMOSPHERE_HEAT_CAPACITY)
        )
        
        self.temperature_ocean = (
            self.temperature_ocean * OCEAN_HEAT_CAPACITY +
            base_temp_ocean * (1 - OCEAN_HEAT_CAPACITY)
        )
        
        self.temperature_land = (
            self.temperature_land * LAND_HEAT_CAPACITY +
            base_temp_land * (1 - LAND_HEAT_CAPACITY)
        )
        
        # 행성 전체 온도는 각 지형의 가중 평균
        self.temperature_planet = (
            self.temperature_atmosphere * 0.3 +  # 대기 영향 30%
            self.temperature_ocean * OCEAN_RATIO * 0.7 +  # 바다 영향
            self.temperature_land * LAND_RATIO * 0.7      # 대륙 영향
        )
    
    def _update_milankovitch_cycles(self):
        """
        밀란코비치 주기 업데이트
        - 이심률 (Eccentricity): 궤도의 타원 정도
        - 자전축 기울기 (Obliquity): 자전축 기울기 변화
        - 세차운동 (Precession): 자전축의 회전
        """
        # 1. 이심률 변화 (100,000년 주기)
        eccentricity_phase = (2 * np.pi * self.current_time) / ECCENTRICITY_CYCLE
        self.eccentricity = ECCENTRICITY_MIN + (ECCENTRICITY_MAX - ECCENTRICITY_MIN) * \
                           (0.5 + 0.5 * np.sin(eccentricity_phase))
        
        # 2. 자전축 기울기 변화 (41,000년 주기)
        obliquity_phase = (2 * np.pi * self.current_time) / OBLIQUITY_CYCLE
        self.obliquity = OBLIQUITY_MIN + (OBLIQUITY_MAX - OBLIQUITY_MIN) * \
                        (0.5 + 0.5 * np.sin(obliquity_phase))
        
        # 3. 세차운동 (26,000년 주기)
        precession_phase = (2 * np.pi * self.current_time) / PRECESSION_CYCLE
        self.precession_angle = precession_phase * (180 / np.pi)  # 라디안을 도로 변환
    
    def _calculate_solar_distance_factor(self):
        """
        이심률과 세차운동에 따른 태양-지구 거리 계수 계산
        거리가 가까우면 태양 복사 에너지 증가
        
        Returns:
            태양 복사 에너지 변화 계수 (1.0 기준)
        """
        # 궤도 상 위치 (세차운동 고려)
        orbital_angle = self.precession_angle + (self.day_night_timer / DAY_NIGHT_CYCLE_DURATION) * 360
        orbital_angle_rad = orbital_angle * (np.pi / 180)
        
        # 타원 궤도에서의 거리 변화
        # r = a(1-e^2)/(1+e*cos(θ))
        distance_factor = (1 - self.eccentricity**2) / (1 + self.eccentricity * np.cos(orbital_angle_rad))
        
        # 거리의 제곱에 반비례 (1/r^2 법칙)
        solar_factor = 1.0 / (distance_factor ** 2)
        
        return solar_factor
    
    def _calculate_seasonal_factor(self):
        """
        자전축 기울기에 따른 계절 변화 계산
        기울기가 클수록 계절 변화 심함
        
        Returns:
            계절 효과 계수 (0.8 ~ 1.2)
        """
        # 태양에 대한 지구 기울기 효과
        obliquity_rad = self.obliquity * (np.pi / 180)
        
        # 낮/밤 사이클 위치에 따른 계절 (여름/겪울)
        seasonal_phase = (self.day_night_timer / DAY_NIGHT_CYCLE_DURATION) * 2 * np.pi
        
        # 기울기에 따른 태양 복사 변화
        seasonal_factor = 1.0 + 0.2 * np.sin(obliquity_rad) * np.cos(seasonal_phase)
        
        return seasonal_factor
    
    def _update_day_night_cycle(self):
        """
        낮/밤 사이클 업데이트
        100스텝마다 낮과 밤이 전환되며, 태양 강도는 점진적으로 변화
        """
        self.day_night_timer += 1
        
        # 주기가 지나면 낮/밤 전환
        if self.day_night_timer >= DAY_NIGHT_CYCLE_DURATION:
            self.is_daytime = not self.is_daytime
            self.day_night_timer = 0
        
        # 태양 강도 점진적 변화 (부드러운 전환)
        if self.is_daytime:
            # 낮이 되면 태양 강도를 서서히 증가
            target_intensity = 1.0
        else:
            # 밤이 되면 태양 강도를 서서히 감소
            target_intensity = NIGHT_SOLAR_REDUCTION
        
        # 현재 강도를 목표 강도로 부드럽게 이동
        self.solar_intensity += (target_intensity - self.solar_intensity) * TRANSITION_SMOOTHNESS
    
    def _get_effective_solar_luminosity(self):
        """
        현재 낮/밤 상태에 따른 유효 태양 광도 계산
        밀란코비치 주기 효과 포함:
        - 이심률: 태양-지구 거리 변화
        - 자전축 기울기: 계절 변화
        - 세차운동: 계절과 궤도 위치의 위상 변화
        
        Returns:
            유효 태양 광도
        """
        # 기본 태양 광도 (낮/밤 고려)
        base_luminosity = self.solar_luminosity * self.solar_intensity
        
        # 밀란코비치 효과 적용
        distance_factor = self._calculate_solar_distance_factor()  # 이심률 + 세차운동
        seasonal_factor = self._calculate_seasonal_factor()        # 자전축 기울기
        
        # 최종 태양 광도
        effective_luminosity = base_luminosity * distance_factor * seasonal_factor
        
        return effective_luminosity
    
    def step(self):
        """시뮬레이션 한 스텝 실행"""
        # 무한 시뮬레이션 (시간 제한 없음)
        
        # 밀란코비치 주기 업데이트
        self._update_milankovitch_cycles()
        
        # 낮/밤 사이클 업데이트
        self._update_day_night_cycle()
        
        # 온실 기체 농도 업데이트
        self._update_greenhouse_gases()
        
        # 온실효과 계산
        self.greenhouse_effect = self._calculate_greenhouse_effect()
        
        # 지구 방출 효율 업데이트
        self._update_earth_emissivity()
        
        
        # 유효 태양 광도 (낮/밤 고려)
        effective_solar_luminosity = self._get_effective_solar_luminosity()
        
        # 빈 땅 면적 계산
        self.area_bare_ground = 1 - self.area_black_daisy - self.area_white_daisy
        
        # 최소 면적 보장
        if self.area_black_daisy < MIN_AREA_THRESHOLD:
            self.area_black_daisy = MIN_AREA_THRESHOLD
        if self.area_white_daisy < MIN_AREA_THRESHOLD:
            self.area_white_daisy = MIN_AREA_THRESHOLD
        
        # 행성 평균 알베도 계산 (대륙 부분만 - 데이지 영향)
        # 대륙에서의 데이지 비율 계산
        land_albedo = (
            (self.area_bare_ground * ALBEDO_LAND) +
            (self.area_black_daisy * ALBEDO_BLACK_DAISY) +
            (self.area_white_daisy * ALBEDO_WHITE_DAISY)
        )
        
        # 행성 전체 알베도 (바다 + 대륙)
        self.planetary_albedo = (
            ALBEDO_OCEAN * OCEAN_RATIO +
            land_albedo * LAND_RATIO
        )
        
        # 지형별 온도 계산 (열용량 고려)
        self._calculate_terrain_temperatures(effective_solar_luminosity)
        
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
        self.history_atmosphere_temp.append(self.temperature_atmosphere)
        self.history_ocean_temp.append(self.temperature_ocean)
        self.history_land_temp.append(self.temperature_land)
        self.history_black_daisy.append(self.area_black_daisy)
        self.history_white_daisy.append(self.area_white_daisy)
        self.history_co2.append(self.co2_concentration)
        self.history_o2.append(self.o2_concentration)
        self.history_ch4.append(self.ch4_concentration)
        self.history_h2o.append(self.h2o_concentration)
        self.history_greenhouse_effect.append(self.greenhouse_effect)
        self.history_emissivity.append(self.earth_emissivity)
        
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
