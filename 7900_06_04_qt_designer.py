# used to parse files more easily 
from __future__ import with_statement
# Numpy module 
import numpy as np
# for command-line arguments 
import sys
# Qt4 bindings for core Qt functionalities (non-GUI) 
from PyQt5 import QtCore 
# Python Qt4 bindings for GUI objects 
from PyQt5 import QtGui
from PyQt5 import QtWidgets
# import the MainWindow widget from the converted .ui files 
from Ui_qtdesigner import Ui_mplMainWindow
from scipy import signal
class DesignerMainWindow(QtWidgets.QMainWindow, Ui_mplMainWindow):   
    """Customization for Qt Designer created window"""    
    def __init__(self, parent = None):        
        # initialization of the superclass        
        super(DesignerMainWindow, self).__init__(parent)        
        # setup the GUI --> function generated by pyuic4        
        self.setupUi(self)
        # connect the signals with the slots        
        self.mplpushButton.clicked.connect(self.update_graph)
        self.mplaactionOpen.triggered.connect(self.select_file) 
        self.mplactionQuit.triggered.connect(app.quit)
        self.lineEdit_2.setReadOnly(True)
        self.thresholdSlider.valueChanged.connect(self.threshold_changed)
        
    def threshold_changed(self, value):
        self.lineEdit_2.setText(str(value))
        
    def select_file(self):        
        """opens a file select dialog"""        
        # open the dialog and get the selected file        
        file = QtWidgets.QFileDialog.getOpenFileName()        
        # if a file is selected        
        if file:            
            # update the lineEdit text with the selected filename            
            self.lineEdit.setText(str(file[0]))
    def parse_file(self, filename):
        """Parse a text file to extract letters frequencies""" 
         # dict initialization        
        letters = {}
        # lower-case letter ordinal numbers
        for i in range(97, 122 + 1):
            letters[chr(i)] = 0
        # parse the input file
        with open(filename) as f: 
            for line in f: 
                for char in line: 
                    # counts only letters  
                    if ord(char.lower()) in range(97, 122 + 1):
                        letters[char.lower()] += 1
        # compute the ordered list of keys and relative values
        k = sorted(letters.keys())
        v = [letters[ki] for ki in k]
        return k, v
    def get_the_wave(self, filename):
        col1 = np.loadtxt(filename,  delimiter='\t',  usecols = (0,  ),  dtype = float)
        col2 = np.loadtxt(filename,  delimiter='\t',  usecols = (1,  ),  dtype = float)
        return col1,  col2
        
    def update_graph(self):
        """Updates the graph with new letters frequencies"""
        # get the letters frequencies
        #l, v = self.parse_file(self.lineEdit.text())
        time,  voltage = self.get_the_wave(self.lineEdit.text())
        # clear the Axes
        self.mpl.canvas.ax.clear()
        self.mpl.canvas.bx.clear()
        # draw a bar chart for letters and their frequencies
        # set width to 0.5 and shift bars of 0.25, to be centered
        #self.mpl.canvas.ax.bar(np.arange(len(l))-0.25, v, width=0.5)
        # reset the X limits
        #self.mpl.canvas.ax.set_xlim(xmin=-0.25, xmax=len(l)-0.75)
        # set the X ticks & tickslabel as the letters
        #self.mpl.canvas.ax.set_xticks(range(len(time)))
        #self.mpl.canvas.ax.set_xticklabels(time)
        # enable grid only on the Y axis
        self.mpl.canvas.ax.get_xaxis().grid(True)  
        self.mpl.canvas.ax.get_yaxis().grid(True)
        self.mpl.canvas.ax.plot(voltage,  'k')
        
        # draw a bar chart for letters and their frequencies
        # set width to 0.5 and shift bars of 0.25, to be centered
        #self.mpl.canvas.bx.bar(np.arange(len(l))-0.25, v, width=0.5)
        updated_voltage = np.fft.rfft(voltage)
        for i in range(len(updated_voltage)):
            if abs(updated_voltage[i]) < self.thresholdSlider.value():
                updated_voltage[i] = 0
        updated_voltage = np.fft.irfft(updated_voltage)
        m = []
        for i in range(len(updated_voltage)):
            m.append(-updated_voltage[i])
        self.mpl.canvas.bx.plot(updated_voltage,  'b')
        peakkind  =  signal.find_peaks_cwt(m, np.arange(1,2500))
        for i in peakkind:
            self.mpl.canvas.bx.annotate('local',  xy=(i,  m[i]), \
            arrowprops = dict(facecolor = 'black', shrink = 0.1))
        # reset the X limits
#        self.mpl.canvas.bx.set_xlim(xmin=-0.25, xmax=len(l)-0.75)
        # set the X ticks & tickslabel as the letters
  #      self.mpl.canvas.bx.set_xticks(range(len(l)))
    #    self.mpl.canvas.bx.set_xticklabels(l)
        # enable grid only on the Y axis
        self.mpl.canvas.bx.get_yaxis().grid(True)        
        self.mpl.canvas.bx.get_xaxis().grid(True)   
        # force an image redraw
        self.mpl.canvas.draw()
        # create the GUI application 
        # instantiate the main window
   #     dmw = DesignerMainWindow()
        # show it 
  #      dmw.show() 
        # start the Qt main loop execution, exiting from this script
        # with the same return code of Qt application


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dmw = DesignerMainWindow()
    dmw.show()
    sys.exit(app.exec_())
