#include "population.h"
#include "myitem.h"
#include "dialog.h"

Population::Population()
{
    MyItem *item = new MyItem();
    maxMoves = item->maxMoves;
    Dialog *win = new Dialog();
    ItemCount = win->ItemCount;
    distances = new int[ItemCount];

    //for (int i=0; i<maxMoves; ++i) bestSpeed[i] = 5;

    for (int i=0; i<ItemCount; ++i)
        distances[i] = 1000;

    QDateTime cd = QDateTime::currentDateTime();
    qsrand(cd.toTime_t());
}

void Population::getDatas(int qnum, int dist, int *vector, bool SpeedVect)
{
    distances[qnum] = dist;

    /*bool full = true;
    for (int i=0; i<ItemCount; ++i)
        if (distances[i] == -1)
            full = false;
    if (full) {*/

        int best = distances[0];
        int bestInd = 0;
        for (int i=0; i<ItemCount; ++i)
            if (distances[i]<best){
                best = distances[i];
                bestInd = i;
            }
        if (bestInd == qnum){
            if (SpeedVect)
                bestSpeed = vector;
            else
                bestAngle = vector;

            if (SpeedVect){
                for (int i=0; i<maxMoves; ++i)
                    if (qrand()%100==1)
                        bestSpeed[i] = (qrand()%10);
            }
            else{
                for (int i=0; i<maxMoves; ++i)
                    if (qrand()%100==1)
                        bestAngle[i] += (qrand()%2==1 ? (qrand()%10) : -(qrand()%10));
            }
        }


    //}
}

