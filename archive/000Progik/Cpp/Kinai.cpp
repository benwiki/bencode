#include <iostream>
#include <stdio.h>
#include <time.h>
#include <fstream>
#include <algorithm>
#include <random>
using namespace std;

bool szamszoveg(string);
bool szame(char);
bool ell(string,int,bool);
long long int convert(string, int, long long int);
void feltolt(string, string**,int);
void feltoltint(string, int**, int);

int main(){
	srand(time(NULL));
	random_device rd;
	mt19937 g(rd());
	int maxopp = 3;
	string choice;
	cout << "Hi! This is a program for practicing chinese.\n\nYou can choose from these menu points:";
AGAIN:
	cout<<"\n\t1. Practice numbers\n\t2. Practice date\n\t3. Words\n\n";
	do {
	cout << "Pick what you want (1/2/3): ";
	cin >> choice;
	if (ell(choice,maxopp,1)) cout << "Wrong!!!!!!!\n";
	}while (ell(choice,maxopp,1));
	switch (stoi(choice)){
		
		
		
		
		
		
		
		case 1:{
		    int min, max, x;
		    cout << "Please give the min and max values!\n\tmin:";
		    cin>>min;
		    cout<<"\tmax:";
		    cin>>max;
		    x = max-min+1;
		    cout << "\nI will give you numbers, \nyou should say them out loud in chinese.\nNext number comes when you press ENTER. \nIf you want to get out of here, \ntype 'o' and then press ENTER.\n\n";
		    bool ft = true;
		    while (1){
		    	cout << rand()%x+min;
		    	if(ft) cin.ignore(1);
		    	if(cin.get()==111) {
		    		cout << "\nBack to the menu:\n";
		    		goto AGAIN;
		    	}
		    	ft = false;
		    }
	    }
	    
	    
	    
	    
	    
	    
	    
		case 2:{
		    cout<<"\nI'll give you some dates, that you can\npractice by saying it out loud in chinese.\nNext date comes by pressing ENTER.\nIf you want to get back to menu,\ntype 'o' and press ENTER\n\n";
		    bool ft = true;
		    while (1){
		    	cout<<rand()%121+1900<<". "<<rand()%12+1<<". "<<rand()%31+1<<".";
		    	if (ft) cin.ignore(1);
		    	if(cin.get()==111) {
		    		cout << "\nBack to the menu:\n";
		    		goto AGAIN;
		    	}
		    	ft = false;
		    }
		    break;
		}
		
		
		
		
		
		
		
		case 3:{
			AGAIN2:
		    cout << "\nSubmenus:\n\t1. Topics\n\t2. Practice words randomly\n\t3. Reset Chinese words file \n\t   / create words file\n\t4. Back to menu\n\n";
		    do{
	        cout << "Pick what you want (1/2/3/4): ";
	        cin >> choice;
	        maxopp = 4;
	        if (ell(choice,maxopp,1)) cout << "Wrong!!!!!!!\n";
	        }while (ell(choice,maxopp,1));
	        switch (stoi(choice)){
	        	
	        	
	        	
	        	
	        	
	        	
	        	case 1:{
	        		AGAIN3:
	        	cout<<"\nSub-submenus:\n\t1. Practice words by topics\n\t2. Upload words to topics\n\t3. Upload topics\n\t4. Back to submenus\n\n";
	        		do {
	        		cout<<"Pick what you want (1/2/3/4): ";
	        		cin >> choice;
	        		maxopp = 4;
	        		if (ell(choice,maxopp,1)) cout<<"Wrong!!!!!!!\n";
	        		}while (ell(choice,maxopp,1));
	        		switch (stoi(choice)){
	        			
	        			
	        			
	        			
	        			
	        			case 1:{
	        				ifstream topin;
	        				topin.open("topics.txt", ios::in);
	        				ifstream inf;
	        				inf.open("words.txt", ios::in);
	        				string topic;
	        				int a =0;
	        				cout<<"\nPlease choose a topic!";
	        				cout<<"\n\t0. Default";
	        				while (1){
	        					topic = "";
	        					getline(topin, topic);
	        					if (topic=="") break;
	        					++a;
	        					cout<<"\n\t"<<a<<". "<<topic;
	        				}
	        				do{
	        					cout<<"\nNumber of the topic: ";
	        					cin >> topic;
	        					if (ell(topic,a,0)) cout << "Wrong!!!!!!";
	        				}while (ell(topic,a,0));
	        				int ot =0, linenum=0, x=0;
	        				string chw, tran, getc, gett, words = "", topic2, gbnumc="", gbnumt="", gbnums="", stopics="";
	        				while (1){
	        					chw = "";
	        					tran = "";
	        					getline(inf, topic2);
	        					//stopics+=topic2+";";
	        					getline(inf, chw);
	        					//getline(inf, gbnumc);
	        					getline(inf, tran);
	        					//getline(inf, gbnumt);
	        					/*
	        					gbnums+= gbnumc+"^"+gbnumt+";";
	        					*/
	        					if (chw==""||tran=="") break;
	        					if (topic == topic2) {
	        						words += chw+"^"+tran+";";
	        						++linenum;
	        					}
	        				}
	        				/*
	        				int gubear[linenum][2];
	        				int **gbap;
	        				gbap = new int*[linenum];
	        				for (int i=0;i<linenum;++i)
	        					gbap[i] = gubear[i];
	        				feltoltint(gbnums,gbap, linenum);
	        				
	        				*/
	        				cout<<"\nChoose the mode:\n\t1. Translating chinese words\n\t2. Translating english words\n\t3. Periodically change\n";
	        				maxopp = 3;
	        				bool justc=false, justt=false;
	        				int pc=linenum;
	        				do {
	        					cout<<"Pick what you want (1/2/3): ";
	        					cin >> choice;
	        					if (ell(choice, maxopp,1)) cout<<"Wrong!!!!!!!\n";
	        				}while (ell(choice, maxopp,1));
	        				switch (stoi(choice)){
	        					case 1: {justc=true;
	        					break;}
	        					case 2:{ justt=true;
	        					break;}
	        					case 3: {cout<<"\nGive the num of the periods(max "<< linenum <<"): ";
	        					cin>>pc;
	        					break;}
	        				}
	        				cout << "\n\n\nI'll give you words and you should \nwrite the translation.\nBack to the menu: type ###\n\n";
	        				string wa[linenum][2];
	        				string *wp[linenum];
	        				for(int i=0;i<linenum;++i)
	        					wp[i]=wa[i];
	        					
	        				feltolt(words, wp, linenum);
	        				shuffle(wa, wa+linenum, g);
	        				int bad=0, good=0;
	        				for (int i=0;i<linenum;++i){
	        					if (justc || ot%(pc*2) >= pc)
	        						cout <<wa[i][0];
	        					else 
	        						cout<<wa[i][1];
	        					cout << ": ";
	        					cin >> gett;
	        					if (justc?gett == wa[i][1] : justt?gett==wa[i][0] : ot%(pc*2)>=pc?gett==wa[i][1]:gett==wa[i][0]){
	        						cout << "Correct!";
	        						++good;
	        						//++gubear[i][(justc ? 1 : justt ? 0 : ot%(pc*2)>=pc ? 1 : 0)];
	        					}
	        					else if(gett =="###")
	        					{
	        						cout<<"\nScore: "<<good<<" correct, "<<bad<<" wrong -> "<<(float)good/(float)(good+bad)*100<<"%";
	        						cin.ignore();
	        						cin.get();
	        						inf.close();
	        						goto AGAIN3;
	        					}
	        					else {
	        						cout << "Sorry, wrong!\nThe answer is: ";
	        						if (justc || ot%(pc*2)>=pc) cout<< wa[i][1];
	        						else cout<<wa[i][0];
	        						++bad;
	        						//--gubear[i][(justc ? 1 : justt ? 0 : ot%(pc*2)>=pc ? 1 : 0)];
	        					}
	        					cin.ignore(1);
	        					cin.get();
	        					cout<<endl;
	        					++ot;
	        				}
	        				cout << "All words practiced!\nScore: "<<good<<" correct, "<<bad<<" wrong -> "<<(float)good/(float)linenum*100<<"%";
	        				cin.get();
	        				inf.close();
	        				goto AGAIN3;
	        			}
	        			
	        			
	        			
	        			
	        			
	        			
	        			case 2:{
	        				string topic;
	        				int a=0;
	        				ofstream outf;
	        				outf.open("words.txt", ios_base::app);
	        				ifstream topin;
	        				topin.open("topics.txt", ios::in);
	        				cout<<"\nPlease, choose a topic!\nBE CAREFUL, all of your words that you\nupload now, will be assigned to\nthe topic you choose now!!";
	        				cout<<"\n\t0. Default";
	        				while (1){
	        					topic = "";
	        					getline(topin, topic);
	        					if (topic=="") break;
	        					++a;
	        					cout<<"\n\t"<<a<<". "<<topic;
	        				}
	        				do {
	        				cout<<"\nNumber of the topic: ";
	        				cin >> choice;
	        				if (ell(choice,a,0)) cout<<"Wrong!!!!!!!";
	        				}while (ell(choice,a,0));
	        				
	        				string newword;
	        				bool noch1mal=true;
	        				char noch;
	        				while(noch1mal){
	        					outf << choice<<"\n";
	        					cout<<"Chinese pinyin word (with á,à,ă,ā): ";
	        					cin >> newword;
	        					outf << newword+"\n";
	        					cout << "Translation: ";
	        					cin >> newword;
	        					outf << newword+"\n";
	        					cout <<"\nAn other one? (y/n): ";
	        					cin >> noch;
	        					if (noch =='n' || noch == 'N') noch1mal = false;
	        				}
	        				outf.close();
	        				topin.close();
	        				goto AGAIN3;
	        				break;
	        			}
	        			
	        			
	        			
	        			
	        			
	        			
	        			
	        			case 3:{
	        				ofstream topout;
	        				topout.open("topics.txt", ios_base::app);
	        				string top;
	        				bool noch1mal=true;
	        				string noch;
	        				do{
	        					cout <<"\nName of the new topic: ";
	        					cin >> top;
	        					topout << top+"\n";
	        					cout<<"\nAn other one? (y/n): ";
	        					cin >> noch;
	        					if (noch=="n"||noch=="N") noch1mal = false;
	        				}while (noch1mal);
	        				topout.close();
	        				goto AGAIN3;
	        				break;
	        			}
	        			
	        			
	        			case 4:{
	        				goto AGAIN2;
	        				break;
	        			}
	        		}
	        		break;
	        	}
	        	
	        	
	        	
	        	
	        	
	        	
	        	
	        	case 2:{
	        		ifstream inf;
	        		inf.open("words.txt", ios::in);
	        		int ot =0, linenum=0;
	        		string chw, tran, getc, gett, words = "",topic2, gbnumc="", gbnumt="", gbnums="", stopics="";
	        		while (1){
	        			chw = "";
	        			tran = "";
	        			getline(inf, topic2);
	        			//stopics+=topic2+";";
	        			getline(inf, chw);
	        			//getline(inf, gbnumc);
	        			getline(inf, tran);
	        			//getline(inf, gbnumt);
	        			if(chw==""||tran=="") break;
	        			words += chw+"^"+tran+";";
	        			//gbnums+=gbnumc+"^"+ gbnumt+";";
	        			++linenum;
	        		}
	        		cout<<"\nChoose the mode:\n\t1. Translating chinese words\n\t2. Translating english words\n\t3. Periodically change\n";
	        		maxopp = 3;
	        		bool justc=false, justt=false;
	        		int pc=linenum;
	        		do {
	        			cout<<"Pick what you want (1/2/3): ";
	        			cin >> choice;
	        			if (ell(choice, maxopp,1)) cout<<"Wrong!!!!!!!\n";
	        		}while (ell(choice, maxopp,1));
	        		switch (stoi(choice)){
	        			case 1: {justc=true;
	        			break;}
	        			case 2:{ justt=true;
	        			break;}
	        			case 3: {cout<<"\nGive the num of the periods(max "<<linenum<<"): ";
	        			cin>>pc;
	        			break;}
	        		}
	        		cout << "\n\n\nI'll give you words and you should \nwrite the translation.\nBack to the menu: type ###\n\n";
	        		string wa[linenum][2];
	        		string *wp[linenum];
	        		for(int i=0;i<linenum;++i)
	        			wp[i]=wa[i];
	        		feltolt(words, wp, linenum);
	        		shuffle(wa, wa+linenum, g);
	        		
	        		int bad=0, good=0;
	        		for (int i=0;i<linenum;++i){
	        			if (justc || ot%(pc*2) >= pc)
	        				cout <<wa[i][0];
	        			else 
	        				cout<<wa[i][1];
	        			cout << ": ";
	        			cin >> gett;
	        			if (justc?gett == wa[i][1] : justt?gett==wa[i][0] : ot%(pc*2)>=pc?gett==wa[i][1]:gett==wa[i][0]){
	        				cout << "Correct!";
	        				++good;
	        			}
	        			else if(gett =="###")
	        			{
	        				cout<<"\nScore: "<<good<<" correct, "<<bad<<" wrong -> "<<(float)good/(float)(good+bad)*100<<"%";
	        				cin.ignore();
	        				cin.get();
	        				inf.close();
	        				goto AGAIN2;
	        			}
	        			else {
	        				cout << "Sorry, wrong!\nThe answer is: ";
	        				if (justc || ot%(pc*2)>=pc) cout<< wa[i][1];
	        				else cout<<wa[i][0];
	        				++bad;
	        			}
	        			cin.ignore(1);
	        			cin.get();
	        			cout<<endl;
	        			++ot;
	        		}
	        		cout << "All words practiced!\nScore: "<<good<<" correct, "<<bad<<" wrong -> "<<(float)good/(float)linenum*100<<"%";
	        		cin.get();
	        		inf.close();
	        		goto AGAIN2;
	        		break;
	        	}
	        	
	        	
	        	
	        	
	        	
	        	
	        	
	        	case 3:{
	        		char sure;
	        		cout << "Are you sure? (y/n): ";
	        		cin >> sure;
	        		if (sure=='y'||sure=='Y'){
	        			cout<<"I mean... really? (y/n): ";
	        			cin >> sure;
	        			if (sure=='y'||sure=='Y'){
	        				ofstream file;
	        				file.open("words.txt",
	        				ofstream::out | ofstream::trunc);
	        				file.close();
	        				cout << "\nOkay I deleted it's content / I created the file.";
	        				cin.ignore(1);
	        				cin.get();
	        				goto AGAIN2;
	        			}
	        		}
	        		break;
	        	}
	        	case 4:{
	        		cout << "\nBack to the menu:\n";
	        		goto AGAIN;
	        		break;
	        	}
	        }
	        break;
		}
	}
}

long long int convert(string s, int l, long long int k)
{
	if (l>0) return convert(s, l-1, k*10)+(s[l-1]-'0')*k;
	else return 0;
}

bool szamszoveg(string s) {
	bool e;
	if (s[0]=='-'){
		e = true;
		for (int i=1;i<s.size();++i) if (!szame(s[i])) e = false;
		if (e) return true;
		else return false;
	}
	else {
		e = true;
		for (int i=0;i<s.size();++i) if (!szame(s[i])) e = false;
		if (e) return true;
		else return false;
	}
}

bool szame(char c){
	if (c=='0'||c=='1'||c=='2'||c=='3'||c=='4'||c=='5'||c=='6'||c=='7'||c=='8'||c=='9') return true;
	else return false;
}

bool ell(string c, int max, bool min){
	return !szamszoveg(c)||(szamszoveg(c)&&(stoi(c)<min||stoi(c)>max));
}

void feltolt(string s, string **tomb, int n){
	int j = 0;
	for (int i=0;i<n;++i){
		while (s[j]!='^'){
			tomb[i][0] += s[j];
			++j;
		}
		++j;
		while (s[j]!=';'){
			tomb[i][1] += s[j];
			++j;
		}
		++j;
	}
}

void feltoltint(string s, int **tomb, int n){
	string stomb[n][2];
	int j = 0;
	for (int i=0;i<n;++i){
		while (s[j]!='^'){
			stomb[i][0] += s[j];
			++j;
		}
		++j;
		while (s[j]!=';'){
			stomb[i][1] += s[j];
			++j;
		}
		++j;
	}
	for (int i=0;i<n;++i){
		tomb[i][0]=convert(stomb[i][0], stomb[i][0].length(),1);
		tomb[i][1]=convert(stomb[i][1], stomb[i][1].length(),1);
	}
}