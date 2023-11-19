import re
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from scientific_text_indicators import TextIndicators

class ScLakhas:
    def __init__(self, num_phrases=3, input_text=None):
        """
        Initializes the SMASummarizer instance.

        Parameters:
        - num_phrases (int): Number of phrases to extract in the summary.
        - input_text (str): The input text for summarization.
        """
        self.num_phrases = num_phrases
        self.input_text = input_text

    def text_segmentation(self):
        """
        Segments the text into sentences using NLTK's sent_tokenize.

        Parameters:
        - text (str): The input text.

        Returns:
        - List[str]: List of sentences.
        """
        return sent_tokenize(self.input_text)

    def phrases_segmentation(self, sentence):
        """
        Tokenizes a sentence into words and appends '\n\n' to the end.

        Parameters:
        - sentence (str): The input sentence.

        Returns:
        - List[str]: List of words with '\n\n' at the end.
        """
        return word_tokenize(sentence) + ['\n\n']

    def normalization(self, text):
        """
        Normalizes the text by transforming uppercase to lowercase, replacing acronyms,
        formatting values like dates and numbers, handling contractions, and removing diacritics.

        Parameters:
        - text (str): The input text.

        Returns:
        - List[str]: List of tokenized and normalized phrases.
        """
        # Transform uppercase to lowercase, leaving proper nouns
        text = ' '.join([word.lower() if word.islower() or word.isupper() else word for word in text.split()])

        # Acronyms and Abbreviations
        acronyms_and_abbreviations = {
            'usa': 'USA',
            'u.s.a.': 'USA',
            's.m.a': 'SMA',
            'sma': 'SMA',
            'etc.': 'et cetera',
            'e.g.': 'for example',
            'i.e.': 'that is',
            'fig.': 'figure',
            'eq.': 'equation'
            # Add more as needed
        }
        for acronym, expansion in acronyms_and_abbreviations.items():
            text = re.sub(fr'\b{re.escape(acronym)}\b', expansion, text)

        # Format values like dates and numbers
        text = re.sub(r'\b(\d+|\d+\.\d+)\b', lambda x: str(int(float(x.group(0)))), text)
        text = re.sub(r'\b(\d{1,2} \w+ \d{4}|\d{1,2}\.\d{1,2}\.\d{2,4})\b', 'DATE', text)
        text = re.sub(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b', 'EMAIL', text)

        contractions = {
            "y’ll": "you all",
            "they're": 'they are',
            "they've": 'they have',
            "can't": "cannot",
            "won't": "will not",
            "it's": "it is",
            "doesn't": "does not",
            "don't": 'do not',
            "hasn't": 'has not',
            "haven't": 'have not',
            "wasn't": 'was not'
        }
        for contraction, expansion in contractions.items():
            text = re.sub(fr'\b{re.escape(contraction)}\b', expansion, text)

        # Diacritics
        text = ''.join([c for c in text if ord(c) < 128])  # remove non-ASCII characters

        return self.phrases_segmentation(text)

    def remove_stopwords(self, words):
        """
        Removes stopwords from a list of words.

        Parameters:
        - words (List[str]): List of words.

        Returns:
        - List[str]: List of words without stopwords.
        """
        stop_words = set(stopwords.words('english'))
        return [word for word in words if word not in stop_words]

    def lemmatization(self, words):
        """
        Lemmatizes a list of words.

        Parameters:
        - words (List[str]): List of words.

        Returns:
        - List[str]: List of lemmatized words.
        """
        lemmatizer = WordNetLemmatizer()
        return [lemmatizer.lemmatize(word) for word in words]

    def frequency_calculation(self, words):
        """
        Calculates the frequency of each word in a list.

        Parameters:
        - words (List[str]): List of words.

        Returns:
        - Dict[str, int]: Dictionary with word frequencies.
        """
        word_freq = {}
        for word in words:
            if word in word_freq:
                word_freq[word] += 1
            else:
                word_freq[word] = 1
        return word_freq

    def weights_calculation(self, sentences, sentence, word_freq):
        """
        Calculates the weight of a sentence based on various criteria.

        Parameters:
        - sentences (List[str]): List of sentences.
        - sentence (str): The target sentence.
        - word_freq (Dict[str, int]): Dictionary with word frequencies.

        Returns:
        - float: The calculated weight of the sentence.
        """
        # Assign weights to each criterion
        C = 2
        K = 1.5
        CN = 1.2

        # Calculate weight based on word frequency
        sentence_weight = sum(word_freq.get(word, 0) for word in word_tokenize(sentence))

        # Check for cues
        sentence_weight += TextIndicators.get_cue_phrase_weight(sentence=sentence, density=C)

        # Check for keywords
        sentence_weight += TextIndicators.get_keywords_weight(sentence=sentence, density=K)

        # Connectivity of sentences
        previous_sentence = sentences[sentences.index(sentence) - 1] if sentences.index(sentence) > 0 else ''
        if previous_sentence:
            # Check for connectivity (overlap of words between sentences)
            overlap = len(set(word_tokenize(sentence)) & set(word_tokenize(previous_sentence)))
            sentence_weight += overlap * CN

        return sentence_weight

    def extract_n_most_weighted_phrases(self, sentences, word_freq):
        """
        Extracts the n most weighted phrases from a list of sentences.

        Parameters:
        - sentences (List[str]): List of sentences.
        - word_freq (Dict[str, int]): Dictionary with word frequencies.
        - n (int): Number of phrases to extract.

        Returns:
        - List[str]: List of the n most weighted phrases.
        """
        ranked_sentences = []
        for sentence in sentences:
            weight = self.weights_calculation(sentences, sentence, word_freq)
            ranked_sentences.append((sentence, weight))

        ranked_sentences.sort(key=lambda x: x[1], reverse=True)
        return [sentence for sentence, _ in ranked_sentences[:self.num_phrases]]

    def clean_spaces_and_commas(self, text):
        """
        Cleans spaces before periods and commas, removes spaces within parentheses,
        and replaces consecutive commas with a single comma.

        Parameters:
        - text (str): The input text.

        Returns:
        - str: The cleaned text.
        """
        # Remove space before each period or comma
        text = re.sub(r'\s+([.,])', r'\1', text)

        # Remove spaces within parentheses
        text = re.sub(r'\(\s+(\w+\s*\w*)\s+\)', r'(\1)', text)

        # Replace ", ," with a single comma
        text = re.sub(r',\s*,', ',', text)

        return text
    
    def process_text(self):
        """
        Processes the input text and returns the n most weighted phrases.

        Returns:
        - List[str]: List of the n most weighted phrases.
        """
        sentences = self.text_segmentation()

        processed_phrases, processed_words = [], []
        for sentence in sentences:
            phrases = self.phrases_segmentation(sentence)
            words = self.normalization(' '.join(phrases))
            words = self.remove_stopwords(words)
            words = self.lemmatization(words)
            processed_words.extend(words)
            processed_phrases.append((' '.join(words)).lstrip())

        word_frequency = self.frequency_calculation(processed_words)

        n_most_weighted_phrases = self.extract_n_most_weighted_phrases(processed_phrases, word_frequency)

        return n_most_weighted_phrases

    def summarize(self):
        """
        Displays the original and summarized text.

        Parameters:
        - original_text (str): The original input text.
        - summarized_text (List[str]): List of the n most weighted phrases.
        """
        summarized_text = self.process_text()

        print("************ Original Text ************")
        print(self.input_text)

        with open('./Summarized Text.txt', 'w') as f:
            f.write(self.clean_spaces_and_commas(''.join(summarized_text)))

        print("\n************ Summary ************")
        print(self.clean_spaces_and_commas(''.join(summarized_text)))
