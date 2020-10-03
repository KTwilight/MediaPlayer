import re


class Lyrics:
    name = ""
    timeline = list()
    text = list()

    def __init__(self):
        None

    def cal_time(self, lrc_time):
        time = re.match(r'(\d{2})\:(\d{2})\.(\d{2})', lrc_time)
        minute = int(time[1])
        second = int(time[2])
        millisecond = int(time[3])
        ans = minute*60000 + second * 1000 + millisecond * 10
        return ans

    def set_text(self,lyric_name):
        self.timeline.clear()
        self.text.clear()
        with open(lyric_name, 'r', encoding='utf-8') as lyric_read:
            for i in lyric_read.readlines():
                temp = re.match(r"\[([^\[\]]*)\](.*)", i)
                self.timeline.append(self.cal_time(temp[1]))
                self.text.append(temp[2].replace('\u3000', ' '))
        print(self.timeline)