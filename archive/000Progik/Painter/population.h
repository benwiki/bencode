#ifndef POPULATION_H
#define POPULATION_H

#include <QPainter>
#include <QGraphicsItem>
#include <QGraphicsScene>

class Population
{
public:
    Population();
    int maxMoves;
    int ItemCount;
    int *distances;
    void getDatas(int, int, int*, bool);
    int *bestSpeed;
    int *bestAngle;
};

#endif // POPULATION_H
