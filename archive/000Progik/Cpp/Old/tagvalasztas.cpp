#include <iostream>
#include <cstdlib>
#include <time.h>
#include <algorithm>
#include <vector>
using namespace std;
int myr(int i){return rand()%i;}
int main(){
	string nevek[]={"bence1", "bence2","benke","iván","örs","maxi","koppány","levi","dénes","balázs"};
	int jegyzes[10];
	for(int i=0;i<10;++i) jegyzes[i]=0;
	srand(unsigned(time(0)));
	int r=0;
	for(int i=0;i<10;++i){
		r=rand()%10;
		while(jegyzes[r]){
			r= rand()%10;
		}
		if(i==5) cout<<"*************\n";
		jegyzes[r]=1;
		cout<<nevek[r]<<endl;
	}
}