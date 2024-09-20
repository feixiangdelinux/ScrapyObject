import json
import time

from be import VideoBean


# 读取JSON文件
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data


if __name__ == '__main__':
    print('开始')
    timestamp = int(time.time())
    jsonStr = read_json_file('D:\\aqdav1.json')
    print("原始数据一共: " + str(len(jsonStr)))
    jsonStrText = read_json_file('D:\\aqdavText.json')
    print("原始数据一共: " + str(len(jsonStrText)))
    videoList = []
    for i in jsonStr:
        for j in jsonStrText:
            if i['vUrl'] == j['vUrl']:
                video = VideoBean()
                video.id = 0
                video.name = i['name']
                video.url = i['url']
                video.tags = i['tags']
                video.pUrl = i['pUrl']
                video.vUrl = i['vUrl']
                videoList.append(video)
    print("视频数据一共: " + str(len(videoList)))
    jsonStr.clear()
    videoFinalList = []
    for i in videoList:
        tinydict = {'id': 0, 'name': i.name, 'url': '', 'tags': i.tags, 'pUrl': i.pUrl, 'vUrl': i.vUrl}
        videoFinalList.append(tinydict)
    videoList.clear()
    # 将JSON数组转换为字符串
    json_string = json.dumps(videoFinalList)
    # 将字符串写入txt文件
    with open('D:\\aqdavok.json', 'w') as file:
        file.write(json_string)
    endTime = int(time.time())
    print(str(endTime - timestamp))
    print('结束')
