#include "Muveletek.h"

int Muveletek::convert0(int a)
{
  int b=0; // inicializalas szukseges. pl: int b=0;
  if (a<4) b = 0;
  else if (a >=3 && a <7) b = 1; // HIBA! szam nincs deklaralva
  else if (a >=7 && a <10) b = 2; // HIBA! szam nincs deklaralva
  return b; //HIBA!!! b nincs inicializalva, ha nem mesz bele egyik agba sem. Azatz nem tudod hogy mi az erteke. Lehet akar teljesen rossz is. Egy visszamaradt szemet a memoriaban.
}

int Muveletek::convert1(int a)
{
  int b=0; // inicializalas szukseges. pl: int b=0;
  if (a<4) b = a-1;
  else if (a >=3 && a<7) b = a-4; // HIBA! szam nincs deklaralva
  else if (a >=7 && a<10) b = a-7; // HIBA! szam nincs deklaralva
  return b; // HIBA!!! b nincs inicializalva, ha nem mesz bele egyik agba sem. Azatz nem tudod hogy mi az erteke. Lehet akar teljesen rossz is. Egy visszamaradt szemet a memoriaban.
}

int Muveletek::firstcheck(bool ret)
{
  int k=0;
  for (int i=0; i<3; ++i) { // ++i itt ugyanazt csinalja es egy elemi muvelettel kevesebbet hajt vegre. Tehat gyorsabb egy kicsit.
    for (int j=0; j<3; ++j) { // ++j itt ugyanazt csinalja es egy elemi muvelettel kevesebbet hajt vegre. Tehat gyorsabb egy kicsit.
      if (table[i][j]=='O' || table[i][j]=='X') {
        ++k; // ++k itt ugyanazt csinalja es egy elemi muvelettel kevesebbet hajt vegre. Tehat gyorsabb egy kicsit.
      }
    }
  }
  if (k == 9) {
    std::cout << "\nDONTETLEN!\n";
    ret = true; // Ha int a visszateresi ertek akkor nem lehet true-val visszaterni
  }
  for (int i=0; i<3; ++i) { // ++i itt ugyanazt csinalja es egy elemi muvelettel kevesebbet hajt vegre. Tehat gyorsabb egy kicsit.
    if (table[i][0]=='X'&&table[i][1]=='X'&&table[i][2]=='X') {
      std::cout << "\nNYERTEL! :)\n";
      ret = true; // Ha int a visszateresi ertek akkor nem lehet true-val visszaterni
    }
  }
  for (int i=0; i<3; ++i) { // ++i itt ugyanazt csinalja es egy elemi muvelettel kevesebbet hajt vegre. Tehat gyorsabb egy kicsit.
    if (table[0][i]=='X'&&table[1][i]=='X'&&table[2][i]=='X') {
      std::cout << "\nNYERTEL! :)\n";
      ret = true; // Ha int a visszateresi ertek akkor nem lehet true-val visszaterni
    }
  }
  if ((tabtable[0][0]=='X' && table[1][1]=='X' && table[2][2]=='X') ||
      (table[0][2]=='X' && table[1][1]=='X' && table[2][0]=='X')) {
    std::cout << "\nNYERTEL! :)\n";
    ret = true; // Ha int a visszateresi ertek akkor nem lehet true-val visszaterni
  }
}

int Muveletek::ellsor(char betu)
{
	int egyket, harom;
	if(betu == 'O') {
    egyket='O';
    harom='X';
}
  else {
    egyket='X';
    harom='O';
}
  for (int i=0; i<3; ++i) {
    if (kif && table[i][0]==egyket && table[i][1]==egyket && table[i][2]!=harom){
      return 'O';
    }
    else if (kif && table[i][0]==egyket && table[i][2]==egyket && table[i][1]!=harom){
      return 'O';
    }
    else if (kif && table[i][1]==egyket && table[i][2]==egyket && table[i][0]!=harom){
      return 'O';
    }
    // Mi tortenik ha nem mgy bele egyik agba sem. Szerintem igy le se fordul.
}

int Muveletek::elloszlop(char table[3][3], char egyket, char harom)
{
  for (int i=0; i<3; i++) {
    if (kif && table[0][i]==egyket && table[1][i]==egyket && table[2][i]!=harom){
      return 'O';
    }
    else if (kif && table[0][i]==egyket && table[2][i]==egyket && table[1][i]!=harom){
      return 'O';
    }
    else if (kif && table[1][i]==egyket && table[2][i]==egyket && table[0][i]!=harom){
      return 'O';
    }
  }
  // Mi tortenik ha nem mgy bele egyik agba sem. Szerintem igy le se fordul.
}

int Muveletek::ellatl(char table[3][3], char egyket, char harom)
{
  if (kif && table[0][0]==egyket && table[1][1]==egyket && table[2][2]!=harom){
    return 'O';
  }
  else if (kif && table[0][0]==egyket && table[2][2]==egyket && table[1][1]!=harom){
    return 'O';
  }
  else if (kif && table[1][1]==egyket && table[2][2]==egyket && table[0][0]!=harom){
    return 'O';
  }
  else if (kif && table[2][0]==egyket && table[1][1]==egyket && table[0][2]!=harom){
    return 'O';
  }
  else if (kif && table[2][0]==egyket && table[0][2]==egyket && table[1][1]!=harom){
    return 'O';
  }
  else if (kif && table[0][2]==egyket && table[1][1]==egyket && table[2][0]!=harom){
    return 'O';
  }
  // Mi tortenik ha nem mgy bele egyik agba sem. Szerintem igy le se fordul.
}
