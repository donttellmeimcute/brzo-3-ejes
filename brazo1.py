import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider, QLabel
from PyQt6.QtCore import Qt, QTimer
import serial

ser = serial.Serial('COM4', 115200, timeout=0)  # Establecer timeout a 0 para lectura no bloqueante

class ControlServo(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.sliders = {}
        self.labels = {}

        # Control solo para ejes X, Y, Z
        for eje in ['X', 'Y', 'Z']: 
            slider = QSlider(Qt.Orientation.Horizontal)
            slider.setMinimum(0)
            slider.setMaximum(255)
            slider.sliderReleased.connect(self.slider_cambiado)
            self.sliders[eje] = slider
            layout.addWidget(slider)

            etiqueta = QLabel(f"Valor actual: 0")
            self.labels[eje] = etiqueta
            layout.addWidget(etiqueta)

        self.setLayout(layout)

    def slider_cambiado(self):
        slider = self.sender()
        valor = slider.value()

        for eje, obj_slider in self.sliders.items():
            if obj_slider is slider:
                valor_servo = self.mapear_valor(valor)  
                enviar_comando(eje, valor_servo)

    def actualizar_sliders(self):
        try:
            while ser.in_waiting:  # Leer todos los bytes disponibles
                valor = ser.readline().decode().strip()
                if valor:  
                    print("Recibido:", valor)  
                    self.parsear_feedback_arduino(valor)
        except serial.SerialException:
            pass

    def mapear_valor(self, valor):
        return int(round(valor * (180 / 255))) 

    def parsear_feedback_arduino(self, datos):
        try:
            eje, valor_servo = datos.split(':')
            if eje in self.sliders:
                valor_slider = int(int(valor_servo) * (255 / 180))
                self.sliders[eje].setValue(valor_slider)
                self.labels[eje].setText(f"Valor actual: {valor_servo}")
        except ValueError:
            print("Arduino envió datos inválidos")


def enviar_comando(coordenada, valor):
    comando = f"{coordenada}:{valor}\n"
    ser.write(comando.encode())
    print(f"Enviado: {comando}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = ControlServo()
    ventana.show()

    temporizador = QTimer()
    temporizador.timeout.connect(ventana.actualizar_sliders)
    temporizador.start(20)  # Actualizar cada 20 milisegundos

    sys.exit(app.exec())
