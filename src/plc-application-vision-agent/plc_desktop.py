import sys
import time
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSlider, QProgressBar, QFrame, QListWidget, QCheckBox, QButtonGroup, QRadioButton, QMessageBox)
from PySide6.QtCore import Qt, QTimer
import pyqtgraph as pg
from PySide6.QtGui import QPainter, QColor, QFont, QLinearGradient

class PLCState:
    def __init__(self):
        self.start_pump = False
        self.stop_pump = False
        self.high_level = False
        self.low_level = True
        self.pump_running = False
        self.alarm = False
        self.tank_level = 0.0
        self.valve_opening = 100.0
        self.last_start_pump = False
        self.last_stop_pump = False
        self.chart_level = []
        self.chart_valve = []
        self.max_chart = 30
        self.event_log = []
        self.last_alarm = False
        self.last_pump = False
        self.auto_mode = True
        self.manual_valve = True
        self.manual_level = 0.0

    def scan(self):
        # Tank simulation
        if self.auto_mode:
            fill_rate = 0.5 if self.pump_running and self.valve_opening > 0 else 0.0
            drain_rate = 0.2 if not self.pump_running and self.valve_opening > 0 else 0.0
            self.tank_level += fill_rate
            self.tank_level -= drain_rate
            self.tank_level = max(0.0, min(100.0, self.tank_level))
            self.valve_opening = 100.0
        else:
            # Only allow tank level to change if valve is open
            if self.manual_valve:
                self.tank_level = self.manual_level
            # If valve is closed, keep tank level constant
            self.valve_opening = 100.0 if self.manual_valve else 0.0
        # High/Low level sensors auto-update
        self.high_level = self.tank_level >= 95
        self.low_level = self.tank_level > 5
        # Pump logic
        if self.start_pump and not self.pump_running and not self.high_level:
            self.pump_running = True
            self.log_event("Pump started")
        if self.stop_pump and not self.last_stop_pump:
            self.pump_running = False
            self.log_event("Pump stopped (manual)")
        if self.high_level and self.pump_running:
            self.pump_running = False
            self.log_event("Pump stopped (high level)")
        self.last_start_pump = self.start_pump
        self.last_stop_pump = self.stop_pump
        # Alarm logic
        self.alarm = (self.tank_level > 98 or not self.low_level)
        if self.alarm and not self.last_alarm:
            self.log_event("Alarm ON")
        if not self.alarm and self.last_alarm:
            self.log_event("Alarm OFF")
        self.last_alarm = self.alarm
        # Chart data
        self.chart_level.append(self.tank_level)
        self.chart_valve.append(self.valve_opening)
        if len(self.chart_level) > self.max_chart:
            self.chart_level.pop(0)
            self.chart_valve.pop(0)

    def log_event(self, msg):
        t = time.strftime("%H:%M:%S")
        self.event_log.append(f"[{t}] {msg}")
        if len(self.event_log) > 10:
            self.event_log.pop(0)

class TankWidget(QWidget):
    def __init__(self, plc_state):
        super().__init__()
        self.plc_state = plc_state
        self.setMinimumHeight(180)

    def paintEvent(self, event):
        painter = QPainter(self)
        w, h = self.width(), self.height()
        margin = 40
        tank_width = w // 2
        tank_height = h // 3
        tank_left = (w - tank_width) // 2
        tank_top = margin + 40
        # Draw tank outline
        painter.setPen(QColor('#2563eb'))
        painter.setBrush(QColor('#e0e7ef'))
        painter.drawRect(tank_left, tank_top, tank_width, tank_height)
        # Draw water level with gradient
        level = self.plc_state.tank_level / 100.0
        water_h = int(tank_height * level)
        if water_h > 0:
            gradient = QLinearGradient(tank_left, tank_top + tank_height, tank_left, tank_top + tank_height - water_h)
            gradient.setColorAt(0, QColor('#38bdf8'))
            gradient.setColorAt(1, QColor('#0ea5e9'))
            painter.setBrush(gradient)
        else:
            painter.setBrush(QColor('#38bdf8'))
        painter.drawRect(tank_left+2, tank_top + tank_height - water_h, tank_width-4, water_h)
        # Draw tank level number (large, bold, outlined, always readable)
        percent_text = f"{self.plc_state.tank_level:.1f}%"
        font = painter.font()
        font.setPointSize(32)
        font.setBold(True)
        painter.setFont(font)
        for dx, dy in [(-2,0),(2,0),(0,-2),(0,2)]:
            painter.setPen(QColor('white'))
            painter.drawText(tank_left, tank_top + tank_height//2 + dy, tank_width, 50, Qt.AlignCenter, percent_text)
        painter.setPen(QColor('black'))
        painter.drawText(tank_left, tank_top + tank_height//2, tank_width, 50, Qt.AlignCenter, percent_text)
        # Draw alarm (top center above tank)
        if self.plc_state.alarm:
            painter.setBrush(QColor('#ef4444'))
            painter.setPen(QColor('#991b1b'))
            painter.drawEllipse(tank_left + tank_width//2 - 18, tank_top - 50, 36, 36)
            painter.setFont(QFont('Arial', 14, QFont.Bold))
            painter.drawText(tank_left + tank_width//2 - 60, tank_top - 60, 120, 20, Qt.AlignCenter, "ALARM!")
        # Draw sensors (left of tank, vertically aligned)
        label_font = QFont('Arial', 10)
        painter.setFont(label_font)
        sensor_circle_d = 28
        sensor_x = tank_left - 60
        sensor_y_high = tank_top
        sensor_y_low = tank_top + tank_height - sensor_circle_d
        label_padding = 16
        # High Level
        painter.setBrush(QColor('#22c55e') if self.plc_state.high_level else QColor('#b0b8c1'))
        painter.setPen(QColor('black'))
        painter.drawEllipse(sensor_x, sensor_y_high, sensor_circle_d, sensor_circle_d)
        painter.drawText(sensor_x + sensor_circle_d + label_padding, sensor_y_high + sensor_circle_d//2 + 5, "High Sensor")
        # Low Level
        painter.setBrush(QColor('#22c55e') if self.plc_state.low_level else QColor('#b0b8c1'))
        painter.drawEllipse(sensor_x, sensor_y_low, sensor_circle_d, sensor_circle_d)
        painter.drawText(sensor_x + sensor_circle_d + label_padding, sensor_y_low + sensor_circle_d//2 + 5, "Low Sensor")
        # Draw pump (below tank, left)
        pump_x = tank_left + 30
        pump_y = tank_top + tank_height + 40
        pump_color = QColor('#22c55e') if self.plc_state.pump_running else QColor('#b0b8c1')
        painter.setBrush(pump_color)
        painter.setPen(QColor('black'))
        painter.drawEllipse(pump_x, pump_y, 36, 36)
        painter.setFont(QFont('Arial', 12, QFont.Bold))
        painter.drawText(pump_x - 10, pump_y + 55, 60, 20, Qt.AlignCenter, "Pump")
        # Draw valve (below tank, right)
        valve_x = tank_left + tank_width - 66
        valve_y = tank_top + tank_height + 40
        valve_color = QColor('#22c55e') if self.plc_state.valve_opening > 0 else QColor('#b0b8c1')
        painter.setBrush(valve_color)
        painter.setPen(QColor('black'))
        painter.drawEllipse(valve_x, valve_y, 36, 36)
        painter.drawText(valve_x - 10, valve_y + 55, 60, 20, Qt.AlignCenter, "Valve")

class PLCApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Water Tank System Simulation")
        self.setMinimumSize(950, 850)
        self.state = PLCState()
        self.init_ui()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plc)
        self.timer.start(50)  # 50 ms scan
        self.tank_empty_popup_shown = False

    def init_ui(self):
        layout = QVBoxLayout()
        # Mode Switch
        mode_frame = QFrame()
        mode_layout = QHBoxLayout()
        self.radio_auto = QRadioButton("Auto Mode")
        self.radio_manual = QRadioButton("Manual Mode")
        self.radio_auto.setChecked(True)
        self.radio_auto.toggled.connect(self.set_mode)
        mode_layout.addWidget(self.radio_auto)
        mode_layout.addWidget(self.radio_manual)
        mode_frame.setLayout(mode_layout)
        # Digital Inputs
        input_frame = QFrame()
        input_layout = QHBoxLayout()
        self.btn_start = QPushButton("Start Pump")
        self.btn_start.setCheckable(False)
        self.btn_start.setToolTip("Momentary: Press to start pump")
        self.btn_start.pressed.connect(lambda: self.set_input('start_pump', True))
        self.btn_start.released.connect(lambda: self.set_input('start_pump', False))
        self.btn_stop = QPushButton("Stop Pump")
        self.btn_stop.setCheckable(False)
        self.btn_stop.setToolTip("Momentary: Press to stop pump")
        self.btn_stop.pressed.connect(lambda: self.set_input('stop_pump', True))
        self.btn_stop.released.connect(lambda: self.set_input('stop_pump', False))
        input_layout.addWidget(self.btn_start)
        input_layout.addWidget(self.btn_stop)
        input_frame.setLayout(input_layout)
        # Outputs
        output_frame = QFrame()
        output_layout = QHBoxLayout()
        self.lbl_pump = QLabel("Pump Running: OFF")
        self.led_pump = QLabel()
        self.led_pump.setFixedSize(20, 20)
        self.lbl_alarm = QLabel("Alarm: OFF")
        self.led_alarm = QLabel()
        self.led_alarm.setFixedSize(20, 20)
        output_layout.addWidget(self.led_pump)
        output_layout.addWidget(self.lbl_pump)
        output_layout.addSpacing(20)
        output_layout.addWidget(self.led_alarm)
        output_layout.addWidget(self.lbl_alarm)
        output_frame.setLayout(output_layout)
        # Manual Controls
        manual_frame = QFrame()
        manual_layout = QHBoxLayout()
        self.slider_level = QSlider(Qt.Horizontal)
        self.slider_level.setMinimum(0)
        self.slider_level.setMaximum(100)
        self.slider_level.setValue(0)
        self.slider_level.setToolTip("Set tank level in Manual mode")
        self.slider_level.valueChanged.connect(self.set_manual_level)
        self.btn_valve = QPushButton("Open Valve")
        self.btn_valve.setCheckable(True)
        self.btn_valve.setChecked(True)
        self.btn_valve.setToolTip("Toggle valve open/close in Manual mode")
        self.btn_valve.clicked.connect(self.toggle_valve)
        manual_layout.addWidget(QLabel("Manual Tank Level:"))
        manual_layout.addWidget(self.slider_level)
        manual_layout.addWidget(self.btn_valve)
        manual_frame.setLayout(manual_layout)
        # Tank Visualization
        self.tank_widget = TankWidget(self.state)
        # Live Chart
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('w')
        self.plot_widget.addLegend()
        self.plot_widget.setYRange(0, 100)
        self.plot_level = self.plot_widget.plot(pen=pg.mkPen('g', width=2), name='Tank Level')
        self.plot_valve = self.plot_widget.plot(pen=pg.mkPen('b', width=2), name='Valve Opening')
        # Event Log
        log_frame = QFrame()
        log_layout = QVBoxLayout()
        self.log_list = QListWidget()
        log_layout.addWidget(QLabel("Event/Alarm Log:"))
        log_layout.addWidget(self.log_list)
        log_frame.setLayout(log_layout)
        # Add to main layout
        layout.addWidget(mode_frame)
        layout.addWidget(input_frame)
        layout.addWidget(output_frame)
        layout.addWidget(manual_frame)
        layout.addWidget(self.tank_widget)
        layout.addWidget(self.plot_widget)
        layout.addWidget(log_frame)
        self.setLayout(layout)
        self.update_manual_controls()

    def set_input(self, name, value):
        setattr(self.state, name, value)

    def set_mode(self):
        self.state.auto_mode = self.radio_auto.isChecked()
        self.update_manual_controls()

    def update_manual_controls(self):
        manual_enabled = not self.state.auto_mode
        self.slider_level.setEnabled(manual_enabled)
        self.btn_valve.setEnabled(manual_enabled)

    def set_manual_level(self, value):
        self.state.manual_level = float(value)

    def toggle_valve(self):
        self.state.manual_valve = self.btn_valve.isChecked()
        self.btn_valve.setText("Open Valve" if self.state.manual_valve else "Close Valve")

    def update_plc(self):
        self.state.scan()
        # Outputs
        self.lbl_pump.setText(f"Pump Running: {'ON' if self.state.pump_running else 'OFF'}")
        self.led_pump.setStyleSheet(f"background: {'#22c55e' if self.state.pump_running else '#b0b8c1'}; border-radius: 10px; border: 1.5px solid #15803d;")
        self.lbl_alarm.setText(f"Alarm: {'ON' if self.state.alarm else 'OFF'}")
        self.led_alarm.setStyleSheet(f"background: {'#ef4444' if self.state.alarm else '#b0b8c1'}; border-radius: 10px; border: 1.5px solid #991b1b;")
        # Tank visualization
        self.tank_widget.update()
        # Chart
        self.plot_level.setData(self.state.chart_level)
        self.plot_valve.setData(self.state.chart_valve)
        # Event log
        self.log_list.clear()
        for event in reversed(self.state.event_log):
            self.log_list.addItem(event)
        # Manual controls feedback
        if not self.state.auto_mode:
            self.slider_level.setValue(int(self.state.manual_level))
            self.btn_valve.setText("Open Valve" if self.state.manual_valve else "Close Valve")
        # Show popup if tank is empty in auto mode
        if self.state.auto_mode and self.state.tank_level == 0.0 and not self.tank_empty_popup_shown:
            self.tank_empty_popup_shown = True
            msg = QMessageBox(self)
            msg.setWindowTitle("ALARM")
            msg.setText("<span style='font-size:36pt; color:red; font-weight:bold;'>ALARM: Tank is EMPTY!</span>")
            msg.setIcon(QMessageBox.Critical)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
            self.activateWindow()
            self.raise_()
        if self.state.tank_level > 0.0:
            self.tank_empty_popup_shown = False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = PLCApp()
    win.show()
    sys.exit(app.exec()) 