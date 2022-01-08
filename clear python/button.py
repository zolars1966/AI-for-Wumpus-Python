class Button:
    def __init__(self, point1, point2, func_type, func, *args):
        self.x1, self.y1 = self.point1 = point1
        self.x2, self.y2 = self.point2 = point2
        self.coords = [[self.x1, self.y1], [self.x2, self.y1], [self.x2, self.y2], [self.x1, self.y2]]
        self.rect = [[self.x1, self.y1], [self.x2 - self.x1, self.y2 - self.y1]]
        self.state = "unpressed"
        self.is_pressed = False
        self.work_function = func
        self.func_type = func_type
        if self.func_type == "static":
            self.args = args
        elif self.func_type != "dynamic":
            self.func_type = "static"
            print("Invalid func type, func type was set as static")

    def coll(self, mouse_pos, *args):
        if self.x1 <= mouse_pos[0] <= self.x2:
            if self.y1 <= mouse_pos[1] <= self.y2:
                self.state = "pressed" if self.state == "unpressed" else "unpressed"
                self.is_pressed = not self.is_pressed

                if self.func_type == "static":
                    self.work_function(*self.args)
                else:
                    self.work_function(*args)
                
                return True
        
        return False
