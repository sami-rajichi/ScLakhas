class TextIndicators:
    """
    A class containing methods for handling cue phrases and keywords in scientific texts.
    """

    @staticmethod
    def cue_indicators():
        """
        Returns lists of bonus, stigma, and null indicators.

        Returns:
        - Tuple[List[str], List[str], List[str], List[str]]: Tuple containing bonus, stigma,
          and null indicators.
        """
        # Bonus Indicators (Positive)
        bonus = [
            "significant", "notable", "important", "remarkable", "crucial",
            "unique", "evident", "promising", "conclusive", "particular",
            "remarkably", "especially", "distinctive", "noteworthy", "pivotal",
            "essentially", "noteworthy", "strikingly", "advantageous", "influential",
            "positively", "substantially", "considerably", "markedly", "profoundly"
        ]

        # Stigma Indicators (Negative)
        stigma = [
            "limitation", "challenge", "constraint", "drawback", "shortcoming",
            "deficiency", "impediment", "barrier", "restriction", "pitfall",
            "downside", "flaw", "hindrance", "disadvantage", "weakness",
            "obstacle", "difficulty", "impairment", "inadequacy", "deterrent",
            "disadvantageous", "inhibitor", "obstruction", "issue", "concern"
        ]

        # Null Indicators (Neutral)
        nulls = [
            "participant", "methodology", "procedure", "variable", "measurement",
            "parameter", "control", "comparison", "analysis", "implication",
            "aspect", "facet", "element", "factor", "component",
            "detail", "feature", "attribute", "characteristic", "consideration",
            "dimension", "part", "segment", "portion", "respect",
            "circumstance", "condition", "context", "situation", "variable",
            "factor", "consideration", "variable", "condition", "aspect",
            "observation", "feature", "characteristic", "element", "parameter"
        ]

        # Combine all indicators
        return bonus+stigma+nulls, bonus, stigma, nulls

    @staticmethod
    def keywords_indicators():
        """
        Returns a list of single-word keyword indicators for health and genetics.

        Returns:
        - List[str]: List of single-word keyword indicators.
        """
        keyword_indicators = [
        "genetic", "genomic", "mutation", "allele", "polymorphism", "sequencing", "genome",
        "expression", "variant", "inheritance", "phenotype", "genotype", "molecular", "biomarker",
        "health", "disease", "prevention", "treatment", "clinical", "epidemiology", "public_health",
        "precision", "outcome", "population", "disparity",
        "chronic", "promotion", "lifestyle", "healthcare", "wellness", "intervention",
        "determinant", "community", "management", "policy",
        "factor", "innovation", "research", "equity",
        "delivery", "care", "global", "preventive",
        "advancement", "analysis", "impact", "screening", "markers",
        "screen", "diagnosis", "therapy", "protocol", "study",
        "protocol", "screen", "diagnosis", "therapy", "protocol",
        "study", "outcome", "association", "risk", "factors",
        "healthcare", "regulation", "biological", "geneticist", "screen",
        "data", "patient", "medicine", "precision", "trial",
        "genotype", "outcomes", "community", "population", "genetic",
        "molecular", "laboratory", "biological", "population", "cell",
        "population", "behavior", "socioeconomic", "morbidity", "mortality",
        "intervention", "treatment", "pathway", "public", "protocol"
        ]
        return keyword_indicators

    @staticmethod
    def get_cue_phrase_weight(sentence, density):
        """
        Calculates the weight of cue phrases in a sentence based on density.

        Parameters:
        - sentence (str): The target sentence.
        - density (float): The density factor.

        Returns:
        - float: The calculated weight of cue phrases in the sentence.
        """
        cue_weight = 0
        indicators = TextIndicators.cue_indicators()
        # Check for cue phrases
        for cue in indicators[0]:
            if cue in sentence:
                if cue in indicators[1]:
                    cue_weight += 2
                elif cue in indicators[2]:
                    cue_weight -= 1
                elif cue in indicators[3]:
                    cue_weight += 0
        return density * cue_weight

    @staticmethod
    def get_keywords_weight(sentence, density):
        """
        Calculates the weight of keywords in a sentence based on density.

        Parameters:
        - sentence (str): The target sentence.
        - density (float): The density factor.

        Returns:
        - float: The calculated weight of keywords in the sentence.
        """
        keywords_weight = 0
        indicators = TextIndicators.keywords_indicators()
        # Check for cue phrases
        for keyword in indicators:
            if keyword in sentence:
                keywords_weight += 1.5
        return density * keywords_weight