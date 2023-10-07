#include <iostream>
using namespace std;

int Abs(int);

int main(){
	for (int i=0; i<8; ++i){
		for (int k=0; k<i;++k){
			cout<<" ";
		}
		for (int j=1; j<9-i;++j){
			cout<<j;
		}
		cout<<endl;
	}
	cout<<endl;
	for (int i=0; i<8; ++i){
		for (int j=1; j<9-i;++j){
			cout<<9-j-i;
		}
		for (int k=0; k<i;++k){
			cout<<" ";
		}
		cout<<endl;
	}
	cout<<endl;
	for (int i=1; i<9; ++i){
		for (int k=0;k<9-i;++k){
			cout<<" ";
		}
		for (int j=0; j<i;++j){
			cout<<i-j;
		}
		cout<<endl;
	}
	cout<<endl;
	int l=1;
	for (int i=1; i<9; ++i){
		for (int k=0;k<9-i;++k){
			cout<<" ";
		}
		for (int j=0; j<l+2; ++j){
			if(i-j!=0 && i-j!=-1) cout<<Abs(i-j);
		}
		l+=2;
		cout<<endl;
	}
}

int Abs(int sz){
	if (sz<0) return sz-2*sz;
	else return sz;
}