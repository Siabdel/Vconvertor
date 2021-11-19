import sys
from PyQt4 import QtGui, QtCore
 
 
class Exemple(QtGui.QMainWindow):
   
    def __init__(self):
        super(Exemple, self).__init__()
    
        self.initUI()
         
    def initUI(self):
       
        bouton = QtGui.QPushButton("Button 1", self)
        bouton.move(50, 100)
       
        self.connect(bouton, QtCore.SIGNAL('clicked()'),
            self.cliquer)
    
        self.resize(290, 150)
    
    
    def cliquer(self):
        # code pour ouvrir ta nouvelle fenetre
        pass

if __file__ == "__main__" :
    app = QtGui.QApplication(sys.argv)
    ex = Exemple()
    ex.show()
    sys.exit(app.exec_())