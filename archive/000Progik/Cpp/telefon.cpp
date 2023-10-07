#include <iostream>
#include <fstream>
using namespace std;

int mpbe(int, int, int);
long long int convert(string,int,int);

int main(){
	ifstream hivas;
	hivas.open("hivas.txt");
	string sor;
	int sorok=0;
	while (1){
		sor="";
		getline(hivas, sor);
		if (sor =="") break;
		++sorok;
	}
	hivas.close();
	hivas.open("hivas.txt");
	
	struct Tarol {
		int indit[3];
		int bef[3];
	};
	
	Tarol *emb;
	emb = new Tarol[sorok];
	int j=0;
	string idp[6];
	for (int i=0; i<sorok; ++i){
		j=0;
		for (int k=0;k<6;++k) idp[k]="";
		getline(hivas, sor);
		for (int k=0;k<5;++k){
			while (sor[j]!=' '){
				idp[k]+=sor[j];
				++j;
			}
			++j;
		}
		while (sor[j]!='\0'){
			idp[5]+=sor[j];
			++j;
		}
		cout<<idp[5].length()<<endl;
		for (int k=0;k<3;++k){
			emb[i].indit[k]=convert(idp[k], idp[k].length()-1,1);
			emb[i].bef[k]=convert(idp[k+3], idp[k+3].length()-1,1);
		}
	}
	//mmmmmmmmmmmmmmmm
	cout<<"3 Feladat:\n";
	int hivsz=0, kov;
	for (int i=0;i<sorok-1;++i){
		kov=emb[i+1].indit[0];
		++hivsz;
		if (emb[i].indit[0]!=kov){
			cout<<emb[i].indit[0]<<". ora: "<<hivsz<<endl;
			hivsz=0;
		}
	}
	//mmmmmmmmmmmmmmmm
	cout<<"\n\n4.Feladat:\nA leghosszabb ideig vonalban levo\nhivo a(z) ";
	int maxh=0,kulonbseg,ind=0;
	cout<<endl;
	for (int i=0; i<sorok; ++i){
		kulonbseg=mpbe(emb[i].bef[0], emb[i].bef[1], emb[i].bef[2])- mpbe(emb[i].indit[0], emb[i].indit[1], emb[i].indit[2]);
		cout<< emb[i].bef[2]<<endl;
		if (kulonbseg>maxh){
			maxh=kulonbseg;
			ind=i;
		}
	}
	cout<<ind<<". sorban volt es "<<maxh <<" masodpercet\nbeszelt.";
	cout<<endl<<mpbe(6, 54,58)- mpbe(6, 51, 8);
}

int mpbe(int o, int p, int mp){
	return o*3600+p*60+mp;
}

long long int convert(string s,int n, int m){
	if (n>0) return convert(s,n-1,m*10)+ (s[n]-48)*m;
	else return (s[n]-48)*m;
}