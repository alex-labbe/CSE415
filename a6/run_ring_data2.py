from binary_perceptron import BinaryPerceptron # Your implementation of binary perceptron
from plot_bp import PlotBinaryPerceptron
import csv  # For loading data.
from matplotlib import pyplot as plt  # For creating plots.
import remapper as remap

class PlotRingBP(PlotBinaryPerceptron):

    def __init__(self, bp, IS_REMAPPED=False, plot_all=True, n_epochs=20):
        super().__init__(bp, plot_all, n_epochs)
        self.IS_REMAPPED = IS_REMAPPED

    def read_data(self):
        """
        Read training data from the given dataset
        Also reads testing data if necessary
        ---
        Contains a placeholder train dataset
        """
        data_as_strings = list(csv.reader(open('ring-data.csv'), delimiter=','))
        self.TRAINING_DATA = [[float(f1), float(f2), int(c)] for [f1, f2, c] in data_as_strings]
        
        if self.IS_REMAPPED:
            MAPPED_DATA = []
            for d in self.TRAINING_DATA:
                x,y = remap.remap(d[0],d[1])
                MAPPED_DATA.append([x,y,d[2]])
            self.TRAINING_DATA = MAPPED_DATA

    def plot(self):
        #plt.title("Iris setosa (blue) vs iris versicolor (red)")
        #plt.xlabel("Sepal length")
        #plt.ylabel("Petal length")
        plt.legend(loc='best')
        plt.show()

if __name__=='__main__':
    binary_perceptron = BinaryPerceptron(alpha=0.5)
    pbp = PlotRingBP(binary_perceptron, IS_REMAPPED=True, plot_all=False,  n_epochs=1000)
    pbp.train()
    pbp.test()
    pbp.plot()