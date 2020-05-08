import networkx as nx
import sys, getopt
import pickle
import os


CURRENT_DIR = os.path.dirname(__file__)
GRAPH_PKL_PATH = os.path.join(CURRENT_DIR, 'ppr_graph.pkl')
SYMPTOMS_PKL_PATH = os.path.join(CURRENT_DIR, 'ppr_symptoms.pkl')

class PPRSimilarSymptoms(object):


	def get_similar_symptoms(self, G, symptoms, personal_symptoms=[], similar_limit=5):

		result = []

		personal_symptoms = [i.lower() for i in personal_symptoms]
		personalized = dict()
		found = False
		for i in personal_symptoms:
			if i in symptoms:
				personalized[i] = 1
				found = True

		if not found: # user symptom not in db, returning empty list
			return result

		if len(personalized) > 0:
			pr = nx.pagerank(G, personalization= personalized,alpha=0.85)#, weight='weight')
		else:
			pr = nx.pagerank(G, alpha=0.85)
		ranking = [(key, val) for key, val in pr.items()]
		ranking = sorted(ranking, key=lambda x: x[1], reverse=True)
		counter = 0

		for u, v in ranking:
			if u not in personal_symptoms:
				if u == 'symptoms':
					continue
				counter += 1
				result.append(u)

				if counter >= similar_limit:
					break

		return result

if __name__ == "__main__":

    symptoms = []
    limit = 5
    try:
        args = getopt.getopt(sys.argv[1:], "hs:l:", ["symptoms=","limit="])
    except getopt.GetoptError:
      print('filename.py -s <comma-separated symptoms> -l <number of results required>')
      sys.exit(2)

    for arg in args[0]:
        if '-s' in arg:
            symptoms = str(arg[1]).split(",")
        if '-l' in arg:
            limit = int(arg[1])

    rankings = similar_symptoms(symptoms, limit)
    print("Results for entered symptoms -", ",".join(symptoms))
    [print(str(i+1) + '. ' + ranking) for i, ranking in enumerate(rankings)]
