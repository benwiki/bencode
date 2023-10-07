#include <iostream>
using namespace std;

int main()
{
	float szam;
	cin >> szam;
	for (float i = 1.0; i <= 10000.0; ++i)
	{
		for (float j = 1.0; j <= 10000.0; ++j)
		{
			if (i/ j == szam)
			{
				cout << i << "/" << j << "=" << szam<<endl;
			}
		}
	}
	cout<<"vege";
}