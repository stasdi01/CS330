#!/usr/bin/env python3
"""
Serving `pyjokes` via templates

@authors: Dimitrije Stasic
@version: 2024.10
"""

import random

import pyjokes
from flask import Flask, abort, render_template, request
from pyjokes.exc import PyjokesError

LANGUAGES = {
    "cs": "CZECH",
    "de": "GERMAN",
    "en": "ENGLISH",
    "es": "SPANISH",
    "eu": "BASQUE",
    "fr": "FRENCH",
    "gl": "GALICIAN",
    "hu": "HUNGARIAN",
    "it": "ITALIAN",
    "lt": "LITHUANIAN",
    "pl": "POLISH",
    "sv": "SWEDISH",
}

CATEGORIES = ["all", "chuck", "neutral"]
NUMBERS = range(1,10)

app = Flask(__name__)

@app.get("/")
def index():
    """Render the template with form"""
    return render_template("base.html", languages=LANGUAGES, categories=CATEGORIES, joke_count=NUMBERS)

@app.post("/")
def index_jokes():
    """Render the template with jokes"""
    if not request.form:
        abort(405)

    language = request.form.get("language", "en")
    category = request.form.get("category", "all")
    number = int(request.form.get("number", 1))
    
    jokes = get_jokes(language, category, number)
    
    return render_template("jokes.html", jokes=jokes, languages=LANGUAGES, categories=CATEGORIES, joke_count=NUMBERS)



def get_jokes(
    language: str = "en",
    category: str = "all",
    number: int = 1,
) -> list[str]:
    """Return a list of jokes"""
    try:
        jokes = pyjokes.get_jokes(language=language, category=category)
        if not jokes:
            return ["No kidding!"]

        return random.sample(jokes, min(len(jokes),number))
    except PyjokesError:
        return ["No kidding!"]

