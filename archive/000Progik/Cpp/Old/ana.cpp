#include <iostream>
using namespace std;

string Ana(string, int);

int main(){
	Ana("BENKE", 0);
}

string Ana(string nev, int e){
	for (int i=e; i<nev.length(); ++i){
		if (e!=nev.length()) cout<<nev[i]+Ana(nev,e+1);
	}
}