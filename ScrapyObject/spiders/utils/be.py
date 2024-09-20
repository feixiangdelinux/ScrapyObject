import json
import time


# 读取JSON文件
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data


class VideoBean:
    id = 0
    name = ''
    url = ''
    e = ''
    i = ''
    tags = ''
    pUrl = ''
    vUrl = ''

    def __eq__(self, other):
        return self.pUrl == other.pUrl and self.vUrl == other.vUrl

    def __hash__(self):
        return hash(self.pUrl + self.vUrl)


class CkeBean:
    id = 0
    vUrl = ''


if __name__ == '__main__':
    print('开始')
    timestamp = int(time.time())
    jsonStr = read_json_file('D:\\aqdav.json')
    print("原始数据一共: " + str(len(jsonStr)))
    videoList = []
    for i in jsonStr:
        video = VideoBean()
        video.id = 0
        video.name = i['name']
        video.url = i['url']
        video.tags = i['tags']
        video.pUrl = i['pUrl']
        video.vUrl = i['vUrl']
        videoList.append(video)
    jsonStr.clear()
    print(len(videoList))
    test_list = list(set(videoList))
    print(len(test_list))
    print("原始数据去重后一共: " + str(len(test_list)))
    for i in test_list:
        if len(i.pUrl) == 0:
            test_list.remove(i)
        elif len(i.vUrl) == 0:
            test_list.remove(i)
    print(len(test_list))
    # str = json.dumps(test_list).encode('utf-8').decode('unicode_escape')
    # with open('D:\\aqdav_new.json', 'w', encoding='utf-8') as f:
    #     f.write(str)

    # json_str = json.JSONEncoder().encode(test_list)
    # with open('D:\\aqdav_new.json', 'w') as file:
    #     file.write(json_str)
    videoFinalList = []
    for i in test_list:
        tinydict = {'id': 0, 'name': i.name, 'url': '', 'tags': i.tags, 'pUrl': i.pUrl, 'vUrl': i.vUrl}
        videoFinalList.append(tinydict)
    test_list.clear()

    # 将JSON数组转换为字符串
    json_string = json.dumps(videoFinalList)
    # 将字符串写入txt文件
    with open('D:\\aqdav1.json', 'w') as file:
        file.write(json_string)

    endTime = int(time.time())
    print(str(endTime - timestamp))
    print('结束')
