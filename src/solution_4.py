import numpy as np


def initialize_parameters(n_in, n_out):
    """
    Helper function to initialize some form of random weights and Zero biases
    Args:
        n_in: size of input layer
        n_out: size of output/number of neurons
    Returns:
        params: a dictionary containing W and b
    """

    params = dict()  # initialize empty dictionary of neural net parameters W and b

    params['W'] = np.random.randn(n_out, n_in) *0.01  # set weights 'W' to small random gaussian
    params['b'] = np.zeros((n_out, 1))    # set bias 'b' to zeros

    return params

class LinearLayer:
    """
        This Class implements all functions to be executed by a linear layer
        in a computational graph
        Args:
            input_shape: input shape of Data/Activations
            n_out: number of neurons in layer
            ini_type: initialization type for weight parameters, default is "plain"
                      Opitons are: plain, xavier and he
        Methods:
            forward(A_prev)
            backward(upstream_grad)
            update_params(learning_rate)
    """

    def __init__(self, input_shape, n_out):
        """
        The constructor of the LinearLayer takes the following parameters
        Args:
            input_shape: input shape of Data/Activations
            n_out: number of neurons in layer
        """

        self.m = input_shape[1]  # number of examples in training data
        # `params` store weights and bias in a python dictionary
        self.params = initialize_parameters(input_shape[0], n_out)  # initialize weights and bias
        self.Z = np.zeros((self.params['W'].shape[0], input_shape[1]))  # create space for resultant Z output

    def forward(self, A_prev):
        """
        This function performs the forwards propagation using activations from previous layer
        Args:
            A_prev:  Activations/Input Data coming into the layer from previous layer
        """

        self.A_prev = A_prev  # store the Activations/Training Data coming in
        self.Z = np.dot(self.params['W'], self.A_prev) + self.params['b']  # compute the linear function

    def backward(self, upstream_grad):
        """
        This function performs the back propagation using upstream gradients
        Args:
            upstream_grad: gradient coming in from the upper layer to couple with local gradient
        """

        # derivative of Cost w.r.t W
        self.dW = np.dot(upstream_grad, self.A_prev.T)

        # derivative of Cost w.r.t b, sum across rows
        self.db = np.sum(upstream_grad, axis=1, keepdims=True)

        # derivative of Cost w.r.t A_prev
        self.dA_prev = np.dot(self.params['W'].T, upstream_grad)

    def update_params(self, learning_rate=0.1):
        """
        This function performs the gradient descent update
        Args:
            learning_rate: learning rate hyper-param for gradient descent, default 0.1
        """

        self.params['W'] = self.params['W'] - learning_rate * self.dW  # update weights
        self.params['b'] = self.params['b'] - learning_rate * self.db  # update bias(es)

class SigmoidLayer:
    """
    This file implements activation layers
    inline with a computational graph model
    Args:
        shape: shape of input to the layer
    Methods:
        forward(Z)
        backward(upstream_grad)
    """

    def __init__(self, shape):
        """
        The consturctor of the sigmoid/logistic activation layer takes in the following arguments
        Args:
            shape: shape of input to the layer
        """
        self.A = np.zeros(shape)  # create space for the resultant activations

    def forward(self, Z):
        """
        This function performs the forwards propagation step through the activation function
        Args:
            Z: input from previous (linear) layer
        """
        self.A = 1 / (1 + np.exp(-Z))  # compute activations

    def backward(self, upstream_grad):
        """
        This function performs the  back propagation step through the activation function
        Local gradient => derivative of sigmoid => A*(1-A)
        Args:
            upstream_grad: gradient coming into this layer from the layer above
        """
        # couple upstream gradient with local gradient, the result will be sent back to the Linear layer
        self.dZ = upstream_grad * self.A*(1-self.A)

def compute_cost(Y, Y_hat):
    """
    This function computes and returns the Cost and its derivative.
    The is function uses the Squared Error Cost function -> (1/2m)*sum(Y - Y_hat)^.2
    Args:
        Y: labels of data
        Y_hat: Predictions(activations) from a last layer, the output layer
    Returns:
        cost: The Squared Error Cost result
        dY_hat: gradient of Cost w.r.t the Y_hat
    """
    m = Y.shape[1]

    cost = (1 / (2 * m)) * np.sum(np.square(Y - Y_hat))
    cost = np.squeeze(cost)  # remove extraneous dimensions to give just a scalar

    dY_hat = -1 / m * (Y - Y_hat)  # derivative of the squared error cost function

    return cost, dY_hat


if __name__ == "__main__":

    X = np.array([
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1]
    ])

    Y = np.array([
        [0],
        [1],
        [1],
        [0]
    ])

    X_train = X.T
    Y_train = Y.T

    learning_rate = 1
    number_of_epochs = 5000

    np.random.seed(48) # set seed value so that the results are reproduceable
    # (weights will now be initailzaed to the same pseudo-random numbers, each time)


    # Our network architecture has the shape: 
    # (input)--> [Linear->Sigmoid] -> [Linear->Sigmoid]->[Linear->Sigmoid] -->(output)  

    #------ LAYER-1 ----- define hidden layer that takes in training data 
    Z1 = LinearLayer(input_shape=X_train.shape, n_out=5)
    A1 = SigmoidLayer(Z1.Z.shape)

    #------ LAYER-2 ----- define output layer that take is values from hidden layer
    Z2= LinearLayer(input_shape=A1.A.shape, n_out=3)
    A2= SigmoidLayer(Z2.Z.shape)


    #------ LAYER-3 ----- define output layer that take is values from 2nd hidden layer
    Z3= LinearLayer(input_shape=A2.A.shape, n_out=1)
    A3= SigmoidLayer(Z3.Z.shape)

    costs = [] # initially empty list, this will store all the costs after a certian number of epochs

    # Start training
    for epoch in range(number_of_epochs):
    
        # ------------------------- forward-prop -------------------------
        Z1.forward(X_train)
        A1.forward(Z1.Z)
        
        Z2.forward(A1.A)
        A2.forward(Z2.Z)
        
        Z3.forward(A2.A)
        A3.forward(Z3.Z)
        
        # ---------------------- Compute Cost ----------------------------
        cost, dA3 = compute_cost(Y=Y_train, Y_hat=A3.A)
        
        # print and store Costs every 100 iterations.
        if (epoch % 100) == 0:
            print("Cost at epoch#{}: {}".format(epoch, cost))
            costs.append(cost)
        
        # ------------------------- back-prop ----------------------------
        A3.backward(dA3)
        Z3.backward(A3.dZ)
        
        A2.backward(Z3.dA_prev)
        Z2.backward(A2.dZ)
        
        A1.backward(Z2.dA_prev)
        Z1.backward(A1.dZ)
        
        # ----------------------- Update weights and bias ----------------
        Z3.update_params(learning_rate=learning_rate)
        Z2.update_params(learning_rate=learning_rate)
        Z1.update_params(learning_rate=learning_rate)