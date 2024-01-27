import error
from util import *
from binance.client import Client
import numpy as np
from BellmanFordFast import BellmanFordFast
from error import BellmanFordError

key, secret = CONFIG()
client = Client(key, secret)

info = client.get_exchange_info()

iToName = {-1:"None"}
NameToI = {}
N = 0

# This figures out which symbols are being traded and writes them in a dictionary

for i in range(len(info["symbols"])):
    temp = info["symbols"][i]["baseAsset"]
    if (temp not in NameToI.keys()
            and temp != "PAX"
            and temp != "DAI"
            and temp != "UST"
            and "USD" not in temp):
        iToName[N] = temp
        NameToI[temp] = N
        N = N + 1

def findOpportunities():
    currentTickers = client.get_all_tickers()
    data = np.full((N,N), np.inf)

    #TODO The following lines can still be optimized, but as those lines are
    # mostly to show the Bellman Ford Algorithm in action, it is left for a later time

    # Write the new Ticker data in the dataArray
    for i in currentTickers:
        symbol = i['symbol']
        for j in [3, 4, 5]:
            if symbol[:j] in NameToI and symbol[j:] in NameToI and i["price"] != 0:
                firstSymbol = NameToI[symbol[:j]]
                secondSymbol = NameToI[symbol[j:]]
                data[int(firstSymbol), int(secondSymbol)] = -np.log(float(i["price"]))
                # The - log is important to convert the problem from finding the max after multiplication to something
                # understandable for the bellman ford algo
                break
        continue
    data = data.flatten()
    data.astype(dtype=np.float64)
    try:
        bf = BellmanFordFast(data)
        print(bf.visSolution(
            lambda startNode, endNode, weight:
            "Weight of " + iToName[startNode] + " to " + iToName[endNode] + "\t =" + str(np.exp(-weight))))
    except BellmanFordError:
        print("No solution this time")




if __name__ == '__main__':
    while(True):
        findOpportunities()