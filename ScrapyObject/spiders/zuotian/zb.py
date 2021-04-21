import time

from ScrapyObject.spiders.zuotian.entity.DaHuaBean import get_flight_flag_info, get_flag_name, save_flight_flag
from ScrapyObject.spiders.zuotian.util.MouseUtil import MouseUtil
from ScrapyObject.spiders.zuotian.util.ZuoTianUtil import fly_destination, click_task, click_tool_bar, replenish_piece, clean_your_backpack


def zuo_tian():
    """
    做天
    """
    print("开始")
    t = time.time()
    for i in range(1):
        lis = get_flight_flag_info('./a979899.txt')
        click_tool_bar(1)
        spare_flag = get_flag_name(lis, '长安杂货店(14,11)')
        task_flag = get_flag_name(lis, '天宫(95,44)')
        fly_destination(task_flag.goods_position_y, task_flag.goods_position_x)
        replenish_piece(task_flag, spare_flag)
        time.sleep(2)
        MouseUtil().left_click(290, 260)
        click_task(4)
        time.sleep(1)

        # 杀三头魔王24,32
        click_tool_bar(1)
        task_flag = get_flag_name(lis, '御马监(24,34)')
        fly_destination(task_flag.goods_position_y, task_flag.goods_position_x)
        time.sleep(2)
        replenish_piece(task_flag, spare_flag)
        MouseUtil().left_click(290, 270)
        click_task(1)
        time.sleep(15)

        # 杀黑山妖王85,10
        click_tool_bar(1)
        task_flag = get_flag_name(lis, '御马监(85,10)')
        fly_destination(task_flag.goods_position_y, task_flag.goods_position_x)
        time.sleep(2)
        replenish_piece(task_flag, spare_flag)
        MouseUtil().left_click(300, 220)
        click_task(1)
        time.sleep(15)

        # 杀蓝色妖王108,39
        click_tool_bar(1)
        task_flag = get_flag_name(lis, '御马监(108,39)')
        fly_destination(task_flag.goods_position_y, task_flag.goods_position_x)
        time.sleep(2)
        replenish_piece(task_flag, spare_flag)
        MouseUtil().left_click(295, 240)
        click_task(1)
        time.sleep(15)

        # 杀万年熊王106,66
        click_tool_bar(1)
        task_flag = get_flag_name(lis, '御马监(106,66)')
        fly_destination(task_flag.goods_position_y, task_flag.goods_position_x)
        time.sleep(2)
        replenish_piece(task_flag, spare_flag)
        MouseUtil().left_click(300, 240)
        click_task(1)
        time.sleep(15)
        save_flight_flag(lis, './a979899.txt')
    a = time.time()
    print(int(a) - int(t))


def recovery_goods():
    """
    回收物品
    """
    for i in range(5):
        MouseUtil().left_click(131+(160*i), 1060)
        click_tool_bar(4)
        MouseUtil().move_to(590, 210)
        MouseUtil().click_left()
        clean_your_backpack()



if __name__ == '__main__':
    print("开始")