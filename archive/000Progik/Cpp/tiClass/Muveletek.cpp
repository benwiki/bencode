#include "Muveletek.h"
#include "Table.h"
#include <iostream>

int Muveletek::convert_y(int szam)
{
  int b=0;
  if (szam<4) b = 0;
  else if (szam >=3 && szam<7) b = 1;
  else if (szam >=7 && szam<10) b = 2;
  else cerr<<"Hibas szamkod!";
  return b;
}

int Muveletek::convert_x(int a)
{
  int b=0;
  if (szam>0 && szam<4) b = szam-1;
  else if (szam>3 && szam<7) b = szam-4;
  else if (szam>6 &&szam<10) b = szam-7;
  else cerr<<"Hibas szamkod!";
  return b;
}

char* Muveletek::firstcheck()
{
  int k=0;
  for (int i=0; i<3; ++i)
    for (int j=0; j<3; j++)
      if (table[i][j]=='O' || table[i][j]=='X')
        ++k;
        
  if (k == 9) {
    std::cout << "\nDONTETLEN!\n";
    return "draw";
  }
  for (int i=0; i<3; ++i)
    if ((table[i][0]=='X'&&table[i][1]=='X'&&table[i][2]=='X') || (table[0][i]=='X'&&table[1][i]=='X'&&table[2][i]=='X')) {
      std::cout << "\nNYERTEL! :)\n";
      player_won=true;
    }
  if ((table[0][0]=='X' && table[1][1]=='X' && table[2][2]=='X') ||
      (table[0][2]=='X' && table[1][1]=='X' && table[2][0]=='X')) {
    std::cout << "\nNYERTEL! :)\n";
    player_won=true;
  }
}

char Muveletek::ellsor(char egyket, char harom)
{
  for (int i=0; i<3; i++) {
    if (table[i][0]==egyket && table[i][1]==egyket && table[i][2]!=harom)
      return 'O';
    else if (table[i][0]==egyket && table[i][2]==egyket && table[i][1]!=harom)
      return 'O';
    else if (table[i][1]==egyket && table[i][2]==egyket && table[i][0]!=harom)
      return 'O';
  }
  return '';
}

char Muveletek::elloszlop(char egyket, char harom)
{
  for (int i=0; i<3; i++) {
    if (table[0][i]==egyket && table[1][i]==egyket && table[2][i]!=harom)
      return 'O';
    else if (table[0][i]==egyket && table[2][i]==egyket && table[1][i]!=harom)
      return 'O';
    else if (table[1][i]==egyket && table[2][i]==egyket && table[0][i]!=harom)
      return 'O';
  }
  return '';
}

char Muveletek::ellatl(char egyket, char harom)
{
  if (table[0][0]==egyket && table[1][1]==egyket && table[2][2]!=harom)
    putO(9);
  else if (table[0][0]==egyket && table[2][2]==egyket && table[1][1]!=harom)
    putO(5);
  else if (table[1][1]==egyket && table[2][2]==egyket && table[0][0]!=harom)
    putO(1);
  else if (table[2][0]==egyket && table[1][1]==egyket && table[0][2]!=harom)
    putO(3)
  else if (table[2][0]==egyket && table[0][2]==egyket && table[1][1]!=harom)
    putO(5);
  else if (table[0][2]==egyket && table[1][1]==egyket && table[2][0]!=harom)
    putO(7);
  else{
  	do{
  		
}
