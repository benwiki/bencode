#ifndef MYITEM_H
#define MYITEM_H

#include <QPainter>
#include <QGraphicsItem>
#include <QGraphicsScene>

class MyItem : public QGraphicsItem
{
public:
    MyItem();
    QRectF boundingRect() const;
    void paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget);
    int moves;
    int maxMoves;
    int sumMoves;
    bool stop;
    int xpos();
    int ypos();
    int qnum;
    int track;
    int *bestSpeed;
    int *bestAngle;
    int *distances;
    bool *NewGen;

    int *angle;
    int *speed;

protected:
    void advance(int phase);

};

#endif // MYITEM_H
