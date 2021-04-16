import json


class FlightFlagBean:
    def __init__(self, goods_position, goods_position_y, goods_position_x, flight_chess_info, times_left):
        """
        飞行旗信息模型
        :param goods_position: 飞行旗在哪个包中(一共4个包)
        :param goods_position_y: 飞行旗在物品栏的第几行(1-4)
        :param goods_position_x: 飞行旗在物品栏的第几列(1-6)
        :param flight_chess_info: 飞行旗在哪个地图,具体坐标是什么
        :param times_left: 飞行旗信息飞行棋所剩次数
        """
        self.goods_position = goods_position
        self.goods_position_y = goods_position_y
        self.goods_position_x = goods_position_x
        self.flight_chess_info = flight_chess_info
        self.times_left = times_left


def generate_flight_flag(path):
    """
    生成飞行旗数据文件
    :return:
    """
    list = []
    list.append(FlightFlagBean(1, 1, 1, '天宫(37,33)', 30).__dict__)
    list.append(FlightFlagBean(1, 1, 2, '御马监(10,35)', 30).__dict__)
    list.append(FlightFlagBean(1, 1, 3, '御马监(100,10)', 30).__dict__)
    list.append(FlightFlagBean(1, 1, 4, '御马监(105,45)', 30).__dict__)
    list.append(FlightFlagBean(1, 1, 5, '御马监(110,100)', 30).__dict__)
    list.append(FlightFlagBean(1, 1, 6, '长安杂货店(12,11)', 30).__dict__)

    list.append(FlightFlagBean(1, 2, 1, '备用棋', 30).__dict__)

    str = json.dumps(list).encode('utf-8').decode('unicode_escape')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(str)


def read_json(pash):
    """
    读取配置文件
    :param pash: json文件路径
    :return:
    """
    f = open(pash, 'r', encoding="utf-8")
    return f.read()


def get_flight_flag_info(path):
    """
    读取配置文件来获取飞行旗数据
    :return:
    """
    myClassReBuild = json.loads(read_json(path))
    lis = []
    for letter in myClassReBuild:
        lis.append(FlightFlagBean(letter['goods_position'], letter['goods_position_y'], letter['goods_position_x'],
                                  letter['flight_chess_info'], letter['times_left']))
    return lis


def save_flight_flag(lis, path):
    list = []
    for i in lis:
        list.append(i.__dict__)
    str = json.dumps(list).encode('utf-8').decode('unicode_escape')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(str)


def get_flag_name(lis, name):
    """
    根据name获取对应飞行旗
    :param lis: 飞行旗总数据
    :param name: 名称
    :return:
    """
    for flag in lis:
        if flag.flight_chess_info == name:
            return flag


def get_flag_yx(lis, y, x):
    """
    根据位置(y,x)获取对应飞行旗
    :param lis: 飞行旗总数据
    :param y: 飞行旗在物品栏的第几行(1-4)
    :param x: 飞行旗在物品栏的第几列(1-6)
    :return:
    """
    for flag in lis:
        if flag.goods_position_y == y and flag.goods_position_x == x:
            return flag


if __name__ == '__main__':
    # generate_flight_flag('../a979899.txt')
    # generate_flight_flag('../b979899.txt')
    # generate_flight_flag('../c979899.txt')
    # generate_flight_flag('../d979899.txt')
    generate_flight_flag('../zuotian/e979899.txt')
    # generate_flight_flag('../f979899.txt')
