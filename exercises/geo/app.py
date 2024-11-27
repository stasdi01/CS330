#!/usr/bin/env python3
"""
Geography query app

@authors:
@version: 2024.11
"""

import pathlib
import sqlite3

from dotenv import load_dotenv
from flask import Flask, abort, flash, redirect, render_template, request, url_for
from werkzeug.wrappers import Response


def create_app():
    """Create Flask app"""
    this_app = Flask(__name__)
    if pathlib.Path(".flaskenv").exists():
        this_app.config.from_prefixed_env()
    else:
        load_dotenv("exercises/geo/.flaskenv")
        this_app.config.from_prefixed_env()
    return this_app


app = create_app()


def get_data_from_db(query: str, params: tuple | None = None) -> list:
    """Retrieve data from the database

    :param query: parametrized query to execute
    :param params: query parameters
    """
    db_path = pathlib.Path("world.sqlite3")

    if not db_path.exists():
        db_path = pathlib.Path("exercises/geo/world.sqlite3")
    
    if not db_path.exists():
        raise FileNotFoundError("There is no database file")
    try:
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            return [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []


@app.route("/")
def index() -> str:
    """Display default page"""
    return render_template("index.html")


@app.get("/country")
def country_form():
    """Display country search form"""
    query = "SELECT DISTINCT name FROM country ORDER BY name;"
    countries = get_data_from_db(query)
    return render_template("country.html", countries=countries, entity="Country")


@app.get("/country/<string:name>")
def country_info(name: str):
    """Display country information"""
    query = """
    SELECT 
        c.name,
        CASE 
            WHEN ci.name IS NULL OR ci.name = 'N/A' THEN '' 
            ELSE ci.name 
        END as capital,
        c.continental_region,
        COALESCE(c.subregion, '') as subregion,
        c.area,
        COALESCE(c.population_2023, 0) as population,
        CASE 
            WHEN c.area > 0 AND c.population_2023 IS NOT NULL 
            THEN ROUND(CAST(c.population_2023 AS FLOAT) / c.area, 2)
            ELSE 0
        END as density,
        COALESCE(c.government_system, '') as government
    FROM country c
    LEFT JOIN city ci ON c.capital = ci.id
    WHERE c.name = ?;
    """
    result = get_data_from_db(query, (name,))
    if not result:
        abort(404, description=f"Country '{name}' not found.")
    return render_template("index.html", data=result[0])


@app.get("/region")
def region_form() -> str | Response:
    """Display region search form"""
    
    query = "SELECT DISTINCT continental_region FROM country ORDER BY continental_region;"
    regions = get_data_from_db(query)
    return render_template("region.html", regions=regions, entity="Region")

@app.get("/region/<string:name>")
def region_info(name: str):
    """Display region information"""
    
    query = """
    SELECT 
        c.name,
        COALESCE(ci.name, '') as capital,
        c.continental_region,
        COALESCE(c.subregion, '') as subregion,
        c.area,
        COALESCE(c.population_2023, 0) as population,
        CASE 
            WHEN c.area > 0 AND c.population_2023 IS NOT NULL 
            THEN ROUND(CAST(c.population_2023 AS FLOAT) / c.area, 2)
            ELSE 0
        END as density,
        COALESCE(c.government_system, '') as government
    FROM country c
    LEFT JOIN city ci ON c.capital = ci.id
    WHERE c.continental_region = ?
    ORDER BY c.name;
    """
    results = get_data_from_db(query, (name,))
    if not results:
        abort(404, description=f"Region '{name}' not found.")
    return render_template("index.html", data=results)

@app.get("/subregion")
def subregion_form() -> str | Response:
    """Display subregion search form"""
    
    query = "SELECT DISTINCT subregion FROM country WHERE subregion IS NOT NULL ORDER BY subregion;"
    subregions = get_data_from_db(query)
    return render_template("subregion.html", subregions=subregions, entity="Subregion")


from urllib.parse import unquote
@app.get("/subregion/<string:name>")
def subregion_info(name: str):
    """Display subregion information"""
    name = unquote(name)
    query = """
    SELECT 
        c.name,
        COALESCE(ci.name, '') as capital,
        c.continental_region,
        COALESCE(c.subregion, '') as subregion,
        c.area,
        COALESCE(c.population_2023, 0) as population,
        CASE 
            WHEN c.area > 0 AND c.population_2023 IS NOT NULL 
            THEN ROUND(CAST(c.population_2023 AS FLOAT) / c.area, 2)
            ELSE 0
        END as density,
        COALESCE(c.government_system, '') as government
    FROM country c
    LEFT JOIN city ci ON c.capital = ci.id
    WHERE c.subregion = ?
    ORDER BY c.name;
    """
    results = get_data_from_db(query, (name,))
    if not results:
        abort(404, description=f"Subregion '{name}' not found.")
    return render_template("index.html", data=results)


@app.errorhandler(404)
def not_found(err):
    
    return render_template("index.html", error=str(err)), 404


if __name__ == "__main__":
    app.run()
