import time

from ScrapyObject.spiders.zuotian.entity.DaHuaBean import get_flight_flag_info, get_flag_name, save_flight_flag
from ScrapyObject.spiders.zuotian.util.MouseUtil import MouseUtil
from ScrapyObject.spiders.zuotian.util.ZuoTianUtil import fly_destination, click_task, click_tool_bar, replenish_piece, \
    clean_your_backpack, lian_hua


def zuo_tian():
    """
    做天
    """
    t = time.time()
    for i in range(999):
        lis = get_flight_flag_info('./a979899.txt')
        spare_flag = get_flag_name(lis, '长安杂货店(14,11)')
        click_tool_bar(1)
        task_flag = get_flag_name(lis, '天宫(97,48)')
        fly_destination(task_flag.goods_position_y, task_flag.goods_position_x)
        replenish_piece(task_flag, spare_flag)
        time.sleep(2)
        MouseUtil().left_click(202, 210)
        click_task(4)
        time.sleep(1)

        # 杀三头魔王24,32
        click_tool_bar(1)
        task_flag = get_flag_name(lis, '御马监(27,35)')
        fly_destination(task_flag.goods_position_y, task_flag.goods_position_x)
        time.sleep(2)
        replenish_piece(task_flag, spare_flag)
        MouseUtil().left_click(170, 280)
        click_task(1)
        time.sleep(16)

        # 杀黑山妖王85,10
        click_tool_bar(1)
        task_flag = get_flag_name(lis, '御马监(87,13)')
        fly_destination(task_flag.goods_position_y, task_flag.goods_position_x)
        time.sleep(2)
        replenish_piece(task_flag, spare_flag)
        MouseUtil().left_click(205, 200)
        click_task(1)
        time.sleep(16)

        # 杀蓝色妖王108,39
        click_tool_bar(1)
        task_flag = get_flag_name(lis, '御马监(111,42)')
        fly_destination(task_flag.goods_position_y, task_flag.goods_position_x)
        time.sleep(2)
        replenish_piece(task_flag, spare_flag)
        MouseUtil().left_click(240, 210)
        click_task(1)
        time.sleep(16)

        # 杀万年熊王106,66
        click_tool_bar(1)
        task_flag = get_flag_name(lis, '御马监(110,69)')
        fly_destination(task_flag.goods_position_y, task_flag.goods_position_x)
        time.sleep(2)
        replenish_piece(task_flag, spare_flag)
        MouseUtil().left_click(180, 270)
        click_task(1)
        save_flight_flag(lis, './a979899.txt')
        print(i + 1)
        time.sleep(16)
    a = time.time()
    print(int(a) - int(t))


def zuo_tian_kuai(duration=1.0, cishu=1):
    """
    做天
    """
    t = time.time()
    for i in range(cishu):
        lis = get_flight_flag_info('./a979899.txt')
        spare_flag = get_flag_name(lis, '长安杂货店(14,11)')
        click_tool_bar(1, duration)
        task_flag = get_flag_name(lis, '天宫(97,48)')
        fly_destination(task_flag.goods_position_y, task_flag.goods_position_x, duration)
        replenish_piece(task_flag, spare_flag)
        time.sleep(duration)
        MouseUtil().left_click(202, 210, duration)
        click_task(4, duration)

        # 杀三头魔王24,32
        click_tool_bar(1, duration)
        task_flag = get_flag_name(lis, '御马监(27,35)')
        fly_destination(task_flag.goods_position_y, task_flag.goods_position_x, duration)
        replenish_piece(task_flag, spare_flag)
        time.sleep(duration)
        MouseUtil().left_click(170, 280, duration)
        click_task(1, duration)
        time.sleep(14)

        # 杀黑山妖王85,10
        click_tool_bar(1, duration)
        task_flag = get_flag_name(lis, '御马监(87,13)')
        fly_destination(task_flag.goods_position_y, task_flag.goods_position_x, duration)
        replenish_piece(task_flag, spare_flag)
        time.sleep(duration)
        MouseUtil().left_click(205, 200, duration)
        click_task(1, duration)
        time.sleep(14)

        # 杀蓝色妖王108,39
        click_tool_bar(1, duration)
        task_flag = get_flag_name(lis, '御马监(111,42)')
        fly_destination(task_flag.goods_position_y, task_flag.goods_position_x, duration)
        replenish_piece(task_flag, spare_flag)
        time.sleep(duration)
        MouseUtil().left_click(240, 210, duration)
        click_task(1, duration)
        time.sleep(14)

        # 杀万年熊王106,66
        click_tool_bar(1, duration)
        task_flag = get_flag_name(lis, '御马监(110,69)')
        fly_destination(task_flag.goods_position_y, task_flag.goods_position_x)
        replenish_piece(task_flag, spare_flag)
        time.sleep(duration)
        MouseUtil().left_click(180, 270, duration)
        click_task(1, duration)
        save_flight_flag(lis, './a979899.txt')
        print(i + 1)
        time.sleep(14)
    a = time.time()
    print(int(a) - int(t))


def recovery_goods():
    """
    回收物品
    """
    for i in range(5):
        MouseUtil().left_click(131 + (160 * i), 1060)
        click_tool_bar(4)
        MouseUtil().move_to(590, 210)
        MouseUtil().click_left()
        clean_your_backpack()


def mai_dongxi(beibao):
    click_tool_bar(4)
    MouseUtil().move_to(590, 210)
    MouseUtil().click_left()
    clean_your_backpack(beibao)


def dakabutong():
    for i in range(5):
        if i != 0:
            MouseUtil().left_click(122 + (160 * i), 1060, 0.5)
        mai_dongxi(3)
        MouseUtil().left_click(122 + (160 * i), 1060, 0.5)
    MouseUtil().left_click(122, 1060, 0.5)


if __name__ == '__main__':
    print("开始")
    # lian_hua(1)
    lian_hua()

    # for i in range(1):
    #     lian_hua()

    # zuo_tian_kuai(0.5, 99)
    # click_tool_bar(1)
    # fly_destination(2, 1)
    # dakabutong()
    # click_tool_bar(1)
    # select_inventory(1)
    # click_tool_bar(1)
