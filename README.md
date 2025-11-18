# 🌍 Daisyworld Advanced Simulator

가이아 이론을 설명하는 데이지월드 모델의 고급 대화형 시뮬레이션 프로그램입니다. 밀란코비치 주기, 광합성/호흡 시스템, 해양-대륙 지형을 포함한 현실적인 지구 시스템 모델링을 제공합니다.

## 📖 데이지월드란?

데이지월드(Daisyworld)는 영국의 과학자 제임스 러브록(James Lovelock)이 가이아 가설을 설명하기 위해 1983년에 제안한 컴퓨터 시뮬레이션 모델입니다.

### 핵심 개념
- **검은 데이지**: 열을 흡수하여 주변 온도를 높임
- **흰 데이지**: 열을 반사하여 주변 온도를 낮춤
- **자기조절**: 데이지들이 자발적으로 행성 온도를 최적 상태로 유지

## ✨ 주요 기능

### 1. 🌱 데이지 생태계 및 광합성/호흡 시스템
- 검은 데이지와 흰 데이지의 경쟁 및 공존
- 온도에 따른 성장률 변화 (최적 온도: 295.5K / 22.35°C)
- **광합성 시스템** (낮): CO₂ 흡수 + O₂ 생성
- **호흡 시스템** (24시간): CO₂ 배출 + O₂ 소비
- 온도에 따른 광합성 효율 변화 (온도↑ → 광합성↑)
- 개체군 동역학 (출생, 사망, 면적 변화)

### 2. 🌍 해양-대륙 지형 시스템
- **바다 70% / 대륙 30%** 비율 (지구와 동일)
- 지형별 독립적인 온도 계산
  - 대기 온도: 250K 초기값
  - 해양 온도: 250K 초기값
  - 대륙 온도: 250K 초기값
- 지형별 열용량 (온도 변화 속도):
  - 대기: 0.88 (12% 변화)
  - 바다: 0.96 (4% 변화, 매우 느림)
  - 대륙: 0.90 (10% 변화)
- 지형별 알베도 (반사율):
  - 바다: 0.06 (94% 흡수)
  - 대륙: 0.30 (70% 흡수)

### 3. 🌡️ 대기 및 온실효과
- **4가지 대기 기체 추적**:
  - O₂ (산소): 210,000ppm (~21%), 광합성/호흡 순환
  - CO₂ (이산화탄소): 400ppm, 기준 온실효과
  - CH₄ (메탄): 1.8ppm, CO₂ 대비 25배 강력
  - H₂O (수증기): 10,000ppm (~1%), 온도 기반 증발/응결
- 온실가스 동적 평형 시스템 (상한선 설정)
- 온실효과에 따른 지구 복사 방출 효율 계산
- 슈테판-볼츠만 법칙 기반 온도 계산

### 4. 🪐 밀란코비치 주기 (Milankovitch Cycles)
실제 지구의 천문학적 주기를 시뮬레이션에 적용:

**이심률 (Eccentricity)**:
- 주기: 10,000 스텝 (~417일, ~1.14년)
- 범위: 0.0 ~ 0.06
- 효과: 태양-지구 거리 변화 → 태양 복사 에너지 변동

**자전축 기울기 (Obliquity)**:
- 주기: 4,100 스텝 (~171일, ~5.7개월)
- 범위: 22.1° ~ 24.5° (현재 23.5°)
- 효과: 계절 변화 강도 조절

**세차운동 (Precession)**:
- 주기: 2,600 스텝 (~108일, ~3.6개월)
- 범위: 0° ~ 360°
- 효과: 계절과 궤도 위치의 위상 변화

→ 빙하기-간빙기 순환 재현 가능!

### 5. 🌞🌙 현실적인 낮/밤 사이클
- **24스텝 = 1일** (1 스텝 = 1시간)
- 점진적 태양 강도 변화 (급격한 온도 변화 방지)
- 밤에도 42% 에너지 유지 (대기 산란, 지구 복사열)
- 실시간 배경색 전환 (흰색 ↔ 검은색)
- 목표 온도 범위:
  - 낮: 295-305K (22-32°C)
  - 밤: 268-278K (-5~5°C)
  - 일교차: ~30°C

### 6. 📊 실시간 시각화 (이중 창)
#### Pygame 창 - 행성 시각화
- 800×800 픽셀 3D 행성 렌더링
- **바다(파란색) / 대륙(녹색) 지형** 800개 포인트
- **대기층** 반투명 렌더링 (30픽셀 두께)
- 300개 데이지 개체 실시간 렌더링
- 낮/밤 배경색 점진적 전환
- 상세 정보 표시:
  - 시간 및 낮/밤 상태
  - 밀란코비치 변수 (이심률, 기울기, 세차)
  - 온도 (대기/바다/대륙)
  - 데이지 개체수
  - 대기 조성 (O₂, CO₂, CH₄, H₂O)
  - 온실효과

#### Matplotlib 창 - 통계 그래프 (3개)
- **그래프 1**: 데이지 개체수 변화
- **그래프 2**: 행성 온도 변화
- **그래프 3**: 온실가스 농도 변화 (CO₂, CH₄, H₂O)
- 동적 X/Y축 범위 자동 조정
- 자동 그래프 저장 (PNG, 300 DPI)

## 🚀 설치 및 실행

### 필요한 패키지
```bash
pip install pygame matplotlib numpy
```

### 실행 방법
```bash
python main.py
```

## 📁 프로젝트 구조

```
데이지 월드/
├── main.py                    # 메인 실행 파일
├── simulator.py               # 시뮬레이션 코어 로직
├── visualizer_pygame.py       # Pygame 시각화
├── visualizer_matplotlib.py   # Matplotlib 그래프
├── main.cpp                   # C++ 버전 (텍스트 출력)
├── results/                   # 시뮬레이션 결과 저장 폴더
└── README.md                  # 프로젝트 설명서
```

## 🎮 사용법

### 기본 조작
1. **프로그램 시작**: `python main.py` 실행
2. **2개 창 자동 오픈**:
   - Pygame 창: 행성 시각화
   - Matplotlib 창: 실시간 그래프
3. **시뮬레이션 종료**: Pygame 창 닫기
4. **결과 저장**: 종료 시 자동으로 `results/` 폴더에 PNG 저장

### 화면 정보
- **Time**: 현재 시뮬레이션 스텝 (1 스텝 = 1시간)
- **Day/Night**: 낮/밤 상태 및 전환 백분율 (0~100)
- **Solar Intensity**: 현재 태양 강도 (0.0~1.0)
- **Milankovitch Cycles**:
  - Eccentricity: 이심률 (0.0~0.06)
  - Obliquity: 자전축 기울기 (22.1~24.5°)
  - Precession: 세차운동 각도 (0~360°)
- **Temperatures**:
  - Atmosphere: 대기 온도 (K)
  - Ocean: 해양 온도 (K)
  - Land: 대륙 온도 (K)
- **Daisies**: Black/White 데이지 면적 비율
- **Atmosphere**:
  - O₂: 산소 농도 (ppm)
  - CO₂: 이산화탄소 농도 (ppm)
  - CH₄: 메탄 농도 (ppm)
  - H₂O: 수증기 농도 (ppm)
  - GH Effect: 총 온실효과

## ⚙️ 주요 상수 설정

### ⏱️ 시간 시스템
```python
TIME_STEP_SECONDS = 3600            # 1 스텝 = 1시간 (3600초)
DAY_NIGHT_CYCLE_DURATION = 24       # 1일 = 24 스텝
FPS = 20                            # 20 FPS → 1초에 20 스텝
```
→ **시뮬레이션 속도: 현실의 72,000배**

### 🌍 물리 상수
```python
STEFAN_BOLTZMANN_CONSTANT = 5.6696e-8  # 슈테판-볼츠만 상수
BASE_EARTH_EMISSIVITY = 1.0             # 기본 지구 복사 방출 효율
GREENHOUSE_EFFECT_COEFFICIENT = 0.38    # 온실효과 계수
```

### 🗺️ 지형 설정
```python
# 비율
OCEAN_RATIO = 0.7                   # 바다 70%
LAND_RATIO = 0.3                    # 대륙 30%

# 알베도 (반사율)
ALBEDO_OCEAN = 0.06                 # 바다: 6% 반사, 94% 흡수
ALBEDO_LAND = 0.3                   # 대륙: 30% 반사, 70% 흡수
ALBEDO_BLACK_DAISY = 0.25           # 검은 데이지: 25% 반사
ALBEDO_WHITE_DAISY = 0.75           # 흰 데이지: 75% 반사

# 열용량 (온도 변화 속도)
ATMOSPHERE_HEAT_CAPACITY = 0.88     # 대기: 12% 변화
OCEAN_HEAT_CAPACITY = 0.96          # 바다: 4% 변화 (매우 느림)
LAND_HEAT_CAPACITY = 0.90           # 대륙: 10% 변화
```

### 🌡️ 초기 온도
```python
INITIAL_TEMPERATURE = 250.0         # 모든 온도 250K (-23°C)에서 시작
```

### 🌱 생태계 파라미터
```python
OPTIMAL_TEMPERATURE = 295.5         # 최적 성장 온도 (K / 22.35°C)
DEATH_RATE = 0.3                    # 사망률 30%
TEMPERATURE_FEEDBACK_FACTOR = 20    # 온도 피드백 계수
INITIAL_BLACK_DAISY = 0.01          # 초기 검은 데이지 1%
INITIAL_WHITE_DAISY = 0.01          # 초기 흰 데이지 1%
```

### 💨 대기 조성 초기값
```python
INITIAL_O2_CONCENTRATION = 210000.0  # O₂: 210,000 ppm (~21%)
INITIAL_CO2_CONCENTRATION = 400.0    # CO₂: 400 ppm
INITIAL_CH4_CONCENTRATION = 1.8      # CH₄: 1.8 ppm
INITIAL_H2O_CONCENTRATION = 10000.0  # H₂O: 10,000 ppm (~1%)
```

### 🌿 광합성/호흡
```python
PHOTOSYNTHESIS_BASE_RATE = 2.0           # 광합성 기본 속도
RESPIRATION_RATE = 1.0                    # 호흡 속도
PHOTOSYNTHESIS_TEMP_COEFFICIENT = 0.01   # 온도당 1% 효율 증가
```

### 🌞 낮/밤 사이클
```python
DAY_NIGHT_CYCLE_DURATION = 24       # 24시간 = 1일
NIGHT_SOLAR_REDUCTION = 0.42        # 밤에 42% 에너지 유지
TRANSITION_SMOOTHNESS = 0.08        # 점진적 전환 속도
```

### 🪐 밀란코비치 주기
```python
# 이심률 (Eccentricity)
ECCENTRICITY_CYCLE = 10000          # 주기: 10,000 스텝
ECCENTRICITY_MIN = 0.0              # 최소: 0.0 (원형)
ECCENTRICITY_MAX = 0.06             # 최대: 0.06

# 자전축 기울기 (Obliquity)
OBLIQUITY_CYCLE = 4100              # 주기: 4,100 스텝
OBLIQUITY_MIN = 22.1                # 최소: 22.1°
OBLIQUITY_MAX = 24.5                # 최대: 24.5°
CURRENT_OBLIQUITY = 23.5            # 현재: 23.5°

# 세차운동 (Precession)
PRECESSION_CYCLE = 2600             # 주기: 2,600 스텝
```

### ☀️ 태양 광도
```python
INITIAL_SOLAR_LUMINOSITY = 450      # 초기값: 450
SOLAR_LUMINOSITY_INCREASE_RATE = 0.0  # 증가율: 0 (고정)
```

## 🔬 시뮬레이션 메커니즘

### 1. 지형별 온도 계산
슈테판-볼츠만 법칙 + 열용량:
```
T_base = [(S × (1 - α_terrain)) / (ε × σ)]^(1/4)
T_new = T_old × HC + T_base × (1 - HC)
```
- `S`: 유효 태양 광도 (밀란코비치 주기 적용)
- `α_terrain`: 지형별 알베도 (바다 0.06, 대륙 0.30)
- `ε`: 복사 방출 효율 (온실효과 반영)
- `HC`: 열용량 (대기 0.88, 바다 0.96, 대륙 0.90)

### 2. 밀란코비치 효과
유효 태양 광도 계산:
```
S_eff = S_base × I_solar × F_distance × F_seasonal
```
- `I_solar`: 낮/밤 태양 강도 (0.42 ~ 1.0)
- `F_distance`: 거리 계수 = 1 / r² (이심률 + 세차운동)
- `F_seasonal`: 계절 계수 = 1 + 0.2×sin(obliquity)×cos(phase)

### 3. 광합성 및 호흡
**낮 (광합성 > 호흡)**:
```
P_rate = P_base × (1 + T × P_coeff)  # 온도 기반 효율
CO₂: -P_rate + R_rate  (순효과: 감소)
O₂:  +P_rate - R_rate  (순효과: 증가)
```

**밤 (호흡만)**:
```
CO₂: +R_rate  (증가)
O₂:  -R_rate  (감소)
```

### 4. 데이지 성장률
포물선 함수:
```
GF = 1 - k × (T_opt - T)²
```
- 최적 온도 295.5K에서 최대 성장
- 온도가 멀어질수록 성장률 감소

### 5. 온실효과
```
GE = (CO₂×1.0 + CH₄×25.0 + H₂O×0.1) / 3.0
ε = ε₀ × (1 - GE × 0.38)
```
- 온실효과 증가 → 방출 효율 감소 → 온도 상승

### 6. 대기 조성 변화
```
CO₂: 광합성/호흡, 범위 50~800 ppm
CH₄: 생물 활동/분해, 범위 0.5~5 ppm
H₂O: 온도 기반 증발/응결, 범위 1,000~25,000 ppm
O₂: 광합성/호흡, 범위 150,000~250,000 ppm
```

## 📈 데이터 출력

### 자동 저장 파일
- **파일명**: `daisyworld_simulation_YYYYMMDD_HHMMSS.png`
- **위치**: `results/` 폴더
- **형식**: PNG, 300 DPI 고해상도
- **내용**:
  - 상단: 데이지 개체수 그래프
  - 중단: 행성 온도 그래프
  - 하단: **온실가스 농도 그래프 (신규!)**

### 추가 설정 파일
- **파일명**: `initial_settings.txt`
- **내용**: 모든 초기 설정값, 상수, 시간 변환표

### 콘솔 출력
```
Total simulation steps: 500
Final temperature: 287.34 K
Final black daisy area: 0.4523
Final white daisy area: 0.3821
```

## 🎯 교육적 활용

### 학습 목표
1. **가이아 이론 이해**: 생명체가 환경을 조절하는 메커니즘
2. **피드백 시스템**: 양성/음성 피드백의 역할
3. **생태계 평형**: 자기조절 시스템의 안정성
4. **기후 과학**: 온실효과와 온도 조절

### 실험 아이디어
1. **밀란코비치 주기 관찰**: 10,000 스텝 이상 실행 → 빙하기 패턴 확인
2. **광합성 효율 변경**: PHOTOSYNTHESIS_TEMP_COEFFICIENT 조정 → O₂/CO₂ 균형 변화
3. **열용량 비교**: OCEAN_HEAT_CAPACITY 변경 → 일교차 변화 측정
4. **초기 온도 실험**: 250K vs 300K 시작 → 평형 도달 시간 비교
5. **온실효과 강도**: GREENHOUSE_EFFECT_COEFFICIENT 조정 → 온난화 시뮬레이션
6. **지형 비율**: OCEAN_RATIO 변경 → 행성 안정성 연구
7. **낮/밤 주기**: DAY_NIGHT_CYCLE_DURATION 변경 → 생태계 적응 관찰

## 🛠️ 커스터마이징

### 시뮬레이션 속도 조정
```python
# visualizer_pygame.py
FPS = 20  # 프레임 속도 (높을수록 빠름)
```

### 데이지 개수 변경
```python
# simulator.py
NUM_DAISIES = 300  # 화면에 표시할 데이지 수
```

### 온실효과 강도 조정
```python
# simulator.py
GREENHOUSE_EFFECT_COEFFICIENT = 0.3  # 온실효과 계수
```

## ⏰ 시간 변환표

| 시뮬레이션 시간 | 현실 시간 (20 FPS) |
|---------------|-------------------|
| 1 스텝 (1시간) | 0.05초 |
| 24 스텝 (1일) | 1.2초 |
| 100 스텝 | 5초 |
| 1,000 스텝 | 50초 |
| 2,600 스텝 (세차 1주기) | 2.2분 |
| 4,100 스텝 (기울기 1주기) | 3.4분 |
| 10,000 스텝 (이심률 1주기) | 8.3분 |

→ **72,000배 빠른 시뮬레이션!**

## 🐛 알려진 제한사항

1. ~~**열용량 미구현**~~ → ✅ **구현 완료** (대기/바다/대륙 독립적 열용량)
2. **공간적 균일성**: 모든 지역이 동일한 온도 (위도별 차이 없음)
3. **단순화된 생태계**: 2종만 고려 (실제는 수천 종)
4. ~~**고정된 온실 기체**~~ → ✅ **구현 완료** (광합성/호흡 시스템)
5. **단순화된 밀란코비치**: 실제 주기를 1000배 축소

## 🔮 향후 개선 계획

- [x] 열용량(Thermal Inertia) 추가
- [x] 밀란코비치 주기 구현
- [x] 광합성/호흡 시스템
- [x] 해양-대륙 지형 구분
- [ ] 공간적 온도 분포 (위도별 차이)
- [ ] 다양한 생물 종 추가
- [ ] 대기 순환 모델
- [ ] GUI 컨트롤 패널 추가
- [ ] 3D 시각화
- [ ] 화산 활동, 운석 충돌 등 이벤트 시스템

## 📚 참고 자료

- Lovelock, J. E. (1983). "Daisyworld: a cybernetic proof of the Gaia hypothesis"
- Watson, A. J., & Lovelock, J. E. (1983). "Biological homeostasis of the global environment"
- [Gaia Hypothesis - Wikipedia](https://en.wikipedia.org/wiki/Gaia_hypothesis)
- [Daisyworld Model - Wikipedia](https://en.wikipedia.org/wiki/Daisyworld)

## 📄 라이선스

이 프로젝트는 교육 목적으로 제작되었습니다.

## 👥 기여

버그 리포트, 기능 제안, Pull Request 환영합니다!

---

**Made with 🌍 for understanding planetary self-regulation**
