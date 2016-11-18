def get_category(tweet):
	final_cat = []
	#FILTERS stores the user-defined categories which can be chosen 
	FILTERS = ['sports', 'politics', 'business', 'music', 'tech', 'health', 'finance', 'india', 'books', 'celebrity']
	for category in FILTERS:
		if category in tweet:
			final_cat.append(category)
	return final_cat


