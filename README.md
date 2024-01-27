# SuperFastBinanceArbitrage
Algorithm to find arbitrage opportunities on Binance. Uses an in C++ implemented Bellman Ford Algorithm and a python wrapper to improve speed. My my goal on this project was to learn how to include C++ files for python.

# How to use it

Run compileAndTest.sh to see if the C++ library (g++) compiled correctly, insert your credentials in CONFIG.py and then start binanceArbitrageFinder.py. Up until now (not very surprisingly), the program has not found any arbitrage opportunities.

# Improvements

- The algorithm in the C++ file can be improved e.g. with the improvement proposed by Yen in 1970
- The data handling between the C++ and python part can be optimised

Seen that I have reached my goal and learned how to add super fast C++ routines tp Python programs, I will solve those problems in a future semester break.
