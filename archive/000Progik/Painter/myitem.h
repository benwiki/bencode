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

protected:
    void advance(int phase);

private:
    int *angle;
    int *speed;
    void (*getData)(int, int, int*, bool);
    int *bestSpeed;
    int *bestAngle;
};

#endif // MYITEM_H
