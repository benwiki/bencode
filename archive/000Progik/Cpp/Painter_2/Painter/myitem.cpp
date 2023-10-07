#include "myitem.h"
#include "population.h"
#include "dialog.h"
#include <ctime>
#include <iostream>
#include <qmath.h>

MyItem::MyItem(){
    maxMoves=300;

    speed = new int[maxMoves];
    angle = new int[maxMoves];

    moves = 0;
    stop = false;

    int lastOne = qrand()%360;
    int add;
    for (int i=0; i<maxMoves; ++i){
        add = qrand()%41-20;
        angle[i] = lastOne+add;
        lastOne += add;
    }

    for (int i=0; i<maxMoves; ++i){
        speed[i] = (qrand()%10);
    }

    int StartX = 400;
    int StartY = 400;

    setPos(mapToParent(StartX, StartY));
}

QRectF MyItem::boundingRect() const{
    return QRect(0, 0, 5, 5);
}


void MyItem::paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget){
    QRectF rect = boundingRect();
    QBrush Brush(Qt::black);
    painter->fillRect(rect, Brush);
    painter->drawRect(rect);
}

int MyItem::xpos(){
    return this->pos().x();
}

int MyItem::ypos(){
    return this->pos().y();
}

void MyItem::advance(int phase){
    if (!phase) return;

    if(moves < maxMoves){
        if(xpos() > 0 && xpos() < 498 && ypos() > 0 && ypos() < 496){
            setPos(mapToParent(0, speed[moves]));
            setRotation(angle[moves]);
        }
        else if(!stop){
            sumMoves = moves;
            stop = true;
            int dist = qSqrt(xpos()*xpos() + ypos()*ypos());
            qDebug()<<"Uploaded the dist of"<<qnum<<":"<<dist;
            distances[qnum]=dist;
        }
        ++moves;
    }
    else if (*NewGen){
        qDebug()<<"New gen created"<<qnum;
        setPos(250, 250);
        moves = 0;
        for (int i=0; i<maxMoves; ++i)
            qDebug()<<bestSpeed[i];
        speed = bestSpeed;
        angle = bestAngle;
        stop = false;
        *NewGen=false;
    }
}
