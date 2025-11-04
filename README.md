# 🌍 Daisyworld Simulator

가이아 이론을 설명하는 데이지월드 모델의 대화형 시뮬레이션 프로그램입니다. Pygame과 Matplotlib을 활용하여 실시간으로 행성 생태계의 자기조절 메커니즘을 시각화합니다.

## 📖 데이지월드란?

데이지월드(Daisyworld)는 영국의 과학자 제임스 러브록(James Lovelock)이 가이아 가설을 설명하기 위해 1983년에 제안한 컴퓨터 시뮬레이션 모델입니다.

### 핵심 개념
- **검은 데이지**: 열을 흡수하여 주변 온도를 높임
- **흰 데이지**: 열을 반사하여 주변 온도를 낮춤
- **자기조절**: 데이지들이 자발적으로 행성 온도를 최적 상태로 유지

## ✨ 주요 기능

### 1. 🌱 데이지 생태계 시뮬레이션
- 검은 데이지와 흰 데이지의 경쟁 및 공존
- 온도에 따른 성장률 변화 (최적 온도: 295.5K)
- 개체군 동역학 (출생, 사망, 면적 변화)

### 2. 🌡️ 대기 및 온실효과
- **3가지 온실 기체 추적**:
  - CO₂ (이산화탄소): 기준 온실효과
  - CH₄ (메탄): CO₂ 대비 25배 강력
  - H₂O (수증기): 온도에 따라 변동
- 온실효과에 따른 지구 복사 방출 효율 동적 계산
- 슈테판-볼츠만 법칙 기반 온도 계산

### 3. 🌞🌙 낮/밤 사이클
- 50스텝마다 자동으로 낮과 밤 전환
- 점진적 태양 강도 변화 (급격한 온도 변화 방지)
- 실시간 배경색 전환 (흰색 ↔ 검은색)
- 낮/밤에 따른 온도 변화 시뮬레이션

### 4. 📊 이중 창 실시간 시각화
#### Pygame 창 - 행성 시각화
- 800×800 픽셀 원형 행성
- 300개 데이지 개체 실시간 렌더링
- 낮/밤 배경색 점진적 전환
- 실시간 통계 정보 표시

#### Matplotlib 창 - 통계 그래프
- 데이지 개체수 변화 그래프
- 행성 온도 변화 그래프
- 동적 X축 범위 조정
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
- **Time**: 현재 시뮬레이션 스텝
- **Day/Night**: 낮/밤 상태 및 전환 타이머
- **Solar Intensity**: 현재 태양 강도 (0.0~1.0)
- **Temperature**: 행성 온도 (Kelvin)
- **Black/White Daisy**: 각 데이지의 면적 비율
- **Solar Luminosity**: 태양 광도
- **Greenhouse Gases**: CO₂, CH₄, H₂O 농도
- **Greenhouse Effect**: 총 온실효과
- **Emissivity**: 지구 복사 방출 효율

## ⚙️ 주요 상수 설정

### 물리 상수
```python
STEFAN_BOLTZMANN_CONSTANT = 5.6696e-8  # 슈테판-볼츠만 상수
BASE_EARTH_EMISSIVITY = 1.0             # 기본 지구 복사 방출 효율
```

### 알베도 (반사율)
```python
ALBEDO_BARE_GROUND = 0.5    # 빈 땅: 50%
ALBEDO_BLACK_DAISY = 0.25   # 검은 데이지: 25% (열 흡수)
ALBEDO_WHITE_DAISY = 0.75   # 흰 데이지: 75% (열 반사)
```

### 생태계 파라미터
```python
OPTIMAL_TEMPERATURE = 295.5         # 최적 성장 온도 (K)
DEATH_RATE = 0.3                    # 사망률
TEMPERATURE_FEEDBACK_FACTOR = 20    # 온도 피드백 계수
```

### 온실 기체 초기 농도
```python
INITIAL_CO2_CONCENTRATION = 400.0    # CO₂: 400 ppm
INITIAL_CH4_CONCENTRATION = 1.8      # CH₄: 1.8 ppm
INITIAL_H2O_CONCENTRATION = 10000.0  # H₂O: 10000 ppm (~1%)
```

### 낮/밤 사이클
```python
DAY_NIGHT_CYCLE_DURATION = 50      # 전환 주기 (스텝)
NIGHT_SOLAR_REDUCTION = 0.0        # 밤의 태양 광도 (0 = 완전 차단)
TRANSITION_SMOOTHNESS = 0.1        # 전환 부드러움 (10% 단계)
```

## 🔬 시뮬레이션 메커니즘

### 1. 온도 계산
슈테판-볼츠만 법칙 기반:
```
T = [(S × (1 - α)) / (ε × σ)]^(1/4)
```
- `S`: 유효 태양 광도 (낮/밤 고려)
- `α`: 행성 평균 알베도
- `ε`: 복사 방출 효율 (온실효과 반영)
- `σ`: 슈테판-볼츠만 상수

### 2. 데이지 성장률
포물선 함수:
```
GF = 1 - k × (T_opt - T)²
```
- 최적 온도에서 최대 성장
- 온도가 멀어질수록 성장률 감소

### 3. 온실효과
```
ε = ε₀ × (1 - GE × c)
```
- 온실효과 증가 → 방출 효율 감소 → 온도 상승

### 4. 낮/밤 전환
```
I(t+1) = I(t) + (I_target - I(t)) × s
```
- 점진적 태양 강도 변화 (부드러운 전환)

## 📈 데이터 출력

### 자동 저장 파일
- **파일명**: `daisyworld_simulation_YYYYMMDD_HHMMSS.png`
- **위치**: `results/` 폴더
- **형식**: PNG, 300 DPI 고해상도
- **내용**:
  - 상단: 데이지 개체수 그래프
  - 하단: 행성 온도 그래프

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
1. 태양 광도 증가율 변경 → 적응력 관찰
2. 온실 기체 농도 조정 → 온도 변화 측정
3. 낮/밤 주기 변경 → 생태계 반응 분석
4. 초기 데이지 비율 조정 → 경쟁 역학 연구

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

## 🐛 알려진 제한사항

1. **열용량 미구현**: 온도가 즉각 반응 (현실보다 급격함)
2. **공간적 균일성**: 모든 지역이 동일한 온도
3. **단순화된 생태계**: 2종만 고려
4. **고정된 온실 기체**: 자동 증가 없음 (수동 조정 필요)

## 🔮 향후 개선 계획

- [ ] 열용량(Thermal Inertia) 추가
- [ ] 공간적 온도 분포 (위도별 차이)
- [ ] 다양한 생물 종 추가
- [ ] 자동 온실 기체 배출 시나리오
- [ ] GUI 컨트롤 패널 추가
- [ ] 3D 시각화

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
