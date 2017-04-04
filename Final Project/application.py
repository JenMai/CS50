#TODO
# Delete goals when delete in sheet
# set proper comments

from flask import Flask, flash, redirect, render_template, request, url_for
import sqlite3
import ast

#--------------------
# Configure app
#--------------------
app = Flask(__name__)
app.secret_key = "It's Owl Stretching Time"                                                 # only for flash() purpose.

#--------------------
# Configure pointer for database
#--------------------
conn = sqlite3.connect("bulletdb.db", check_same_thread=False)
conn.row_factory = sqlite3.Row
db = conn.cursor()

#--------------------
# Generate table according to sheet
#--------------------
@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        sheetEdit = request.get_data().decode('utf-8')                                      # get Ajax's POST from any action from index
        sheetEdit = ast.literal_eval(sheetEdit)                                             # turn into proper Python object
        
        if sheetEdit['action'] == 0:                                                        # if user clicked on delete
            db.execute("DELETE FROM journal WHERE task_id = ?", [sheetEdit['taskID']])
            conn.commit()
            db.execute("DELETE FROM goals WHERE task_id = ?", [sheetEdit['taskID']])
            conn.commit()
            db.execute("DELETE FROM reflinks WHERE task_id = ?", [sheetEdit['taskID']])
            conn.commit()
            
            flash("Deleted!")
            return "deleted"
            
        if sheetEdit['action'] == 1:                                                        # if user reset timer
            db.execute("""UPDATE journal SET mindone = 0, minleft = obj_int 
                        WHERE task_id = ? """, [sheetEdit['taskID']])
            conn.commit()
            
            flash("Timer reset!")
            return "reset"

    else:                                                                                   # generate sheet on GET request
        db.execute("SELECT * FROM journal ORDER BY task") 
        taskSheet = db.fetchall()
        taskDicts = []
        
        for elements in taskSheet:                                                          # dictionary factory : https://docs.python.org/3/library/sqlite3.html#row-objects
            dict = {}                                                                       # kinda for fun and readability on index.html
            row = tuple(elements)
            keys = tuple(elements.keys())
            
            for i in range(len(row)):
                dict[keys[i]] = row[i]
            
            taskDicts.append(dict)
            
        totalLeft = 0
        totalDone = 0
            
        for task in taskDicts:
            totalLeft += task['minleft']
            totalDone += task['mindone']
        
        return render_template("index.html", tasks=taskDicts, totalLeft=totalLeft,\
                                totalDone=totalDone)
        

#--------------------
# Render /add or receive new task
#--------------------   
@app.route('/add', methods=["GET", "POST"])
def add():
    if request.method == "POST":
        addData = request.get_data().decode('utf-8')
        addData = ast.literal_eval(addData)
        
        result = (addData['task'], addData['objective'], addData['minute'], \
                    0, addData['goal'], addData['minute'])
        
        db.execute("SELECT task FROM journal WHERE task = ?", [addData['task']])
        
        if any(db.fetchall()):                                                               # check if task already exists
            flash("Task already exist!")
            return "already exist"
        
        db.execute("""INSERT INTO journal(task, objective, minleft, mindone, goal, obj_int) 
                    VALUES(?, ?, ?, ?, ?, ?)""", result)
        conn.commit()
        
        flash("New task added!")
        return redirect(url_for("index"))
        
    else:
        return render_template("add.html")
        
        
#--------------------
# Render subgoal page according to task, receive AJAX according to events
#--------------------
@app.route('/goal', methods=["GET", "POST"])
def goal():
    if request.method == "POST":
        subData = request.get_data().decode('utf-8')
        subData = ast.literal_eval(subData)
        
        if subData['action'] == 1:                                                           # if user is adding a subgoal
            db.execute("INSERT INTO goals(task_id, subgoal) VALUES(?, ?)", \
                        [subData['taskID'], subData['subgoal']])
            conn.commit()
            
            flash("New sub-goal added!")
            return "subgoal added"
            
        if subData['action'] == 0:                                                           # if user is deleting subgoals (checked box)
            sqlDelete="DELETE FROM goals WHERE sub_id in ({seq})".format( 
                    seq=','.join(['?']*len(subData['subgoalsID'])))                          # prepare SQL command based on size of array:
                                                                                             # http://stackoverflow.com/questions/5766230/select-from-sqlite-table-where-rowid-in-list-using-python-sqlite3-db-api-2-0
            db.execute(sqlDelete, subData['subgoalsID'])
            conn.commit()
            
            flash("Deleted!")
            return "deleted"
            
        if subData['action'] == 2:                                                           # if user is marking subs as done (checked box)
            sqlUpdate="UPDATE goals SET done = 1 WHERE done = 0 AND sub_id in ({seq})".format( \
                    seq=','.join(['?']*len(subData['subgoalsID']))) 
                    
            db.execute(sqlUpdate, subData['subgoalsID'])
            conn.commit()
            
            flash("Marked as done!")
            return "done"
    

    else:
        if not request.args.get("g"):                                                       # ensure proper usage for query
            raise RuntimeError("Missing task for goal")
            
        g = [request.args.get("g", None)]

        db.execute("SELECT task_id, task, goal FROM journal WHERE task = ?", g)
        queryCheck = list(db.fetchone())
        
        if any(queryCheck) == False:
            return redirect(url_for("index"))                                               # return to index if queried goal page doesn't exist
        
        db.execute("""SELECT sub_id, subgoal, done FROM goals WHERE task_id = ? 
                    ORDER BY subgoal""", [queryCheck[0]])
        getSub = db.fetchall()
        
        if any(getSub) == False:
            getSub = None
            #return render_template("goal.html", task=queryCheck, subgoals=getSub)

        return render_template("goal.html", task=queryCheck, subgoals=getSub)               # go to queried goal page, according to task

#--------------------
# Render subgoal page according to task, receive AJAX according to events (similar to goal)
#--------------------
@app.route('/references', methods=["GET", "POST"])
def ref():
    if request.method == "POST":
        refData = request.get_data().decode('utf-8')
        refData = ast.literal_eval(refData)
        
        if refData['action'] == 1:
            db.execute("INSERT INTO reflinks(task_id, reference, link) VALUES(?, ?, ?)", \
                        [refData['taskID'], refData['refTitle'], refData['link']])
            conn.commit()
            
            flash("New reference added!")
            return "ref added"
            
        if refData['action'] == 0:
            sqlDelete="DELETE FROM reflinks WHERE ref_id in ({seq})".format(
                    seq=','.join(['?']*len(refData['refsID'])))                      

            db.execute(sqlDelete, refData['refsID'])
            conn.commit()
            
            flash("Deleted!")
            return "deleted"

    else:
        if not request.args.get("r"):
            raise RuntimeError("Missing task for references")
            
        r = [request.args.get("r", None)]

        db.execute("SELECT task_id, task FROM journal WHERE task = ?", r)
        queryCheck = list(db.fetchone())
        
        if any(queryCheck) == False:
            return redirect(url_for("index"))
        
        db.execute("""SELECT ref_id, reference, link FROM reflinks WHERE task_id = ? 
                    ORDER BY reference""", [queryCheck[0]])
        getRef = db.fetchall()
        
        if any(getRef) == False:
            getRef = None

        return render_template("reference.html", task=queryCheck, references=getRef)

#--------------------
# Render timer page according to task, receive AJAX to update timer
#--------------------
@app.route('/timer', methods=["GET", "POST"])
def timer():
    if request.method == "POST":
        timerData = request.get_data().decode('utf-8')
        timerData = ast.literal_eval(timerData)
        
        db.execute("SELECT minleft, mindone FROM journal WHERE task_id = ? ",\
        [timerData['taskID']])
        taskSheet = list(db.fetchone())

        taskSheet[1] += timerData['minutes']                                               # add timer's result to the total done so far
        
        if (taskSheet[0] - timerData['minutes']) < 0:                                      # prevent negative value for minleft on sheet
           taskSheet[0] = 0
           
        else:
           taskSheet[0] -= timerData['minutes']                                            # subtract timer's result from time left
            
        result = [taskSheet[0], taskSheet[1], timerData['taskID']]
        
        db.execute("UPDATE journal SET minleft = ?, mindone = ? WHERE task_id = ? ",\
                    result)
        conn.commit()
        
        flash("Time added!")
        return "time updated"
        
    else:
        if not request.args.get("t"):                                                      # ensure proper usage for query
            raise RuntimeError("Missing task for timer")
            
        t = [request.args.get("t", None)]
        db.execute("SELECT task_id, task FROM journal WHERE task = ?", t)
        queryCheck = list(db.fetchone())
        
        if any(queryCheck) == False:
            return redirect(url_for("index"))
        
        return render_template("timer.html", task=queryCheck)                             # go to queried timer page, according to task