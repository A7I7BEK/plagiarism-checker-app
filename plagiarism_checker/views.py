from django.shortcuts import render, redirect
from django.http import HttpResponse
import re
from googlesearch import search
from nltk.tokenize import sent_tokenize



def index(request):
	return render(request, 'index.html')


def result(request):

	# Get text from POST request and clean it
	post_text = request.POST['text']
	post_text_cleaned = clean_html(post_text)


	# Divide text into sentences using nltk.tokenize
	sentence_list = sent_tokenize(post_text_cleaned)
	sentence_all = []
	for x in sentence_list:
		sentence_all += x.split(', ')  # Divide sentences by comma(,)

	sentence_list = sentence_all.copy()  # Sentences are copied to iterate them again
	sentence_all = []
	for x in sentence_list:
		sentence_all += x.split('and ')  # Divide sentences by conjunction 'and'

	sentence_list = sentence_all.copy()
	sentence_all = []
	for x in sentence_list:
		sentence_all += x.split('but ')  # Divide sentences by conjunction 'but'

	sentence_list = sentence_all.copy()
	sentence_all = []
	for x in sentence_list:
		sentence_all += x.split('when ')  # Divide sentences by conjunction 'when'

	sentence_list = sentence_all.copy()
	sentence_all = []
	for x in sentence_list:
		sentence_all += x.split('if ')  # Divide sentences by conjunction 'if'


	# Remove strings with less than 2 words
	sentence_all = list(filter(lambda y: len(y.split()) > 2, sentence_all))


	# If no sentence then render another view
	if len(sentence_all) == 0:
		return render(request, 'index.html', {'error_message': True})


	search_found_source = []
	search_found_count = 0
	for x in sentence_all:
		temp_search_list = search_google('"' + x + '"')  # Search every sentence with Google

		if len(temp_search_list) > 0:
			search_found_count += 1  # Count found search result
			search_found_source.append({'key': x, 'value': temp_search_list})  # Create dictionary from search result


	# Calculate percentage of found sentences
	plagiarism_percent = (search_found_count / len(sentence_all)) * 100


	# Render all data
	return render(request, 'result.html', {'percent': plagiarism_percent, 'source': search_found_source, 'sentence_count': len(sentence_all)})





def clean_html(raw_html):
	clean_r = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
	clean_text = re.sub(clean_r, ' ', raw_html)
	clean_text = " ".join(clean_text.split())
	return clean_text


def search_google(text):
	search_result = []

	for item in search(text, tld="com", num=3, start=1, stop=3, pause=2):
		search_result.append(item)

	return search_result
