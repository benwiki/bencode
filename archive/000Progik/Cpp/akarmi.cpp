#include <iostream>
using namespace std;

int sz(long);

int main(){
	int x;
	while (1) {
		cin>>x;
		cout<<sz(x)<<endl;
	}
}

int sz(long cuc){
	if (cuc!=1) return cuc*sz(cuc-1);
}