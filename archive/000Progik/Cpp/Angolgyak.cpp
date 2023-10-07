#include <iostream>
#include <fstream>

using namespace std;

int main(){
	ifstream inf;
	inf.open("words.txt", ios::in);
	string s, ossz="";
	inf>>s;
	cout<<s;
	int megvot=0;
	while (s!=""){
		megvot=0;
		for (int i=0; i<s.length(); ++i){
			if (s[i] == '\t') ++megvot;
			else if (!(s[i]==' '))
				ossz+=s[i];
			if (megvot==3)
				ossz+='-';
		}
		ossz+=';';
		getline(inf, s);
	}
	cout<<ossz;
}