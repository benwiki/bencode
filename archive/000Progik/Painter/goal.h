#ifndef GOAL_H
#define GOAL_H

#include <QPainter>
#include <QGraphicsItem>
#include <QGraphicsScene>

class Goal : public QGraphicsItem
{
public:
    Goal();
    QRectF boundingRect() const;
    void paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget);
};

#endif // GOAL_H
