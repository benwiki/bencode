#include <fstream>
using namespace std;

int main(){
	ifstream inf;
	ofstream outf;
	inf.open("words.txt");
	outf.open("testwords.txt");
	string copy="";
	getline(inf, copy);
	while (copy != ""){
		outf << copy << "\n";
		getline(inf, copy);
		outf << copy << " ";
		getline(inf, copy);
		outf << copy <<"\n";
		getline(inf, copy);
		outf << copy << " ";
		getline(inf, copy);
		outf << copy<<"\n";
		getline(inf, copy);
	}
}