#include <iostream>
#include <random>
#include <string>
#include <fstream>

void GenRandomSeq(const std::string& path) {
    std::mt19937 generator(std::random_device{}());
    int min = 0;
    int max = 1;
    std::uniform_int_distribution<int> distribution(min, max);
    std::string seq;
    for (int i = 0; i < 128; ++i) {
        seq+= std::to_string(distribution(generator));
    }
    std::ofstream file(path);
	file << seq;
}

int main(){
    GenRandomSeq("Random_sequence_cpp.txt");
}