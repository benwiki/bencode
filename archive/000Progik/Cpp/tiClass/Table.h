#ifndef TABLE_H
#define TABLE_H
class Muveletek;

class Table{
public:
  Table();
  void vektprint();
  void putX(int);

  char table[3][3];
  bool ret;
  
  Muveletek* convert_y(int);
  Muveletek* convert_x(int);
};

#endif