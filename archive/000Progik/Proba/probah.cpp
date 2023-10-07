#include <iostream>
#include <fstream>
#include <time.h>
using namespace std;

struct Wordstruct{
	int proba;
};

bool shuffleWords(Wordstruct*);

int main(){
	srand(time(0));
	Wordstruct *word=new Wordstruct[10];
	for (int i=0; i<10; ++i) word[i].proba=i+1;
	shuffleWords(word);
	cout<<endl<<endl;
	for (int i=0; i<10; ++i) cout<<word[i].proba<<" ";
}

bool shuffleWords(Wordstruct *word){
	int wnum = 10;
	int *used = new int[wnum];
	Wordstruct *copy = new Wordstruct[wnum];
	for (int i=0; i<wnum; ++i){
		copy[i] = word[i];
		used[i] = 0;
	}
	int r;
	for (int i=0; i<wnum; ++i){
		r = rand()%(wnum-i);
		cout<<r<<" ";
		while (used[r]) r++;
		word[r] = copy[i];
		used[r] = 1;
		cout<<r<<endl;
	}
	delete [] copy;
	delete [] used;
}
	