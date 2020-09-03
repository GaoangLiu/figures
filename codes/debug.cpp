#include <iostream>
#include <vector>
#include <map>

int main() {
    int j = 0; 
    std::vector<int> vv(3, 0);
    vv[0] = 192929;
    std::map<int, int> cc; 
    for(int i = 0; i < 10; i++) {
        std::cout << i * 3 << std::endl; 
        j = i & 1 ? i + 1: i* 3; 
        vv[i % 3] = j;
        cc[i] = j; 
    }
    return 0; 
}
