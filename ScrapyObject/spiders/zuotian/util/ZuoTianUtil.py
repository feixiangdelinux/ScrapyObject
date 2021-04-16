from ScrapyObject.spiders.zuotian.util.MouseUtil import MouseUtil


def click_task(x):
    """
    领取任务
    :param x: 领取第几个任务
    :return:
    """
    MouseUtil().left_click(165, 270 + (x * 18))


def click_tool_bar(x):
    """
    打开物品栏
    :param x: 点第几个栏
    :return:
    """
    MouseUtil().left_click(493 + (x * 30), 615)


def select_inventory(x):
    """
    选择背包
    :param x: 第几个背包
    :return:
    """
    MouseUtil().left_click(762, 314 + (x * 51))


def right_goods(y, x):
    """
    右键使用指定位置的物品,比如飞行棋
    :param y: 水平位置(取值范围1-6)
    :param x: 垂直位置(取值范围1-4)
    :return:
    """
    horizontal_one = 471
    vertical_one = 366
    distance = 51
    horizontal_one = horizontal_one + ((x - 1) * distance)
    vertical_one = vertical_one + ((y - 1) * distance)
    MouseUtil().right_click(horizontal_one, vertical_one)


def left_goods(y, x):
    """
    左键选择指定位置的物品
    :param y: 水平位置(取值范围1-6)
    :param x: 垂直位置(取值范围1-4)
    :return:
    """
    horizontal_one = 471
    vertical_one = 366
    distance = 51
    horizontal_one = horizontal_one + ((x - 1) * distance)
    vertical_one = vertical_one + ((y - 1) * distance)
    MouseUtil().left_click(horizontal_one, vertical_one)


def buy_grocery(y, x, num):
    """
    杂货店购买物品
    :param y: 第几行
    :param x: 第几个
    :return:
    """
    # 点击npc
    MouseUtil().left_click(585, 400)
    # 点击第一个购买物品
    click_task(1)
    # 鼠标移动到对应的飞行棋上面
    MouseUtil().left_click(229 + (51 * x), 131 + (51 * y))
    # 购买
    for i in range(num):
        MouseUtil().left_click(405, 507)
    # 关闭
    MouseUtil().left_click(568, 120)


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


def fly_destination(y, x):
    """
    使用物品栏指定位置的飞行棋飞到目的地
    :param y: 飞行棋所在第几行
    :param x: 飞行棋是第几个
    :return:
    """
    right_goods(y, x)
    click_task(1)


def replenish_piece(task_flag, spare_flag, buy_flag):
    """

    :param task_flag:
    :param spare_flag:
    :param buy_flag:
    :return:
    """
    task_flag.times_left = task_flag.times_left - 1
    if task_flag.times_left == 0:
        move_goods_two(spare_flag.goods_position_y, spare_flag.goods_position_x, task_flag.goods_position_y,
                       task_flag.goods_position_x)
        MouseUtil().click_right()
        task_flag.times_left = 30
        fly_destination(buy_flag.goods_position_y, buy_flag.goods_position_x)
        buy_flag.times_left = buy_flag.times_left - 1
        # 关闭物品栏
        click_tool_bar(1)
        # 购买第一个物品
        if buy_flag.times_left == 0:
            buy_grocery(1, 1, 2)
        else:
            buy_grocery(1, 1, 1)
        # 打开物品栏
        click_tool_bar(1)
        if buy_flag.times_left == 0:
            right_goods(buy_flag.goods_position_y, buy_flag.goods_position_x)
            buy_flag.times_left = 30
