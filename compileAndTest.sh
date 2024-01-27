g++ -c -fPIC extern.cpp -o extern.o
g++ -shared -o extern.so extern.o 
python3 BellmanFordFast.py