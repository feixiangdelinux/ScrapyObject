import time

from pynput.mouse import Button, Controller


class MouseUtil:
    mouse = Controller()

    def move_to(self, dx, dy, duration=1):
        """鼠标移动到某一位置
        :param int dx: 水平位置.
        :param int dy: 垂直位置.
        """
        time.sleep(duration)
        self.mouse.position = (dx, dy)

    def click_left(self, duration=1):
        """点击鼠标左键(一次)
        """
        time.sleep(duration)
        self.mouse.press(Button.left)
        self.mouse.release(Button.left)

    def click_left_two(self, duration=1):
        """点击鼠标左键(两次)
        """
        time.sleep(duration)
        self.mouse.press(Button.left)
        self.mouse.release(Button.left)
        self.mouse.press(Button.left)
        self.mouse.release(Button.left)

    def click_right(self, duration=1):
        """点击鼠标右键(一次)
        """
        time.sleep(duration)
        self.mouse.press(Button.right)
        self.mouse.release(Button.right)

    def left_click(self, dx, dy, duration=1):
        """左键点击指定位置
        :param int dx: 水平位置.
        :param int dy: 垂直位置.
        """
        self.move_to(dx, dy, duration)
        self.click_left(duration)

    def right_click(self, dx, dy, duration=1):
        """右键点击指定位置
        :param int dx: 水平位置.
        :param int dy: 垂直位置.
        """
        self.move_to(dx, dy, duration)
        self.click_right(duration)
