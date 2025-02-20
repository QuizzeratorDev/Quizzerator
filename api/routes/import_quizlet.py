from typing import List, Dict, Optional
from bs4 import BeautifulSoup
import logging
from dataclasses import dataclass
from time import sleep
from random import uniform
import requests
import json
from zenrows import ZenRowsClient

@dataclass
class QuizTerm:
    term: str
    definition: str

class QuizletError(Exception):
    """Custom exception for Quizlet-related errors"""
    pass
headers = {
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
  'accept-encoding': 'gzip, deflate, br',
  'accept-language': 'en-US,en;q=0.9',
  'cache-control': 'max-age=0',
  'cookie': 'yourcookie',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-site': 'none',
  'sec-fetch-user': '?1',
  'upgrade-insecure-requests': '1',
  'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 12239.92.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.136 Safari/537.36',
}
class Quizlet:
    """A class to scrape and parse Quizlet flashcard sets"""
    
    # Known possible class names for term containers
    TERM_CLASSES = [
        'svzelo6',
        'SetPageTerm-content',
        'SetPageTerm-wordSide',
        'SetPageTerm-definitionSide',
        'SetPageTerm-smallSide',
        'TermText notranslate',
        'SetPageTerm-side',
        'SetPageTerms-term'
    ]
    
    def __init__(self, quiz_url: str, api_key: str):
        if not quiz_url or not quiz_url.startswith('https://quizlet.com/'):
            raise ValueError("Invalid Quizlet URL provided")
        self.client = ZenRowsClient(api_key)
        self.quiz_url = quiz_url
        self.logger = self._setup_logger()
        
    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger('QuizletScraper')
        logger.setLevel(logging.DEBUG)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger

    def _find_terms_with_class(self, soup: BeautifulSoup, class_name: str) -> List:
        """Try to find terms using a specific class name"""
        terms = soup.find_all('div', class_=class_name)
        self.logger.debug(f"Found {len(terms)} elements with class '{class_name}'")
        if terms:
            return terms

    def get_quiz(self) -> List[QuizTerm]:
        self.logger.info(f"Fetching quiz from URL: {self.quiz_url}")
        
        try:
            # Enhanced parameters for better JavaScript rendering
            params = {"js_render":"true","wait_for":"div.SetPageTerm-content"}
            
            response = self.client.get(self.quiz_url, params=params, headers=headers)
            response.raise_for_status()
            
            self.logger.debug(f"Response status code: {response.status_code}")
            self.logger.debug(f"Response headers: {response.headers}")
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Save full HTML for debugging
            with open('debug_output.html', 'w', encoding='utf-8') as f:
                f.write(soup.prettify())
            self.logger.debug("Saved full HTML to debug_output.html")
            
            # Try to find terms using various methods
            terms = []
            
            # 1. Try embedded JSON data first
            terms = self._try_extract_from_script(soup)
            if terms:
                self.logger.info(f"Successfully extracted {len(terms)} terms from embedded JSON")
                return [QuizTerm(term=t['term'], definition=t['definition']) for t in terms]
            
            # 2. Try different known class names
            for class_name in self.TERM_CLASSES:
                terms = self._find_terms_with_class(soup, class_name)
                if terms:
                    self.logger.info(f"Found {len(terms)} terms using class '{class_name}'")
                    break
            
            if not terms:
                # Look for any divs with 'term' in the class name
                self.logger.debug("Searching for elements with 'term' in class name...")
                all_elements = soup.find_all(class_=True)
                term_elements = [el for el in all_elements if 'term' in el.get('class', [''])[0].lower()]
                self.logger.debug(f"Found {len(term_elements)} elements with 'term' in class name")
                if term_elements:
                    self.logger.debug("Sample term elements found:")
                    for el in term_elements[:3]:
                        self.logger.debug(f"Class: {el.get('class')}")
                        self.logger.debug(el.prettify()[:200])
                
                raise QuizletError("No terms found in the quiz")
            
            quiz_terms = []
            for term in terms:
                # Try various selectors for terms and definitions
                term_text = term.find('span', class_='TermText')
                if not term_text:
                    term_text = term.find('div', class_=lambda x: x and 'word' in x.lower())
                
                definition = term.find_next('span', class_='TermText')
                if not definition:
                    definition = term.find_next('div', class_=lambda x: x and 'definition' in x.lower())
                
                if term_text and definition:
                    quiz_terms.append(QuizTerm(
                        term=term_text.get_text(strip=True),
                        definition=definition.get_text(strip=True)
                    ))
            
            self.logger.info(f"Successfully collected {len(quiz_terms)} terms")
            return quiz_terms
            
        except requests.exceptions.RequestException as e:
            raise QuizletError(f"Failed to fetch quiz content: {str(e)}")
        except Exception as e:
            raise QuizletError(f"Error processing quiz content: {str(e)}")

    def get_quiz_dict(self) -> List[Dict[str, str]]:
        return [{"term": term.term, "definition": term.definition} 
                for term in self.get_quiz()]

if __name__ == "__main__": 
    try:
        scraper = Quizlet("https://quizlet.com/gb/559378704/de-romanis-chapter-4-verbs-flash-cards", "54573b0923c1b2ae75797a28b6b438e0525a8383") # Quizlet set then ZenRows API key
        terms = scraper.get_quiz()  # Get list of QuizTerm objects
        # Or get dictionary format
        terms_dict = scraper.get_quiz_dict()
        
        print(terms)
        print("\n -------------------------------- \n")
        print(terms_dict)
    except QuizletError as e:
        print(f"Error: {e}")