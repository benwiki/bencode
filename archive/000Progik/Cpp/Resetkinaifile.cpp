#include <fstream>
using namespace std;

int main(){
	ofstream file;
	file.open("kszavak.txt", ofstream::out | ofstream::trunc);
	file.close();
}