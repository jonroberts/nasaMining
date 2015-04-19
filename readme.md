SpaceTag Automatic Keyword Extraction
=====================================

NASA SpaceApps 2015
-------------------

Instructions - Keyword Extraction
---------------------------------

**TBD**

Instructions - Related Datasets (Word Embedding Method)
-------------------------------------------------------

**keyword_similarity_vec.py**

Run keyword_similarity_vec.py to generate the keyword vectors
    
- This depends on the word embedding vectors provided by the Spacy library (<a href="http://honnibal.github.io/spaCy/">http://honnibal.github.io/spaCy/</a>)
- Vectors for multi-word keyphrases are produced by adding together the vectors of each individual word. The motivation for this is 
     that the word embedding vectors exhibit the same semantically meaningful algebraic properties as other word2vec embeddings. E.g. 
     when considering the keywords "earth science" and "geology", the cosine similarity between V<sub>earth</sub> + V<sub>science</sub> 
     and V<sub>geology</sub> is much closer than between either V<sub>earth</sub> or V<sub>science</sub> individually  

**project_similarity_vec_centroid.py**

Run project_similarity_vec_centroid.py to calculate the 25 most similar datasets for each dataset based on the cosine similarity between mean keyword vectors.
    
- Each dataset contains some number of keywords, N, each with their own vector representation of dimension D; in order to simplify the distance calculation 
     between one dataset with a keyword matrix K<sub>1</sub> of dimension N<sub>1</sub> x D, and a second with K<sub>2</sub> of dimension N<sub>2</sub> x D,
     we take the mean value across keywords for each dimension in D, producing 1 x D centroid vectors C<sub>1</sub> and C<sub>2</sub>. 
     Project similarities are then calculated by taking the cosine distance between each centroid vector.
- The related datasets will be inserted into a mongo collection

Instructions - Related Datasets (Synsets Method)
------------------------------------------------

Generating project similiarty scores is a two step process, and there are two scripts that must be run:

**keyword_similarity.py**:

This generates a similarty score for every pair of words among all keywords. So the keywords 'earth science',
'atmosphere', and 'air quality' would product a five words [earth, science, atmosphere, air, quality] and
10 pairs. Words are not pair with themselves, are case insensitive, and are unordered.

For each pair of words a core between 0 and 1 is set, 0 being not at all related and 1 being identical. Each
element in the synset of the first word is compared to each in the synset of the second word. The highest scoring
pair is kept as the score for that pair of words. If either word is not in WordNet, the score is 0, unless
they happen to be identical, in which case it is 1.

Synset are groups of cognitively related words and are available as a free resource as part of WordNet. 
More info is available at <a href="https://wordnet.princeton.edu/">https://wordnet.princeton.edu/</a>

The similarty function path_similarity() is used, which measures "shortest path that connects the senses in the
is-a (hypernym/hypnoym) taxonomy". There are several other similarty function available, but there was not
enough time to test them all. See section 5 on <a href="http://www.nltk.org/howto/wordnet.html">http://www.nltk.org/howto/wordnet.html</a> for details.

This step is kept separate from the project level scores because it can take a very long time to run, and because
it may not be necesary to rerun when new projects are added if those new project only contain preexisting
keywords
	
To run: 

simply execute the script. The following values are hard coded:
		
		input:	data/nasa_kw.json
		output:	data/keyword_synset_scores.json
		
**project_similarty.py**:

This generates a similarty score for every pair of projects based on their keywords. Each individual word from
the keywords of one project are compared to the words from the keywords in a second project. Scores for each
pair of words are looked up from keyword data produced by the keyword similarty script. Those scores are 
simply summed together. The result is the similarty score between the two projects
	

Example:	

using the 2 projects in example.json
    
Project 1 contains the keywords "EARTH SCIENCE", "HYDROSPHERE", "SURFACE WATER" and project 2 contains
"EARTH SCIENCE", "ATMOSPHERE", "AIR QUALITY", "ATMOSPHERIC CHEMISTRY" 
    
Produces the list of words (note the 'u' in a python generated flag denoting Unicode)

    [u'earth', u'science', u'hydrosphere', u'surface', u'water', u'atmosphere', u'air', u'quality', u'atmospheric', u'chemistry']

The keyword script generates 45 scored pairs from these words:

		[{"score": 0.1111111111111111, "keyword": ["earth", "science"]},
		 {"score": 0.2, "keyword": ["earth", "hydrosphere"]},
		 {"score": 0.25, "keyword": ["earth", "surface"]},
		 {"score": 0.3333333333333333, "keyword": ["earth", "water"]},
		 {"score": 0.25, "keyword": ["earth", "atmosphere"]},
		 {"score": 0.3333333333333333, "keyword": ["earth", "air"]},
		 {"score": 0.25, "keyword": ["earth", "quality"]},
		 {"score": 0.25, "keyword": ["earth", "atmospheric"]},
		 {"score": 0.25, "keyword": ["earth", "chemistry"]},
		 {"score": 0.08333333333333333, "keyword": ["science", "hydrosphere"]},
		 {"score": 0.2, "keyword": ["science", "surface"]},
		 {"score": 0.1111111111111111, "keyword": ["science", "water"]},
		 {"score": 0.125, "keyword": ["science", "atmosphere"]},
		 {"score": 0.125, "keyword": ["science", "air"]},
		 {"score": 0.14285714285714285, "keyword": ["science", "quality"]},
		 {"score": 0.0, "keyword": ["science", "atmospheric"]},
		 {"score": 0.3333333333333333, "keyword": ["science", "chemistry"]},
		 {"score": 0.3333333333333333, "keyword": ["hydrosphere", "surface"]},
		 {"score": 0.125, "keyword": ["hydrosphere", "water"]},
		 {"score": 0.25, "keyword": ["hydrosphere", "atmosphere"]},
		 {"score": 0.25, "keyword": ["hydrosphere", "air"]},
		 {"score": 0.1, "keyword": ["hydrosphere", "quality"]},
		 {"score": 0.0, "keyword": ["hydrosphere", "atmospheric"]},
		 {"score": 0.1111111111111111, "keyword": ["hydrosphere", "chemistry"]},
		 {"score": 0.25, "keyword": ["surface", "water"]},
		 {"score": 0.25, "keyword": ["surface", "atmosphere"]},
		 {"score": 0.25, "keyword": ["surface", "air"]},
		 {"score": 0.25, "keyword": ["surface", "quality"]},
		 {"score": 0.25, "keyword": ["surface", "atmospheric"]},
		 {"score": 0.125, "keyword": ["surface", "chemistry"]},
		 {"score": 0.2, "keyword": ["water", "atmosphere"]},
		 {"score": 0.3333333333333333, "keyword": ["water", "air"]},
		 {"score": 0.2, "keyword": ["water", "quality"]},
		 {"score": 0.2, "keyword": ["water", "atmospheric"]},
		 {"score": 0.25, "keyword": ["water", "chemistry"]},
		 {"score": 1.0, "keyword": ["atmosphere", "air"]},
		 {"score": 0.5, "keyword": ["atmosphere", "quality"]},
		 {"score": 0.0, "keyword": ["atmosphere", "atmospheric"]},
		 {"score": 0.16666666666666666, "keyword": ["atmosphere", "chemistry"]},
		 {"score": 0.5, "keyword": ["air", "quality"]},
		 {"score": 0.3333333333333333, "keyword": ["air", "atmospheric"]},
		 {"score": 0.25, "keyword": ["air", "chemistry"]},
		 {"score": 0.0, "keyword": ["quality", "atmospheric"]},
		 {"score": 0.16666666666666666, "keyword": ["quality", "chemistry"]},
		 {"score": 0.0, "keyword": ["atmospheric", "chemistry"]}]
	
Note that 'air' and 'atmosphere' have a score of 1.0. This is because 'air' is in the synset for 'atmosphere'
and vice versa

air:

    [Synset('air.n.01'), Synset('air.n.02'), Synset('air.n.03'), Synset('breeze.n.01'), Synset('atmosphere.n.03'), 
     Synset('air.n.06'), Synset('tune.n.01'), Synset('air.n.08'), Synset('air_travel.n.01'), Synset('air_out.v.01'), 
     Synset('air.v.02'), Synset('air.v.03'), Synset('publicize.v.01'), Synset('air.v.05'), Synset('vent.v.02')]

atmosphere:

    [Synset('atmosphere.n.01'), Synset('standard_atmosphere.n.01'), Synset('atmosphere.n.03'), 
     Synset('atmosphere.n.04'), Synset('atmosphere.n.05'), Synset('air.n.03')]

A similarty matrix is created, measuring the distance between each word in synset 1 with each word in synset 2. The
highest score is kept. In this case, that is 1.0

The score the similarity of the 2 projects, they keywords of each are again broken into single word entities:

    [u'earth', u'science', u'hydrosphere', u'surface', u'water']
    [u'earth', u'science', u'atmosphere', u'air', u'quality', u'atmospheric', u'chemistry']

Each combination of words, using one from each set, is looked up in the similarity table. The following matches are
found, and contribute to the final sum score (all other pairs scored 0):

    (u'earth', u'earth', 1.0)
    (u'earth', u'science', 0.1111111111111111)
    (u'earth', u'quality', 0.25)
    (u'science', u'science', 1.0)
    (u'hydrosphere', u'science', 0.08333333333333333)
    (u'hydrosphere', u'quality', 0.1)
    
The final similarity score between these two project is then 2.5444444444444447

