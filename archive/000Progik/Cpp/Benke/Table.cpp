#include "Table.h"

Table::Table()
{
  for (int i=0; i<3; i++) {
    for (int j=0; j<3; j++) {
      table[i][j] = '.';
    }
  }
}

void Table::vektprint()
{
  for (int i=0; i<3; i++) {
    for (int j=0; j<3; j++) {
      std::cout << table[i][j] << " ";
    }
    std::cout << std::endl;
  }
}

void Table::putX(int n)
{
  int sz, sz2;
  sz = m.convert0(n);
  sz2 = m.convert1(n);
  table[sz][sz2] = 'X';
}
