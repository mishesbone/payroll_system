import os
import re
import logging
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Try to download NLTK resources, handle offline scenarios
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
except Exception as e:
    print(f"NLTK data download failed: {e}")

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class NLPProcessor:
    """
    Natural Language Processing for interpreting payroll-related queries
    """
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        
        # Try to get stopwords, handle case if NLTK data isn't available
        try:
            self.stop_words = set(stopwords.words('english'))
        except:
            self.stop_words = set()
        
        # Define intents and their keywords
        self.intent_keywords = {
            'salary_info': ['salary', 'pay', 'earning', 'wage', 'compensation', 'income', 'paycheck'],
            'attendance': ['attendance', 'present', 'absent', 'late', 'leave', 'sick', 'vacation'],
            'tax': ['tax', 'deduction', 'withholding', 'taxable'],
            'report': ['report', 'summary', 'stats', 'statistics', 'analytics', 'trend'],
            'employee_info': ['employee', 'staff', 'personnel', 'worker', 'person'],
            'department_info': ['department', 'division', 'team', 'unit', 'group'],
            'overtime': ['overtime', 'extra hours', 'additional time', 'extra work'],
            'benefits': ['benefit', 'insurance', 'retirement', 'pension', '401k', 'bonus'],
            'payroll_schedule': ['schedule', 'payment date', 'payday', 'cycle'],
            'comparison': ['compare', 'difference', 'versus', 'vs', 'against', 'than']
        }
        
        # Entity patterns (for regex extraction)
        self.entity_patterns = {
            'employee_id': r'(?:employee|staff|worker)\s*(?:id|number|#)?\s*[:#]?\s*(\w+\d+|\d+)',
            'employee_name': r'(?:employee|staff|worker)?\s*(?:name)?\s*[:#]?\s*([A-Z][a-z]+\s+[A-Z][a-z]+)',
            'date': r'(\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{2,4}[-/]\d{1,2}[-/]\d{1,2})',
            'month': r'(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)',
            'year': r'(?:year|yr)?\s*[:#]?\s*(20\d{2})',
            'department': r'(?:department|dept|division|team)?\s*[:#]?\s*([A-Za-z]+(?:\s+[A-Za-z]+)*)',
            'amount': r'(?:amount|sum|total)?\s*[:#]?\s*(\$?\d+(?:,\d{3})*(?:\.\d{2})?)',
            'percentage': r'(\d+(?:\.\d+)?\s*%)',
            'comparison_period': r'(?:compare|comparison|vs|versus)\s+(\w+\s+\d{4})\s+(?:to|and|with)\s+(\w+\s+\d{4})'
        }
        
    def preprocess_text(self, text):
        """Preprocess text by tokenizing, removing stopwords and lemmatizing"""
        text = text.lower()
        tokens = word_tokenize(text)
        tokens = [self.lemmatizer.lemmatize(word) for word in tokens if word not in self.stop_words]
        return tokens
    
    def analyze_query(self, query_text):
        """
        Analyze a natural language query to identify intent and entities
        """
        try:
            processed_tokens = self.preprocess_text(query_text)
            processed_text = ' '.join(processed_tokens)
            
            intent_scores = {intent: sum(1 for keyword in keywords if keyword.lower() in processed_text)
                             for intent, keywords in self.intent_keywords.items()}
            
            intent = max(intent_scores, key=intent_scores.get) if any(intent_scores.values()) else 'unknown'
            
            entities = {entity: re.findall(pattern, query_text) for entity, pattern in self.entity_patterns.items()}
            entities = {k: v[0] if v else None for k, v in entities.items()}
            
            time_references = {
                'last month': datetime.now() - timedelta(days=30),
                'last year': datetime.now().year - 1,
                'this month': datetime.now().month,
                'this year': datetime.now().year,
                'previous quarter': (datetime.now().month - 1) // 3
            }
            
            for ref, value in time_references.items():
                if ref in query_text.lower():
                    entities[ref] = value
            
            return intent, entities
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return 'error', {}

# Example Usage
if __name__ == "__main__":
    nlp = NLPProcessor()
    query = "What was my salary in July 2023?"
    intent, entities = nlp.analyze_query(query)
    print(f"Intent: {intent}\nEntities: {entities}")
