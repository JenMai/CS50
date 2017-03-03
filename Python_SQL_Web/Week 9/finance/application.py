from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import gettempdir
import time

from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = gettempdir()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():
    cashCheck = db.execute("SELECT cash FROM users WHERE id = :user_id", \
                            user_id=session["user_id"])                                      # get cash for dollar format
    
    cashUser = usd(cashCheck[0]["cash"])
    
    portfolio = any(db.execute("SELECT * FROM transactions WHERE user_id = :user_id",\
                    user_id=session["user_id"]))                                             # check if returns a list of dict
    
    if portfolio == False:                                                                   # if empty, display empty sheet
        portfolio = [{'symbol': '0',
                    'names': '0',
                    'shares': 0,
                    'price': 0,
                    'total': 0,
                    }]
        grdTotal = cashUser
        return render_template("index.html", portfolio=portfolio, cashUser=cashUser, \
                                grdTotal= grdTotal) 
        
    portfolio = db.execute("""SELECT symbol, name, SUM(shares) AS shares, 
                            price, SUM(total) AS total FROM transactions WHERE 
                            user_id = :user_id GROUP BY symbol""", user_id=session["user_id"]) # sum values in portfolio
    
    sumTotal = db.execute("""SELECT SUM(total) AS sumTotal FROM transactions WHERE 
                            user_id= :user_id""", user_id=session["user_id"])
                            
    grdTotal = cashCheck[0]["cash"] + sumTotal[0]["sumTotal"]                                  # sum cash and shares
    grdTotal = usd(grdTotal)
    
    for i in range(0,len(portfolio)):                                                          # set values to a proper money format
       portfolio[i]["price"] = usd(portfolio[i]["price"])
       portfolio[i]["total"] = usd(portfolio[i]["total"])
    
    return render_template("index.html", portfolio=portfolio, cashUser=cashUser, \
                            grdTotal=grdTotal)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock.// TODO"""
    
    if request.method == "POST":                                                                # if user is sending forms (POST request)
        
        if not request.form.get("quote"):                                                       # ensure proper usage for inputs
            return apology("missing symbol")
            
        elif not request.form.get("share"):
            return apology("no share entered")
            
        elif request.form.get("share").isalpha():
            return apology("invalid input for shares")
            
        inptShares = int(request.form.get("share"))
            
        if inptShares < 1: 
            return apology("invalid number of shares")
        
        lkCheck = lookup(request.form.get("quote"))
        
        if lkCheck == None:                                                                     # if no symbol found
            return apology("invalid symbol")
            
        total = lkCheck["price"] * inptShares
        cashCheck = db.execute("SELECT cash FROM users WHERE id = :user_id", \
                                user_id=session["user_id"])                                     # get current cash
        
        if cashCheck[0]["cash"] < total:                                                        # check if user can afford shares
            return apology("unaffordable share(s)")
        
        cashCheck[0]["cash"] -= total
        
        db.execute("""INSERT INTO transactions VALUES (:user_id, :symbol, 
                    :name, :shares, :price, :total, :date)""",user_id=session["user_id"], \
                    symbol=lkCheck["symbol"], name=lkCheck["name"], shares=inptShares, \
                    price=lkCheck["price"], total=total, date=time.strftime('%Y-%m-%d %H:%M:%S'))
        
        db.execute("UPDATE users SET cash = :cash where id= :user_id", cash=cashCheck[0]["cash"],\
        user_id=session["user_id"])
        
        flash("Bought!")
        return redirect(url_for("index"))

    else:                                                                                       # if page requested with GET
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions. //TODO"""
    
    transHistory = db.execute("""SELECT symbol, shares, price, date 
                            FROM transactions WHERE user_id = :user_id ORDER BY date DESC""", \
                            user_id=session["user_id"])
    print(transHistory)
    
    for i in range(0,len(transHistory)):                                                        # set values to dollar format
        transHistory[i]["price"] = usd(transHistory[i]["price"])
        
    return render_template("history.html", transHistory=transHistory)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()
    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote. //TODO"""
    if request.method == "POST":
        
        if not request.form.get("quote"):                                                         # if form is let blank
            return apology("missing symbol")
            
        lkCheck = lookup(request.form.get("quote"))
        
        if lkCheck == None:                                                                       # if no symbol found
            return apology("invalid symbol")
            
        else:
            lkName, lkSymbol = lkCheck["name"], lkCheck["symbol"]                                 # get the values from dict returned
            lkPrice = usd(lkCheck["price"]) # format price
            return render_template("quoted.html", name=lkName, symbol=lkSymbol, price=lkPrice)
        
    else: # if page requested with GET
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user. // TODO """
    if request.method == "POST":
        
        if not request.form.get("username"):                                                      # ensure proper usage
            return apology("missing username")
           
        elif not request.form.get("password"):
            return apology("missing password")
            
        elif not request.form.get("confirmPassword"):
            return apology("must confirm password")
            
        elif request.form.get("password") != request.form.get("confirmPassword"):                 # ensure password has no typo
            return apology("passwords don't match")
        
        hash = pwd_context.encrypt(request.form.get("password"))                                  # encrypt password for database
        
        result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",\
                            username=request.form.get("username"), hash=hash)                     # ensure username doesn't exist
        
        if not result:                                                                            # if query returns an error
            return apology("username already exists")
        
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
        
        session["user_id"] = rows[0]["id"]                                                        # connect user if successfully signed in
        
        return redirect(url_for("index"))
        
    else:                                                                                         # if page requested with GET
        return render_template("register.html")
        
@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    """Change user's password. // TODO (personal touch) """
    if request.method == "POST":
           
        if not request.form.get("password"):                                                      # ensurer proper usage
            return apology("missing password")
            
        pwCheck = db.execute("SELECT hash FROM users WHERE id = :user_id",\
                            user_id=session["user_id"])
                            
        if not pwd_context.verify(request.form.get("password"), pwCheck[0]["hash"]):              # ensure old password is correct
            return apology("invalid password")
            
        elif not request.form.get("newPassword"):
            return apology("missing password")
            
        elif not request.form.get("confirmPassword"):
            return apology("must confirm password")
            
        elif request.form.get("newPassword") != request.form.get("confirmPassword"):              # ensure password has no typo
            return apology("new passwords don't match")
            
        elif request.form.get("newPassword") == request.form.get("password"):                     # ensure passwords are different
            return apology("passwords are identical")
        
        hash = pwd_context.encrypt(request.form.get("newPassword"))                               # encrypt password for database
        
        db.execute("UPDATE users SET hash = :hash WHERE id = :user_id",\
                    hash=hash, user_id=session["user_id"])
        
        return redirect(url_for("index"))
        
    else:
        return render_template("settings.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock. //TODO"""
    if request.method == "POST":
        
        if not request.form.get("quote"):                                                         # ensure proper usage for inputs
            return apology("missing symbol")
            
        elif not request.form.get("share"):
            return apology("no share entered")
            
        elif request.form.get("share").isalpha():
            return apology("invalid input for shares")
            
        inptShares = int(request.form.get("share"))
        
        if inptShares < 1: 
            return apology("invalid number of shares")
        
        lkCheck = lookup(request.form.get("quote"))                                               # sell at stock's current price (+checking)
        
        if lkCheck == None:
            return apology("invalid symbol")
        
        symbCheck = db.execute("""SELECT SUM(shares) AS shares FROM transactions WHERE user_id = :user_id
                                AND symbol = :symbol""",user_id=session["user_id"],\
                                symbol=lkCheck["symbol"])

        if (symbCheck[0]["shares"] == None) or (symbCheck[0]["shares"] == 0):                     # check if user owns shares
            return apology("no share owned")
            
        elif symbCheck[0]["shares"] < inptShares:
            return apology("too many shares")

        total = lkCheck["price"] * inptShares                                                     # prepare and update cash with current price
        
        cashCheck = db.execute("SELECT cash FROM users WHERE id = :user_id", \
                                user_id=session["user_id"])
                                
        cashCheck[0]["cash"] += total

        db.execute("UPDATE users SET cash = :cash where id= :user_id", cash=cashCheck[0]["cash"],\
        user_id=session["user_id"])
        
        inptShares *= -1                                                                          # update for index
        total *= -1

        db.execute("""INSERT INTO transactions VALUES (:user_id, :symbol, 
                    :name, :shares, :price, :total, :date)""",user_id=session["user_id"], \
                    symbol=lkCheck["symbol"], name=lkCheck["name"], shares=inptShares, \
                    price=lkCheck["price"], total=total, date=time.strftime('%Y-%m-%d %H:%M:%S')) # update values
                    
        flash("Sold!")
                    
        return redirect(url_for("index"))
    
    else:
        return render_template("sell.html")
