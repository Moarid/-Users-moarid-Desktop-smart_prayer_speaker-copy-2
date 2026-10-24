import time

class GUIManager:
    def __init__(self, lcd, touch=None):
        self.lcd = lcd
        self.touch = touch
        self.pages = {}
        self.current_page = None
        self.page_stack = []
        self.last_touch_time = 0
        self.touch_delay_ms = 300

    def register_page(self, name, page):
        self.pages[name] = page

    def show(self, name):
        if name not in self.pages:
            print("Page not found:", name)
            return

        if self.current_page:
            self.page_stack.append(self.current_page)

        self.current_page = name
        self.pages[name].draw(self.lcd)

    def go_home(self):
        self.page_stack = []
        self.current_page = "home"
        self.pages["home"].draw(self.lcd)

    def back(self):
        if len(self.page_stack) > 0:
            self.current_page = self.page_stack.pop()
        else:
            self.current_page = "home"

        self.pages[self.current_page].draw(self.lcd)

    def handle_touch(self, x, y):
        if self.current_page is None:
            return

        page = self.pages[self.current_page]

        target = page.handle_touch(x, y)

        if target is None:
            return

        if target == "back":
            self.go_home()
        else:
            self.show(target)

    def tick(self):
        if self.touch is None:
            return

        now = time.ticks_ms()

        if time.ticks_diff(now, self.last_touch_time) < self.touch_delay_ms:
            return

        point = self.touch.get_point()

        if point is None:
            return

        x, y = point

        self.last_touch_time = now
        self.handle_touch(x, y)