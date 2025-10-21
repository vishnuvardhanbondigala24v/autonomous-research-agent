import spacy

nlp = spacy.load("en_core_web_sm")

def extract_triples(text):
    """
    Extracts subject-verb-object triples from text using spaCy.

    Args:
        text (str): Input text.

    Returns:
        List[Tuple[str, str, str]]: List of (subject, relation, object) triples.
    """
    triples = []
    doc = nlp(text)

    for sent in doc.sents:
        subj = ""
        obj = ""
        verb = ""

        for token in sent:
            if "subj" in token.dep_:
                subj = token.text
            elif "obj" in token.dep_:
                obj = token.text
            elif token.pos_ == "VERB":
                verb = token.lemma_

        if subj and verb and obj:
            triples.append((subj, verb, obj))

    return triples
