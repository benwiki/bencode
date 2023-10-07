#include <iostream>
#include <fstream>
#include <string>
using namespace std;

void felbont(string, int**, char*, int);
long long int convert(string, int, long long int);
bool ellszin(char, char);

int main(){
    ifstream utca;
    utca.open("kerites.txt");
    string be, tarol="";
    int sorok=0;
    
    while (1){
        be = "";
        getline(utca, be);
        if (be=="") break;
        tarol += (be + ",");
        ++sorok;
    }
    
    int oldker[sorok][2];
    char all[sorok];
    
    int *okp[sorok];
    char *ap;
    for(int i=0; i<sorok; ++i) okp[i] = oldker[i];
    ap = all;
    
    felbont(tarol, okp, ap, sorok);
    
    cout<<"2. Feladat:\nAz eladott telkek szama: "<<sorok<<endl<<endl;
    
    int utolsooldal=oldker[sorok-1][0];
    int hszam = ((utolsooldal==0) ? 0 : -1);
    for (int i=0; i<sorok; ++i)
    	if (oldker[i][0]==utolsooldal)
    		hszam+=2;
    cout<<"3. Feladat:\nA "<<((utolsooldal==0)?"paros":"paratlan")<<" oldalon adtak el az utolso hazat.\nA hazszama: "<<hszam;
    
    string ptlanszinek="";
    int van=0;
    for (int i=0;i<sorok;++i)
    	if (oldker[i][0]==1)
    		ptlanszinek+=all[i];
    for (int i=0;i<ptlanszinek.length()-1;++i){
    	if (ptlanszinek[i]==ptlanszinek[i+1]&& ellszin(ptlanszinek[i], ptlanszinek[i+1])){
    		van=1+(i*2);
    		break;
    	}
    }
    if (van!=0)
    	cout<<"\n\n4.Feladat: \nSzomszedossal egyezik a kerites szine: "<<van;
    
    int hazbe;
    cout<<"Adjon meg egy házszámot: ";
    cin >> hazbe;
    string posszinek="";
    for (int i=0;i<sorok;++i)
    	if (oldker[i][0]==0)
    		posszinek+=all[i];
    
}

void felbont(string s, int **tomb, char *kar, int n){
    int j=0;
    string numstr="";
    for (int i=0; i<n; ++i){
    	numstr="";
        tomb[i][0] = s[j]-'0';
        j += 2;
        while(s[j] != ' '){
            numstr += s[j];
            ++j;
        }
        tomb[i][1] = convert(numstr, numstr.length(), 1);
        ++j;
        kar[i] = s[j];
        j +=3;
    }
}

long long int convert(string s, int l, long long int k){
	if (l>0) return convert(s, l-1, k*10)+(s[l-1]-'0')*k;
	else return 0;
}

bool ellszin(char e, char k){
	if (e!=':'&&e!='#'&&k!=':'&&k!='#')
		return true;
	else return false;
}