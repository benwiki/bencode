#include <iostream>
using namespace std;

int fakt(int);
void kiir(int, int);
void swapchar(char*, char*);
void swapint(int*, int*);

int main(){
	string szo;
	int jo=0;
	bool fasz= true;
	int wl;
	cin >> wl;
//	cout << endl;
//	int wl = szo.length();
	int word[wl];
	for (int i=0; i<wl; ++i) word[i]=i;
	int n, m;
	//cout<<szo<<endl;
	for (int i=0; i<fakt(wl); ++i){
		fasz=true;
		for (int j=0; j<wl; ++j)
			if (j!=0 && j!=wl-1 && word[j]<word[j-1] && word[j]<word[j+1]) fasz=false;
		if (fasz) ++jo;
		n = -1;
		for (int j=wl-2; j>=0; --j){
			if (word[j]<word[j+1]){
				n = j;
				break;
			}
		}
		
		if (n==-1){
			//cout<<endl<<"Kesz.";
			cout<<jo;
			return 0;
		}
		//else if (n==0) cout<<"~~~~~~~~\n";
		
		for (int j=wl-1; j>=0; --j){
			if (word[j]>word[n]){
				m = j;
				break;
			}
		}
		
		swapint(&word[n], &word[m]);
	//	swapchar(&szo[n], &szo[m]);
		
		int resz = wl-n-1;
		int hind;
		if (resz%2==0){
			for (int k=n+1; k<n+1+resz/2; ++k){
				hind=wl-1-(k-(n+1));
				swapint(&word[k], &word[hind]);
			//	swapchar(&szo[k], &szo[hind]);
			}
		}
		else {
			for (int k=n+1; k<n+1+(resz-1)/2; ++k){
				hind=wl-1-(k-(n+1));
				swapint(&word[k], &word[hind]);
			//	swapchar(&szo[k], &szo[hind]);
			}
		}
		//cout << szo;
		//cout <<endl;
	}
}

int fakt(int szam){
	if (szam!=1) return szam*fakt(szam-1);
	else return 1;
}

void swapchar (char *c1, char *c2){
	char c3;
	c3 = *c1;
	*c1=*c2;
	*c2=c3;
}

void swapint (int *i1, int *i2){
	int i3;
	i3 = *i1;
	*i1=*i2;
	*i2=i3;
}