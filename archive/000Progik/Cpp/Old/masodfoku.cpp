#include <iostream>
#include "math.h"
using namespace std;

int main()
{
	float a, b, c;
	float ae, be, ce;

	cout << "Másodfokú egyenletmegoldó program. \n";
	while (1){
		cout << "\na = ";
		cin >> ae;
		cout << "b = ";
		cin >> be;
		cout << "c = ";
		cin >> ce;

		a = (float)ae;
		b = (float)be;
		c = (float)ce;

		float x1 = ((-1.0) * b + sqrt(b * b - 4.0 * a * c)) / (2.0 * a);
		float x2 = ((-1.0) * b - sqrt(b * b - 4.0 * a * c)) / (2.0 * a);

		cout << "Zérushelyek:\nx1 = " << x1 << "\nx2 = " << x2 << "\n";
	}
}