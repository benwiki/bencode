#include <iostream>
using namespace std;

int main(){
	int tomb[37][28][2];
	int ossz=0;
	for (int i=0; i<37; i+=1)
		for (int j=0; j<28; ++j){
		tomb[i][j][0]=1+i*28+j;
		tomb[i][j][1]=1+j*37+i;}
	for (int i=0; i<37; ++i)
		for (int j=0; j<28; ++j)
		if (tomb[i][j][0]==tomb[i][j][1]) cout<<i<<" "<<j<<" "<<tomb[i][j][0]<<endl;
}