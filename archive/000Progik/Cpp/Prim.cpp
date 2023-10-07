#include <iostream>
#include "math.h"
using namespace std;

bool szamszoveg(string);
bool szame(char);
long long int convert(string,int,long long int);

int main()
{
	bool ujra = false, osszetett;
	char uj;
	long long int med, pr = 0, ossz = 0;
	double arany;
	long long int szam;
		cout << "Prímműveletek. ";
		ELEJE:
		cout<<"\nMit szeretnél csinálni? \n\t1. Megadott x szám prím-e\n\t2. Prímek kiíratása x-ig\n\t3. Prímtényezős felbontás\nMelyiket szeretnéd indítani? (1/2/3): ";
		int mi;
		cin >> mi;
		switch (mi)
		{
		case 1:
			{
				cout << "\nVissza a menühöz: írj bármit ami nem szám.";
				string inp;
				long long int sz;
				do {
				cout<<"\nÍrj be egy számot: ";
				osszetett = false;
				cin >> inp;
				if (!szamszoveg(inp)) goto ELEJE;
				else sz = convert(inp, inp.length(), 1);
				for (int p = 2; p <= sqrt(sz); ++p)
				{
					if (sz % p == 0)
					{
						cout << "\nÖsszetett szám! " << p << "-el osztható. (" << p << "*" << sz
							/ p << ")\n";
						osszetett = true;
						break;
					}
				}
				if (!osszetett)
					cout << "\nPrím!\n";
				
				} while (1);
				break;
			}

		case 2:
			{
				pr = 0;
				string inp;
				cout << "\nVissza a menühöz: írj bármit ami nem szám.";
				do {
				cout << "\nMeddig akarod kiiratni a primeket? : ";
				cin >> inp;
				if (!szamszoveg(inp)) goto ELEJE;
				else med = convert(inp, inp.length(), 1);
				for (int i = 2; i < med; ++i)
				{
					osszetett = false;
					for (int p = 2; p <= sqrt(i); ++p)
					{
						if (i % p == 0)
						{
							osszetett = true;
							break;
						}
					}
					if (!osszetett)
					{
						cout << i << " ";
						++pr;
					}
				}
				cout << "\n\nÖsszesen " << pr << " db prímet találtam " << med <<
					"-ig, a prímek aránya " << (double)pr / (double)med *100 << "%\n";
				} while (1);
				break;
			}
			case 3:{
				cout << "\nVissza a menühöz: írj bármit ami nem szám.";
				string inp;
				do{
				cout<<"\nÍrd ide a számot: ";
				cin >> inp;
				if (!szamszoveg(inp)) goto ELEJE;
				else szam = convert(inp, inp.length(), 1);
				cout<<endl;
				while (szam!=1){
					osszetett = false;
					for (int p = 2; p <= sqrt(szam); ++p)
					{
						if (szam % p == 0)
						{
							osszetett = true;
							cout<<szam<<" | "<<p<<"\n";
							szam /=p;
							break;
						}
					}
					if (!osszetett)
					{
						cout<<szam<<" | "<<szam<<"\n";
						szam =1;
					}
				}
				cout <<"1\n";
				}while(1);
			}
		}
}

bool szamszoveg(string s) {
	bool e;
	if (s[0]=='-'){
		e = true;
		for (int i=1;i<s.size();++i) if (!szame(s[i])) e = false;
		if (e) return true;
		else return false;
	}
	else {
		e = true;
		for (int i=0;i<s.size();++i) if (!szame(s[i])) e = false;
		if (e) return true;
		else return false;
	}
}

bool szame(char c){
	if (c=='0'||c=='1'||c=='2'||c=='3'||c=='4'||c=='5'||c=='6'||c=='7'||c=='8'||c=='9') return true;
	else return false;
}

long long int convert(string s, int l, long long int k)
{
	if (l>0) return convert(s, l-1, k*10)+(s[l-1]-'0')*k;
	else return 0;
}