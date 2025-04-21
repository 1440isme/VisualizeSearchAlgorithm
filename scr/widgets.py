from abc import ABC, abstractmethod # Tạo lớp trừu tượng (Abstract Base Classes)
from enum import Enum
import pygame


# Lấy các hằng số từ file constants.py
from .constants import (
    BLACK, 
    DARK_BLUE,
    WHITE, 
    WIDTH,
    HEIGHT
)

# ================ Lớp cơ sở cho widget ================
class Widget(ABC): #Kế thừa ABC để thành lớp trừu tượng
    x: int 
    y: int
    width: int 
    height: int
    
    screen: pygame.surface.Surface # bề mặt để vẽ widget
    rect: pygame.rect.Rect # tạo hình chữ nhật bao quanh widget
    text: str # văn bản nếu có

    @abstractmethod
    def draw(self) -> None: # hàm để vẽ lên màn hình
        pass

    @abstractmethod
    def set_surface(self, surf: pygame.surface.Surface) -> None: # gán bề mặt đã vẽ
        pass


# ================ Thiết kế các button ================

class Button(Widget):
    def __init__(self,
        text: str,
        x: float | str, 
        y: float | str,
        padding: int = 5,
        font_size: int = 18,
        bold: bool = False,
        outline: bool = False,
        foreground_color: pygame.Color = pygame.Color(0,0,0), # màu chữ 
        background_color: pygame.Color = pygame.Color(255,255,255),
        surface: pygame.surface.Surface | None = None
    ) -> None:
        if surface:
            self.surface = surface  # Changed from self.screen to self.surface
        self.text = text
        self.padding = padding
        self.outline = outline # có vẽ viền không ?
        self.foreground_color = foreground_color
        self.background_color = background_color

        # Chọn font
        if bold:
            font = pygame.font.Font("assets/font/Montserrat-Bold.ttf", font_size)
        else:
            font = pygame.font.Font("assets/font/Montserrat-Regular.ttf", font_size)
        

        self.text_surf = font.render(self.text, True, foreground_color) # tạo bề mặt text
        self.text_rect = self.text_surf.get_rect() # lấy kích thước của text
        
        # Tính kích thước nút
        self.width = self.text_rect.width + padding * 2
        self.height = self.text_rect.height + padding * 2

        # Canh giữa nếu x/y là "center"
        if x == "center":
            x = (WIDTH - self.width) / 2
        if y == "center":
            y = (HEIGHT - self.height) / 2

        # Tạo hình chữ nhật đại diện cho nút
        self.rect = pygame.Rect(float(x), float(y), self.width, self.height)

        # Đặt vị trí cho text:
        self.text_rect.topleft = self.rect.x + padding, self.rect.y + padding

    def set_surface(self, surf: pygame.surface.Surface) -> None:
        self.surface = surf  # Changed from self.screen to self.surface

    def draw(self):
        """ Vẽ nút (các label)
        Args:
            surf (pygame.surface.Surface): Window surface
        Returns:
            bool: True nếu người dùng nhấn nút này
        """
        action = False # Mặc định không click
        pos = pygame.mouse.get_pos() # lấy vị trí của chuột
        action = self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] # kiểm tra click
        
        # Vẽ nút
        pygame.draw.rect(self.surface, self.background_color, self.rect)  # Changed from self.screen to self.surface

        if self.outline:
            pygame.draw.rect(self.surface, BLACK, self.rect, width=self.outline)  # Changed from self.screen to self.surface

        text_x, text_y = self.rect.x + self.padding, self.rect.y + self.padding
        self.surface.blit(self.text_surf, (text_x, text_y))  # Changed from self.screen to self.surface

        return action
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}{tuple(vars(self).values())!r}"
    
# ================ Thiết kế các Label ================
class Label(Button):
    def draw(self) -> None:
        """Vẽ nhãn văn bản
        Args:
            surf (pygame.surface.Surface): Destination surface
            (giống Button nhưng không xử lí click)
    
        """
        # Vẽ hình chữ nhật đại diện cho label
        pygame.draw.rect(self.surface, self.background_color, self.rect)

        # Vẽ viền
        if self.outline:
            pygame.draw.rect(self.surface, BLACK, self.rect, width=self.outline)

        # Render văn bản
        text_x, text_y = self.rect.x + self.padding, self.rect.y + self.padding
        self.surface.blit(self.text_surf, (text_x, text_y))

# ================ Thiết kế các Menu ================
"""
Định hướng: tạo menu dạng popup gồm một button chính và một danh sách các Widget con.
Menu sẽ hiển thị khi người dùng nhấn vào nút chính.
"""
class Menu(Widget):
    def __init__(
        self, 
        surface: pygame.surface.Surface,
        button: Button,
        children: list[Widget]
    )-> None:
        self.surface = surface  # Changed from self.screen to self.surface
        self.button = button
        self.children = children
        self.clicked = False # trạng thái của menu (đang mở hay ko)
        self.selected: Widget | None = None # lưu lại Widget được chọn từ menu (nếu có)
        self.custom_button = None  # Sẽ lưu trữ reference đến CustomButton nếu được dùng

        self.height = sum(child.rect.height for child in children) # lấy tổng chiều cao của các mục
        self.width = max(child.rect.width for child in children) # lấy chiều rộng của thằng to nhất

        self.x = self.button.rect.x - 10 # nhít nhẹ bên trái để nhìn đẹp hơn
        self.y = self.button.rect.y

        if self.width < self.button.width:
            self.width = self.button.width + 40
            self.x = self.button.rect.x

        children[0].rect.x = self.x
        children[0].rect.top = self.button.rect.bottom

        for i in range(1, len(children)):
            child = children[i]
            prev = children[i - 1]
            child.rect.x = self.x
            child.rect.top = prev.rect.bottom

        # hiển thị vùng popup menu
        self.rect = self.button.rect
        self.popup_rect = pygame.Rect(self.x - 20, 
                                    self.button.rect.bottom, # rect.y + rect.height
                                    self.width + 40,
                                    self.height + 20)
        
    def set_surface(self, surf: pygame.surface.Surface) -> None:
        self.surface = surf  # Changed from self.screen to self.surface
        self.button.set_surface(surf)

    def draw(self) -> bool:
        """Vẽ menu

        Args: 
            surf (pygame.surface.Surface): Window surface
        
        Returns: 
            bool: Khi bất kì button trong menu đc nhấn
        """
        # Kiểm tra xem nút có được tham chiếu từ CustomButton không
        # Nếu không, gọi draw thông thường của Button
        clicked = False
        if hasattr(self, 'custom_button') and self.custom_button:
            # Chỉ kiểm tra click mà không vẽ, vì đã được vẽ trong visualize_mode.py
            mouse_pos = pygame.mouse.get_pos()
            clicked = (self.button.rect.collidepoint(mouse_pos) and 
                     pygame.mouse.get_pressed()[0])
        else:
            clicked = self.button.draw()
            
        self.selected = None

        if clicked:
            # Toggle the dropdown state when button is clicked
            self.clicked = not self.clicked
            return False

        if not self.clicked:
            return False
        
        # Xử lí nút khi đc nhấn hoặc ko
        action = False
        pygame.draw.rect(
            self.surface,
            DARK_BLUE,
            self.popup_rect,
            border_radius= 10
        )

        # Xử lí chọn
        for child in self.children:
            if child.draw():
                self.selected = child
                self.clicked = False # một nút con được nhấn thì đóng menu
                action = True

        return action
    
# ================ Orientation ================
class Orientation(Enum):
    HORIZONTAL = "X"
    VERTICAL = "Y"

# ================ Alignment ================
class Alignment(Enum):
    CENTER = "C"
    LEFT = "L"
    RIGHT = "R"
    TOP = "T"
    BOTTOM = "B"
    NONE = "N"

# ================ TableCell ================

"""Đại diện một ô trong bảng, có thể chứa 1 widget, màu nền và căn chỉnh"""
class TableCell:
    def __init__(
        self, 
        child: Widget,
        color: tuple[int, int, int] = WHITE,
        align: Alignment = Alignment.NONE
    ) -> None:
        self.child = child
        self.color = color
        self.alignment = align
        self.rect = pygame.Rect(child.rect)

    def draw(self, surf: pygame.surface.Surface) -> None:
        pygame.draw.rect(surf, self.color, self.rect)
        self.child.draw()

# ================ Table ================
"""Lớp Table là Widget dạng bảng, chứa nhiều TableCell dạng lưới (rows * cols)"""

class Table(Widget):
    def __init__(
        self,
        x: int, 
        y: int, 
        rows: int, 
        columns: int,
        children: list[list[TableCell]], # danh sách mảng 2 chiều chứa các ô
        color: tuple[int, int, int] = WHITE,
        padding: int = 0,
        surface: pygame.surface.Surface | None = None,
    )-> None:
        self.x, self.y = 0,0
        self.padding = padding

        if surface:
            self.screen = surface
            self.x = x
            self.y = y

        self.rows = rows
        self.columns = columns
        self.children = children

        # tính chiều rộng lớn nhất của từng cột, *zip: đảo chiều ma trận (lấy từng cột)
        max_col_widths = [max(child.rect.width for child in col)
                          for col in zip(*self.children)]
        
        # gán lại chiều rộng cho các cell
        idx = 0
        for col in zip(*self.children):
            for child in col:
                child.rect.width = max_col_widths[idx]
            
            idx += 1

        # tính self.width, self.height
        self.width = self.padding * 2
        self.height = self.padding * 2
        self.width += sum(max_col_widths)

        for row in self.children:
            self.height += max([child.rect.height for child in row])

        # Xác định vị trí từng cell trong bảng
        y = self.padding
        for row in range(self.rows):
            x = self.padding
            for col in range(self.columns):
                child = children[row][col]
                child.rect.x = x
                child.rect.y = y

                match child.alignment:
                    case Alignment.CENTER:
                        child.child.rect.center = child.rect.center
                    case Alignment.RIGHT:
                        child.child.rect.center = child.rect.center
                        child.child.rect.right =  child.rect.right
                    case _: # giá trị mặc định
                        child.child.rect.center = child.rect.center
                        child.child.rect.left = child.rect.left
                
                x += children[row][col].rect.width

            y += max(children[row][i].rect.height for i in range(self.columns))

        # Tạo surface riêng cho bảng
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(color)
        self.rect = pygame.Rect(x, y, self.width, self.height)

        # Gán surface cho từng widget
        for row in self.children:
            for child in row:
                child.child.set_surface(self.surface)

    def set_surface(self, surf: pygame.surface.Surface) -> None:
        self.screen = surf

    def draw(self):
        for row in self.children:
            for child in row:
                child.draw(self.surface)
        self.screen.blit(self.surface, self.rect)

# ================ Thiết kế Popup ================
"""Một cửa sổ nổi (Popup window)"""

class Popup(Widget):
    def __init__(
        self, 
        surface: pygame.surface.Surface,
        x: int,
        y: int,
        children: list[Widget],
        padding: int,
        color: tuple[int, int, int] = WHITE,
        width: int | None = None,
        height: int | None = None,
        orientation: Orientation = Orientation.HORIZONTAL,
        x_align: Alignment = Alignment.NONE,
        y_align: Alignment = Alignment.NONE,
    ) -> None:
        self.screen = surface
        self.children = children
        self.x = x
        self.y = y
        self.width = width if width else 0
        self.height = height if height else 0

        # Tính width, height nếu chưa truyền vào
        if orientation == Orientation.HORIZONTAL: # TH: Các widget xếp ngang
            content_width = sum(child.rect.width for child in children)
            content_height = max(child.rect.height for child in children)
        else: # TH: Các widget xếp dọc
            content_width = max(child.rect.width for child in children)
            content_height = sum(child.rect.height for child in children)

        if self.width == 0:
            self.width = content_width

        if self.height == 0:
            self.height = content_height
        
        if padding:
            self.width += padding * 2
            self.height += padding * 2

        # Tạo surface riêng và rect cho popup
        self.padding = padding
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(color)
        self.rect = pygame.Rect(x - padding, y - padding,
                                self.width, self.height)

        # Gán surface cho từng widget con
        for child in children:
            child.set_surface(self.surface)
        
        # Xử lí căn lề và layout
        if orientation == Orientation.HORIZONTAL:
            match x_align:
                case Alignment.CENTER:
                    children[0].rect.left = (
                        self.width - content_width) // 2
                case Alignment.RIGHT:
                    children[0].rect.left = (
                        self.width - self.padding - content_width)
                case _:
                    children[0].rect.left = self.padding

            match y_align:
                case Alignment.CENTER:
                    children[0].rect.centery = (self.height) // 2
                case Alignment.BOTTOM:
                    children[0].rect.top = (
                        self.height - self.padding - content_height
                    )
                case _:
                    children[0].rect.top = self.padding

            for i in range(1, len(children)):
                child = children[i]
                prev = children[i - 1]
                child.rect.x = prev.rect.right
                child.rect.y = self.padding

                if y_align == Alignment.CENTER:
                    child.rect.centery = prev.rect.centery
                elif y_align != Alignment.NONE:
                    child.rect.top = prev.rect.top
        else:
            match x_align:
                case Alignment.CENTER:
                    children[0].rect.centerx = self.width // 2
                case Alignment.RIGHT:
                    children[0].rect.left = (
                        self.width - self.padding - content_width)
                case _:
                    children[0].rect.left = self.padding

            match y_align:
                case Alignment.CENTER:
                    children[0].rect.top = (
                        self.height - content_height) // 2
                case Alignment.BOTTOM:
                    children[0].rect.top = (
                        self.height - self.padding - content_height
                    )
                case _:
                    children[0].rect.top = self.padding

            for i in range(1, len(children)):
                child = children[i]
                prev = children[i - 1]
                child.rect.y = prev.rect.bottom
                child.rect.x = self.padding

                if x_align == Alignment.CENTER:
                    child.rect.centerx = prev.rect.centerx
                elif x_align != Alignment.NONE:
                    child.rect.left = prev.rect.left

        self.close_btn = Button(
            surface=self.surface,
            text="   X   ",
            x=0,
            y=0,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            font_size=20, outline=False
        )
        self.close_btn.rect.right = self.rect.right
        self.close_btn.rect.top = self.rect.top

    def set_surface(self, surf: pygame.surface.Surface) -> None:
        self.screen = surf
        self.close_btn.set_surface(surf)

    def update_center(self, center: tuple[int, int]):
        self.rect.center = center
        self.close_btn.rect.right = self.rect.right
        self.close_btn.rect.top = self.rect.top

    def draw(self) -> bool:
        for child in self.children:
            child.draw()

        self.screen.blit(self.surface, self.rect)
        return self.close_btn.draw()




