#include <iostream>
#include <string>
using namespace std;

int main(){
	string E;
	cout << "Írd be az egyenletet!\n";
	cin >> E;
	string Er1="", Er2="";
	int i=0;
	while (E[i] != '='){
		Er1+=E[i];
		++i;
	}
	++i;
	for (int j=i; j<E.length(); ++j)
		Er2+=E[j];
	for (i=0; i<Er1.length(); ++i)
	if (
}