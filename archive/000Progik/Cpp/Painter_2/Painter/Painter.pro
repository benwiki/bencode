#-------------------------------------------------
#
# Project created by QtCreator 2019-05-25T09:18:19
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = Painter
TEMPLATE = app


SOURCES += main.cpp\
        dialog.cpp \
    myitem.cpp \
    goal.cpp \
    population.cpp

HEADERS  += dialog.h \
    myitem.h \
    goal.h \
    population.h

FORMS    += dialog.ui
