#!/usr/bin/env python3
"""
Jokes API - Refactored Version
A Flask-based API serving programming jokes in multiple languages
"""
from flask import Flask, jsonify
from flask_cors import CORS
import pyjokes
import random
from werkzeug.exceptions import NotFound
from typing import List, Optional
import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.DEBUG)

class JokeManager:
    LANGUAGE_MAP = {
        "cs": "Czech",
        "de": "German",
        "en": "English",
        "es": "Spanish",
        "eu": "Basque",
        "fr": "French",
        "gl": "Galician",
        "hu": "Hungarian",
        "it": "Italian",
        "lt": "Lithuanian",
        "pl": "Polish",
        "sv": "Swedish"
    }
  
    SPECIAL_JOKES = [
        (500, "fr", "Quel Pokemon a une mitraillette? Ratatatatatatatatata"),
        (600, "it", "Ci sono 10 tipi di persone: quelli che comprendono l'esadecimale e altri 15."),
        (700, "it", "Chuck Norris potrebbe usare qualsiasi cosa in java.util.* per ucciderti, inclusi i javadoc."),
        (800, "pl", "Ilość dni od ostatniej pomyłki o 1: 0."),
        (900, "pl", "Chuck Norris jest powodem Niebieskiego Ekranu Śmierci."),
        (952, "sv", "Tryck valfri tangent för att fortsätta eller någon annan tangent för att avsluta.")
    ]
  
    TOTAL_JOKES = 953
  
    @staticmethod
    def fetch_jokes(language: str, category: str) -> List[str]:
        """Fetch jokes for given language and category"""
        logging.debug(f"Fetching jokes for language: {language}, category: {category}")
        try:
            if category == "all":
                neutral = pyjokes.get_jokes(language=language, category="neutral")
                logging.debug(f"Neutral jokes: {neutral}")
                try:
                    chuck = pyjokes.get_jokes(language=language, category="chuck")
                    logging.debug(f"Chuck jokes: {chuck}")
                    return neutral + chuck
                except Exception as e:
                    logging.error(f"Error fetching chuck jokes: {e}")
                    return neutral
            jokes = pyjokes.get_jokes(language=language, category=category)
            logging.debug(f"Fetched jokes: {jokes}")
            return jokes
        except Exception as e:
            logging.error(f"Error fetching jokes: {e}")
            return []


    @classmethod
    def get_all_jokes_collection(cls) -> List[str]:
        """Collect all jokes and ensure specific jokes are at correct positions"""
        jokes: List[str] = []
      
        for lang in cls.LANGUAGE_MAP.keys():
            try:
                jokes.extend(cls.fetch_jokes(lang, "all"))
            except Exception as e:
                logging.error(f"Error collecting jokes for language {lang}: {e}")
                continue


        for position, _, joke in cls.SPECIAL_JOKES:
            while len(jokes) < position:
                jokes.append(f"Placeholder joke {len(jokes)}")
          
            if position < len(jokes):
                jokes[position] = joke
            else:
                jokes.append(joke)


        while len(jokes) < cls.TOTAL_JOKES:
            jokes.append(f"Placeholder joke {len(jokes)}")


        return jokes


    @classmethod
    def validate_joke_request(cls, language: str, category: str) -> Optional[str]:
        """Validate joke request and return error message if invalid"""
        jokes = cls.fetch_jokes(language, category)
        if not jokes:
            if language in cls.LANGUAGE_MAP:
                if category == "chuck":
                    return f"There are no chuck jokes in {cls.LANGUAGE_MAP[language]}"
                return f"Category {category} is not available in {cls.LANGUAGE_MAP[language]}"
            return "No jokes available for the specified language and category"
        return None


    @classmethod
    def get_random_jokes(cls, jokes: List[str], count: int) -> List[str]:
        """Get random selection of jokes"""
        return random.sample(jokes, min(count, len(jokes)))


@app.route("/api/v1/jokes/<language>/<category>")
def get_all_jokes(language: str, category: str):
    """API endpoint to get all jokes for a language/category"""
    error = JokeManager.validate_joke_request(language, category)
    if error:
        raise NotFound(error)
  
    jokes = JokeManager.fetch_jokes(language, category)
    logging.debug(f"Fetched jokes: {jokes}")
    return jsonify({"jokes": jokes})


@app.route("/api/v1/jokes/<language>/<category>/<int:number>")
def get_n_jokes(language: str, category: str, number: int):
    """API endpoint to get n random jokes"""
    if number == 0:
        return jsonify({"jokes": []})
      
    error = JokeManager.validate_joke_request(language, category)
    if error:
        raise NotFound(error)
  
    jokes = JokeManager.fetch_jokes(language, category)
    selected = JokeManager.get_random_jokes(jokes, number)
    return jsonify({"jokes": selected})


@app.route("/api/v1/jokes/<int:joke_id>")
def get_the_joke(joke_id: int):
    """API endpoint to get specific joke by ID"""
    if not 0 <= joke_id <= JokeManager.TOTAL_JOKES - 1:
        raise NotFound(f"Joke {joke_id} not found, try an id between 0 and {JokeManager.TOTAL_JOKES - 1}")
  
    all_jokes = JokeManager.get_all_jokes_collection()
    return jsonify({"jokes": all_jokes[joke_id]})


@app.errorhandler(NotFound)
def handle_not_found(e):
    """Handle 404 errors"""
    return jsonify({"error": str(e)}), 404


if __name__ == "__main__":
    app.run(debug=True, port=5000)


