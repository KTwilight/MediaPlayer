from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia
import sys
import time
import Lyrics


class MusicLyrics(QtWidgets.QMainWindow):
    rows = 100
    cols = 160
    is_pause = True
    rows_border_lyrics = 5
    rows_principle_lyrics = 10
    rows_upper_widget = 95
    rows_bottom_widget = rows - rows_upper_widget
    rows_left_image = 65
    rows_left_title = rows - rows_left_image
    cols_left_widget = 64
    cols_right_widget = cols - cols_left_widget
    num_upper_border_lyrics = 8
    num_lower_border_lyrics = 8
    num_border_lyrics = num_upper_border_lyrics + num_lower_border_lyrics
    num_lyrics = num_upper_border_lyrics + num_lower_border_lyrics + 1
    cur_path = "./"
    songs_lyrics = Lyrics.Lyrics()

    def __init__(self):
        super().__init__()
        # 一些底层
        # 计时器

        self.song_timer = QtCore.QTimer()
        self.song_timer.start(100)
        self.song_timer.timeout.connect(self.play)

        # 音乐播放器
        self.player = QtMultimedia.QMediaPlayer()

        # 主界面
        self.main_widget = QtWidgets.QWidget()
        self.main_widget.setObjectName("main_widget")
        self.main_layout = QtWidgets.QGridLayout()

        # 左侧
        self.left_widget = QtWidgets.QWidget()
        self.left_layout = QtWidgets.QGridLayout()
        self.left_widget.setObjectName("left_widget")
        self.left_image = QtWidgets.QLabel()
        self.left_image.setObjectName("left_image")
        self.left_image.setAlignment(QtCore.Qt.AlignCenter)
        self.left_title = QtWidgets.QLabel()
        self.left_title.setObjectName("left_title")
        self.left_title.setAlignment(QtCore.Qt.AlignCenter)

        # 右侧
        self.right_widget = QtWidgets.QWidget()
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setObjectName("right_widget")
        self.principal_lyrics = QtWidgets.QLabel()
        self.principal_lyrics.setObjectName("principal_lyrics")
        self.border_lyrics = list()

        # 生成歌词
        for i in range(self.num_border_lyrics):
            self.border_lyrics.append(QtWidgets.QLabel())

        for i in self.border_lyrics:
            i.setObjectName("border_lyrics")

        self.lyrics = list()

        for i in range(self.num_upper_border_lyrics):
            self.lyrics.append(self.border_lyrics[i])
        self.lyrics.append(self.principal_lyrics)
        for i in range(self.num_lower_border_lyrics):
            self.lyrics.append(self.border_lyrics[i+self.num_upper_border_lyrics])

        # 底部
        self.bottom_widget = QtWidgets.QWidget()
        self.bottom_widget.setObjectName("bottom_widget")
        self.bottom_layout = QtWidgets.QGridLayout()

        # 上一首歌
        self.bottom_pre_song = QtWidgets.QPushButton()
        self.bottom_pre_song.setObjectName("bottom_pre_song")
        # 播放与暂停
        self.bottom_play = QtWidgets.QPushButton()
        self.bottom_play.setObjectName("bottom_play")
        # 下一首歌
        self.bottom_next_song = QtWidgets.QPushButton()
        self.bottom_next_song.setObjectName("bottom_next_song")

        # 开始时间
        self.bottom_time_now = QtWidgets.QLabel()
        self.bottom_time_now.setObjectName("bottom_time_now")
        # 结束时间
        self.bottom_time_end = QtWidgets.QLabel()
        self.bottom_time_end.setObjectName("bottom_time_end")

        # 歌曲进度条
        self.bottom_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.bottom_slider.setObjectName("bottom_slider")
        self.bottom_slider.sliderMoved[int].connect(lambda: self.player.setPosition(self.bottom_slider.value()))

        self.bottom_volume = QtWidgets.QLabel()
        self.bottom_volume.setObjectName("bottom_volume")

        # 音量进度条
        self.bottom_volume_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.bottom_volume_slider.setObjectName("bottom_volume_slider")
        self.bottom_volume_slider.sliderMoved[int].connect(lambda: self.player.setVolume(self.bottom_volume_slider.value()))
        self.bottom_volume_slider.setValue(self.bottom_volume_slider.maximum())
        self.initialize()

    def initialize(self):
        # 主要布局
        self.setFixedSize(1600, 1000)
        self.setCentralWidget(self.main_widget)
        self.main_widget.setLayout(self.main_layout)
        self.main_layout.addWidget(self.left_widget, 0, 0, self.rows_upper_widget, self.cols_left_widget)
        self.main_layout.addWidget(self.right_widget, 0, self.cols_left_widget, self.rows_upper_widget, self.cols_right_widget)
        self.main_layout.addWidget(self.bottom_widget, self.rows_upper_widget, 0, self.rows_bottom_widget, self.cols)

        # 左侧布局
        self.left_widget.setLayout(self.left_layout)
        self.left_layout.addWidget(self.left_image, 20, 0, self.rows_left_image, self.cols_left_widget)
        self.left_layout.addWidget(self.left_title, self.rows_left_image+20, 0, self.rows_left_title, self.cols_left_widget)

        # 右侧布局
        self.right_widget.setLayout(self.right_layout)
        for i in range(self.num_upper_border_lyrics):
            self.right_layout.addWidget(self.border_lyrics[i], 5*i, self.cols_left_widget, 5, self.cols_right_widget)
        self.right_layout.addWidget(self.principal_lyrics, 5*self.num_upper_border_lyrics, self.cols_left_widget, 15, self.cols_right_widget)
        for i in range(self.num_lower_border_lyrics):
            self.right_layout.addWidget(self.border_lyrics[i+self.num_upper_border_lyrics], 5*(i+self.num_upper_border_lyrics+3), self.cols_left_widget, 5, self.cols_right_widget)
        # 下方布局
        self.bottom_widget.setLayout(self.bottom_layout)
        self.bottom_layout.addWidget(self.bottom_pre_song, self.rows_upper_widget, 10, self.rows_bottom_widget, 5)
        self.bottom_layout.addWidget(self.bottom_play, self.rows_upper_widget, 20, self.rows_bottom_widget, 5)
        self.bottom_layout.addWidget(self.bottom_next_song, self.rows_upper_widget, 30, self.rows_bottom_widget, 5)
        self.bottom_layout.addWidget(self.bottom_time_now, self.rows_upper_widget, 40, self.rows_bottom_widget, 4)
        self.bottom_layout.addWidget(self.bottom_slider, self.rows_upper_widget, 44, self.rows_bottom_widget, 90)
        self.bottom_layout.addWidget(self.bottom_time_end, self.rows_upper_widget, 134, self.rows_bottom_widget, 4)
        self.bottom_layout.addWidget(self.bottom_volume, self.rows_upper_widget, 138, self.rows_bottom_widget, 5)
        self.bottom_layout.addWidget(self.bottom_volume_slider, self.rows_upper_widget, 145, self.rows_bottom_widget, 15)

        self.left_title.setText(" ")
        for i in range(self.num_lyrics):
            self.lyrics[i].setText(" ")
            self.lyrics[i].setAlignment(QtCore.Qt.AlignCenter)

        self.bottom_time_now.setText("00:00")
        self.bottom_time_end.setText("00:00")

        self.bottom_play.clicked.connect(self.play_music)
        self.bottom_pre_song.clicked.connect(self.open_folder)
        self.bottom_next_song.clicked.connect(self.quit)

        self.main_widget.setStyleSheet('''
            QWidget#main_widget{
                border-image:url(./image/background.jpg);
            }
        ''')

        self.left_widget.setStyleSheet('''
            QLabel#left_image{
            }
            QLabel#left_title{
                color:black;
                font-size:50px;
                font-weight:700;
                font-family: "思源宋体", Helvetica, Arial, sans-serif;
            }
        ''')
        self.right_widget.setStyleSheet('''
            QWidget#right_widget{
                background-color: rgba(0, 0, 0, 0.5);
            } 
            QLabel#border_lyrics{
                color:white;
                font-size:30px;
                font-weight:700;
                font-family: "思源宋体", Helvetica, Arial, sans-serif;
            }
            QLabel#principal_lyrics{
                color:white;
                font-size:55px;
                font-weight:700;
                font-family: "思源宋体", Helvetica, Arial, sans-serif;
            }
        ''')
        self.bottom_widget.setStyleSheet('''
            QWidget#bottom_widget{
                background:#232326;
            }
            QLabel#bottom_time_now{
                color:white;
                font-size:20px;
                font-weight:700;
            }
            QLabel#bottom_time_end{
                color:white;
                font-size:20px;
                font-weight:700;
                
            }
            QPushButton#bottom_pre_song{
                border-image:url(./image/文件夹.png);
                width:40px;
                height:47px;
                
            }
            QPushButton#bottom_play{
                border-image:url(./image/播放键.png);
                width:50px;
                height:50px;
            }
            QPushButton#bottom_next_song{
                border-image:url(./image/退出.png);
                width:47px;
                height:47px;
            }
            QLabel#bottom_volume{
                border-image:url(./image/音量.png);
                width:45px;
                height:47px;
            
            }
            
        ''')

    def play(self):
        if not self.is_pause:
            self.bottom_slider.setMinimum(0)
            self.bottom_slider.setMaximum(self.player.duration())
            self.bottom_slider.setValue(self.player.position())
            self.bottom_time_now.setText(time.strftime('%M:%S', time.localtime(self.player.position() / 1000)))
            self.bottom_time_end.setText(time.strftime('%M:%S', time.localtime(self.player.duration() / 1000)))
            self.set_lyrics()

    def get_time_index(self):
        lower = 0
        upper = len(self.songs_lyrics.timeline)
        mid = int((lower + upper)/2)
        while lower != upper:
            mid = int((lower + upper)/2)
            if self.player.position() < self.songs_lyrics.timeline[mid]:
                upper = mid
            elif self.player.position() > self.songs_lyrics.timeline[mid]:
                lower = mid
            if upper == (lower + 1):
                break
        return lower

    def set_lyrics(self):
        index = self.get_time_index()
        for i in range(-8, 9, 1):
            if index + i < 0 or (index + i) >= len(self.songs_lyrics.text):
                self.lyrics[i+8].setText(" ")
            else:
                self.lyrics[i+8].setText(self.songs_lyrics.text[index + i])

    def play_music(self):
        if self.is_pause:
            self.player.play()
        else:
            self.player.pause()

        self.is_pause = not self.is_pause

    def open_folder(self):
        self.cur_path = QtWidgets.QFileDialog.getExistingDirectory(self, "选取文件夹", "./")
        if self.cur_path:
            self.left_image.setPixmap(QtGui.QPixmap(self.cur_path+"/cover.png"))
            folder_name = self.cur_path.split("/")[-1]
            print(folder_name)
            song_text = folder_name.split(" ")
            self.left_title.setText(song_text[0] + "\n" + song_text[1])
            self.songs_lyrics.set_text(self.cur_path+"/lyrics.txt")
            self.player.setMedia(QtMultimedia.QMediaContent(QtCore.QUrl(self.cur_path+"/song.mp3")))
            self.is_pause = True
            self.bottom_time_now.setText("00:00")
            self.bottom_time_end.setText(time.strftime('%M:%S', time.localtime(self.player.duration() / 1000)))
            self.bottom_slider.setValue(0)
            self.set_lyrics()

    def quit(self):
        QtWidgets.QApplication.quit()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    gui = MusicLyrics()
    gui.show()
    gui.showFullScreen()
    sys.exit(app.exec_())