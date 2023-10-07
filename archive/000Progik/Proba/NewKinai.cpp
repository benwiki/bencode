#include <iostream>
#include <stdio.h>
#include <time.h>
#include <fstream>
#include <algorithm>
#include <random>
using namespace std;

bool szamszoveg(string);
bool szame(char );
bool ell(string,int,int );
long long int convert(string, int, long long int);
void feltolt(string, string**,int );
void feltoltint(string, int**, int);
void felttop(string, int*, int);
bool mistyped(string, string);
long wordcount();
long topiccount();

struct Index{
	int state[2], value[2];
};

/*struct Wordstruct{
	string MotherLw, ForeignLw;
	int qnum, topic;
	int index[2], bad[2], value[2];
};*/

const int goodlimit = 4;
const int badlimit = -2;

int main(){
	srand(time(NULL));
	random_device rd;
	mt19937 g(rd());
	cout << "Hi! This is a program for practicing chinese.\n\nYou can choose from these menu points:";
AGAIN:
	cout<<"\n\t1. Practice numbers\n\t2. Practice date\n\t3. Words\n\n";
	int maxopp = 3;
	string choice;
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
		    cout << "\nSubmenus:\n\t1. Topics\n\t2. Practice words randomly\n\t3. My progress with the words\n\t4. Reset Chinese words file \n\t   / create words file\n\t5. Back to menu\n\n";
		    maxopp = 5;
		    do{
                cout << "Pick what you want (1/2/3/4/5): ";
                cin >> choice;
				if (ell(choice,maxopp,1)) cout << "Wrong!!!!!!!\n";
	        } while (ell(choice,maxopp,1));
	        switch (stoi(choice)){






	        	case 1:{
	        		AGAIN3:
                    cout<<"\nSub-submenus:\n\t1. Practice words by topics\n\t2. Upload words to topics\n\t3. Upload topics\n\t4. Back to submenus\n\n";
                    maxopp = 4;
	        		do {
                        cout<<"Pick what you want (1/2/3/4): ";
                        cin >> choice;
                        if (ell(choice,maxopp,1)) cout<<"Wrong!!!!!!!\n";
	        		} while (ell(choice,maxopp,1));
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
	        				} while (ell(topic,a,0));
	        				int ot =0, linenum=0;
	        				/*
	        				int topic=AskForTopic();
	        				Wordstruct *word = new Wordstruct[wnum];
	        				feltolt(word);
	        				*/
	        				string chw, tran, gett, words = "", topic2, gbnumc="", gbnumt="", gbnums="", stopics="";
	        				while (1){
	        					chw = "";
	        					tran = "";
	        					inf >> topic2;
	        					stopics+=topic2+";";
	        					inf>>chw;
	        					inf>>gbnumc;
	        					inf>>tran;
	        					inf>>gbnumt;
	        					if (chw==""||tran=="") break;
	        					gbnums+= gbnumc+"^"+gbnumt+";";
								words += chw+"^"+tran+";";
	        					++linenum;
	        				}

							int toparr[linenum];
	        				felttop(stopics,toparr,linenum);

	        				int gubear[linenum][2];
	        				int **gbap;
	        				gbap = new int*[linenum];
	        				for (int i=0;i<linenum;++i)
	        					gbap[i] = gubear[i];
	        				feltoltint(gbnums,gbap,linenum);

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

							Index *ind;
							ind = new Index[linenum];

	        				int badsum=0;
							for (int i=0; i<linenum; ++i){
								if (gubear[i][0] >= goodlimit){
									ind[i].state[0] = 1;
									ind[i].value[0] = gubear[i][0]-goodlimit;
								}
								else if (gubear[i][0] <= badlimit){
									ind[i].state[0] = -1;
									ind[i].value[0] = abs(gubear[i][0]-badlimit)/2+1;
                                    if (justt || (!justc && !justt)) badsum += ind[i].value[0];
								}
								if (gubear[i][1] >= goodlimit){
									ind[i].state[1] = 1;
									ind[i].value[1] = gubear[i][1]-goodlimit;
								}
								else if (gubear[i][1] <= badlimit){
									ind[i].state[1] = -1;
									ind[i].value[1] = abs(gubear[i][1]-badlimit)/2+1;
									if (justc || (!justc && !justt)) badsum += ind[i].value[1];
								}
							}

	        				string wa[linenum + badsum][3];
	        				string eredetiwa[linenum][2];
	        				string *wp[linenum];
	        				for(int i=0;i<linenum;++i){
	        					wp[i]=wa[i];
	        					wa[i][2]=to_string(i);
	        				}
							feltolt(words, wp, linenum);

							int glob=linenum;
	        				for(int i=0;i<linenum;++i){
	        					eredetiwa[i][0] = wa[i][0];
								eredetiwa[i][1] = wa[i][1];
								if (justc && ind[i].state[1] == -1){
									for (int k=0; k<ind[i].value[1]; ++k){
										wa[glob][0]	= wa[i][0];
										wa[glob][2] = wa[i][2];
										wa[glob++][1] = wa[i][1];
									}
								}
								else if (justt && ind[i].state[0] == -1){
									for (int k=0; k<ind[i].value[0]; ++k){
										wa[glob][0]	= wa[i][0];
										wa[glob][2] = wa[i][2];
										wa[glob++][1] = wa[i][1];
									}
								}
								else if(!justc && !justt && ind[i].state[0]==-1){
									for (int k=0; k<ind[i].value[0]; ++k){
										wa[glob][0]	= wa[i][0];
										wa[glob][2] = wa[i][2];
										wa[glob++][1] = wa[i][1];
									}
									for (int k=0; k<ind[i].value[1]; ++i){
										wa[glob][0]	= wa[i][0];
										wa[glob][2] = wa[i][2];
										wa[glob++][1] = wa[i][1];
									}
								}
							}
	        				shuffle(wa, wa+linenum+badsum, g);
	        				cout << "\n\n\nI'll give you words and you should \nwrite the translation.\nBack to the menu: type ###\n\n";
	        				int bad=0, good=0, f;
	        				bool lang = (justc?true:justt?false:ot%(pc*2)>=pc?true:false);
	        				for (int i=0;i<linenum + badsum;++i){
	        					for (int k=0; k<linenum; ++k)
	        							if (eredetiwa[k][0] == wa[i][0] && k == stoi(wa[i][2])) {
	        								f=k;
	        								break;
	        							}
								if (toparr[f] == convert(topic,topic.length(),1) && !(ind[f].state[lang?1:0] == 1 && rand()%100+1 < (ind[f].value[lang?1:0]<7 ? ind[f].value[lang?1:0]*15 : 95))){
									MTT:
	        						if (lang)
	        							cout <<wa[i][0];
	        						else
	        							cout<<wa[i][1];
	        						cout << ": ";
	        						cin >> gett;
	        						if (lang?gett == wa[i][1] : gett==wa[i][0]){
	        							cout << "Correct!";
	        							++good;
	        							++gubear[f][lang?1:0];
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
	        							if (mistyped(gett, lang ? wa[i][1] : wa[i][0])){
	        								cout<<"Did you mistype it? Well, try again!";
	        								cin.ignore(1);
	        								cin.get();
	        								goto MTT;
	        							}
	        							cout << "Sorry, wrong!\nThe answer is: ";
	        							if (lang) cout<< wa[i][1];
	        							else cout<<wa[i][0];
	        							++bad;
	        							--gubear[f][lang?1:0];
	        						}
	        						cin.ignore(1);
	        						cin.get();
	        						cout<<endl;
	        						if (!justt && !justc) ++ot;
	        					}
	        				}
	        				cout << "All words practiced!\nScore: "<<good<<" correct, "<<bad<<" wrong -> "<<(float)good/(float)(good+bad)*100<<"%";
	        				inf.close();
	        				ofstream outf;
	        				outf.open("words.txt", ofstream::out | ofstream::trunc);
	        				for (int i=0; i<linenum; ++i){
	        					outf<<toparr[i]<<"\n";
	        					outf<<eredetiwa[i][0]<<" ";
	        					outf<<gubear[i][0]<<"\n";
	        					outf<<eredetiwa[i][1]<<" ";
	        					outf<<gubear[i][1]<<"\n";
	        				}
	        				outf.close();
	        				cin.ignore(1);
	        				cin.get();
	        				goto AGAIN3;
	        			}






	        			case 2:{
	        				string topic;
	        				int a=0;
	        				ofstream outf;
	        				outf.open("words.txt", ios_base::app);
	        				ifstream topin;
	        				topin.open("topics.txt", ios::in);
	        				cout<<"\nPlease, choose a topic!\nBE CAREFUL, all of your words that you\nupload now, will be assigned to\nthe topic you choose now!!\n(if you want to stop, type ###!)";
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
	        				while(1){
	        					cout<<"\nChinese pinyin word (with á,à,ă,ā): ";
	        					cin >> newword;
	        					if (newword=="###")
	        						break;
	        					outf << choice<<"\n";
	        					outf << newword+"\n0\n";
	        					cout << "Translation: ";
	        					cin >> newword;
	        					outf << newword+"\n0\n";
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
	        				cout<<"\nIf you want to stop, type ###!\n";
	        				while (1){
	        					cout <<"\nName of the new topic: ";
	        					cin >> top;
	        					if (top=="###") break;
	        					topout << top+"\n";
	        				}
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
	        		srand(time(NULL));
	        		ifstream inf;
	        		inf.open("words.txt", ios::in);
	        		int ot =0, linenum=0;
	        		string chw, tran, gett, words = "",topic2, gbnumc="", gbnumt="", gbnums="", stopics="";
	        		while (1){
	        			chw = "";
	        			tran = "";
	        			inf >> topic2;
	        			stopics+=topic2+";";
	        			getline(inf, chw);
	        			inf>>chw;
	        			inf>>gbnumc;
	        			inf>>tran;
	        			inf>>gbnumt;
	        			if(chw==""||tran=="") break;
	        			words += chw+"^"+tran+";";
	        			gbnums+=gbnumc+"^"+ gbnumt+";";
	        			++linenum;
	        		}

	        		int toparr[linenum];
					felttop(stopics,toparr,linenum);

					int gubear[linenum][2];
					int **gbap;
					gbap = new int*[linenum];
					for (int i=0;i<linenum;++i)
						gbap[i] = gubear[i];
					feltoltint(gbnums,gbap,linenum);

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

	        		Index *ind;
					ind = new Index[linenum];

	    			int badsum=0;
					for (int i=0; i<linenum; ++i){
						if (gubear[i][0] >= goodlimit){
							ind[i].state[0] = 1;
							ind[i].value[0] = gubear[i][0]-goodlimit;
						}
						else if (gubear[i][0] <= badlimit){
							ind[i].state[0] = -1;
							ind[i].value[0] = abs(gubear[i][0]-badlimit)/2+1;
							if (justt || (!justc && !justt)) badsum += ind[i].value[0];
						}
						if (gubear[i][1] >= goodlimit){
							ind[i].state[1] = 1;
							ind[i].value[1] = gubear[i][1]-goodlimit;
						}
						else if (gubear[i][1] <= badlimit){
							ind[i].state[1] = -1;
							ind[i].value[1] = abs(gubear[i][1]-badlimit)/2+1;
							if (justc || (!justc && !justt)) badsum += ind[i].value[1];
						}
					}

	   		 	string wa[linenum + badsum][3];
	   		 	string eredetiwa[linenum][2];
	   		 	string *wp[linenum];
	   	 		for(int i=0;i<linenum;++i){
	      		 		wp[i]=wa[i];
	      		 		wa[i][2] = to_string(i);
	   		 	}
					feltolt(words, wp, linenum);

					int glob=linenum;
	        		for(int i=0;i<linenum;++i){
	        			eredetiwa[i][0] = wa[i][0];
						eredetiwa[i][1] = wa[i][1];
						if (justc && ind[i].state[1] == -1){
							for (int k=0; k<ind[i].value[1]; ++k){
								wa[glob][0]	= wa[i][0];
								wa[glob][2] = wa[i][2];
								wa[glob++][1] = wa[i][1];
							}
						}
						else if (justt && ind[i].state[0] == -1){
							for (int k=0; k<ind[i].value[0]; ++k){

								wa[glob][0]	= wa[i][0];
								wa[glob][2] = wa[i][2];
								wa[glob++][1] = wa[i][1];
							}
						}
						else if(!justc && !justt){
							for (int k=0; k<ind[i].value[0] && ind[i].state[0]==-1; ++k){
								wa[glob][0]	= wa[i][0];
								wa[glob][2] = wa[i][2];
								wa[glob++][1] = wa[i][1];
							}
							for (int k=0; k<ind[i].value[1] && ind[i].state[1]==-1; ++k){
								wa[glob][0]	= wa[i][0];
								wa[glob][2] = wa[i][2];
								wa[glob++][1] = wa[i][1];
							}
						}
					}

	        		shuffle(wa, wa+linenum+badsum, g);
	        		cout << "\n\n\nI'll give you words and you should \nwrite the translation.\nBack to the menu: type ###\n\n";
	        		int bad=0, good=0, f;
	        		bool lang = (justc?true:justt?false:ot%(pc*2)>=pc?true:false);

	        		for (int i=0;i<linenum+badsum;++i){
	        			for (int k=0; k<linenum; ++k)
	        				if (eredetiwa[k][0] == wa[i][0] && k == stoi(wa[i][2])) {
	        					f=k;
	        					break;
	        				}
	        			if (!(ind[f].state[lang?1:0] == 1 && rand()%100+1<(ind[f].value[lang?1:0]<7 ? ind[f].value[lang?1:0]*15 : 95))){
	        				MTR:
							if (lang)
	        					cout <<wa[i][0];
	        				else
	        					cout<<wa[i][1];
	        				cout << ": ";
	        				cin >> gett;
	        				if (lang?gett == wa[i][1]:gett==wa[i][0]){
	        					cout << "Correct!";
	        					++good;
								++gubear[f][lang?1:0];
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
	        					if (mistyped(gett, lang ? wa[i][1] : wa[i][0])){
	        						cout<<"Did you mistype it? Well, try again!";
	        						cin.ignore(1);
	        						cin.get();
	        						goto MTR;
	        					}
	        					cout << "Sorry, wrong!\nThe answer is: ";
	        					if (lang) cout<< wa[i][1];
	        					else cout<<wa[i][0];
	        					++bad;
								--gubear[f][lang?1:0];
	        				}
	        				cin.ignore(1);
	        				cin.get();
	        				cout<<endl;
	        				if (!justc && !justt) ++ot;
	        			}
	        		}
	        		cout << "All words practiced!\nScore: "<<good<<" correct, "<<bad<<" wrong -> "<<(float)good/(float)(good+bad)*100<<"%";
	        		cin.get();
	        		inf.close();
	        		ofstream outf;
	        		outf.open("words.txt", ofstream::out | ofstream::trunc);
	        		for (int i=0; i<linenum; ++i){
	        			outf<<toparr[i]<<"\n";
	        			outf<<eredetiwa[i][0]<<" ";
	        			outf<<gubear[i][0]<<"\n";
	        			outf<<eredetiwa[i][1]<<" ";
	        			outf<<gubear[i][1]<<"\n";
	        		}
	        		outf.close();
	        		goto AGAIN2;
	        	}








				case 3:{
					ifstream topin;
	        		topin.open("topics.txt", ios::in);
	        		string *topics;
	        		string topic;
	        		int toplines=0;
	        		getline(topin, topic);
	        		while (topic!=""){
	        			++toplines;
	        			getline(topin, topic);
	        		}
	        		topin.close();
	        		topin.open("topics.txt", ios::in);
	        		topics=new string[toplines];
	        		getline(topin, topic);
	        		int t=0;
	        		while (topic!=""){
	        			topics[t]=topic;
	        			++t;
	        			getline(topin, topic);
	        		}
	        		
					ifstream inf;
					inf.open("words.txt", ios::in);
					int ot =0, linenum=0;
	        		string chw, tran, gett, topic2, words, gbnumc="", gbnumt="", gbnums="", stopics="";
	        		while (1){
	        			chw = "";
	        			tran = "";
	        			inf >> topic2;
	        			stopics+=topic2+";";
	        			inf>>chw;
	        			inf>>gbnumc;
	        			inf>>tran;
	        			inf>>gbnumt;
	        			if(chw==""||tran=="") break;
	        			words += chw+"^"+tran+";";
	        			gbnums+=gbnumc+"^"+ gbnumt+";";
	        			++linenum;
	        		}
	        		
	        		int toparr[linenum];
					felttop(stopics,toparr, linenum);

					int gubear[linenum][2];
					int **gbap;
					gbap = new int*[linenum];
					for (int i=0;i<linenum;++i)
						gbap[i] = gubear[i];
					feltoltint(gbnums,gbap,linenum);

					string wa[linenum][2];
					string *wp[linenum];
	   				for(int i=0;i<linenum;++i)
	      					wp[i]=wa[i];
					feltolt(words, wp, linenum);
					
					Index *ind;
					ind = new Index[linenum];

					for (int i=0; i<linenum; ++i){
						if (gubear[i][0] >= goodlimit){
							ind[i].state[0] = 1;
							ind[i].value[0] = gubear[i][0]-goodlimit;
						}
						else if (gubear[i][0] <= badlimit){
							ind[i].state[0] = -1;
							ind[i].value[0] = abs(gubear[i][0]-badlimit)/2+1;
						}
						if (gubear[i][1] >= goodlimit){
							ind[i].state[1] = 1;
							ind[i].value[1] = gubear[i][1]-goodlimit;
						}
						else if (gubear[i][1] <= badlimit){
							ind[i].state[1] = -1;
							ind[i].value[1] = abs(gubear[i][1]-badlimit)/2+1;
						}
					}
					
					int bsum=0, gsum=0;
					bool cg, eg, cb, eb;
					cg=cb=eg=eb=false;

					for (int i=0; i<linenum; ++i){
						if (gubear[i][0]>=goodlimit) cg=true;
						if (gubear[i][0]<=badlimit)	cb = true;
						if (gubear[i][1]>=goodlimit) eg = true;
						if (gubear[i][1]<=badlimit)	eb=true;
					}
					cout<<endl;
					
					int volt[linenum];
					for (int i=0; i<linenum; ++i)
						volt[i]=0;
					int best, b;
					
					if (cg){
						cout << "\n\nChinese words with an index of "<<goodlimit<<", or more than "<<goodlimit<<":\n\n";
						for (int i=0; i<linenum; ++i){
							best=0;
							b=0;
							for (int j=0; j<linenum; ++j)
								if (gubear[j][0]>best && !volt[j]){
									best=gubear[j][0];
									b=j;
								}
							if (ind[b].state[0]==1 && !volt[b]){
								cout << "\t-" << wa[b][0] << " : " << gubear[b][0] << " ("<<100-(ind[b].value[0]<7 ? ind[b].value[0]* 15 : 95)<<"%)"<< endl; ++gsum;
							}
							volt[b]=1;
						}
					}
					
					for (int i=0; i<linenum; ++i)
						volt[i]=0;
					
					if (eg){
						cout << "\n\nEnglish words with an index of "<<goodlimit<<", or more than "<<goodlimit<<":\n\n";
						for (int i=0; i<linenum; ++i){
							best=0;
							b=0;
							for (int j=0; j<linenum; ++j)
								if (gubear[j][1]>best && !volt[j]){
									best=gubear[j][1];
									b=j;
								}
							if (ind[b].state[1]==1 && !volt[b]){
								cout << "\t-" << wa[b][1] << " : " << gubear[b][1] << " ("<<100-(ind[b].value[1]<7 ? ind[b].value[1]* 15 : 95)<<"%)"<<endl; ++gsum;
							}
							volt[b]=1;
						}
					}
					
					for (int i=0; i<linenum; ++i)
						volt[i]=0;
					
					if (cb) {
						cout << "\n\nChinese words with an index of "<<badlimit<<", or less than "<<badlimit<<":\n\n";
						for (int i=0; i<linenum; ++i){
							best=0;
							b=0;
							for (int j=0; j<linenum; ++j)
								if (gubear[j][0]<best && !volt[j]){
									best=gubear[j][0];
									b=j;
								}
							if (ind[b].state[0]==-1 && !volt[b]){
								cout << "\t-" << wa[b][0] << " : " << gubear[b][0] << " (+"<< ind[b].value[0]<<")"<<endl; ++bsum;
							}
							volt[b]=1;
						}
					}
					
					for (int i=0; i<linenum; ++i)
						volt[i]=0;
					
					if (eb){
						cout << "\n\nEnglish words with an index of "<<badlimit<<", or less than "<<badlimit<<":\n\n";
						for (int i=0; i<linenum; ++i){
							best=0;
							b=0;
							for (int j=0; j<linenum; ++j)
								if (gubear[j][1]<best && !volt[j]){
									best=gubear[j][1];
									b=j;
								}
							if (ind[b].state[1]==-1 && !volt[b]){
								cout << "\t-" << wa[b][1] << " : " << gubear[b][1] << " (+"<< ind[b].value[1]<<")"<< endl; ++bsum;
							}
							volt[b]=1;
						}
					}
					cout<<(cg||cb||eg||eb?"\nThe rest is":"\nAll words are")<<" between "<<badlimit<<" and "<<goodlimit<<".";
					cout << "\n\nTotal: " << gsum/((float)linenum*2)*100 << "% good, and "<< bsum/((float)linenum*2)*100<< "% bad words.";
					
					string multiple="";
					bool elso;
					for (int k=0; k<2; ++k){
					for (int i=0; i<linenum; ++i)
						volt[i]=0;
					for (int i=0; i<linenum; ++i){
						multiple="";
						if (volt[i]) continue;
						elso = true;
						for (int j=i+1; j<linenum; ++j){
							if (wa[i][k] == wa[j][k]){
								if (elso) 
								multiple+=topics[ toparr[i]-1]+" ";
								multiple+=topics[ toparr[j]-1]+" ";
								volt[i]=1;
								elso=false;
							}
						}
						if(multiple!="")
							cout<<"\n\nWARNING: This word ("<<wa[i][k]<<") exists\nin multiple topics: "<<multiple;
					}
					}
					cin.ignore();
					cin.get();
					goto AGAIN2;
				}






	        	case 4:{
	        		char sure;
	        		cout << "Are you sure? (y/n): ";
	        		cin >> sure;
	        		if (sure=='y'||sure=='Y'){
	        			cout<<"I mean... really? (y/n): ";
	        			cin >> sure;
	        			if (sure=='y'||sure=='Y'){
	        				ofstream file;
	        				file.open("words.txt", ofstream::out | ofstream::trunc);
	        				file.close();
	        				cout << "\nOkay I deleted it's content / I created the file.";
	        				cin.ignore(1);
	        				cin.get();
	        				goto AGAIN2;
	        			}
	        		}
	        		break;
	        	}
	        	case 5:{
	        		cout << "\nBack to the menu:\n";
	        		goto AGAIN;
	        		break;
	        	}
	        }
	        break;
		}
	}
}

long long int convert(string s, int l, long long int k){
	int x=0, minusz=1;
	if (s[0]=='-'){
		x=1;
		minusz = -1;
	}
	if (l>x) return convert(s, l-1, k*10)+minusz*(s[l-1]-'0')*k;
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

bool ell(string c, int max, int min){
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

void felttop(string s, int *tomb, int n){
	string stomb[n];
	int j = 0;
	for (int i=0;i<n;++i){
		while (s[j]!=';'){
			stomb[i] += s[j];
			++j;
		}
		++j;
	}
	for (int i=0;i<n;++i){
		tomb[i]=convert(stomb[i], stomb[i].length(),1);
	}
}

bool mistyped (string inp, string orig){
	float val=0;
	float il = inp.length(), ol=orig.length();
	if (il>ol){
		for (int i=0; i<ol; ++i)
			if (inp[i]==orig[i])
				++val;
	}
	else if (il<ol){
		for (int i=0; i<il; ++i)
			if (inp[i]==orig[i])
				++val;
	}
	else{
		for (int i=0; i<ol; ++i)
			if (inp[i]==orig[i])
				++val;
	}
	if (val/ol*(il>ol ? ol/il : il/ol)>0.5)
		return true;
	else
		return false;
}

long wordcount(){
	ifstream inf;
	inf.open("words.txt");
	long count=0;
	string input="";
	getline(inf, input);
	while (input != ""){
		++count;
		getline(inf, input);
		getline(inf, input);
		getline(inf, input);
	}
	return count;
}

long topiccount(){
	ifstream inf;
	inf.open("topics.txt");
	long count=0;
	string input="";
	getline(inf, input);
	while (input != ""){
		++count;
		getline(inf, input);
	}
	return count;
}

/*
void shuffleWords(Wordstruct *word){
	int wnum = wordcount();
	int *used = new int[wnum];
	Wordstruct *copy = new Wordstruct[wnum];
	for (int i=0; i<wnum; ++i){
		copy[i] = word[i];
		used[i] = 0;
	}
	int r;
	for (int i=0; i<wnum; ++i){
		r = rand()%(wnum-i);
		while (used[r]) ++r;
		word[r] = copy[i];
		used[r] = 1;
	}
	delete [] copy;
	delete [] used;
}

bool feltolt(Wordstruct *word){
	ifstream inf;
	inf.open("words.txt");
	int wnum=wordcount();
	string input;
	for (int i=0; i<wnum; ++i){
		word[i].qnum=i;
	    inf>>input;
	    word[i].topic= stoi(input);
	    inf>>word[i].ForeignLw;
	    inf>>input;
	    word[i].index[0]= stoi(input);
	    inf>>word[i].MotherLw;
	    inf>>input;
	    word[i].index[1]= stoi(input);
	    for (int k=0; k<2; ++k){
	    	if (word[i].index[k] >= goodlimit){
	        	word[i].state[k]=1;
	        	word[i].value[k]= word[i].index[k]-goodlimit;
	        }
	        else if (word[i].index[k] <= badlimit){
	        	word[i].state[k]=-1;
	        	word[i].value[k]= abs(word[i].index[k]-badlimit)/2+1;
	        }
	    }
	}
	inf.close()
}

int AskForTopic(){
	ifstream topin;
	topin.open("topics.txt", ios::in);
	int tnum=topiccount();
	cout<<"\nPlease choose a topic!";
	cout<<"\n\t0. Default";
	for (int i=0; i<tnum; ++i){
		getline(topin, topic);
	    cout<<"\n\t"<<i+1<<". "<<topic;
	}
	do{
		cout<<"\nNumber of the topic: ";
		cin >> topic;
		if (ell(topic,tnum,0)) cout << "Wrong!!!!!!";
	} while (ell(topic,tnum,0));
	topin.close();
	
	return stoi(topic);
}

void FillBack(Wordstruct *word){
	int wnum=wordcount();
	ofstream outf;
	outf.open("words.txt", ofstream::out | ofstream::trunc);
	for (int i=0; i<wnum; ++i){
		outf<<word[i].topic<<"\n";
		outf<<word[i].ForeignLw<<" "<<word[i].index[0]<<"\n";
		outf<<word[i].MotherLw<<" "<<word[i].index[1]<<"\n";
	}
	outf.close();
}*/