#include "population.h"
#include "myitem.h"
#include "dialog.h"

Population::Population()
{
    MyItem *item = new MyItem();
    maxMoves = item->maxMoves;

    ItemCount = 1;

    /*QDateTime cd = QDateTime::currentDateTime();
    qsrand(cd.toTime_t());*/

    distances = new int[ItemCount];
    for (int i=0; i<ItemCount; ++i)
        distances[i] = -1;

    sumMovesDatas = new int*[ItemCount];
    speedDatas = new int*[ItemCount];
    angleDatas = new int*[ItemCount];

    NewGen = false;

    bestAngle = new int[maxMoves];
    bestSpeed = new int[maxMoves];
}

QRectF Population::boundingRect() const
{
    return QRect(0, 0, 0, 0);
}

void Population::paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget)
{
    QRectF rect = boundingRect();
    QBrush Brush(Qt::black);
    painter->fillRect(rect, Brush);
    painter->drawRect(rect);
}

void Population::advance(int phase)
{
    if (!phase) return;

    bool full = true;
    for (int i=0; i<ItemCount; ++i)
        if (distances[i] == -1)
            full = false;

    if (full) {
        qDebug()<<"\nIt got full";
        int best = distances[0];
        int bestInd = 0;
        for (int i=0; i<ItemCount; ++i)
            if (distances[i] < best || (distances[i]==best && sumMovesDatas[i] < sumMovesDatas[bestInd])){
                best = distances[i];
                bestInd = i;
            }
        qDebug()<<"Best rect: "<<bestInd;

        bestSpeed = speedDatas[bestInd];
        bestAngle = angleDatas[bestInd];

        for (int i=0; i<maxMoves; ++i)
            bestSpeed[i]=5;
            //if (qrand()%100==1)
                //bestSpeed[i] = (qrand()%10);

        for (int i=0; i<maxMoves; ++i)
            if (qrand()%100==1)
                bestAngle[i] += (qrand()%2==1 ? (qrand()%20) : -(qrand()%20));

        NewGen = true;
        for (int i=0; i<ItemCount; ++i)
            distances[i] = -1;
        qDebug()<<"Ready for new gen - pop over";
    }
}

