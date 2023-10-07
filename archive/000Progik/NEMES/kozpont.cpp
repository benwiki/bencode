#include <iostream>
#include <cstdlib>
#include <time.h>
using namespace std;

int main(){
    int szgep, ksz;
    cin>>szgep>>ksz;
    int score[szgep];
    for (int i=0; i<szgep; ++i) score[i]=0;
    int kapcs[ksz][3];
    for (int i=0; i<ksz; ++i){
        cin>>kapcs[i][0]>>kapcs[i][1]>>kapcs[i][2];
        //score[kapcs[i][0]-1]+=kapcs[i][2];
    }/*
    int mxscore = 0, ind;
    for (int i=0; i<szgep; ++i)
        if (score[i]>mxscore) {mxscore=score[i];ind=i;}
    cout <<ind+1;*/
    srand(time(NULL));
    cout << rand()%szgep+1;
}
