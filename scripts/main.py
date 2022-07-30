import cv2
import numpy as np
import pyautogui as pygui
from mss import mss
from sys import exit
from time import sleep
from rods import rods_dict


class FishBot:
    def __init__(self, rod: str) -> None:
        self.IMG_SIZE = 80
        self.sct = mss()
        self.rod = rods_dict[rod.lower().capitalize()]
        self.prev = 0
        self.hsv = None
        self.mask = None

    def click(self) -> None:
        pygui.mouseDown()
        sleep(0.01)
        pygui.mouseUp()

    # Makes screenshots
    def get_screen(self) -> None:
        # Get cursor position
        x, y = pygui.position()

        # Set indents and area
        mon = {
            "top": y - self.IMG_SIZE // 2,
            "left": x - self.IMG_SIZE // 2,
            "width": self.IMG_SIZE,
            "height": self.IMG_SIZE
        }
        # Make screenshot
        img = self.sct.grab(mon)

        # Convert img to hsv color model
        self.hsv = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2HSV)

    # Creates mask for hsv image
    def create_mask(self) -> None:
        match len(self.rod):
            case 2:
                # If float have only 1 color
                lower_bound = np.array(self.rod[1])
                upper_bound = np.array(self.rod[0])

                self.mask = cv2.inRange(self.hsv, lower_bound, upper_bound)

            case 4:
                # If float have 2 colors
                lower_bound = np.array(self.rod[1])
                upper_bound = np.array(self.rod[0])
                mask1 = cv2.inRange(
                    self.hsv, lower_bound, upper_bound)

                lower_bound = np.array(self.rod[3])
                upper_bound = np.array(self.rod[2])
                mask2 = cv2.inRange(
                    self.hsv, lower_bound, upper_bound)

                self.mask = mask1 + mask2

    def fish(self) -> None:
        try:
            print("Начало через 10 сек")
            sleep(10)
            self.click()
            sleep(0.75)

            while True:
                self.get_screen()
                self.create_mask()
                has_color = np.sum(self.mask)

                # If the float dips under the water too much
                if has_color <= (self.prev * 0.55):
                    print("Забрал")
                    self.click()
                    sleep(1)
                    print("Закинул")
                    self.click()
                    sleep(0.75)

                self.prev = has_color

        except KeyboardInterrupt:
            cv2.destroyAllWindows()
            exit()


# Print full list of rods
def list_of_rods() -> str:
    print("Список всех удочек: ")
    for i, rod in enumerate(rods_dict.keys()):
        print(f"{i+1}. {rod}")

    dot = input("\nКакая у тебя >>> ")
    return dot


if __name__ == "__main__":
    rod = list_of_rods()
    bot = FishBot(rod)
    bot.fish()
