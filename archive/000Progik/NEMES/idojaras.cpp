#include <iostream>
using namespace std;

int main(){
    int nap, K, L;
    cin >> nap>>K>>L;
    int *hom=new int[nap];
    for (int i=0; i<nap; ++i)
        cin >> hom[i];
    int *mh=new int[nap];
    for (int i=0; i<nap; ++i) mh[i]=0;
    for (int i=1; i<nap-1; ++i){
        if(hom[i]>hom[i-1]&&hom[i]>hom[i+1])
            mh[i]=2;
        else if(hom[i]<hom[i-1]&&hom[i]<hom[i+1])
            mh[i]=1;
    }
    int megold =0;
    int Km, Lm;
    int ind;
    /*if (K+L>2) ind = K+L-1;
    else ind=1;
    for (int i=0; i<nap-K-L; ++i){
        for (int j=i+ind; j<nap; ++j){
            Km=Lm=0;
            for (int k=i; k<=j; ++k){
                if (mh[k]==2)++Km;
                else if(mh[k]==1)++Lm;
            }
            if (Km==K&&Lm==L) ++megold;
        }
    }*/
    int elotte,utana;
    int i=0;
    int elozo=0;
    do{
        elotte=utana=0;
        Km=Lm=0;
        while(!(Km==K&&Lm==L)&&i<nap){
            if (mh[i]==2) ++Km;
            else if(mh[i]==1)++Lm;
            else if(Km==0&&Lm==0)++elotte;
            ++i;
        }
        while(mh[i]!=1&&mh[i]!=2&&i<nap){
            ++utana; ++i;
        }
        i=elozo;
        while(mh[i]!=1&&mh[i]!=2&&i<nap) ++i;
        ++i;
        elozo = i;
        if(Km==K&&Lm==L) megold+=(elotte+1)*(utana+1);
    }while(!(i==nap+1));
    cout << endl<<endl<<megold;
}
