#include <iostream>
using namespace std;
int abs(int n){
    if(n<0) return n-2*n;
    else return n;
}
int main(){
    int sor, oszlop, kul;
    cin>>sor>>oszlop>>kul;
    int pont[sor][oszlop];
    int most[2];
    int indul[]={0,0};
    int ut=0;
    for (int i=0; i<sor; ++i)
        for(int j=0; j<oszlop; ++j)
            cin >> pont[i][j];
    for (int i=0; i<sor; ++i){
        for(int j=0; j<oszlop; ++j){
            if((i!=sor-1?abs(pont[i][j]-pont[i][j+1])<=kul:0) || (j!=oszlop-1?abs(pont[i][j]-pont[i+1][j])<=kul:0)){
                indul[0]=i;
                indul[1]=j;
                goto KEZDODIK;
            }
        }
    }
    KEZDODIK:
    bool kesz=false;
    string merre="";
    int i, j;
    i = indul[0];
    j = indul[1];
    while (!kesz){
        kesz =true;
        if(i!=sor-1&&j!=oszlop-1){
            if(abs(pont[i][j]-pont[i][j+1])<=kul) {++ut; merre+='J'; kesz=false; ++j;}
            else if(abs(pont[i][j]-pont[i+1][j])<=kul) {++ut; merre+='L'; kesz=false; ++i;}
        }
        else if(i==sor-1&&j!=oszlop-1)
            if(abs(pont[i][j]-pont[i][j+1])<=kul) {++ut; merre+='J'; kesz=false; ++j;}
        else if(i!=sor-1&&j==oszlop-1)
            if(abs(pont[i][j]-pont[i+1][j])<=kul) {++ut; merre+='L'; kesz=false; ++i;}
    }
    cout <<ut<<endl<<indul[0]<<" "<<indul[1]<<endl<<merre;
}


