std::string megold[N];
for(int i=0; i<N; ++i){
    megold[N]="";
}
for(int i=0; i<N; ++i){
    for(int j=0; j<szavak[i].length(); ++j){
        for(int k=0; k<8; ++k){
            for(int l=0; l<szavak2[k]; ++l){
                if(szavak[i][j] == betuk[k][l]) megold[N] += k+2;
            }
        }
    }
}