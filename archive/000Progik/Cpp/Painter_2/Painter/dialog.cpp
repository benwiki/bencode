#include "dialog.h"
#include "ui_dialog.h"
#include "myitem.h"
#include "goal.h"
#include "population.h"

Dialog::Dialog(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::Dialog)
{
    qDebug()<<"It started";
    ui->setupUi(this);

    scene = new QGraphicsScene(this);
    ui->graphicsView->setScene(scene);
    ui->graphicsView->setRenderHint(QPainter::Antialiasing);

    scene->setSceneRect(0, 0, 500, 500);

    QDateTime cd = QDateTime::currentDateTime();
    qsrand(cd.toTime_t());

    ItemCount = 1;

    Population *pop = new Population();
    scene->addItem(pop);

    for (int i=0; i<ItemCount; ++i){
        MyItem *item = new MyItem();
        item->qnum = i;
        item->bestSpeed = pop->bestSpeed;
        item->bestAngle = pop->bestAngle;
        item->distances = pop->distances;
        item->NewGen = &pop->NewGen;
        pop->speedDatas[i] = item->speed;
        pop->angleDatas[i] = item->angle;
        pop->sumMovesDatas[i] = &item->sumMoves;
        scene->addItem(item);
    }
    qDebug()<<"Items created";

    Goal *goal = new Goal();
    scene->addItem(goal);

    timer = new QTimer(this);
    connect(timer, SIGNAL(timeout()), scene, SLOT(advance()));
    timer->start(10);



}

Dialog::~Dialog()
{
    delete ui;
}
