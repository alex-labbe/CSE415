"""binary_perceptron.py
One of the starter files for use in CSE 415, Autumn 2023
Assignment 6.
Complete this python file.

This program can be run from the given Python program
called run_2_class_2_feature_iris_data.py.
"""


def student_name():
    return "Alexandre Labbe"  # Replace with your own name here


class BinaryPerceptron:
    """
    Class representing the Binary Perceptron
    ---
    It is an algorithm that can learn a binary classifier
    """
    
    def __init__(self, weights=None, alpha=2):
        """
        Initialize the Binary Perceptron
        ---
        weights: Weight vector of the form [w_0, w_1, ..., w_{n-1}, bias_weight]
        alpha: Learning rate
        """
        if weights is None:
            self.weights = [0, 0, 0]
        else:
            self.weights = weights[:]
        self.alpha = alpha
        self.k = 1
    
    def classify(self, x_vector):
        """
        Method that classifies a given data point into one of 2 classes
        ---
        Inputs:
        x_vector = [x_0, x_1, ..., x_{n-1}]
        Note: y (correct class) is not part of the x_vector.

        Returns:
        y_hat: Predicted class
              +1 if the current weights classify x_vector as positive i.e. the required dot product must be >=0,
        else  -1 if it is classified as negative.
        """
        # ADD YOUR CODE HERE
        t = x_vector[:] # create a copy of the x_vector
        if len(t) != len(self.weights): # if there is a bias
            t.append(1)                 # add value 1 because the associated value when evaluating bias is always 1
        dot_product = sum(x*y for x, y in zip(t, self.weights)) # calculate dot product
        return 1 if dot_product >= 0 else -1

    
    def train_with_one_example(self, x_vector, y):
        """
        Method that updates the model weights using a particular training example (x_vector,y)
        and returns whether the model weights were actually changed or not
        ---
        Inputs:
        x_vector: Feature vector, same as method classify
        y: Actual class of x_vector
            +1 if x_vector represents a positive example,
        and -1 if it represents a negative example.
        Returns:
        weight_changed: True if there was a change in the weights
                        else False
        """
        # essentially the update functio

        ## check for incorrect classification
        """
        t = self.classify(x_vector)
        if t != y:
            self.k += 1
            # update weights
            s = 1 if y == 1 else -1
            bias = self.weights[-1]
            x_copy = x_vector[:]
            x_copy.append(1)
            saX = [x*self.alpha*s/self.k for x in x_copy]
            self.weights = [x+y for x, y in zip(saX, self.weights[:])]
            weight_updates = [self.alpha/self.k * x * s for x in self.weights[:-1]]
            self.weights = [x-y for x, y in zip(self.weights[:-1], weight_updates)]
            self.weights.append(bias - self.alpha/self.k * s)
            return True
        return False"""
        guess = self.classify(x_vector)
        if guess != y:
            old_bias = self.weights[-1]
            self.weights = [x + ((self.alpha/self.k)*v*y) for x,v in zip(self.weights[:-1], x_vector)]
            self.weights.append(old_bias + self.alpha/self.k*y)
            print(self.weights)
            self.k += 1
            return True
        return False

    

    
    def train_for_an_epoch(self, training_data):
        """
        Method that goes through the given training examples once, in the order supplied,
        passing each one to train_with_one_example.
        ---
        Input:
        training_data: Input training data
        [[x_vector_1, y_1], [x_vector_2, y_2], ...]
        where each x_vector is concatenated with the corresponding y value.

        Returns:
        changed_count: Return the number of weight updates.
        (If zero, then training has converged.)
        """

        """
        changed_count = 0
        for data in training_data:
            x_vector = data[:-1]  # all elements except the last one
            y = data[-1]          # the last element is the class label
            if self.train_with_one_example(x_vector, y):
                changed_count += 1
        return changed_count
        """
        changed_count = 0
        for data in training_data:
            x_vector, y = data[:-1], data[-1]
            changed = self.train_with_one_example(x_vector, y)
            if changed: changed_count += 1
        return changed_count



def sample_test():
    """
    May be useful while developing code
    Trains the binary perceptron using a synthetic training set
    Prints the weights obtained after training
    """


    
    """DATA = [
        [-2, 7, +1],
        [1, 10, +1],
        [3, 2, -1],
        [5, -2, -1]]
    bp = BinaryPerceptron()
    print("Training Binary Perceptron for 3 epochs.")
    for i in range(3):
        bp.train_for_an_epoch(DATA)
    print("Binary Perceptron weights:")
    print(bp.weights)
    print("Done.")"""

    bp = BinaryPerceptron()
    bp.weights = [-1, -1, 1]
    bp.train_with_one_example([3, 11], 1)
    bp.train_with_one_example([2, 8], -1)



    






if __name__ == '__main__':
    sample_test()
