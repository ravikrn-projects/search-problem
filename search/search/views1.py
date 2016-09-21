from django.http import HttpResponse, JsonResponse
import random
from collections import defaultdict
from django.shortcuts import render
import csv
import nltk

def index(request):
	import sys  
	reload(sys)  
	sys.setdefaultencoding('utf8')
	global result_data, results, serial_score, token_dict
	result_data = get_data()
	results = get_sample(0.1, result_data)
	write_to_csv(results)
	serial_score = map_serial_score(results)
	token_dict = get_hash(results)
	return render(request, 'index.html', {})

def write_to_csv(results):
	distinct_words = get_distinct_words(results)
	queries = get_random_queries(distinct_words)
	er_count = 0
	with open('distinct_words.csv', 'wb') as csvfile:
	
		try:
			fieldnames = ['word']
			writer = csv.writer(csvfile)
			#writer.writeheader()
			for word in queries:			
				writer.writerow([word])	
		except:
			er_count+=1
	print er_count, 'count', len(queries)

def get_random_queries(words):
	count = 100000
	query = []
	for i in range(count):
		query_length = random.randrange(1,11)
		new_query_list = random.sample(words, query_length)
		new_query = str(','.join(new_query_list))
		query.append(new_query)
	return query

def get_data():
	results = []
	i = 0
	dict1 = {}
	with open('/Users/ravikirangunale/Downloads/finefoods.txt') as inputfile:
		for line in inputfile:			
			try:
				value = line.strip().split(': ')[1]
				if i % 9 == 0:					
					dict1['product_id'] = value
				elif i % 9 == 1:
					dict1['user_id'] = value
				elif i % 9 == 2:
					dict1['profileName'] = value
				elif i % 9 == 3:
					dict1['helpfulness'] = value
				elif i % 9 == 4:
					dict1['score'] = value
				elif i % 9 == 5:
					dict1['review_time'] = value
				elif i % 9 == 6:
					dict1['review_summary'] = value
				elif i % 9 == 7:
					dict1['review_text'] = value
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
	return result[:num]
	#return random.sample(result, num)

def get_distinct_words(text_list):
	distinct_words = []
	for text in text_list:		
		try:
			text_str = text['review_summary']
			distinct_words.extend(text_str.split(' '))
			text_str1 = text['review_text']
			distinct_words.extend(text_str1.split(' '))
			# text_str = nltk.word_tokenize(text['review_summary'])
			# text_str1 = nltk.word_tokenize(text['review_text'])
			# distinct_words.extend(text_str+text_str1)
		except KeyError:
			print text, 'error'
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

			# summary = nltk.word_tokenize(text['review_summary'])
			# review = nltk.word_tokenize(text['review_text'])
			# unique_words = list(set(review+summary))
			#freq gives word and count dict
			for word in unique_words:
				token_dict[word].append(text['id'])
	return token_dict

def map_serial_score(results):
	serial_score = {}
	for item in results:
		serial = item['id']
		score = item['score']
		serial_score[serial] = score
	return serial_score

def get_search(request):
	params = request.GET
	query = str(params['query']).split(',')
	query = [item.strip() for item in query]
	data = get_review(query)
	print query
	response = {'search_data': data}
	try:
		return JsonResponse(response)
	except Exception as e:
		print query, e
		response = {'search_data': ['some_error']}
	return JsonResponse(response)

def get_search1(request):
	params = request.GET
	query = str(params['query']).split(',')
	query = [item.strip() for item in query]
	data = get_review1(query)
	print query
	response = {'search_data': data}
	try:
		return JsonResponse(response)
	except Exception as e:
		print query, e
		response = {'search_data': ['some_error']}
	return JsonResponse(response)

def top_documents(serial_score, document_dict, count):
	doc_list = []
	for serial, value in document_dict.iteritems():
		doc_list.append((serial, value, serial_score[serial]))
	return sorted(doc_list, key=lambda x: (x[1], x[2]), reverse=True)[:count]	

def top_documents(document_dict, count):
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

def get_documents1(query, count):
	document_list = []
	for term in query:
		if len(query) == 1:
			document_list.extend(token_dict[term][:20])
		else:	
			document_list.extend(token_dict[term])
	document_dict = get_frequency(document_list)
	#print document_dict[11265], 'testing'	
	return top_documents(document_dict, count) 


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

def get_review1(query):
	#result_data = get_data()
	#results = get_sample(0.1, result_data)
	#distinct_words = get_distinct_words(results)
	#serial_score = map_serial_score(results)
	#token_dict = get_hash(results)
	k = 20
	result = []
	final_documents = get_documents(query, k)
	for doc in final_documents:
		result.append(result_data[doc[0]])
	return result	