#include "Table.h"
#include "Muveletek.h"

Table::Table() {
  for (int i=0; i<3; i++)
    for (int j=0; j<3; j++)
      table[i][j] = '.';
}

void Table::vektprint(){
  for (int i=0; i<3; i++){
    for (int j=0; j<3; j++)
      std::cout << table[i][j] << " ";
    std::cout << std::endl;
  }
}

void Table::putX(int n){
  int x, y;
  y = convert_y(n);
  x = convert_x(n);
  table[y][x] = 'X';
}

void Table::putO(int n){
  int x, y;
  y = convert_y(n);
  x = convert_x(n);
  table[y][x] = 'O';
}
