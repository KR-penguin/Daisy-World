"""
Daisyworld 시뮬레이션 메인 실행 파일
"""
import threading
from simulator import DaisyworldSimulator
from visualizer_pygame import run_pygame_visualization, PLANET_RADIUS_PX, CENTER_X, CENTER_Y
from visualizer_matplotlib import run_matplotlib_graphs, save_graphs


def main():
    """메인 실행 함수"""
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
    simulator = DaisyworldSimulator(
        planet_radius_px=PLANET_RADIUS_PX,
        center_x=CENTER_X,
        center_y=CENTER_Y
    )
    
    # Matplotlib을 별도 스레드에서 실행
    graph_thread = threading.Thread(target=run_matplotlib_graphs, args=(simulator,), daemon=True)
    graph_thread.start()
    
    # Pygame을 메인 스레드에서 실행
    run_pygame_visualization(simulator)
    
    # 시뮬레이션 종료 후 그래프 저장
    print("\nSaving simulation results...")
    saved_file = save_graphs(simulator)
    
    print("Simulation completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
