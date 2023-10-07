#include <iostream>
#include <cstdlib>
#include "Table.h"
#include "Muveletek.h"

using namespace std;

int main(){
	Table t;
	Muveletek muv;
	int szam, egy = 1, con0, con1;
	bool mehete = true;
	cout << "\nEz egy amoba jatek, a felso tabla mutatja a megtett lepeseket,\naz also pedig mutatja a helyeket. Jo szorakozast!\n\n";
	while (1) {
		mehete = true;
		if (egy > 1) {
			cout << string(100, '\n');
		}
		egy++;
		
		t.vektprint(t.table);
		cout << "\n1 2 3\n4 5 6\n7 8 9\n\n";
		cout << "Hova teszel? irj be egy szamot (1-9)! : ";
		cin >> szam;
		con0 = muv.convert0(szam);
		con1 = muv.convert1(szam);
		
		if (szam == 666) {
			cout << "DIE MADAFAKA DIEEEEEE YOU SATANIST!!!!!!!!!!!\n";
			return 0;
		}
		else if (t.table[con0][con1]=='O'||t.table[con0][con1]=='X') {
			cout << "Mit kepzelsz magadrol?? ENTER de gyorsan!";
			cin.ignore(1);
			cin.get();
			mehete = false;
		}
		else if (szam > 0 && szam < 10) {
			t.putX(t.table, szam);
		}
		else {
			cout << "Rossz parancs! Nyomj ENTER-t!";
			cin.ignore(1);
			cin.get();
			mehete = false;
		}
		
		if (mehete) {
			cout << string(100, '\n');
			t.vektprint(t.table);
			muv.firstcheck(t.table);
			if (t.ret) {
				return 0;
			}
			
			cout << "\nRemek! Nyomj egy ENTERt es a GEP LEP.";
			cin.ignore(1);
			cin.get();
			srand(time(NULL));
			muv.kifele = true;
			while (muv.kifele) {
				
				muv.ellsor('O');
				muv.elloszlop('O');
				muv.ellatl('O');
				
				muv.ellsor('X');
				muv.elloszlop('X');
				muv.ellatl('X');
				
				if(muv.kifele){
					int cucc = rand()%9+1;
					con0 = muv.convert0(cucc);
					con1 = muv.convert1(cucc);
					if (t.table[con0][con1]!='X'&&t.table[con0][con1]!='O') {
						t.table[con0][con1] = 'O';
						muv.kifele = false;
					}
				}
				for (int i=0; i<3; i++) {
					if(t.table[i][0]=='O'&&t.table[i][1]=='O'&&t.table[i][2]=='O'){
						cout << string(100, '\n');
						for (int i=0; i<3; i++) {
							for (int j = 0; j<3; j++) {
								cout << t.table[i][j] << " ";
							}
							cout << "\n";
						}
						cout << "\nVESZTETTEL :(\n";
						return 0;
					}
				}
				for (int i=0; i<3; i++) {
					if(t.table[0][i]=='O'&&t.table[1][i]=='O'&&t.table[2][i]=='O'){
						cout << string(100, '\n');
						for (int i=0; i<3; i++) {
							for (int j = 0; j<3; j++) {
								cout << t.table[i][j] << " ";
							}
							cout << "\n";
						}
						cout << "\nVESZTETTEL :(\n";
						return 0;
					}
				}
				if((t.table[0][0]=='O'&&t.table[1][1]=='O'&&t.table[2][2]=='O')||(t.table[0][2]=='O'&&t.table[1][1]=='O'&&t.table[2][0]=='O')){
					cout << string(100, '\n');
					for (int i=0; i<3; i++) {
						for (int j = 0; j<3; j++) {
							cout << t.table[i][j] << " ";
						}
						cout << "\n";
					}
					cout << "\nVESZTETTEL :(\n\n";
					return 0;
				}
			}
		}
	}
}
