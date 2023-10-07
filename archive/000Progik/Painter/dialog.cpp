#include "dialog.h"
//#include "dialog.ui"
#include "myitem.h"
#include "goal.h"

Dialog::Dialog(QWidget *parent) :
    QDialog(parent)
{
	Ui::Dialog *ui= new Ui::Dialog();
    ui->setupUi(this);

    scene = new QGraphicsScene(this);
    ui->graphicsView->setScene(scene);
    ui->graphicsView->setRenderHint(QPainter::Antialiasing);

    scene->setSceneRect(0, 0, 500, 500);

    QDateTime cd = QDateTime::currentDateTime();
    qsrand(cd.toTime_t());
    
    Population *pop= new Population();
    ItemCount = 10;
    for (int i=0; i<ItemCount; ++i){
        MyItem *item = new MyItem();
        item->qnum = i;
        item->bestSpeed=pop->bestSpeed;
        item->bestAngle=pop->bestAngle;
        scene->addItem(item);
    }

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