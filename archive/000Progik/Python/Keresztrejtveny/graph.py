def graph(arr, layer=0, letters=1, word=0, graphized=[]):
	if layer==0:
		graph(arr, layer=1, graphized=graphized)
		return graphized
	elif letters<len(arr[word]):
		graphized.append(arr[word][letters-1])
		graphized.append([])
		part=graphized[len(graphized)-1]
		new_index=graph(arr, layer+1, letters=letters+1, graphized=part)
	elif word<len(arr):
		cur_word=word
		while cur_word<len(arr) and arr[word][:letters-1] == arr[cur_word][:letters-1]:
			if len(arr[word]) == len(arr[cur_word]):
				graphized.append(arr[cur_word][letters-1])
			elif len(arr[cur_word-1])<len(arr[cur_word]) and arr[cur_word-1][letters-1] == arr[cur_word][letters-1]:
				graphized.append([])
				part=graphized[len(graphized)-1]
				new_index=graph(arr, layer+1, letters+1, cur_word, part)
			cur_word+=1
		return cur_word
		
			
cucc=["abcd", "abce", "abcea", "abceb", "abcf", "abcg"]
print(graph(cucc))
			
			
		