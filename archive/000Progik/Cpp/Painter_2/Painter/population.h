#ifndef POPULATION_H
#define POPULATION_H

#include <QPainter>
#include <QGraphicsItem>
#include <QGraphicsScene>

class Population : public QGraphicsItem
{
public:
    Population();
    int maxMoves;
    int ItemCount;
    int *distances;
    int *bestSpeed;
    int *bestAngle;
    int **sumMovesDatas;
    int **speedDatas;
    int **angleDatas;
    bool NewGen;
    void paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget);
    QRectF boundingRect() const;

protected:
    void advance(int phase);
};

#endif // POPULATION_H
