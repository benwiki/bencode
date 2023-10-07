#include <iostream>
using namespace std;

int Abs(int);

int main(){
	int x;
	while (1){
		cin>>x;
    	cout<<Abs(x)<<endl;
	}
}

int Abs(int sz){
	if (sz<0) return sz-2*sz;
	else return sz;
}