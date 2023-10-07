#include <iostream>
using namespace std;

void feltolt(int** , int );

int main(){
	int tomb[5][2];
	int *pt;
	pt=tomb[0];
	
	//for (int i=0; i<5; ++i) pt[i] = tomb[i];
	for (int i=0; i<5; ++i){
		tomb[i][0]=0;
		tomb[i][1]=0;
	}
	tomb[2][1]=69;
	cout<<&tomb[2][1]<<endl;
	cout<<*(pt+5)
	//feltolt(pt, 5);
	/*for (int i=0;i<5;++i){
		for (int k=0; k<2; ++k){
			cout <<&tomb[i][k]<<endl;
		}
	}*/
}

void feltolt(int **array, int n){
	for (int i=0; i<n; ++i){
		array[i][0]=1;
		array[i][1]=2;
	}
}