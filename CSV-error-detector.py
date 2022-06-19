# pip install pyside6
# pip install langdetect

import sys
import random
import numpy
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
import pandas as pd
import langdetect
from langdetect import detect


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("CSV Visualizer")        
        
        self.tableWidget = QTableWidget()
        
        self.tableWidgetPixel = QTableWidget()
        
        splitter = QSplitter()
        splitter.addWidget(self.tableWidget)
        splitter.addWidget(self.tableWidgetPixel)
        self.setCentralWidget(splitter)

        self.createDockWindow()
        
        self.df = pd.DataFrame()

    def createDockWindow(self):
        #options and instructions dock
        self.dockOptions = QDockWidget("Options", self)
        self.dockOptions.setAllowedAreas(Qt.AllDockWidgetAreas)
        self.dockOptions.DockWidgetFeatures()
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dockOptions)
        self.dockedWidget = QWidget(self)
        
        #Legend dock
        self.dockLegend = QDockWidget("Legend", self)
        self.dockLegend.setAllowedAreas(Qt.AllDockWidgetAreas)
        self.dockLegend.DockWidgetFeatures()
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dockLegend)
        self.dockedWidgetLegend = QWidget(self)
        
        #Statistics dock
        self.dockStats = QDockWidget("CSV Summary", self)
        self.dockStats.setAllowedAreas(Qt.AllDockWidgetAreas)
        self.dockStats.DockWidgetFeatures()
        self.addDockWidget(Qt.RightDockWidgetArea, self.dockStats)
        self.dockedWidgetStats = QWidget(self)
        
        self.dockedWidget.setLayout(QVBoxLayout())
        self.dockedWidget.setMinimumSize(QSize(300,100))
        self.dockOptions.setWidget(self.dockedWidget)
        
        self.dockedWidgetLegend.setLayout(QVBoxLayout())
        self.dockedWidgetLegend.setMinimumSize(QSize(300,100))
        self.dockLegend.setWidget(self.dockedWidgetLegend)
        
        self.dockedWidgetStats.setLayout(QVBoxLayout())
        self.dockedWidgetStats.setMinimumSize(QSize(150,100))
        self.dockStats.setWidget(self.dockedWidgetStats)
        
        #GUI components
        self.btnLoadCSV = QPushButton("LOAD CSV")
        self.label_1 = QLabel("1. LOAD YOUR FILE")
        self.label_1.setStyleSheet("font-weight: bold")
        self.label_2 = QLabel("2. CHOOSE THE ERRORS")
        self.label_2.setStyleSheet("font-weight: bold")
        self.label_3 = QLabel("3. FIND THE ERRORS")
        self.label_3.setStyleSheet("font-weight: bold")
        self.checkbox_missing = QCheckBox("MISSING VALUES")
        self.checkbox_special = QCheckBox("SPECIAL CHARACTERS")
        self.checkbox_negatives = QCheckBox("NEGATIVE VALUES")
        self.visualizerBtn = QPushButton("VISUALIZE!")
        self.label_5 = QLabel(" * NO ERROR = COLOR: GREEN")
        self.label_5.setStyleSheet("color: green;font-weight: bold") 
        self.label_6 = QLabel(" * ERROR: MISSING VALUE, COLOR: BLUE")
        self.label_6.setStyleSheet("color: blue;font-weight: bold") 
        self.label_7 = QLabel(" * ERROR: SPECIAL CHARACTERS, COLOR: ORANGE")
        self.label_7.setStyleSheet("color: darkorange;font-weight: bold") 
        self.label_11 = QLabel(" * ERROR: NEGATIVE VALUES, COLOR: BLACK")
        self.label_11.setStyleSheet("color: black;font-weight: bold") 
        self.label_4 = QLabel("4. SAVE THE FILE")
        self.label_4.setStyleSheet("font-weight: bold")
        self.save = QPushButton("SAVE")
        
        # Add widgets to layout
        self.dockedWidget.layout().addWidget(self.label_1)
        self.dockedWidget.layout().addWidget(self.btnLoadCSV)
        self.dockedWidget.layout().addWidget(self.label_2)
        self.dockedWidget.layout().addWidget(self.checkbox_missing)
        self.dockedWidget.layout().addWidget(self.checkbox_special)
        self.dockedWidget.layout().addWidget(self.checkbox_negatives)
        self.dockedWidget.layout().addWidget(self.label_3)
        self.dockedWidget.layout().addWidget(self.visualizerBtn)
        self.dockedWidgetLegend.layout().addWidget(self.label_5)
        self.dockedWidgetLegend.layout().addWidget(self.label_6)
        self.dockedWidgetLegend.layout().addWidget(self.label_7)
        self.dockedWidgetLegend.layout().addWidget(self.label_11)
        self.dockedWidget.layout().addWidget(self.label_4)
        self.dockedWidget.layout().addWidget(self.save)
        
        #Push everything up
        self.spacer = QSpacerItem(10, 10, QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.dockedWidget.layout().addItem(self.spacer)
        
        # Connect signals
        self.btnLoadCSV.clicked.connect(self.LoadCSV)
        self.checkbox_missing.clicked.connect(self.missing)
        self.checkbox_special.clicked.connect(self.special)
        self.checkbox_negatives.clicked.connect(self.negatives)
        self.visualizerBtn.clicked.connect(self.visualizer)
        self.save.clicked.connect(self.saver)
        
        # Connect pixeltable to main table
        self.tableWidget.cellChanged.connect(self.cell_changed)
        self.tableWidgetPixel.cellPressed.connect(self.clickedOnPixelView)
        
    # Asks user to choose a file and loads it
    def LoadCSV(self):
        self.path = QFileDialog.getOpenFileName(self, 'Open CSV', "/home", 'CSV(*.csv)')[0] 
        missing_values = ["n/a", "na", "--", "-", "NaN", "NA", "/"]
        self.df = pd.read_csv(self.path, na_values = missing_values)
        self.tableWidget.setRowCount(len(self.df))
        self.tableWidget.setColumnCount(len(self.df.columns))
        self.tableWidget.setHorizontalHeaderLabels(self.df.columns)
        
        self.tableWidget.blockSignals(True)
        
        for i in range(len(self.df)):
            for j in range(len(self.df.columns)):
                    # Set text of table item
                item = QTableWidgetItem()
                item.setText(str(self.df.iloc[i,j]))
                self.tableWidget.setItem(i,j, item)
                
        self.tableWidget.blockSignals(False)       
        
        # Initialize the pixel view (e.g., a table view with small cells)
        
        self.tableWidgetPixel.setRowCount(len(self.df))
        self.tableWidgetPixel.setColumnCount(len(self.df.columns))        

        # Set column width and row width fixed
        self.tableWidgetPixel.horizontalHeader().hide()
        self.tableWidgetPixel.verticalHeader().hide()
        
        self.tableWidgetPixel.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.tableWidgetPixel.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)

        PIXEL_SIZE = 7

        self.tableWidgetPixel.horizontalHeader().setMinimumSectionSize(PIXEL_SIZE)
        self.tableWidgetPixel.horizontalHeader().setMaximumSectionSize(PIXEL_SIZE)
        self.tableWidgetPixel.horizontalHeader().setDefaultSectionSize(PIXEL_SIZE)
        
        self.tableWidgetPixel.verticalHeader().setMinimumSectionSize(PIXEL_SIZE)
        self.tableWidgetPixel.verticalHeader().setMaximumSectionSize(PIXEL_SIZE)
        self.tableWidgetPixel.verticalHeader().setDefaultSectionSize(PIXEL_SIZE)

        
        for i in range(len(self.df)):
            for j in range(len(self.df.columns)):
                item = QTableWidgetItem()
                self.tableWidgetPixel.setItem(i,j, item)
        
        
        # CSV summary stats
        C =self.tableWidget.columnCount()
        R =self.tableWidget.rowCount()
        self.label_8 = QLabel("NUMBER OF COLUMNS: "+ str(C))
        self.label_8.setStyleSheet("font-weight: bold") 
        self.label_9 = QLabel("NUMBER OF ROWS: "+ str(R))
        self.label_9.setStyleSheet("font-weight: bold") 
        self.dockedWidgetStats.layout().addWidget(self.label_8)
        self.dockedWidgetStats.layout().addWidget(self.label_9)
        
        self.spacer_dock = QSpacerItem(10, 10, QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.dockedWidgetStats.layout().addItem(self.spacer_dock)
        
    # finds missing values and colors them blue in the tableWidget
    def missing(self):
        self.tableWidget.blockSignals(True)
        print("Checkbox is checked:", self.checkbox_missing.isChecked())
        
        
        if self.checkbox_missing.isChecked():
    
    
            global current_missing 
            current_missing = self.df.isnull()
            
            for x in range(len(current_missing)):
                for z in range(len(current_missing.columns)):
                    
                    item_1 = self.tableWidget.item(x,z)
                    item_2 = self.tableWidgetPixel.item(x,z)
                    
                    if current_missing.iloc[x,z] == True:
                        item_1.setBackground(QColor("blue"))
                        item_2.setBackground(QColor("blue"))
                        
                    else:
                        item_1.setBackground(QColor("green"))
                        item_2.setBackground(QColor("green"))           


        else:  # Check box is not checked (set all to white)
            for i in range(len(self.df)):
                for j in range(len(self.df.columns)):
                    item = self.tableWidget.item(i,j) #Get the item at (row,column)
                    item.setBackground(QColor("white")) #set the background to white
                    
                    ## also do this for the pixel view
                    item = self.tableWidgetPixel.item(i,j)
                    item.setBackground(QColor("white"))
                    
        self.tableWidget.blockSignals(False)  
        

        
    def special(self):
        self.tableWidget.blockSignals(True)
        print("Checkbox is checked:", self.checkbox_special.isChecked())
        
        if self.checkbox_special.isChecked():
            for a in range(len(self.df)):
                for b in range(len(self.df.columns)):
                    
                    item_1 = self.tableWidget.item(a,b)
                    item_2 = self.tableWidgetPixel.item(a,b)
                    i_loc = self.df.iloc[a,b]
                    try:
                        self.langs = detect(i_loc)
                        print(str(self.langs))
                        for k in self.langs:
                            if k == 'en':
                                item_1.setBackground(QColor("green"))
                                item_2.setBackground(QColor("green"))

                            else:
                                item_1.setBackground(QColor("orange"))
                                item_2.setBackground(QColor("orange"))

                    except Exception:
                        continue

        else:  # Check box is not checked (set all to white)
            for i in range(len(self.df)):
                for j in range(len(self.df.columns)):
                    item = self.tableWidget.item(i,j) #Get the item at (row,column)
                    item.setBackground(QColor("white")) #set the background to white

                                ## also do this for the pixel view
                    item = self.tableWidgetPixel.item(i,j)
                    item.setBackground(QColor("white"))
                    
        self.tableWidget.blockSignals(False)  


    def negatives(self):
        self.tableWidget.blockSignals(True)
        print("Checkbox is checked:", self.checkbox_negatives.isChecked())
        
        
        if self.checkbox_negatives.isChecked():
            
            for d in range(len(self.df)):
                for f in range(len(self.df.columns)):
                    
                    item_1 = self.tableWidget.item(d,f)
                    item_2 = self.tableWidgetPixel.item(d,f)
                    
                    try:
                        if int(self.df.iloc[d,f]) < 0:
                            item_1.setBackground(QColor("black"))
                            item_1.setForeground(QColor("yellow"))
                            item_2.setBackground(QColor("black"))

                        else:
                            item_1.setBackground(QColor("green"))
                            item_2.setBackground(QColor("green"))
                        
                    except ValueError as err:
                        pass    


        else:  # Check box is not checked (set all to white)
            for i in range(len(self.df)):
                for j in range(len(self.df.columns)):
                    item = self.tableWidget.item(i,j) #Get the item at (row,column)
                    item.setBackground(QColor("white")) #set the background to white
                    
                    ## also do this for the pixel view
                    item = self.tableWidgetPixel.item(i,j)
                    item.setBackground(QColor("white"))
                    
        self.tableWidget.blockSignals(False)  
           
    def visualizer(self): 
        # Execute the functions for which the checkbox is checked
        
        print("Checkbox missing", self.checkbox_missing.isChecked())
        print("Checkbox special characters", self.checkbox_special.isChecked())
        print("Checkbox negatives", self.checkbox_negatives.isChecked())
        
        if self.checkbox_missing.isChecked():
            self.missing()
            m = current_missing.sum().sum()
            print(m)
            self.label_10 = QLabel("NUMBER OF MISSING VALUES: "+ str(m))
            self.label_10.setStyleSheet("font-weight: bold") 
            self.dockedWidgetStats.layout().addWidget(self.label_10)

            self.spacer_dock = QSpacerItem(10, 10, QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
            self.dockedWidgetStats.layout().addItem(self.spacer_dock)
            
        if self.checkbox_special.isChecked():
            self.special()
            
            #self.label_12 = QLabel("NUMBER OF SPECIAL CHARACTERS: "+ str(g))
            #self.label_12.setStyleSheet("font-weight: bold") 
            #self.dockedWidgetStats.layout().addWidget(self.label_12)

            #self.spacer_dock = QSpacerItem(10, 10, QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
            #self.dockedWidgetStats.layout().addItem(self.spacer_dock)
            
        if self.checkbox_negatives.isChecked():
            self.negatives()
            
            
    def cell_changed(self, row, column):
        print("Edited cell ", row, column, "to text", self.tableWidget.item(row,column).text())
       
        # Update the dataframe
        self.df.iloc[row, column] = self.tableWidget.item(row,column).text()

        # Update colors
        self.visualizer()
        
    
    def clickedOnPixelView(self, row, column):
        print("Clicked on ", row, column, "in pixelview")
        
        item = self.tableWidget.item(row,column)
        
        # Scroll to the item and select it
        self.tableWidget.scrollToItem(item)
        self.tableWidget.setCurrentItem(item)
        
    def saver(self):
        head = []
        for k in range (self.tableWidget.model().columnCount()):
            head.append(self.tableWidget.horizontalHeaderItem(k).text())
            
        file = pd.DataFrame(columns = head)
        
        for row in range(self.tableWidget.rowCount()):
            for col in range(self.tableWidget.columnCount()):
                file.at[row, head[col]] = self.tableWidget.item(row, col).text()
        
        exported = file.to_csv('./corrected_csv.csv', index = False)
        print("CSV file exported")
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.showMaximized()
    sys.exit(app.exec())
