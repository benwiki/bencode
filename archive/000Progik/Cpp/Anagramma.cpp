#include <iostream>
using namespace std;

int fakt(long sz);

int main(){
	/*string nev;
	cout<<"Ird be a neved nagybetukkel: ";
	cin>>nev;
	bool cuc=false;
	char nev2[nev.length()];
	for (int i=0; i<fakt(nev.length()); ++i){
		
	}
	for (int i=0; i<nev.length(); ++i) cout<<nev2[i];*/
	cout<<fakt(8);
	
}

int fakt(long sz){
	if (sz!=1) return sz*fakt(sz-1);
}