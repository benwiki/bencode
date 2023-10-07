#include <iostream>
#include <fstream>
#include <math.h>
using namespace std;

int main(){
	int sorok=0;
	string helyes, sor;
	ifstream valaszok;
	valaszok.open("valaszok.txt");
	getline(valaszok, helyes);
	while (1){
		sor="";
		getline(valaszok, sor);
		if (sor=="") break;
		++sorok;
	}
	valaszok.close();
	valaszok.open("valaszok.txt");
	
	struct Tarol {
		string azon;
		string valasz;
		int pszam=0;
	};
	
	Tarol *emb;
	emb = new Tarol[sorok];
	getline(valaszok, helyes);
	int i=0, j;
	while (1){
		sor = "";
		j=0;
		getline(valaszok, sor);
		if (sor=="") break;
		while (sor[j]!=' '){
			emb[i].azon += sor[j];
			++j;
		}
		++j;
		for (int k=j; k<14+j; ++k)
			emb[i].valasz += sor[k];
		++i;
	}
	//----------------------------------
	cout<<"2. Feladat:\nA versenyen "<<sorok<<" szemely vett reszt.";
	//----------------------------------
	cout<<"\n\n3. Feladat:\nKerem egy versenyzo azonositojat: ";
	string vzo;
	cin >>vzo;
	cout<<"A versenyzo valaszai: ";
	int ind=0;
	for (int i=0; i<sorok; ++i)
		if (emb[i].azon==vzo){
			cout<<emb[i].valasz;
			ind = i;
			break;
		}
	cout<<endl;
	//----------------------------------
	cout<<endl<<"4. Feladat:"<<endl;
	cout<<helyes<<endl;
	for (i=0; i<14; ++i){
		if (helyes[i]==emb[ind].valasz[i])
			cout<<"+";
		else cout<<" ";
	}
	//----------------------------------
	cout<<"\n\n5. Feladat:\nAdjon meg egy feladatszamot: ";
	int fszam, osszpont=0;
	cin >> fszam;
	for (i=0;i<sorok; ++i)
		if (emb[i].valasz[fszam-1]== helyes[fszam-1])
			++osszpont;
	float szazalek = (float)osszpont/ (float)sorok*100;
	float kerszaz =(szazalek>=0. ? floor(szazalek*100.)/100. : ceil(szazalek*100.)/100.);
	cout<<"A feladatra "<<osszpont<<" fo,  a versenyzok "<<kerszaz<<"%-a adott\n helyes valaszt.";
	//----------------------------------
	for (i=0; i<sorok; ++i)
		for (j=0; j<14; ++j){
			if (j<5&&emb[i].valasz[j] == helyes[j]) emb[i].pszam+=3;
			else if (j<10&&emb[i].valasz[j] == helyes[j]) emb[i].pszam+=4;
			else if (j<13&&emb[i].valasz[j] == helyes[j]) emb[i].pszam+=5;
			else if (j==13&&emb[i].valasz[j] == helyes[j]) emb[i].pszam+=6;
		}
	ofstream outf;
	outf.open("pontok.txt");
	for (i=0; i<sorok; ++i)
		outf << emb[i].azon<<" "<<emb[i].pszam<<"\n";
	outf.close();
	//----------------------------------
	cout<<"\n\n7. Feladat: A verseny legjobbjai:\n";
	int elso, masodik, harmadik;
	elso=masodik=harmadik=0;
	for (i=0; i<sorok;++i)
		if (emb[i].pszam>elso)
			elso = emb[i].pszam;
	for (i=0; i<sorok;++i)
		if (emb[i].pszam>masodik && emb[i].pszam<elso)
			masodik = emb[i].pszam;
	for (i=0; i<sorok;++i)
		if (emb[i].pszam>harmadik && emb[i].pszam<masodik)
			harmadik = emb[i].pszam;
	for (i=0; i<sorok;++i)
		if (emb[i].pszam==elso)
			cout<<"1. dij ("<<elso<<" pont): "<< emb[i].azon<<endl;
	for (i=0; i<sorok;++i)
		if (emb[i].pszam==masodik)
			cout<<"2. dij ("<<masodik<<" pont): "<< emb[i].azon<<endl;
	for (i=0; i<sorok;++i)
		if (emb[i].pszam==harmadik)
			cout<<"3. dij ("<<harmadik<<" pont): "<< emb[i].azon<<endl;
}