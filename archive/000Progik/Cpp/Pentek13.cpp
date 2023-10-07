#include <iostream>
using namespace std;

int main(){
	string napok[7] = {"het", "ked", "sze", "csu", "pen", "szo", "vas"};
	int datum[3];
	string nap;
	cout << "Datumot kerek! Szokozokkel elvalasztva ev-ho-nap, aztan a nap neve: ";
	for (int i=0; i<7; ++i) cout<<napok[i]<<"/";
	cout<<endl;
	for (int i=0; i<3; ++i) cin>>datum[i];
	cin>>nap;
	int ind=0;
	for (int i=0; i<7; ++i){
		if (nap==napok[i]) ind=i+1;
	}
	for (int i=0; i<(datum[0]%4==0 &&datum[0]%100!=0) || datum[0]%400==0 ? 366 : 365; ++i) {
		if (ind%7==2&&
	}
	
}