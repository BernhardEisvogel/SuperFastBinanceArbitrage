import ctypes
from ctypes import *
import numpy as np
import math
from error import BellmanFordError

class BellmanFordFast():
    """
    Python Wrapper for the fast Bellman Ford implementation in C++

    This version assumes that every point is reachable from every point.
    Please do not use array sizes bigger then around 500, otherwise the data types in the C++ file have to be adjusted.
    """

    # make sure Python knows what to expect from C++
    mydll = CDLL("extern.so")
    mydll.function.restype = POINTER(c_int)
    mydll.function.argtypes = [c_int, POINTER(c_double)]
    mydll.free_mem.restype = None
    mydll.free_mem.argtypes = [POINTER(c_int)]

    def __init__(self, data, n = -1):
        if n != -1:
            assert type(n) == int
            assert len(data) == n * n
            self.n = n
        else:
            self.n = int(math.sqrt(len(data)))
            if self.n**2 != len(data):
                raise BellmanFordError("Data Error", True)

        if self.n > 859:
            raise BellmanFordError("Please use a smaller n", True)

        self.__data = data

        tracers = c_int(self.n)
        R_c = data.ctypes.data_as(POINTER(c_double))

        # The following variable need to be freed, because it is outside the scope of python
        self.solutionPointer =  self.mydll.function(tracers, R_c)

        # THe 'function' function contains the Belman Ford algorithm
        resultCpp = np.array(np.fromiter(self.solutionPointer, dtype=np.int32, count=self.n+1))
        self.solution = resultCpp[:-1]
        self.startingpoint = resultCpp[-1]
        if self.startingpoint == -1:
            raise BellmanFordError("No Solution has been found")

        
    def getSolution(self):
        return self.solution
        
    def data(self, i, j):
        assert j*self.n + i < len(self.__data)
        return self.__data[j * self.n + i]
        
    def getStartValue(self):
        # get a startingValue
        return self.startingpoint

    def __del__(self):
        # Free the return memory from the c function
        self.mydll.free_mem(self.solutionPointer)

    def visSolution(self, f = lambda startNode, endNode, weight: "Weight of " + str(startNode) + " to " + str(endNode) + "\t =" + str(weight)):
        """

        :param f: a function accepting startnode, endNode, weigth and returning a string.
        Will be displayed after every iteration.

        :return: List with the points visited
        """
        p = list()
        startwert = self.getStartValue()
        count = startwert
        print("Starting Point", count)
        a = self.data(count, self.solution[count])
        p.append(startwert)
        print(f(self.solution[count],count, self.data(count, self.solution[count])))
        p.append(self.solution[count])
        count = self.solution[count]

        while(True):
            # just walk the ring and output something at every step
            a = a + self.data(count, self.solution[count])
            print(f(self.solution[count], count, self.data(count, self.solution[count])))
            p.append(self.solution[count])
            count = self.solution[count]
            if count == startwert:
                break
        print("Gain: ", a)
        return p

def test1():
    n = 50
    data = np.ones((n, n), dtype=np.float64)
    data[3, 7] = -1
    data[7, 9] = -1
    data[9, 12] = -1
    data[12, 3] = -1
    # The program doesnt find the "shortest" way, but it does find a negative way
    # This should be sufficient for our probkem as we don't expect a lot of arbitrage opportunities to exist
    data = data.flatten()
    bf = BellmanFordFast(data)
    print(bf.visSolution())

def test2():
    n = 600
    data = np.random.uniform(low=-0.2, high=12.0, size=n * n)

    for i in range(n):
        data[n * i + i] = 10
    bf = BellmanFordFast(data)
    print(bf.visSolution())

if __name__ == '__main__':
    print("Testing the Bellman Ford Algorithm \n(that runs with python/C++ for maximum speed!!! )")
    test1()
    print("It seems like the test has been passed")

