#include <iostream>
using namespace std;

int main(){
    int asztal, tl, sz, poz, mag;
    cin >> asztal>>tl>>sz;
    int *megold = new int[asztal];
    for (int i=0; i<asztal; ++i) megold[i]=0;
    for (int i=0; i<tl; ++i){
        scanf("%d %d", &poz, &mag);
        for (int j=poz; j<poz+sz; ++j)
            if (megold[j]<mag) megold[j]=mag;
    }
    int minmag=0,ind=0;
    for (int i=0; i<asztal; ++i)
        if(megold[i]!=0){minmag = megold[i]; ind =i; break;}
    for (int i=ind+1; i<asztal; ++i)
        if (megold[i]<minmag&&megold[i]!=0) minmag = megold[i];
    cout << minmag;
}
