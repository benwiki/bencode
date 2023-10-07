#include <iostream>
#include <fstream>
using namespace std;

int main(){
	ifstream naplo;
	naplo.open("naplo.txt");
	int ht=0, sorok=0;
	string sor;
	while (1){
		sor = "";
		getline(naplo, sor);
		if (sor=="") break;
		++sorok;
		if (sor[0]=='#') ++ht;
	}
	naplo.close();
	naplo.open("naplo.txt");
	
	int hanynev[ht];
	int hn=-1;
	while (1){
		sor = "";
		getline(naplo, sor);
		if (sor=="") break;
		if (sor[0]!='#')
			++hanynev[hn];
		else
			++hn;
	}
	naplo.close();
	naplo.open("naplo.txt");
	
	struct Napok{
		int h;
		int n;
		string *nevek;
		string *orak;
	};
	
	Napok *nap;
	nap = new Napok[ht];
	int j=0, k=-1;
	cout<<sorok<<endl;
	cout<<ht<<endl;
	cout<<hn<<endl;
	for (int i=0; i<sorok; ++i){
		getline(naplo, sor);
		hn = hanynev[k];
		j=0;
		if (sor[j]=='#'){
			++k;
			nap[k].nevek= new string[hn];
			nap[k].orak= new string[hn];
			j+=2;
			nap[k].h+= 10*(sor[j]-48); ++j;
			nap[k].h+= (sor[j]-48); 
			j+=2;
			nap[k].n+= 10*(sor[j]-48); ++j;
			nap[k].n+= (sor[j]-48); 
		}
		else {
			string nev;
			for (int m=0; m<hn; ++m){
				do{
					nev+=sor[j];
					++j;
				} while (sor[j]!=' ');
				++j;
				do{
					nev+=sor[j];
					++j;
				}while (sor[j]!=' ');
				nap[k].nevek[m] = nev;
				++j;
				do{
					nap[k].orak[m]+=sor[j];
					++j;
				}while (sor[j]!=' ');
			}
		}
	}
	cout<<nap[2].nevek[0];
}