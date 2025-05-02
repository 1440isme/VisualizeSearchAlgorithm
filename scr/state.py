from scr.pathfinder.models.solution import Solution
from scr.widgets import Label, Popup

"""Đây là một lớp dùng "Singleton pattern" để lưu trạng thái chung toàn cục của ứng dụng"""

class State:
    __instance = None 

    overlay: bool = False # đang hiển thị lớp phủ ko ? 
    label: Label 
    speed_label: Label
    done_visualising: bool = False  # Initialize to False
    need_update: bool
    results: dict[str, dict[str, float]] = {}  # Initialize as empty dict
    run_all_mazes = False
    results_popup: Popup | None = None
    player_mode: bool = False
    show_controls: bool = True

    # Nếu chưa có -> tạo mới, còn đã có -> trả lại cái đã có
    # -> Đảm bảo mọi chương trình dùng chung 1 trạng thái duy nhất
    def __new__(cls):
        if State.__instance is None:
            State.__instance = object.__new__(cls)

        return State.__instance