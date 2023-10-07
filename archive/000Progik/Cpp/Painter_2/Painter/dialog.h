#ifndef DIALOG_H
#define DIALOG_H

#include <QDialog>
#include <QtGui>
#include <QtCore>

namespace Ui {
class Dialog;
}

class Dialog : public QDialog
{
    Q_OBJECT
    
public:
    explicit Dialog(QWidget *parent = 0);
    ~Dialog();
    Ui::Dialog *ui;
    int ItemCount;
    
private:

    QGraphicsScene *scene;
    QTimer *timer;


};

#endif // DIALOG_H
