#include <iostream>
#include <cstdlib>
#include "Table.h"
#include "Muveletek.h"

using namespace std;

int main(){
	Table t;
	Muveletek muv;
	srand(time(NULL));
	int szam, egy = 1, x, y;
	bool mehete = true;
	cout << "\nEz egy amoba jatek, a felso tabla mutatja a megtett lepeseket,\naz also pedig mutatja a helyeket. Jo szorakozast!\n\n";
	while (1) {
		mehete = true;
		if (egy > 1) {
			cout << string(100, '\n');
		}
		egy++;
		
		t.vektprint();
		cout << "\n1 2 3\n4 5 6\n7 8 9\n\n";
		cout << "Hova teszel? irj be egy szamot (1-9)! : ";
		cin >> szam;
		y = muv.convert_y(szam);
		x = muv.convert_x(szam);
		
		if (szam == 666) {
			cout << "DIE MADAFAKA DIEEEEEE YOU SATANIST!!!!!!!!!!!\n";
			return 0;
		}
		else if (t.table[y][x]!='.') {
			cout << "Mit kepzelsz magadrol?? ENTER de gyorsan!";
			cin.ignore(1);
			cin.get();
			mehete = false;
		}
		else if (szam > 0 && szam < 10)
			t.putX(szam);
		else {
			cout << "Rossz parancs! Nyomj ENTER-t!";
			cin.ignore(1);
			cin.get();
			mehete = false;
		}
		
		if (mehete) {
			cout << string(100, '\n');
			t.vektprint();
			muv.firstcheck();
			if (t.ret) {
				return 0;
			}
			
			muv.ellsor('O','X');
			muv.elloszlop('O','X');
			muv.ellatl('O','X');
				
			muv.ellsor('X','O');
			muv.elloszlop('X','O');
			muv.ellatl('X','O');
			
			cout << "\nRemek! Nyomj egy ENTERt es a GEP LEP.";
			cin.ignore(1);
			cin.get();
				
			if(){
				int ran_plc = rand()%9+1;
				y=muv.convert_y(ran_plc);
				x=muv.convert_x(ran_plc);
				if (t.table[y][x]!='X'&&t.table[y][x]!='O') {
					t.table[y][x] = 'O';
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
