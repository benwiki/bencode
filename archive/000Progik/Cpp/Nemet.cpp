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
void felttop(string, int*, int);

struct Index{
	int state[2]={0, 0};
	int value[2]={0, 0};
};

const int goodlimit = 4;
const int badlimit = -4;

int main(){
	srand(time(NULL));
	random_device rd;
	mt19937 g(rd());
	cout << "Üdv! Ezzel a programmal németet gyakorolhatsz.\n\nVálassz az alábbi menüpontok közül:";
AGAIN:
	cout<<"\n\t1. Számok gyakorlása\n\t2. Dátum gyakorlása\n\t3. Szavak\n\n";
	int maxopp = 3;
	string choice;
	do {
	cout << "Válassz (1/2/3): ";
	cin >> choice;
	if (ell(choice,maxopp,1)) cout << "Helytelen!!!!!!!\n";
	}while (ell(choice,maxopp,1));
	switch (stoi(choice)){







		case 1:{
		    int min, max, x;
		    cout << "Add meg a minimum & maximum értékeket!\n\tmin:";
		    cin>>min;
		    cout<<"\tmax:";
		    cin>>max;
		    x = max-min+1;
		    cout << "\nSzámokat adok neked, \nmondd ki ezeket hangosan németül.\nA következő akkor jön, ha ENTER-t nyomsz.\nHa ki akarsz lépni, \nírd, hogy 'o' és nyomj ENTER-t.\n\n";
		    bool ft = true;
		    while (1){
		    	cout << rand()%x+min;
		    	if(ft) cin.ignore(1);
		    	if(cin.get()==111) {
		    		cout << "\nVissza a menübe:\n";
		    		goto AGAIN;
		    	}
		    	ft = false;
		    }
	    }







		case 2:{
		    cout<<"\nDátumokat adok neked, amiket\nkimondhatsz hangosan németül\nA következő akkor jön, ha ENTER-t nyomsz.\nHa ki akarsz lépni, \nírd, hogy 'o' és nyomj ENTER-t.\n\n";
		    bool ft = true;
		    while (1){
		    	cout<<rand()%121+1900<<". "<<rand()%12+1<<". "<<rand()%31+1<<".";
		    	if (ft) cin.ignore(1);
		    	if(cin.get()==111) {
		    		cout << "\nVissza a menübe:\n";
		    		goto AGAIN;
		    	}
		    	ft = false;
		    }
		    break;
		}







		case 3:{
			AGAIN2:
		    cout << "\nAlmenü:\n\t1. Témakörök\n\t2. GYAKORLÁS minden szóból\n\t3. Hogy állok a szavakkal\n\t4. A szófájl tartalmának törlése \n\t   / a szófájl létrehozása\n\t5. Vissza a menübe\n\n";
		    maxopp = 5;
		    do{
                cout << "Válassz (1/2/3/4/5): ";
                cin >> choice;
				if (ell(choice,maxopp,1)) cout << "Helytelen!!!!!!!\n";
	        } while (ell(choice,maxopp,1));
	        switch (stoi(choice)){






	        	case 1:{
	        		AGAIN3:
                    cout<<"\nAl-almenü:\n\t1. GYAKORLÁS témakörök szerint\n\t2. Szavak feltöltése\n\t3. Új témakörök létrehozása\n\t4. Vissza az almenübe\n\n";
	        		do {
                        cout<<"Válassz (1/2/3/4): ";
                        cin >> choice;
                        maxopp = 4;
                        if (ell(choice,maxopp,1)) cout<<"Helytelen!!!!!!!\n";
	        		} while (ell(choice,maxopp,1));
	        		switch (stoi(choice)){





	        			case 1:{
	        				ifstream topin;
	        				topin.open("temakorok.txt", ios::in);
	        				ifstream inf;
	        				inf.open("szavak.txt", ios::in);
	        				string topic;
	        				int a =0;
	        				cout<<"\nVálassz egy témakört!";
	        				cout<<"\n\t0. Alap";
	        				while (1){
	        					topic = "";
	        					getline(topin, topic);
	        					if (topic=="") break;
	        					++a;
	        					cout<<"\n\t"<<a<<". "<<topic;
	        				}
	        				do{
	        					cout<<"\nA témakör száma: ";
	        					cin >> topic;
	        					if (ell(topic,a,0)) cout << "Helytelen!!!!!!";
	        				} while (ell(topic,a,0));
	        				int ot =0, linenum=0;
	        				string chw, tran, gett, words = "", topic2, gbnumc="", gbnumt="", gbnums="", stopics="";
	        				while (1){
	        					chw = "";
	        					tran = "";
	        					getline(inf, topic2);
	        					stopics+=topic2+";";
	        					getline(inf, chw);
	        					getline(inf, gbnumc);
	        					getline(inf, tran);
	        					getline(inf, gbnumt);
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

	        				cout<<"\nVálaszd ki a módot:\n\t1. Német szavak fordítása\n\t2. Magyar szavak fordítása\n\t3. Periódusosan változzon\n";
	        				maxopp = 3;
	        				bool justc=false, justt=false;
	        				int pc=linenum;
	        				do {
	        					cout<<"Válassz (1/2/3): ";
	        					cin >> choice;
	        					if (ell(choice, maxopp,1)) cout<<"Helytelen!!!!!!!\n";
	        				}while (ell(choice, maxopp,1));
	        				switch (stoi(choice)){
	        					case 1: {justc=true;
	        					break;}
	        					case 2:{ justt=true;
	        					break;}
	        					case 3: {cout<<"\nPeriódusok száma (max "<< linenum <<"): ";
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

	        				string wa[linenum + badsum][2];
	        				string eredetiwa[linenum][2];
	        				string *wp[linenum];
	        				for(int i=0;i<linenum;++i)
	        					wp[i]=wa[i];
							feltolt(words, wp, linenum);

							int glob=linenum;
	        				for(int i=0;i<linenum;++i){
	        					eredetiwa[i][0] = wa[i][0];
								eredetiwa[i][1] = wa[i][1];
								if (justc && ind[i].state[1] == -1){
									for (int k=0; k<ind[i].value[1]; ++k){
										wa[glob][0]	= wa[i][0];
										wa[glob++][1] = wa[i][1];
									}
								}
								else if (justt && ind[i].state[0] == -1){
									for (int k=0; k<ind[i].value[0]; ++k){
										wa[glob][0]	= wa[i][0];
										wa[glob++][1] = wa[i][1];
									}
								}
								else if(!justc && !justt){
									for (int k=0; k<ind[i].value[0] && ind[i].state[0]==-1; ++k){
										wa[glob][0]	= wa[i][0];
										wa[glob++][1] = wa[i][1];
									}
									for (int k=0; k<ind[i].value[1] && ind[i].state[1]==-1; ++i){
										wa[glob][0]	= wa[i][0];
										wa[glob++][1] = wa[i][1];
									}
								}
							}
	        				shuffle(wa, wa+linenum+badsum, g);
	        				cout << "\n\n\nSzavakat adok neked, te pedig\nírd be a fordítást!\nVissza a menübe: írd: ###\n\n";
	        				int bad=0, good=0, f;
	        				bool lang = (justc?true:justt?false:ot%(pc*2)>=pc?true:false);
	        				for (int i=0;i<linenum + badsum;++i){
	        					for (int k=0; k<linenum; ++k)
	        							if (eredetiwa[k][0] == wa[i][0]) {
	        								f=k;
	        								break;
	        							}
								if (toparr[f] == convert(topic,topic.length(),1) && !(ind[f].state[lang?1:0] == 1 && rand()%100+1 < (ind[f].value[lang?1:0]<7 ? ind[f].value[lang?1:0]*15 : 95))){
	        						if (lang)
	        							cout <<wa[i][0];
	        						else
	        							cout<<wa[i][1];
	        						cout << ": ";
	        						cin >> gett;
	        						if (lang?gett == wa[i][1] : gett==wa[i][0]){
	        							cout << "Helyes! :)";
	        							++good;
	        							++gubear[f][lang?1:0];
	        						}
	        						else if(gett =="###")
	        						{
	        							cout<<"\nEredmény: "<<good<<" helyes, "<<bad<<" helytelen -> "<<(float)good/(float)(good+bad)*100<<"%";
	        							cin.ignore();
	        							cin.get();
	        							inf.close();
	        							goto AGAIN3;
	        						}
	        						else {
	        							cout << "Helytelen! :(\nA helyes válasz: ";
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
	        				cout << "Végiggyakoroltad!\nEredmény: "<<good<<" helyes, "<<bad<<" helytelen -> "<<(float)good/(float)(good+bad)*100<<"%";
	        				cin.ignore();
	        				cin.get();
	        				inf.close();
	        				ofstream outf;
	        				outf.open("szavak.txt", ofstream::out | ofstream::trunc);
	        				for (int i=0; i<linenum; ++i){
	        					outf<<toparr[i]<<"\n";
	        					outf<<eredetiwa[i][0]<<"\n";
	        					outf<<gubear[i][0]<<"\n";
	        					outf<<eredetiwa[i][1]<<"\n";
	        					outf<<gubear[i][1]<<"\n";
	        				}
	        				outf.close();
	        				goto AGAIN3;
	        			}






	        			case 2:{
	        				string topic;
	        				int a=0;
	        				ofstream outf;
	        				outf.open("szavak.txt", ios_base::app);
	        				ifstream topin;
	        				topin.open("temakorok.txt", ios::in);
	        				cout<<"\nVálassz egy témakört!\nVIGYÁZZ, minden szó amit most beírsz,\nahhoz a témakörhöz lesz csatolva,\namit most választasz!!\n(ha ki akarsz lépni, írd: ###)";
	        				cout<<"\n\t0. Alap";
	        				while (1){
	        					topic = "";
	        					getline(topin, topic);
	        					if (topic=="") break;
	        					++a;
	        					cout<<"\n\t"<<a<<". "<<topic;
	        				}
	        				do {
	        				cout<<"\nA témakör száma: ";
	        				cin >> choice;
	        				if (ell(choice,a,0)) cout<<"Helytelen!!!!!!!";
	        				}while (ell(choice,a,0));

	        				string newword;
	        				bool noch1mal=true;
	        				char noch;
	        				while(1){
	        					outf << choice<<"\n";
	        					cout<<"\nNémet kifejezés: ";
	        					cin >> newword;
	        					if (newword=="###")
	        						break;
	        					outf << newword+"\n0\n";
	        					cout << "Fordítás: ";
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
	        				topout.open("temakorok.txt", ios_base::app);
	        				string top;
	        				bool noch1mal=true;
	        				cout<<"\nHa ki akarsz lépni, írd: ###\n";
	        				while (1){
	        					cout <<"\nAz új témakör neve: ";
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
	        		inf.open("szavak.txt", ios::in);
	        		int ot =0, linenum=0;
	        		string chw, tran, gett, words = "",topic2, gbnumc="", gbnumt="", gbnums="", stopics="";
	        		while (1){
	        			chw = "";
	        			tran = "";
	        			getline(inf, topic2);
	        			stopics+=topic2+";";
	        			getline(inf, chw);
	        			getline(inf, gbnumc);
	        			getline(inf, tran);
	        			getline(inf, gbnumt);
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

	        		cout<<"\nVálaszd ki a módot:\n\t1. Német szavak fordítása\n\t2. Magyar szavak fordítása\n\t3. Periódusosan változzon\n";
	        		maxopp = 3;
	        		bool justc=false, justt=false;
	        		int pc=linenum;
	        		do {
	        			cout<<"Válassz (1/2/3): ";
	        			cin >> choice;
	        			if (ell(choice, maxopp,1)) cout<<"Helytelen!!!!!!!\n";
	        		}while (ell(choice, maxopp,1));
	        		switch (stoi(choice)){
	        			case 1: {justc=true;
	        			break;}
	        			case 2:{ justt=true;
	        			break;}
	        			case 3: {cout<< "\nPeriódusok száma (max "<<linenum<<"): ";
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

	   				string wa[linenum + badsum][2];
	   				string eredetiwa[linenum][2];
	   				string *wp[linenum];
	   				for(int i=0;i<linenum;++i)
	      					wp[i]=wa[i];
					feltolt(words, wp, linenum);

					int glob=linenum;
	        		for(int i=0;i<linenum;++i){
	        			eredetiwa[i][0] = wa[i][0];
						eredetiwa[i][1] = wa[i][1];
						if (justc && ind[i].state[1] == -1){
							for (int k=0; k<ind[i].value[1]; ++k){
								wa[glob][0]	= wa[i][0];
								wa[glob++][1] = wa[i][1];
							}
						}
						else if (justt && ind[i].state[0] == -1){
							for (int k=0; k<ind[i].value[0]; ++k){

								wa[glob][0]	= wa[i][0];
								wa[glob++][1] = wa[i][1];
							}
						}
						else if(!justc && !justt){
							for (int k=0; k<ind[i].value[0] && ind[i].state[0]==-1; ++k){
								wa[glob][0]	= wa[i][0];
								wa[glob++][1] = wa[i][1];
							}
							for (int k=0; k<ind[i].value[1] && ind[i].state[1]==-1; ++k){
								wa[glob][0]	= wa[i][0];
								wa[glob++][1] = wa[i][1];
							}
						}
					}

	        		shuffle(wa, wa+linenum+badsum, g);
	        		cout << "\n\n\nSzavakat adok neked, te pedig\nírd be a fordítást!\nVissza a menübe: írd: ###\n\n";
	        		int bad=0, good=0, f;
	        		bool lang = (justc?true:justt?false:ot%(pc*2)>=pc?true:false);

	        		for (int i=0;i<linenum+badsum;++i){
	        			for (int k=0; k<linenum; ++k)
	        				if (eredetiwa[k][0] == wa[i][0]) {
	        					f=k;
	        					break;
	        				}
	        			if (!(ind[f].state[lang?1:0] == 1 && rand()%100+1<(ind[f].value[lang?1:0]<7 ? ind[f].value[lang?1:0]*15 : 95))){
							if (lang)
	        					cout <<wa[i][0];
	        				else
	        					cout<<wa[i][1];
	        				cout << ": ";
	        				cin >> gett;
	        				if (lang?gett == wa[i][1]:gett==wa[i][0]){
	        					cout << "Helyes! :)";
	        					++good;
								++gubear[f][lang?1:0];
	        				}
							else if(gett =="###")
		        			{
		        				cout<<"\nEredmény: "<<good<<" helyes, "<<bad<<" helytelen -> "<<(float)good/(float)(good+bad)*100<<"%";
	    	    				cin.ignore();
	        					cin.get();
	        					inf.close();
	        					goto AGAIN2;
	        				}
	        				else {
	        					cout << "Helytelen! :(\nA helyes válasz: ";
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
	        		cout << "Végiggyakoroltad!\nEredmény: "<<good<<" helyes, "<<bad<<" helytelen -> "<<(float)good/(float)(good+bad)*100<<"%";
	        		cin.ignore();
	        		cin.get();
	        		inf.close();
	        		ofstream outf;
	        		outf.open("szavak.txt", ofstream::out | ofstream::trunc);
	        		for (int i=0; i<linenum; ++i){
	        			outf<<toparr[i]<<"\n";
	        			outf<<eredetiwa[i][0]<<"\n";
	        			outf<<gubear[i][0]<<"\n";
	        			outf<<eredetiwa[i][1]<<"\n";
	        			outf<<gubear[i][1]<<"\n";
	        		}
	        		outf.close();
	        		goto AGAIN2;
	        	}








				case 3:{
					ifstream inf;
					inf.open("szavak.txt", ios::in);
					int ot =0, linenum=0;
	        		string chw, tran, gett, topic2, words, gbnumc="", gbnumt="", gbnums="", stopics="";
	        		while (1){
	        			chw = "";
	        			tran = "";
	        			getline(inf, topic2);
	        			stopics+=topic2+";";
	        			getline(inf, chw);
	        			getline(inf, gbnumc);
	        			getline(inf, tran);
	        			getline(inf, gbnumt);
	        			if(chw==""||tran=="") break;
	        			words += chw+"^"+tran+";";
	        			gbnums+=gbnumc+"^"+ gbnumt+";";
	        			++linenum;
	        		}

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
					if (cg){
						cout << "\n\nNémet szavak, melyeknek "<<goodlimit<<", vagy több az indexe:\n\n";
						for (int i=0; i<linenum; ++i)
							if (gubear[i][0]>=goodlimit){
								cout << "\t-" << wa[i][0] << " : " << gubear[i][0] << 100-(ind[i].value[0]<7 ? ind[i].value[0]* 15 : 95)<<"%)"<< endl; ++gsum;
							}
					}
					if (eg){
						cout << "\n\nMagyar szavak, melyeknek "<<goodlimit<<", vagy több az indexe:\n\n";
						for (int i=0; i<linenum; ++i)
							if (gubear[i][1]>=goodlimit){
								cout << "\t-" << wa[i][1] << " : " << gubear[i][1] << " ("<<100-(ind[i].value[1]<7 ? ind[i].value[1]* 15 : 95)<<"%)"<<endl; ++gsum;
							}
					}
					if (cb) {
						cout << "\n\nNémet szavak, melyeknek "<<badlimit<<", vagy kevesebb az indexe:\n\n";
						for (int i=0; i<linenum; ++i)
							if (gubear[i][0]<=badlimit){
								cout << "\t-" << wa[i][0] << " : " << gubear[i][0] << " (+"<< ind[i].value[0]<<")"<<endl; ++bsum;
							}
					}
					if (eb){
						cout << "\n\nMagyar szavak, melyeknek "<<badlimit<<", vagy kevesebb az indexe:\n\n";
						for (int i=0; i<linenum; ++i)
							if (gubear[i][1]<=badlimit){
								cout << "\t-" << wa[i][1] << " : " << gubear[i][1] << " (+"<< ind[i].value[1]<<")"<< endl; ++bsum;
							}
					}
					cout<<(cg||cb||eg||eb?"\nA többi":"\nMinden szó ")<<badlimit<<" és "<<goodlimit<<" között van.";
					cout << "\n\nÖsszesen: " << gsum/((float)linenum*2)*100 << "% jó, és "<< bsum/((float)linenum*2)*100<< "% rossz szó.";
					cin.ignore();
					cin.get();
					goto AGAIN2;
				}






	        	case 4:{
	        		char sure;
	        		cout << "Biztos? (i/n): ";
	        		cin >> sure;
	        		if (sure=='i'||sure=='I'){
	        			cout<<"Tényleg? (i/n): ";
	        			cin >> sure;
	        			if (sure=='i'||sure=='I'){
	        				ofstream file;
	        				file.open("szavak.txt", ofstream::out | ofstream::trunc);
	        				file.close();
	        				cout << "\nOk, kitöröltem a fájl tartalmát / létrehoztam a fájlt.";
	        				cin.ignore(1);
	        				cin.get();
	        				goto AGAIN2;
	        			}
	        		}
	        		break;
	        	}
	        	case 5:{
	        		cout << "\nVissza a menübe:\n";
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