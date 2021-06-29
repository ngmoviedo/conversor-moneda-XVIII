from PyQt5.QtWidgets import QComboBox, QDialog, QSpinBox, QLabel, QPushButton
from PyQt5.QtWidgets import QApplication, QGridLayout
import numpy as np

class Conversor(QDialog):
    def __init__(self, *args, **kwargs):
        super(Conversor, self).__init__(*args, **kwargs)

        rel =   [None, 'Maravedises','Reales','Ducados','Reales de a 8','Escudos','Doblones de a 8']     

        # Valor de entrada
        self.inSpinBox = QSpinBox()
        self.inSpinBox.setRange(1,1000000000)
        self.inSpinBox.setValue(1)

        # Unidad de entrada
        self.inComboBox = QComboBox()
        self.inComboBox.addItems(rel[1:])

        # Unidades de salida
        self.outComboBox0 = QComboBox()
        self.outComboBox0.addItems(rel[1:])
        self.outComboBox1 = QComboBox()
        self.outComboBox2 = QComboBox()
        self.outComboBox3 = QComboBox()

        # Resultados
        self.Label0 = QLabel('1')
        self.Label1 = QLabel('0')
        self.Label2 = QLabel('0')
        self.Label3 = QLabel('0')

        # Instrucciones
        self.instruc_de = QLabel('De:')
        self.instruc_a = QLabel('A:')
        self.Button = QPushButton('Convertir')
        self.resto = QLabel('Resto:')
        self.resto_num = QLabel('0 Maravedises')
        self.coma = QLabel(';')

        # Posicion de los controles
        grid = QGridLayout()

        grid.addWidget(self.instruc_de, 0, 0)

        grid.addWidget(self.inSpinBox, 1, 0)
        grid.addWidget(self.inComboBox, 1, 1)
        grid.addWidget(self.Button, 1, 2, 1, 4)
        
        grid.addWidget(self.instruc_a, 2, 0)

        grid.addWidget(self.Label0, 3, 0)
        grid.addWidget(self.outComboBox0, 3, 1)
        grid.addWidget(QLabel(';'), 3, 2)

        grid.addWidget(self.Label1, 3, 3)
        grid.addWidget(self.outComboBox1, 3, 4)
        grid.addWidget(QLabel(';'), 3, 5)

        grid.addWidget(self.Label2, 3, 6)
        grid.addWidget(self.outComboBox2, 3, 7)
        grid.addWidget(QLabel(';'), 3, 8)

        grid.addWidget(self.Label3, 3, 9)
        grid.addWidget(self.outComboBox3, 3, 10)

        grid.addWidget(self.resto, 4, 8)
        grid.addWidget(self.resto_num, 4, 9, 4, 10)

        self.setLayout(grid)

        # Eventos (funciona al pulsar el boton)

        # Al cambiar el valor de una caja de resultados se habilita, si procede, la caja posterior
        self.outComboBox0.currentTextChanged.connect(lambda: self.boxes(1))
        self.outComboBox1.currentTextChanged.connect(lambda: self.boxes(2))
        self.outComboBox2.currentTextChanged.connect(lambda: self.boxes(3))
        

        # Se ejecuta la conversion al pulsar el boton
        self.Button.clicked.connect(lambda: self.actualizar())


#---------------------------------------------------------------------
    def actualizar(self):
        val = self.inSpinBox.value()
        unit_in = self.inComboBox.currentText()
        unit_out =[self.outComboBox0.currentText(), self.outComboBox1.currentText(), self.outComboBox2.currentText(), self.outComboBox3.currentText()]
        c=0
        r=val
        i=0
        s=np.zeros(len(unit_out))
        unit_out=[i for i in unit_out if i]
        for unit in unit_out:
           c, r = self.div(r,unit_in,unit)
           s[i]=s[i]+c # Se asigna el cociente a la posicion de s
           i+=1
        # Si sobra un resto, se devuelve en la ultima posicion de s
        if r != 0:
            self.resto_num.setText((str(int(r))+' '+self.inComboBox.currentText()))


        self.Label0.setText(str(int(s[0])))
        self.Label1.setText(str(int(s[1])))
        self.Label2.setText(str(int(s[2])))
        self.Label3.setText(str(int(s[3])))

#---------------------------------------------------------------------

    def div(self,val,unit_in,unit_out):
          # Diccionario de equivalencias
          rel={'Maravedises':1, 'Reales':34, 'Ducados':374, 'Reales de a 8':272, 'Escudos':544, 'Doblones de a 8':2720}
          # Cociente y resto de la conversion
          c, r = divmod(val*rel[unit_in],rel[unit_out])
          return c, r

#--------------------------------------------------------------------

    def boxes(self,ind):
        # Desbloquea los elementos que correspondan de las siguientes cajas
        rel =   [None, 'Maravedises','Reales','Reales de a 8','Ducados','Escudos','Doblones de a 8']
        Boxes = [self.outComboBox0, self.outComboBox1, self.outComboBox2, self.outComboBox3]
        box0 = Boxes[ind-1]
        item0 = box0.currentText() 
        box = Boxes[ind]
        box.clear()
        if item0:
            # Solo opera si la caja anterior tiene todavía algún elemento
            v = rel[0:rel.index(item0)]
            box.addItems(v)

#----------------------------------------------------------------------
if __name__ == "__main__":
    app = QApplication(['Conversor de moneda dieciochesca'])
    form = Conversor()
    form.show()
    app.exec_()

