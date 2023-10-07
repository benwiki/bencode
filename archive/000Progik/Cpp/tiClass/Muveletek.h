#ifndef MUVELETEK_H
#define MUVELETEK_H
class Table;

class Muveletek{
public:
  int convert_y(int a);
  int convert_x(int a);
  int ellsor(char egyket, char harom);
  int elloszlop(char egyket, char harom);
  int ellatl(char egyket, char harom);
  int firstcheck();
  bool player_won;

  Table* table;
  Table* putO(int);
};

