#include <iostream>
using namespace std;

void csa();
int szamol(int);

int main(){
	csa();
	int x;
	cin >> x;
	cout<<szamol(x);
}

void csa(){
	cout << "Csá!";
}

int szamol(int szam){
	return szam-5;
}