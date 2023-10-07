#include <iostream>
#include <string>

using namespace std;

int main(){
	int db;
	cin>>db;
	string sor;
	cin>>sor;
	if (db==0||db>10000) return 0;
	int doboz[db];
	for (int i=0; i<db; ++i){
		if (sor[i]=='A') doboz[i]=3;
		else if (sor[i]=='B') doboz[i]=2;
		else doboz[i]=1;
	}
	int cdob[db];
	for (int i=0; i<db; ++i) cdob[i]=doboz[i];
	int lepes=0;
	for (int i=0; i<db-1; ++i)
		for (int j=i+1; j<db; ++j)
			if (doboz[i]<doboz[j] && cdob[i]< doboz[j] && doboz[i]!=0 && doboz[j]!=0){
				/*for (int n=0; n<db; ++n) cout<<doboz[n];
				cout<<" "<<cdob[i]<<endl;
				for (int n=0; n<db; ++n){
					if (n==i) cout<<"*";
					else cout<<" ";
				}
				cout<<endl;*/
				doboz[j]=doboz[i];
				doboz[i]=0;
				++lepes;
				break;
			}
	cout<<db-lepes<<endl;
}