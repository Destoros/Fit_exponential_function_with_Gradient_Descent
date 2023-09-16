import numpy as np
from typing import Callable

"""
This function can fit an exponential function in form of 
  f = lambda a,b,c,tau: a - b*np.exp(-(x - c)/tau)
where a,b,c,tau are parameters which will be determined from the fitting function. 
Note: This fitter can only determine the coefficients for functions of this type!

Inside the main() function below is an exemplary call
"""

class FitExponentialFunction:

    coefficients: np.ndarray #array containing the coefficients

    def __init__(self, x: np. ndarray, d: np.ndarray, gamma: float = 0.5, initial_values: np.ndarray = np.ones((4,1)),
                 iter_max: int = 1000 , fix_initial_values: np.ndarray = np.array([False, False, False, False])) -> None:   
        """
        t: time, for entry in t a corresponding value in d has to exist.
        d: measurements, data for which an exponential will be fitted.
        gamma: learning rate of the Gradient Descent algorithm.
        initial_values: init values for the Gradient Descent algorithm.
        iter_max: maximum amount of iterations inside the Gradient Descent algorithm.
        fix_initial_values: array of boolean, if true, the parameter at this place will not be changed during optimization
        """

        #ensure that inital values has the correct shape and number of elements
        initial_values.reshape(-1,1)

        if len(initial_values) != 4:
            raise ValueError(f"The algorithm requires 4 initial values but {len(initial_values)} were provided.")
        
        #set initial values
        self.initial_values = initial_values

        #set learning rate
        self.gamma = gamma

        #set maximum iteration number
        self.iter_max = iter_max

        #define each component for the gradient of the function f
        df_da   = lambda a,b,c,tau: np.sum(-2*(-a + b*np.exp(-(x - c)/tau) + d))/(np.sum( (-a + b*np.exp(-(x - c)/tau) + d)**2 ) + 10)
        df_db   = lambda a,b,c,tau: np.sum(2*np.exp(-(x - c)/tau)*(np.exp(-(x - c)/tau)*b + d - a))/(np.sum((np.exp(-(x - c)/tau)*b + d - a)**2) + 10)
        df_dc   = lambda a,b,c,tau: np.sum(2*b*np.exp(-(x - c)/tau)*(b*np.exp(-(x - c)/tau) + d - a))/(tau*(np.sum((b*np.exp(-(x - c)/tau) + d - a)**2) + 10))
        df_dTau = lambda a,b,c,tau: np.sum(2*b*(x - c)*np.exp(-(x - c)/tau)*(b*np.exp(-(x - c)/tau) + d - a))/( tau**2*(np.sum((b*np.exp(-(x - c)/tau) + d - a)**2) + 10) )

   
        #concatenate the components for the gradient and set certain entries to 0 depending on fix_initial_values
        self.grad_L = lambda a,b,c,tau: np.array([df_da(a,b,c,tau), df_db(a,b,c,tau), df_dc(a,b,c,tau), df_dTau(a,b,c,tau)]).reshape(-1,1) * np.invert(fix_initial_values).reshape(-1,1)


    def fit_exponential(self) -> np.ndarray:
        """
        Fit an exponential in the form of f(a,b,c,tau) = a - b*exp(-(t - c)/tau) to 
        the provided data d at the timestamps t
        """

        u = self.initial_values
        gamma = self.gamma
        iter_max = self.iter_max


        #start the gradient descent search
        for i in range(1, self.iter_max+1):
            u -= self.gamma*self.grad_L(*u.flatten())   

            #reduce the learning rate for the last 10% of iterations
            if i/iter_max > 0.90:
                gamma *= 0.95

            percent_finished = (i*100//iter_max)
            percentile_prints = 2
            if  percent_finished % percentile_prints == 0:
                #print every 10% an update
                
                print(f"\r[{percent_finished//percentile_prints*'='}{(100//percentile_prints - percent_finished//percentile_prints)*' '}]{i*100//iter_max:2}%",end="")

        print("   Done!")#print a newline character

        self.coefficients = u

        return self.coefficients
    
    def get_coefficients(self) -> np.ndarray:
        if not hasattr(self, "coefficients"):
            print("ERROR: Run fit_exponential() before getting the coefficients.")
        return self.coefficients
        
    def get_fitted_function(self) -> Callable:
        "Returns a lambda function which takes the x as input returns the y value"
        if not hasattr(self, "coefficients"):
            print("ERROR: Run fit_exponential() before getting the fitted function.")

        (a,b,c,tau) = self.coefficients #unpack the coefficients
        f = lambda x:  a - b*np.exp(-(x - c)/tau)
        return f


    def print_coefficients(self) -> None:
        if not hasattr(self, "coefficients"):
            print("ERROR: Run fit_exponential() before printing the coefficients.")

        print(f"  a = {self.coefficients[0][0]:.2f}")
        print(f"  b = {self.coefficients[1][0]:.2f}")
        print(f"  c = {self.coefficients[2][0]:.2f}")
        print(f"tau = {self.coefficients[3][0]:.2f}")

        return f"a = {self.coefficients[0][0]:.2f}\nb = {self.coefficients[1][0]:.2f}\nc = {self.coefficients[2][0]:.2f}\ntau = {self.coefficients[3][0]:.2f}"
                  


def main():
    #exemplary call

    from fit_exponential_function import FitExponentialFunction
    import numpy as np
    import matplotlib.pylab as plt

    #CREATE DATA
    #create a time vector with step size 1
    t = np.arange(-20,100, 2)

    #create an exponential function in the form of a - b*exp(-(t - c)/tau)
    d = 40 - 0.3*np.exp(-(t-3)/10) + 0.03*np.random.randn(np.size(t))

    
    #EXECUTE ALGORITHM
    #define some plausible init values (determine this from the plot of the data d)
    init_values = np.array([40,10,10,20], dtype=np.float64).reshape(-1,1)

    #for best performance, fix the parameter a, since it has a huge impact
    fix_init_values = [True, False, False, False]

    #define the class, providing the time, measurements, step size, initial values, max iteration amount an which parameters of the inital values should stay fixed
    fitter = FitExponentialFunction(t, d, gamma=0.1, initial_values=init_values, iter_max=10000, fix_initial_values=fix_init_values)

    #fit the exponential, may take some time
    fitter.fit_exponential()

    #get the fitted exponential in form of a lambda function
    f = fitter.get_fitted_function()

    #print the coefficients
    fitter.print_coefficients()

    #or get them in form of an array
    u = fitter.get_coefficients()

    #PLOT EVERYTHING
    plt.plot(t,d, 'x', label="Measurements")
    plt.grid()
    plt.plot(t,f(t), label="Estimated function")
    plt.legend()
    plt.xlabel("x")
    plt.title("Measurements and fitted exponential function in the form of \nf(x) = a - b*exp(-(t - c)/tau)")
    plt.ylabel("f(x)")

    plt.show()

if __name__ == "__main__":
    main()

        

            

