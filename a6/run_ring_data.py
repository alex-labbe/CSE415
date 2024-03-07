from binary_perceptron import BinaryPerceptron # Your implementation of binary perceptron
from plot_bp import PlotBinaryPerceptron
import csv  # For loading data.
from matplotlib import pyplot as plt  # For creating plots.
import remapper as remap

class PlotRingBP(PlotBinaryPerceptron):

    def __init__(self, bp, plot_all=True, n_epochs=20, is_remap=False):
        super().__init__(bp, plot_all, n_epochs)
        self.is_remap = is_remap

    def read_data(self):
        data_as_strings = list(csv.reader(open('ring-data.csv'), delimiter=','))
        self.TRAINING_DATA = [[float(f1), float(f2), int(c)] for [f1, f2, c] in data_as_strings]
        if self.is_remap:
            data = []
            for row in self.TRAINING_DATA:
                x, y = remap.remap(row[0], row[1])
                data.append([x, y, row[2]])
            self.TRAINING_DATA = data

    def plot(self):
        plt.legend(loc='best')
        plt.show()

if __name__=='__main__':
    binary_perceptron = BinaryPerceptron(alpha=0.5)
    pbp = PlotRingBP(binary_perceptron, plot_all=True, n_epochs=25, is_remap=True)
    pbp.train()
    pbp.test()
    pbp.plot()
