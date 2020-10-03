# MediaPlayer
基于pyqt5写的一个歌词滚动器。
主要是用于需要在舞台上展示歌词啥的工作，不过代码方面还有不少漏洞。
歌曲名字与歌手名字需要在文件夹中写出。
然后内部需要表示封面图片cover.png，歌词lrc文件lyrics.txt，以及播放歌曲song.mp3
不过这种写法确实蠢，请根据自己的实际需求进行改动。

如果出现某些歌曲无法播放的情况，
可能是因为Qt中的多媒体播放，底层是使用DirectShowPlayerService，需要一个DirectShow解码器，例如LAV Filters。
https://files.1f0.de/lavf/LAVFilters-0.74.1.exe

不过当前这个动画效果相当不完善，切换语句之间非常生硬。
以后研究过了再改（
