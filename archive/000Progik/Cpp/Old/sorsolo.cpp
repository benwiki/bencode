#include <iostream>
#include <cstdlib>
#include <time.h>
#include <algorithm>
#include <vector>
using namespace std;
int myr(int i){return rand()%i;}
int main(){
	string nevek[10];
	int jegyzes[10];
	for(int i=0;i<10;++i) jegyzes[i]=0;
	srand(unsigned(time(0)));
	nevek[0]="detektív";
	nevek[1]=nevek[2]="gyilkos";
	for(int i=3;i<10;++i) nevek[i]="ártatlan";
	int r=0;
	for(int i=0;i<10;++i){
		r=rand()%10;
		while(jegyzes[r]){
			r= rand()%10;
			cout<<r<<endl;
		}
		jegyzes[r]=1;
		cout<<"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n";
		cout<<"Nyomj ENTERT!";
		cin.get();	cout<<"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n";
		cout<<nevek[r];
		cin.get();
	}
	cout<<"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n";
	cout<<"\n\n\n\n\n\n\n\n\n\n\n\n\n///////////////////////\nVÉGE\n///////////////////////";
	
}