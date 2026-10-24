import time

class UI:
    def __init__(self, pages):
        self.pages = pages
        self.current_page = "home"
        self.last_touch = 0
        self.buttons_area = []

    def show(self, page_name):
        self.current_page = page_name
        self.draw_page()

    def draw_page(self):
        page = self.pages[self.current_page]
        self.buttons_area = []

        print("\n==============================")
        print("PAGE:", page["title"])
        print("==============================")

        buttons = page["buttons"]

        for i, button in enumerate(buttons):
            label, target = button
            print(str(i + 1) + ".", label)

        if page["back"]:
            print("0. Back")

        print("==============================")

    def tick(self):
        try:
            value = input("Select: ")

            if value == "":
                return

            index = int(value)
            self.press_button(index)

        except Exception as e:
            print("Input error:", e)

    def press_button(self, index):
        page = self.pages[self.current_page]

        if index == 0 and page["back"]:
            self.show(page["back"])
            return

        buttons = page["buttons"]

        if index < 1 or index > len(buttons):
            return

        label, target = buttons[index - 1]

        print("Pressed:", label)

        if target:
            self.show(target)
        else:
            print("Action page only:", label)