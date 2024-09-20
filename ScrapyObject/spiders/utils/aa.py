import time

if __name__ == '__main__':
    print('开始')
    timestamp = int(time.time())
    # 图片宽度
    image_width = 1052
    # 图片高度
    image_height = 4
    # 控件宽度
    widget_width = 310
    print(image_height * widget_width / image_width)
    endTime = int(time.time())
    print(str(endTime - timestamp))
    print('结束')
