"""
Matplotlib을 이용한 그래프 시각화 및 저장 모듈
"""
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime
import os
from simulator import OPTIMAL_TEMPERATURE


def run_matplotlib_graphs(simulator):
    """
    Matplotlib으로 실시간 그래프 표시
    
    Args:
        simulator: DaisyworldSimulator 인스턴스
    """
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


def save_graphs(simulator, output_dir='results'):
    """
    시뮬레이션 결과 그래프를 파일로 저장
    
    Args:
        simulator: DaisyworldSimulator 인스턴스
        output_dir: 저장할 디렉토리 경로
        
    Returns:
        저장된 파일 경로
    """
    # 결과 디렉토리 생성
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 타임스탬프로 파일명 생성
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Figure 생성
    fig, (ax_population, ax_temperature) = plt.subplots(2, 1, figsize=(12, 10))
    fig.suptitle(f'Daisyworld Simulation Results\n{timestamp}', fontsize=16, fontweight='bold')
    
    # 개체수 그래프
    ax_population.plot(simulator.history_time, simulator.history_black_daisy, 'k-', linewidth=2, label='Black Daisy')
    ax_population.plot(simulator.history_time, simulator.history_white_daisy, color='lightblue', linewidth=2, label='White Daisy')
    ax_population.set_xlabel('Time (steps)', fontsize=12)
    ax_population.set_ylabel('Population Area', fontsize=12)
    ax_population.set_title('Daisy Population Over Time', fontsize=13, fontweight='bold')
    ax_population.grid(True, alpha=0.3)
    ax_population.legend(loc='best')
    
    # 온도 그래프
    ax_temperature.plot(simulator.history_time, simulator.history_temperature, 'r-', linewidth=2, label='Planet Temp')
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
    print(f"Total simulation steps: {simulator.current_time}")
    print(f"Final temperature: {simulator.temperature_planet:.2f} K")
    print(f"Final black daisy area: {simulator.area_black_daisy:.4f}")
    print(f"Final white daisy area: {simulator.area_white_daisy:.4f}")
    print(f"{'='*60}\n")
    
    return filename
