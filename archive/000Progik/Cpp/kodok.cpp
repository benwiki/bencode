#include <iostream>
using namespace std;

void iswap( int &, int & );
void cswap( char &, char & );

int main(){
	int db;
	cin>>db;
	string *kodok;
	kodok = new string[db];
	for (int i=0; i<db; ++i)
		cin>>kodok[i];
	int ln=kodok[0].length();
	int **kodsz;
	kodsz = new int*[db];
	for (int i=0; i<ln; ++i) 
		kodsz[i] = new int[ln];
		
	for (int i=0; i<db; ++i)
		for (int j=0; j<ln; ++j)
			kodsz[i][j]=(int)kodok[i][j];
	int n,m;
	for (int i=0; i<db; ++i){
		n=m=-1;
		for (int j=ln-2; j>=0; --j)
			if (kodsz[i][j]<kodsz[i][j+1]){
				n=j;
				break;
			}
		if (n==-1) {
			cout<<"NINCS\n";
			break;
		}
		for (int j=ln-1; j>=0; --j)
			if (kodsz[i][j]>kodsz[i][n]){
				m=j;
				break;
			}
		
		iswap(kodsz[i][n],kodsz[i][m]);
		cswap(kodok[i][n],kodok[i][m]);
		
		int resz = ln-n-1;
		int hind;
		if (resz%2==0)
			for (int k=n+1; k<n+1+resz/2; ++k){
				hind=ln-1-(k-(n+1));
				iswap(kodsz[i][k],kodsz[i][hind]);
				cswap(kodok[i][k],kodok[i][hind]);
			}
		else 
			for (int k=n+1; k<n+1+(resz-1)/2; ++k){
				hind=ln-1-(k-(n+1));
				iswap(kodsz[i][k],kodsz[i][hind]);
				cswap(kodok[i][k],kodok[i][hind]);
			}
		cout<<kodok[i]<<"\n";
		delete[] kodsz[i];
	}
	delete[] kodok;
}

void iswap(int &x, int &y){
	int z;
	z=x; x=y; y=z;
}

void cswap(char &x, char &y){
	char z;
	z=x; x=y; y=z;
}