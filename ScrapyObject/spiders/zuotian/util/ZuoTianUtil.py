import time

from pynput.keyboard import Controller as Conter
from pynput.mouse import Button, Controller

from ScrapyObject.spiders.zuotian.util.MouseUtil import MouseUtil


def click_task(x, duration=1):
    """
    领取任务
    :param x: 领取第几个任务
    :return:
    """
    MouseUtil().left_click(290, 270 + (x * 18), duration)


def click_tool_bar(x, duration=1):
    """
    打开物品栏
    :param x: 点第几个栏
    :return:
    """
    MouseUtil().left_click(493 + (x * 30), 615, duration)


def select_inventory(x, duration=1):
    """
    选择背包
    :param x: 第几个背包
    :return:
    """
    MouseUtil().left_click(1011, 314 + (x * 51), duration)


def right_goods(y, x, duration=1):
    """
    右键使用物品栏中指定位置的物品,比如飞行棋
    :param y: 水平位置(取值范围1-6)
    :param x: 垂直位置(取值范围1-4)
    :return:
    """
    horizontal_one = 720
    vertical_one = 366
    distance = 51
    horizontal_one = horizontal_one + ((x - 1) * distance)
    vertical_one = vertical_one + ((y - 1) * distance)
    MouseUtil().right_click(horizontal_one, vertical_one, duration)


def left_goods(y, x):
    """
    左键点击物品栏中指定位置的物品
    :param y: 水平位置(取值范围1-6)
    :param x: 垂直位置(取值范围1-4)
    :return:
    """
    horizontal_one = 720
    vertical_one = 366
    distance = 51
    horizontal_one = horizontal_one + ((x - 1) * distance)
    vertical_one = vertical_one + ((y - 1) * distance)
    MouseUtil().left_click(horizontal_one, vertical_one)


def buy_grocery(y, x, num):
    """
    从随身商店购买飞行棋
    :param y: 第几行
    :param x: 第几个
    :return:
    """
    MouseUtil().left_click(386 + 250 + (89 * 3), 560)
    MouseUtil().left_click(349 + (51 * 1), 125 + (51 * 1))
    MouseUtil().left_click(349 + (51 * x), 125 + (51 * y))
    # 购买
    for i in range(num):
        MouseUtil().left_click(534, 504)
    MouseUtil().left_click(687, 119)


def move_goods_two(start_y, start_x, end_y, end_x):
    """
    把物品栏里指定位置的物品start_x,start_y移动到另一个位置end_x,end_y
    :param start_y: 起始物品在第几行
    :param start_x: 起始物品是第几个
    :param end_y: 最终移动位置在第几行
    :param end_x: 最终移动位置是第几个
    :return:
    """
    # 选取备用棋
    left_goods(start_y, start_x)
    # 移动到空出的位置
    left_goods(end_y, end_x)


def fly_destination(y, x, duration=1):
    """
    使用物品栏指定位置的飞行棋飞到目的地
    :param y: 飞行棋所在第几行
    :param x: 飞行棋是第几个
    :return:
    """
    right_goods(y, x, duration)
    click_task(1, duration)


def dian_dang_your_backpack():
    mouse = Controller()
    time.sleep(1)
    mouse.position = (530, 150)
    mouse.press(Button.left)
    mouse.position = (860, 150)
    mouse.release(Button.left)
    for y in range(4):
        for x in range(6):
            MouseUtil().left_click(722 + (51 * x), 202 + (51 * y), duration=0.2)
            MouseUtil().click_right(duration=0.1)
            MouseUtil().left_click(850, 479, duration=0.1)


def clean_your_backpack(beibao=1):
    mouse = Controller()
    keyboard = Conter()
    time.sleep(0.4)
    mouse.position = (530 - 180, 150)
    mouse.press(Button.left)
    mouse.position = (860 - 180, 150)
    mouse.release(Button.left)
    for i in range(beibao):
        # if i == 0:
        #     continue
        MouseUtil().left_click(1011, 203 + (51 * i), duration=0.4)
        for y in range(4):
            for x in range(6):
                MouseUtil().left_click(722 + (51 * x), 202 + (51 * y), duration=0.5)
                mouse.position = (830, 412)
                mouse.press(Button.left)
                mouse.position = (818, 412)
                time.sleep(0.4)
                keyboard.press('1')
                keyboard.release('1')
                mouse.release(Button.left)
                MouseUtil().left_click(921, 479, duration=0.1)


def replenish_piece(task_flag, spare_flag):
    """
    从随身商店购买飞行棋
    :param task_flag:
    :param spare_flag:
    :return:
    """
    task_flag.times_left = task_flag.times_left - 1
    if task_flag.times_left == 0:
        click_tool_bar(1)
        move_goods_two(spare_flag.goods_position_y, spare_flag.goods_position_x, task_flag.goods_position_y,
                       task_flag.goods_position_x)
        MouseUtil().click_right()
        task_flag.times_left = 99
        click_task(2)
        MouseUtil().left_click(386 + 249 + (89 * 3), 560)
        MouseUtil().left_click(229 + 125 + (51 * 1), 131 + (51 * 1))
        MouseUtil().left_click(229 + 125 + (51 * 2), 131 + (51 * 1))
        MouseUtil().left_click(405 + 125, 507)
        MouseUtil().left_click(562 + 125, 115)
