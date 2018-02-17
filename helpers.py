import csv
import urllib.request
import json
import sys

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Renders message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(symbol):
    """Look up quote for symbol."""

    # reject symbol if it starts with caret
    if symbol.startswith("^"):
        return None

    # reject symbol if it contains comma
    if "," in symbol:
        return None
    """
    # query Yahoo for quote
    # http://stackoverflow.com/a/21351911
    
    try:

        # GET CSV
        url = "http://download.finance.yahoo.com/d/quotes.csv?f=snl1&s={}".format(symbol)
        webpage = urllib.request.urlopen(url)

        # read CSV
        datareader = csv.reader(webpage.read().decode("utf-8").splitlines())

        # parse first row
        row = next(datareader)

        # ensure stock exists
        try:
            price = float(row[2])
        except:
            return None

        # return stock's name (as a str), price (as a float), and (uppercased) symbol (as a str)
        return {
            "name": row[1],
            "price": price,
            "symbol": row[0].upper()
        }

    except:
        pass
    """

    # query bloomberg.com for quote
    # https://www.bloomberg.com
    # for json, https://stackoverflow.com/a/29494079
    # for https, terminal command: "/Applications/Python\ {your python version here}/Install\ Certificates.command"
    try:
        
        # GET json
        url = "https://www.bloomberg.com/markets/watchlist/recent-ticker/{}:US".format(symbol)
        webpage = urllib.request.urlopen(url)
        
        # parse jason page content
        data = json.loads(webpage.read().decode("utf-8"))
        
        # ensure stock exists
        try:
            check = data["ticker"]
        except:
            return None
        
        #store quote values: name, symbol and price
        qName = data["disp_name"]
        qSymbol = data["ticker"]
        qPrice = data["last_price"]
        
        # return stock's name (as a str), (uppercased) symbol (as a str) and price (as a float)
        return {
            'name': str(qName.upper()),
            'symbol': str(qSymbol.upper()),
            'price': float(qPrice)
    }
    
    except:
        pass


    # query iextrading.com api for quote instead
    # https://iextrading.com/developer/docs/
    # for https, terminal command: "/Applications/Python\ {your python version here}/Install\ Certificates.command"
    try:

        # GET json
        url = "https://api.iextrading.com/1.0/stock/{}/quote".format(symbol)
        webpage = urllib.request.urlopen(url)
        
        # parse jason page content
        data = json.loads(webpage.read().decode("utf-8"))

        # ensure stock exists
        try:
            check = data["symbol"]
        except:
            return None

        #store quote values: name, symbol and price
        qName = data["companyName"]
        qSymbol = data["symbol"]
        qPrice = data["latestPrice"]

        # return stock's name (as a str), (uppercased) symbol (as a str) and price (as a float)
        return {
            'name': str(qName.upper()),
            'symbol': str(qSymbol.upper()),
            'price': float(qPrice)
        }

    except:
        pass

    # query Alpha Vantage for quote instead
    # https://www.alphavantage.co/documentation/
    try:
    
        # GET CSV
        url = "https://www.alphavantage.co/query?apikey=NAJXWIA8D6VN6A3K&datatype=csv&function=TIME_SERIES_INTRADAY&interval=1min&symbol={}".format(symbol)
        webpage = urllib.request.urlopen(url)
    
        # parse CSV
        datareader = csv.reader(webpage.read().decode("utf-8").splitlines())
    
        # ignore first row
        next(datareader)
    
        # parse second row
        row = next(datareader)
    
        # ensure stock exists
        try:
            price = float(row[4])
        except:
            return None
    
        # return stock's name (as a str), price (as a float), and (uppercased) symbol (as a str)
        return {
            "name": symbol.upper(), # for backward compatibility with Yahoo
            "price": price,
            "symbol": symbol.upper()
        }

    except:
        return None


def usd(value):
    """Formats value as USD."""
    return f"${value:,.2f}"
