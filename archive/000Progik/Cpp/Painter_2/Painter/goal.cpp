#include "goal.h"

Goal::Goal()
{
    int StartX = 0;
    int StartY = 0;

    setPos(mapToParent(StartX, StartY));
}

QRectF Goal::boundingRect() const
{
    return QRect(0, 0, 10, 10);
}

void Goal::paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget)
{
    QRectF rect = boundingRect();
    QBrush Brush(Qt::red);

    painter->fillRect(rect, Brush);
    painter->drawRect(rect);
}
