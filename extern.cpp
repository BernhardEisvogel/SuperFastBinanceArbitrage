#include <iostream>
#include <math.h>
#include <random>

const bool debug = false;

extern "C" void version(){
    std::cout << "You are using version 0.1" << std::endl;
}

const long arrayPosition(int i, int j, int edgeLength){
    return i*edgeLength + j;
}
    
extern "C" int* function(int n, double* data){
    // Data has to have size n*2
    
    const int startingPoint = 0;
    int* visited = (int*) malloc(sizeof(int) * (long)(n+1));
    double distance[n];
    double predecessor[n];
    
    memset( distance, INFINITY, (long)n*sizeof(double));
    memset( predecessor,     0, (long)n*sizeof(double));
    for(int z = 0; z<n+1;z++){
        visited[z] = -1;
    }


    if (visited == NULL){
        std::cout << "Memory could not be allocated" << std::endl;
        return NULL;
    }
    
    distance[startingPoint] = 0;
    for (int i = 0; i < n; i++){
        for (int k = 0; k < n; k++){
            if (distance[k] < INFINITY) {
                for (int s = 0; s < n; s++){
                    const double newdistance = distance[k] + data[arrayPosition(k, s, n)];
                    
                    if (distance[s] > newdistance && distance[s] < INFINITY){
                        predecessor[s] = k;
                        distance[s] = newdistance;
                    }
                }
            }
        }
    }
    
    for (int u = 0; u < n; u++){
        for (int v = 0; v < n; v++){
            if (distance[u] + data[arrayPosition(u, v, n)] < distance[v]){
                predecessor[v] = u;
                visited[v] = u;
                while(visited[u] < 0 ){
                    visited[u] = predecessor[u];
                    u = predecessor[u];
                }
                visited[n] = predecessor[u];
                return visited;
                
            }
        }
    }
    if(debug){
        printf("C allocated address %p \n", visited);
    }

    return visited;
}

extern "C" const void free_mem(double *a){
    if(debug){
        printf("freeing address: %p\n", a);
    }
    free(a);
}

const void test1(){
    // This function is for testing the BellmannFordAlgorithm
    int n = 850;
    double test[n*n];
    double lower_bound = -0.05;
    double upper_bound = 12;
    
    std::uniform_real_distribution<double > unif(lower_bound,upper_bound);
    std::default_random_engine re;
    
    for(int i = 0; i< n*n; i++){
        test[i] = unif(re);
    }
    
    // This part does the calculation
    int* result = function(n, test);
    
    // The following part visualises the resutl
    for(int i=0; i<n+1; i++) {
        std::cout << std::to_string(i) <<"\t"<<result[i] << "\t|"<<std::endl;
      }
    std::cout << std::endl;
}

const void test2(){
    
    int n = 50;
    double test[n*n];
    for(int i = 0; i< n*n; i++){
        test[i] = 1;
    }
    test[arrayPosition(3,7,n)] = -1;
    test[arrayPosition(7,9,n)] = -1;
    test[arrayPosition(9,44,n)] = -1;
    test[arrayPosition(44,40,n)] = -1;
    test[arrayPosition(40,3,n)] = -1;
    
    int* result = function(n, test);
    
    // The following part visualises the resutl
    for(int i=0; i<n+1; i++) {
        std::cout << std::to_string(i) <<"\t"<<result[i] << "\t|"<<std::endl;
      }
    std::cout << std::endl;
}

int main()
{
    test2();
    return 0;
}
