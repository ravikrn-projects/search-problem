from django.http import HttpResponse, JsonResponse
import random
from collections import defaultdict
from django.shortcuts import render

def index(request):
	global result_data, results, serial_score, token_dict
	result_data = get_data()
	results = get_sample(0.1, result_data)
	#distinct_words = get_distinct_words(results)
	serial_score = map_serial_score(results)
	token_dict = get_hash(results)
	return render(request, 'index.html', {})

def get_search(request):
	params = request.GET
	query = str(params['query']).split(',')
	query = [item.strip() for item in query]
	print query
	data = get_review(query)
	response = {'search_data': data}
	return JsonResponse(response)

def get_data():
	results = []
	i = 0
	dict1 = {}
	with open('/Users/ravikirangunale/Downloads/finefoods.txt') as inputfile:
		for line in inputfile:			
			try:			
				if i % 9 == 0:					
					dict1['product_id'] = line.strip().split(': ')[1]
				elif i % 9 == 1:
					dict1['user_id'] = line.strip().split(': ')[1]
				elif i % 9 == 2:
					dict1['profileName'] = line.strip().split(': ')[1]
				elif i % 9 == 3:
					dict1['helpfulness'] = line.strip().split(': ')[1]
				elif i % 9 == 4:
					dict1['score'] = line.strip().split(': ')[1]
				elif i % 9 == 5:
					dict1['review_time'] = line.strip().split(': ')[1]
				elif i % 9 == 6:
					dict1['review_summary'] = line.strip().split(': ')[1]
				elif i % 9 == 7:
					dict1['review_text'] = line.strip().split(': ')[1]
				else :
					dict1['id'] = int(i/9)
					results.append(dict1)			
					dict1 = {}
				i+=1
			except IndexError:
				pass
	return results

def get_sample(ratio, result):
	num = int(len(result)*ratio)
	#return result[:num]
	return random.sample(result, num)

def get_distinct_words(text_list):
	distinct_words = []
	for text in text_list:		
		try:
			text_str = text['review_summary']
			distinct_words.extend(text_str.split(' '))
			text_str = text['review_text']
			distinct_words.extend(text_str.split(' '))
		except KeyError:
			print text
	return list(set(distinct_words))	

def get_frequency(document_list):
	freq = {}
	for serial in document_list:
		try:
			freq[serial] += 1
		except:
			freq[serial] = 1
	return freq

def get_hash(text_list):
	token_dict = defaultdict(list)
	for text in text_list:

			summary = text['review_summary'].split(' ')
			review = text['review_text'].split(' ')
			unique_words = list(set(review+summary))
			#freq gives word and count dict
			for word in unique_words:
				token_dict[word].append(text['id'])
	return token_dict

def top_documents(serial_score, document_dict, count):
	doc_list = []
	for serial, value in document_dict.iteritems():
		doc_list.append((serial, value, serial_score[serial]))
	return sorted(doc_list, key=lambda x: (x[1], x[2]), reverse=True)[:count]	

def get_documents(serial_score, token_dict, query, count):
	document_list = []
	for term in query:
		document_list.extend(token_dict[term])
	document_dict = get_frequency(document_list)
	#print document_dict[11265], 'testing'	
	return top_documents(serial_score, document_dict, count) 

def map_serial_score(results):
	serial_score = {}
	for item in results:
		serial = item['id']
		score = item['score']
		serial_score[serial] = score
	return serial_score

def get_review(query):
	#result_data = get_data()
	#results = get_sample(0.1, result_data)
	#distinct_words = get_distinct_words(results)
	#serial_score = map_serial_score(results)
	#token_dict = get_hash(results)
	k = 20
	result = []
	final_documents = get_documents(serial_score, token_dict, query, k)
	for doc in final_documents:
		result.append(result_data[doc[0]])
	return result	