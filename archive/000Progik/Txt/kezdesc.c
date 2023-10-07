#include <stdio.h>
#include <time.h>
typedef enum { false, true } bool;

int main() {
    //65-90, 97-122;
    srand(time(NULL));
    bool ki = false;
    char szo[25];

    printf("Lokj ide egy szot (ekezet nelkul): ");
    scanf("%s", szo);

    int szohossz = strlen(szo);

    char szotgs[szohossz];
    strcpy(szotgs, szo);

    int i, k=0, r;
    char uj[szohossz];
    while(!ki){
        k = k+1;
        for(i = 0; i<szohossz; i=i+1){
            r = rand()%26+97;
            uj[i] = r + '0';
        }
        if(strcmp(szotgs, uj)==0){
            printf("%i probalkozasbol sikerult a gepnek legeneralnia a szavadat.", k);
            ki = true;
        }
    }
}
