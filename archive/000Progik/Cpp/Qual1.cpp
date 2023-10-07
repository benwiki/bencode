#include <iostream>
using namespace std;

int dmg(string);
void swap (char*, char*);

int main(){
	string attack;
	cin >> attack;
	int al = attack.length();
	int dmg1, dmg2;
	int crit=10, hack=0;
	for (int i=0; i<al*al; ++i){
		for (int k=0; k<al-1; ++k){
			dmg1=dmg(attack);
			if (dmg1<=crit){
				if (i==0) cout << attack<<"\n"<<0;
				else cout << attack<<"\n"<<hack;
				return 0;
			}
			swap(&attack[k], &attack[k+1]);
			dmg2=dmg(attack);
			if (dmg2<dmg1){
				++hack;
				break;
			}
			else {
				swap(&attack[k], &attack[k+1]);
			}
		}
	}
	if (dmg(attack)>crit) cout<<"IMPOSSIBLE";
	else cout << 0;
}

int dmg(string att){
	int pow=1;
	int total=0;
	int atlen=att.length();
	for (int i=0; i<atlen; ++i){
		if (att[i] == 's' || att[i] =='S') total += pow;
		else pow *=2;
	}
	return total;
}

void swap (char *c1, char *c2){
	char c3;
	c3 = *c1;
	*c1=*c2;
	*c2=c3;
}