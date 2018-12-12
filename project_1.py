from dattetime import datetime
import time
from functools import partial

#from dateutil.tz import tzutc, tzlocal
import pytz

import sys
import winsound
from PyQt5.QtCore import Qt, QTimer, QDate
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtWidgets import (QWidget, QApplication, 
                             QLCDNumber, QSlider, 
                             QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QToolTip, 
                             QMessageBox, QCalendarWidget)

#time_now = datetime.now()
#print(time_now.strftime("%Y-%m-%d\n%H:%M:%S"))

#for i in range(10):
    #time.sleep(1)
#    time_now = datetime.now()
#    print(time_now.strftime('%H:%M:%S'))
    
#tzutc = tzutc()
#tzlocal = tzlocal()

tzkiev = pytz.timezone('Europe/Kiev') # есть в pytz/zoneinfo
now = datetime.now(tzkiev)
print(now.strftime("%Y-%m-%d\n%H:%M:%S UTC%z"))

#print(tzutc)
#print(tzlocal)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.Window_Options_init()
        self.Main_Clock_Options_init()
        self.Timer_Options_init()
        self.Stopwatch_Options_init()
        self.Calendar_Options_init()
        self.Alarmclock_Options_init()
        
        self.start_main_clock()

#------------------------------------------------------------------------------> Hotkeys
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            reply = QMessageBox.question(self, 'Message', "Выйти из программы?", 
                                         QMessageBox.Yes | QMessageBox.No, 
                                         QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.close()
            
    def Window_Options_init(self): #-------------------------------------------> WindowOptions
        self.setGeometry(200, 200, 1000, 800)
        self.setWindowTitle('Clock')
        self.setWindowIcon(QIcon('clock_icon.png'))
        
    def Main_Clock_Options_init(self): #---------------------------------------> MainClockOptions
        self.main_clock = QLCDNumber(self)
        self.main_clock.setToolTip('Главные часы')
        self.main_clock.move(275, 30)
        self.main_clock.resize(450, 100)    
        self.main_clock.setDigitCount(8)
        
        tzmoscow = pytz.timezone('Europe/Moscow') # есть в pytz/zoneinfo       
        time_now = datetime.now(tzmoscow)
        
        self.main_clock_date_lcd = QLCDNumber(self)
        self.main_clock_date_lcd.setDigitCount(10)
        self.main_clock_date_lcd.resize(200, 80)
        self.main_clock_date_lcd.move(40, 40)
        self.main_clock_date_lcd.setToolTip('День/месяц/год')
        
        self.main_clock_utc_label = QLabel(self)
        self.main_clock_utc_label.resize(200, 40)
        self.main_clock_utc_label.move(840, 40)
        self.main_clock_utc_label.setToolTip('UTC')
        self.main_clock_utc_label.setText(time_now.strftime('UTC %z'))
        
    def Timer_Options_init(self): #--------------------------------------------> TimerOptions
        self.timer = QLCDNumber(self)
        self.timer.setDigitCount(8)
        self.timer.display('00' + ':' + '00' + ':' + '00')
        self.timer_value = '00' + ':' + '00' + ':' + '00'
        
        self.slider_timer_second = QSlider(Qt.Horizontal, self)
        self.slider_timer_minute = QSlider(Qt.Horizontal, self)
        self.slider_timer_hour = QSlider(Qt.Horizontal, self)
        
        self.slider_timer_second.setMinimum(0)
        self.slider_timer_minute.setMinimum(0)
        self.slider_timer_hour.setMinimum(0)
        
        self.slider_timer_second.setMaximum(59)
        self.slider_timer_minute.setMaximum(59)
        self.slider_timer_hour.setMaximum(47)
        
        self.slider_timer_second.valueChanged.connect(self.change_timer_sec)
        self.slider_timer_minute.valueChanged.connect(self.change_timer_min)
        self.slider_timer_hour.valueChanged.connect(self.change_timer_hour)        
        
        self.start_timer_btn = QPushButton('Start', self)
        self.start_timer_btn.clicked.connect(self.start_tick_timer)
        self.start_timer_btn.setToolTip('Запустить таймер')
        
        self.finish_timer_btn = QPushButton('Finish', self)
        self.finish_timer_btn.clicked.connect(self.finish_tick_timer)
        self.finish_timer_btn.setEnabled(False)
        self.finish_timer_btn.setToolTip('Остановить таймер')
        
        self.timer.move(30, 150)
        self.timer.resize(250, 100)
        
        self.slider_timer_second.move(30, 270)
        self.slider_timer_second.resize(200, 30)
        self.label_timer_second = QLabel(self)
        self.label_timer_second.setText('SEC')
        self.label_timer_second.resize(30, 30)
        self.label_timer_second.move(240, 270)
        
        self.slider_timer_minute.move(30, 310)
        self.slider_timer_minute.resize(200, 30)
        self.label_timer_minute = QLabel(self)
        self.label_timer_minute.setText('MIN')
        self.label_timer_minute.resize(30, 30)
        self.label_timer_minute.move(240, 310)
        
        self.slider_timer_hour.move(30, 350)
        self.slider_timer_hour.resize(200, 30) 
        self.label_timer_hour = QLabel(self)
        self.label_timer_hour.setText('HOUR')
        self.label_timer_hour.resize(40, 30)
        self.label_timer_hour.move(240, 350)
        
        self.start_timer_btn.move(30, 400)
        self.start_timer_btn.resize(80, 30)
        
        self.finish_timer_btn.move(200, 400)
        self.finish_timer_btn.resize(80, 30)
        
    def Stopwatch_Options_init(self): #----------------------------------------> StopwatchOptions
        self.stopwatch = QLCDNumber(self)
        self.stopwatch.setDigitCount(8)
        self.stopwatch.display('00:00:00')
        self.stopwatch_value = '00:00:00'
        self.stopwatch.move(720, 150)
        self.stopwatch.resize(250, 100)
        
        self.start_stopwatch_btn = QPushButton(self)
        self.start_stopwatch_btn.setText('Start')
        self.start_stopwatch_btn.resize(80, 30)
        self.start_stopwatch_btn.move(720, 270)
        self.start_stopwatch_btn.clicked.connect(self.start_tick_stopwatch)
        self.start_stopwatch_btn.setToolTip('Запустить секундомер')
        
        self.stop_stopwatch_btn = QPushButton(self)
        self.stop_stopwatch_btn.setText('Finish')
        self.stop_stopwatch_btn.resize(80, 30)
        self.stop_stopwatch_btn.move(890, 270)
        self.stop_stopwatch_btn.setEnabled(False)
        self.stop_stopwatch_btn.clicked.connect(self.stop_tick_stopwatch)
        self.stop_stopwatch_btn.setToolTip('Остановить секундомер')
        
        self.clear_stopwatch_btn = QPushButton(self)
        self.clear_stopwatch_btn.setText('Clear')
        self.clear_stopwatch_btn.resize(80, 30)
        self.clear_stopwatch_btn.move(805, 270)
        self.clear_stopwatch_btn.setEnabled(False)
        self.clear_stopwatch_btn.clicked.connect(self.clear_tick_stopwatch)
        self.clear_stopwatch_btn.setToolTip('Очистить значение на таймере')
 
#------------------------------------------------------------------------------> CalendarOptions   
    def Calendar_Options_init(self):
        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(True)
        self.calendar.clicked[QDate].connect(self.change_calendar_value)
        self.calendar.move(305, 150)
        #self.calendar_value = self.calendar.selectedDate()

#------------------------------------------------------------------------------> AlarmclockOptions   
    def Alarmclock_Options_init(self):
        lines = open('alarmclock_data.txt').read().split('&')
        # lines = 'Date: dd/mm/yyyy\nTime: hh:mm:ss\nType: melody'
        self.alarmclock_value = list(lines)
        self.make_new_alarm_btn = QPushButton(self)
        self.make_new_alarm_btn.setText('New')
        self.make_new_alarm_btn.clicked.connect(self.make_new_alarm)
        
        self.alarmclock_label = QLabel(self)
        self.alarmclock_label.setText('\n\n'.join(self.alarmclock_value))
        
#------------------------------------------------------------------------------> TimerFunc
    def toggle_timer_btns(self, value):
        self.slider_timer_second.setEnabled(value)
        self.slider_timer_minute.setEnabled(value)
        self.slider_timer_hour.setEnabled(value)
        self.start_timer_btn.setEnabled(value)
        
    def start_tick_timer(self):
        if self.timer_value != '00:00:00':
            self.toggle_timer_btns(False)
            self.temp_timer_data = self.timer_value
            self.tick_timer(break_timer=False)
            self.finish_timer_btn.setEnabled(True)
            
    def finish_tick_timer(self):
        self.tick_timer(break_timer=True)
        self.finish_timer_btn.setEnabled(False)
        
    def tick_timer(self, break_timer):
        if break_timer:
            self.toggle_timer_btns(True)
            self.timer.display(self.temp_timer_data)
            self.timer_value = str('00:00:00')
            
        else:   
            timer_value = self.timer_value
            if int(timer_value[6:]) > 0:
                self.change_timer_sec(int(timer_value[6:]) - 1)
                QTimer().singleShot(1000, partial(self.tick_timer, break_timer=False))
            else:
                if int(timer_value[3:5]) > 0:
                    self.change_timer_sec(59)
                    self.change_timer_min(int(timer_value[3:5]) - 1)
                    QTimer().singleShot(1000, partial(self.tick_timer, break_timer=False))
                else:
                    if int(timer_value[:2]) > 0:
                        self.change_timer_sec(59)
                        self.change_timer_min(59)
                        self.change_timer_hour(int(timer_value[:2]) - 1)
                        QTimer().singleShot(1000, partial(self.tick_timer, break_timer=False))
                    else:
                        self.toggle_timer_btns(True)
                        self.timer.display(self.temp_timer_data)
                        self.timer_value = str(self.temp_timer_data)
                        self.finish_timer_btn.setEnabled(False)
                        winsound.PlaySound('timer_1.wav', winsound.SND_FILENAME)
        
    def change_timer_sec(self, value):
        fixed_data = self.timer_value[:6] + str(int(value)).rjust(2, '0')
        self.timer.display(fixed_data)
        self.timer_value = fixed_data
        
    def change_timer_min(self, value):
        fixed_data = self.timer_value[:3] + str(int(value)).rjust(2, '0') + self.timer_value[5:]
        self.timer.display(fixed_data)
        self.timer_value = fixed_data
        
    def change_timer_hour(self, value):
        fixed_data = str(int(value)).rjust(2, '0') + self.timer_value[2:]
        self.timer.display(fixed_data)
        self.timer_value = fixed_data
    
#------------------------------------------------------------------------------> StopwatchFunc  
    def start_tick_stopwatch(self):
        self.temp_stopwatch_data = self.timer_value
        self.stopwatch.display('00:00:00')
        self.stopwatch_value = '00:00:00'
        self.tick_stopwatch(break_stopwatch=False)
        self.stop_stopwatch_btn.setEnabled(True)
        self.start_stopwatch_btn.setEnabled(False)
        
    def stop_tick_stopwatch(self):
        self.tick_stopwatch(break_stopwatch=True)
        self.stop_stopwatch_btn.setEnabled(False)
        self.clear_stopwatch_btn.setEnabled(True)
        
    def clear_tick_stopwatch(self):
        self.stopwatch.display('00:00:00')
        self.stopwatch_value = '00:00:00'
        self.stop_stopwatch_btn.setEnabled(False)
        self.start_stopwatch_btn.setEnabled(True)
        self.clear_stopwatch_btn.setEnabled(False)
        
    def tick_stopwatch(self, break_stopwatch):
        if break_stopwatch:
            self.temp_stopwatch_data = str(self.stopwatch_value)
            self.stopwatch.display(self.temp_stopwatch_data)
            self.stopwatch_value = '99:59:59'
        else:
            stopwatch_value = self.stopwatch_value
            if int(stopwatch_value[6:]) < 59:
                self.change_stopwatch_sec(int(stopwatch_value[6:]) + 1)
                QTimer().singleShot(1000, partial(self.tick_stopwatch, break_stopwatch=False))
            else:
                if int(stopwatch_value[3:5]) < 59:
                    self.change_stopwatch_sec(0)
                    self.change_stopwatch_min(int(stopwatch_value[3:5]) + 1)
                    QTimer().singleShot(1000, partial(self.tick_stopwatch, break_stopwatch=False))
                else:
                    if int(stopwatch_value[:2]) < 99:
                        self.change_stopwatch_sec(0)
                        self.change_stopwatch_min(0)
                        self.change_stopwatch_hour(int(stopwatch_value[:2]) + 1)
                        QTimer().singleShot(1000, partial(self.tick_stopwatch, break_stopwatch=False))
                    else:
                        self.stop_stopwatch_btn.setEnabled(False)
                        self.stopwatch.display(self.temp_stopwatch_data)
                        self.stopwatch_value = str(self.temp_stopwatch_data)        
        
    
    def change_stopwatch_sec(self, value):
        fixed_data = self.stopwatch_value[:6] + str(int(value)).rjust(2, '0')
        self.stopwatch.display(fixed_data)
        self.stopwatch_value = fixed_data
        
    def change_stopwatch_min(self, value):
        fixed_data = self.stopwatch_value[:3] + str(int(value)).rjust(2, '0') + self.stopwatch_value[5:]
        self.stopwatch.display(fixed_data)
        self.stopwatch_value = fixed_data
        
    def change_stopwatch_hour(self, value):
        fixed_data = str(int(value)).rjust(2, '0') + self.stopwatch_value[2:]
        self.stopwatch.display(fixed_data)
        self.stopwatch_value = fixed_data
        
#------------------------------------------------------------------------------> StartMainClock
    def start_main_clock(self):
        time_now = datetime.now()
        self.time_now_value = time_now.strftime('%Y %m %d\n%H:%M:%S')
        self.main_clock.display(time_now.strftime('%H' + ':' + '%M' + ':' + '%S'))
        self.main_clock_date_lcd.display(time_now.strftime('%d-%m-%Y'))
        QTimer().singleShot(1000, self.start_main_clock)

#------------------------------------------------------------------------------> AlarmclockFunc
    def make_new_alarm(self):
        pass
#------------------------------------------------------------------------------> CalendarFunc
    def change_calendar_value(self):
        self.calendar_value = self.calendar.selectedDate()

#------------------------------------------------------------------------------> Main
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())