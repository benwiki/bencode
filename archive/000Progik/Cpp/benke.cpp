#include <iostream>
#include <string>
using namespace std;

int main()
{
	string szo;
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
	char betuk[8][4] =
		{ {'a', 'b', 'c'}, {'d', 'e', 'f'}, {'g', 'h', 'i'}, {'j', 'k', 'l'}, {'m', 'n', 'o'},
	{'p', 'q', 'r', 's'}, {'t', 'u', 'v'}, {'w', 'x', 'y', 'z'}
	};
	int szavak2[8]={3,3,3,3,3,4,3,4};
	string megold[N];
	for (int i = 0; i < N; ++i)
	{
		megold[N] = "";
	}
	for (int i = 0; i < N; ++i)
	{
		for (int j = 0; j < szavak[i].length(); ++j)
		{
			cout<<szavak[i].length()<<endl;
			for (int k = 0; k < 8; ++k)
			{
				for (int l = 0; l < szavak2[k]; ++l)
				{
					if (szavak[i][j] == betuk[k][l]){
						megold[N] += '2';//(char)(k + 2);
						cout<<i<<" "<<j<<" "<<k<<" "<<l<<endl;}
				}
			}
		}
	}
	cout << "#\n" << maxim << "\n#\n" << kev5 << "\n#\n";
	for (int i = 0; i < N; ++i)
	{
		/*if (megold[N] == szo){
			cout << szavak[i];
		}*/
		cout<<megold[i];
	}
}