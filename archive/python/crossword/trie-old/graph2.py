from time import sleep, time

def graph(arr, layer=0, letters=1, word=0, graphized=[]):
	
	if layer==0:
		graph(arr, layer=1, graphized=graphized)
		return graphized
		
	elif letters<=len(arr[word]) and word<len(arr):
		cur_word=word
		
		while cur_word<len(arr) and arr[word][:letters-1] == arr[cur_word][:letters-1]:
			new_index=cur_word
			
			if word==cur_word or arr[cur_word][letters-1] not in graphized:
				graphized.append(arr[cur_word][letters-1])
				#print("!!!!!!", arr[word], arr[cur_word], arr[cur_word][letters-1], layer)
			
			if letters < len(arr[cur_word]):
				#print("??????", cur_word)
				if arr[cur_word-1][:letters]==arr[cur_word][:letters] and cur_word>0:
					graphized.append([''])
				else:
					graphized.append([])
				part=graphized[len(graphized)-1]
				#print(graphized)
				new_index=graph(arr, layer+1, letters+1, cur_word, part)
				
			if new_index==cur_word:
				cur_word+=1
			else: cur_word=new_index
			
		return cur_word
		
	return word
	
	
def search(graph, word, letter=0):
	wlen=len(word)
	if letter<wlen and word[letter] in graph:
		#print(letter, word[letter], "*")
		list_ind=graph.index(word[letter])+1
		if len(graph)>list_ind:
			#print(list_ind, "**")
			part=graph[list_ind]
			if isinstance(part, list):
				#print(part, "***")
				return search(part,word,letter+1)
			elif letter==wlen-1:
				return True
			else:
				return False
		elif letter==wlen-1:
			return True
		else:
			return False
	elif '' in graph and letter==wlen:
		return True
	else:
		return False
		
			
cucc=["abcd", "abce", "abcea", "abceb", "abcf", "abcg", "abd", "abe", "abea", "abeb", "baba", "baby", "bad", "bads", "bejó", "bejön"]
#cucc=["a", "ab", "abc"]
#cucc=["ab", "abc",]
#cucc=["a", "b", "c", "cap"]

#not ready yet - check it!
#not too far from it, boi

#FINALLY READY, I did it instead of learning, hopefully it will help me someday.
f=open('Sort_lemma.txt', 'r', encoding='latin-1')
print('Filet megnyitottam')
kivalogat=[szo.split()[0].lower() for szo in f if len(szo.split())!=0]
print('Kivalogattam')
kivalogat.sort()
f.close()

print("Elkezdtem graffa alakitani")
t=time()
mygraph=graph(kivalogat)
print('Kesz vagyok, es ez', str(time()-t), 'masodperc volt.')

w="cucc"
print('Lassuk mennyi ido 100x a cucc?')
t=time()
for i in range(100):
	what=search(mygraph, w)
print("Ennyi:", str(time()-t), "sec")
print("És:", what)

"""f=open('graph.txt', 'w')
f.write(str(ready))
f.close()

print("File saved successfully.")
			
#YESSSSSS DONEEEEEEEE
#138 másodperc volt a sort lemmát feldolgozniaaaaa!
#k******* gyors!!!!!!"""
