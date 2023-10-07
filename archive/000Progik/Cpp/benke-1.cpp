#include <iostream>
#include <string>
using namespace std;

int main()
{
	int szo;
	string szoo;
	int N;
	cin >> szo;
	cin >> N;
	string szavak[N];
	for (int i = 0; i < N; ++i)
	{
		cin >> szavak[i];
	}

	string maxim = "";
	for (int i = 0; i < N; ++i)
	{
		if (szavak[i].length() > maxim.length())
			maxim = szavak[i];
	}

	int kev5 = 0;
	for (int i = 0; i < N; ++i)
	{
		if (szavak[i].length() < 5)
			++kev5;
	}
	string betuk[8] = {"abc","def","ghi","jkl","mno","pqrs","tuv","wxyz"};
	int convert[N];
	for(int i=0; i<N; ++i) convert[i] = 0;

	for (int i = 0; i < N; ++i){
		for (int j = 0; j < szavak[i].length(); ++j){
			for (int k=0; k<8; ++k){
                for (int l=0; l<betuk[k].length(); ++l){
                    if(szavak[i][j]==betuk[k][l]) convert[i] = convert[i]*10+k+2;
                }
            }
		}
	}
	cout << "#\n" << maxim << "\n#\n" << kev5 << "\n#\n";
	for (int i=0; i<N; ++i){
        if (convert[i]==szo)cout<<szavak[i]<<endl;
	}
	int szavak2[N];
	for (int i=0; i<N; ++i) szavak2[i] = 0;
	for (int i=0; i<N; ++i){
		for (int j=0; j<N; ++j){
			if (j==i) continue;
			else{
				if (convert[i] == convert[j]) szavak2[j] = 1;
			}
		}
	}
	int azonos=0;
	for (int i=0; i<N; ++i) if (szavak2[i]==1) ++azonos;
	cout<<"#\n"<<azonos<<"\n#\n";
	for (int i=0; i<N; ++i) {
		if (szavak2[i]==1) cout<<convert[i]<<" "<<szavak[i]<< endl;
	}
	for (int i=0; i<N; ++i) szavak2[i] = 0;
	for (int i=0; i<N; ++i){
		for (int j=0; j<N; ++j){
			if (j==i) continue;
			else{
				if (convert[i] == convert[j]) szavak2[j] += 1;
			}
		}
	}
	int maxx=0, legtobb=0;
	for (int i=0; i<N; ++i) if (szavak2[i]>maxx) maxx=szavak2[i];
	for (int i=0; i<N; ++i) if (maxx==szavak2[i]) legtobb = convert[i];
	cout<<"#\n"<<legtobb<<"\n#\n";
	for (int i=0; i<N; ++i) if (convert[i]==legtobb) cout<<szavak[i];
	cout<<"\n#\n";
	for (int i=0; i<N; ++i) cout<<convert[i]<<endl;
}