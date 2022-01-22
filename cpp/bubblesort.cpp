#include <iostream>
#include <stdlib.h>
#include <vector>
#include <string>
#include <chrono>


int main() {
  std::vector<int> unordered_list;
  int random_int;
  std::string outputtext;
  int old_j;
  int old_j_plus_1;

  int list_length = 10000;

  // generates random list of integers
  for (int i = 0; i < list_length; i++) {
    random_int = rand() % list_length;
    unordered_list.push_back(random_int);
    outputtext = std::to_string(i) + ":" + std::to_string(unordered_list[i]);
    std::cout << outputtext << std::endl;
  }
  std::chrono::steady_clock::time_point begin = std::chrono::steady_clock::now();
  for (int i = 0; i < unordered_list.size(); i++) {
    for (int j = 0; j < unordered_list.size()-1; j++) {
      if (unordered_list[j] > unordered_list[j+1]) {
        old_j = unordered_list[j];
        old_j_plus_1 = unordered_list[j+1];
        unordered_list[j] = old_j_plus_1;
        unordered_list[j+1] = old_j;
      }
    }
  }
  std::chrono::steady_clock::time_point end = std::chrono::steady_clock::now();
  for (int i = 0; i < unordered_list.size(); i++) {
    std::cout << unordered_list[i] << std::endl;
  }
  std::cout << "Time difference = " << std::chrono::duration_cast<std::chrono::nanoseconds> (end - begin).count() << "[ns]" << std::endl;
}

