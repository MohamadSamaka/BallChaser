
from matplotlib import gridspec
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.gridspec import GridSpec
import numpy as np

MaxNumberOfRows = 11
MaxNumOfSmallerGridUnitsSize = 3
GeneralSizeOfGridUniHight = 4
SizeOfSmallerGridUnitsHight = 1.5
WidthRatioOfGridUnits = [15.4,10]

def FixHightOfGrideCells():
    for i in range(MaxNumOfSmallerGridUnitsSize):
        DashBoard.HightOfGridCells[i] = SizeOfSmallerGridUnitsHight

class DashBoard:
    # SizeOfMainFigureWidth = 25.4
    # SizeOfMainFigureHeight = 36.5
    SizeOfMainFigureWidth = 0
    SizeOfMainFigureHeight = 0
    HightOfGridCells = [GeneralSizeOfGridUniHight]*MaxNumberOfRows #makes an array that has the height of each row
    DataSetSize = 8
    def __init__(self, data):
        FixHightOfGrideCells()
        self.__SetWidthAndHeightOfMainFigureValue()
        self.Data = data
        self.ColumnsLabels = ("PlayerName" ," Id", "FOV", "Height", "Pitch", "Distance", "Stiffness", "Swivel speed", "Transition speed", "Sens")
        self.MainFigure = plt.figure(constrained_layout=True,figsize=(DashBoard.SizeOfMainFigureWidth,DashBoard.SizeOfMainFigureHeight)) #i will try to make the figsize tuple later
        self.Space = gridspec.GridSpec(ncols=2, nrows=11, figure=self.MainFigure, height_ratios = DashBoard.HightOfGridCells, width_ratios = WidthRatioOfGridUnits)
        self.avgData = self.CalculateAVGData()
        self.Median = self.CalculateMedian()
        self.BuildTables()
        self.BuildBars()


    def __SetWidthAndHeightOfMainFigureValue(self):
        DashBoard.SizeOfMainFigureWidth = 25.4
        DashBoard.SizeOfMainFigureHeight = sum(DashBoard.HightOfGridCells)

    
    def CalculateAVGData(self):
        result = []
        DataContainer = [] #sorts each kind if data in one list for example stiffness data gonna be in one list
        for i in range(DashBoard.DataSetSize):
            temp = []
            for data in self.Data:
                temp.append(data[2:][i])
            DataContainer.append(temp)   
        for DataList in DataContainer:
            result.append(float("{:.2f}".format(np.average(DataList)))) #taking 2 digits after the decimal point
        return [result]


    def CalculateMedian(self):
        result = []
        DataContainer = [] #sorts each kind if data in one list for example stiffness data gonna be in one list
        for i in range(DashBoard.DataSetSize):
            temp = []
            for data in self.Data:
                temp.append(data[2:][i])
            temp.sort()
            DataContainer.append(temp)   
        for DataList in DataContainer:
            result.append(float("{:.2f}".format(np.median(DataList)))) #taking 2 digits after the decimal point
            # result.append(np.median(DataList)) #taking 2 digits after the decimal point
        return [result]


    def CalculateAVGDataForAll(self, index):
        Result = {}
        for data in self.Data:
                if data[2:][index] in Result:
                    Result[data[2:][index]] += 1
                else:
                    Result[data[2:][index]] = 1
        
        return [list(Result.keys()), list(Result.values())] #it MUST return a list not a tuble


    def BuildTables(self):
        self.PlayerStatsTable()
        self.avgStatsTable()
        self.MedianTable()


    def BuildBars(self):
        for i in range(0, DashBoard.DataSetSize):
            self.BarhGenerator(i, self.ColumnsLabels[2:][i], i + 3)
    

    def PlayerStatsTable(self):
        fig = self.MainFigure.add_subplot(self.Space[:,0])
        Tab = fig.table(
                cellText=self.Data,
                colLabels=self.ColumnsLabels ,
                # colWidths = [0.07] * 10,
                colColours=["palegreen"] * 10,
                cellLoc='center',
                loc='upper left',
        )
        fig.set_title("Players Stats")
        fig.set_axis_off()
        Tab.auto_set_font_size(False)
        Tab.auto_set_column_width(True)
        Tab.set_fontsize(9)


    def avgStatsTable(self):
        fig = self.MainFigure.add_subplot(self.Space[0,1])
        Tab = fig.table(
                cellText=self.avgData,
                colLabels=self.ColumnsLabels[2:],
                # colWidths = [0.07] * 10,
                colColours=["palegreen"] * 10,
                cellLoc='center',
                loc='best',
        )
        fig.set_title("AVG Stats")
        fig.set_axis_off()
        Tab.auto_set_font_size(False)
        Tab.auto_set_column_width(True)
        Tab.set_fontsize(9)

    
    def MedianTable(self):
        fig = self.MainFigure.add_subplot(self.Space[2,1])
        Tab = fig.table(
                cellText=self.Median,
                # colWidths = [0.07] * 10,
                cellLoc='center',
                loc='best',
        )
        fig.set_title("Median")
        fig.set_axis_off()
        Tab.auto_set_font_size(False)
        Tab.auto_set_column_width(True)
        Tab.set_fontsize(9)


    def BarhGenerator(self, index, title, position):
        DistanceData = self.CalculateAVGDataForAll(index)
        DistanceData[0] = [str(data) for data in DistanceData[0]]
        bar = self.MainFigure.add_subplot(self.Space[position,1])
        bar.barh(DistanceData[0], DistanceData[1])
        bar.set_title(title)
        for i in range(len(DistanceData[1])):
            bar.annotate(str(DistanceData[1][i]), xy=(DistanceData[1][i],i))


    def GetMainFigure(self):
        return self.MainFigure
