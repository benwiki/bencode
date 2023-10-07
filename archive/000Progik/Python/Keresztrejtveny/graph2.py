from time import sleep, time

def graph(arr, layer=0, letters=1, word=0, graphized=[]):
	
	if layer==0:
		graph(arr, layer=1, graphized=graphized)
		return graphized
		
	elif letters<=len(arr[word]) and word<len(arr):
		cur_word=word
		
		while cur_word<len(arr) and arr[word][:letters-1] == arr[cur_word][:letters-1]:
			new_index=cur_word
			
			if arr[cur_word][letters-1] not in graphized:
				graphized.append(arr[cur_word][letters-1])
			
			if letters < len(arr[cur_word]):
				if arr[cur_word-1][:letters]==arr[cur_word][:letters] and cur_word>0:
					graphized.append([''])
				else:
					graphized.append([])
				part=graphized[len(graphized)-1]
				new_index=graph(arr, layer+1, letters+1, cur_word, part)
				
			if new_index==cur_word:
				cur_word+=1
			else: cur_word=new_index
			
		return cur_word
		
	return word
	
	
def search(graph, word, letter=0):
	wlen=len(word)
	if letter<wlen and word[letter] in graph:
		list_ind=graph.index(word[letter])+1
		if len(graph)>list_ind:
			part=graph[list_ind]
			if isinstance(part, list):
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

print(graph(cucc))

"""f=open('Sort_lemma.txt', 'r', encoding='latin-1')
print('Filet megnyitottam')
kivalogat=[szo.split()[0].lower() for szo in f if len(szo.split())!=0]
print('Kivalogattam')
kivalogat.sort()
f.close()

print("Elkezdtem graffa alakitani")

t=time()
ready=graph(kivalogat)

print('I am ready, it was', str(time()-t), 'seconds.')

f=open('graph.txt', 'w')
f.write(str(ready))
f.close()

print("File saved successfully.")
			
#YESSSSSS DONEEEEEEEE
#138 másodperc volt a sort lemmát feldolgozniaaaaa!
#k******* gyors!!!!!!"""