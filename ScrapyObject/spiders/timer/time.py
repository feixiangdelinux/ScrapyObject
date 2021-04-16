from apscheduler.schedulers.blocking import BlockingScheduler
import os

from playsound import playsound


def get_price():
    # playsound(r"C:\Users\linux\Music\八神笑声.mp3")
    playsound(r"D:\1.mp3")

def dojob():
    """
    定时任务,每900秒执行一次get_price()
    :return:
    """
    scheduler = BlockingScheduler()
    scheduler.add_job(get_price, 'interval', seconds=70, id='test_job1')
    # scheduler.add_job(get_price, 'interval', seconds=1200, id='test_job1')
    scheduler.start()


if __name__ == '__main__':
    dojob()
