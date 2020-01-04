
#Import all the required libraries
import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 

# Connection to MongoDB
app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'pet_adopt'
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')

mongo = PyMongo(app)

@app.route('/')

# Search for the advertisment
@app.route('/mysearch')
def mysearch():
    return render_template("SearchPage.html", pet=mongo.db.pet.find(), user=list(mongo.db.user.find()))

# Display the search Result
@app.route('/showsearch', methods=['POST'])
def showsearch():
    mykeyword = request.form.get('searchPetCat')
    mydata = {"petCat":  mykeyword}
    mypet=mongo.db.pet.find(mydata)
    myuser=mongo.db.user.find()
    return render_template("searchResult.html", pet=mypet,user=list(myuser))  

# Form for user to key in new advertisment
@app.route('/add_adv')
def add_adv():
    return render_template("add_user.html", pet=mongo.db.user.find())

# Post the information to MongoDB database
@app.route('/insert_adv/', methods=['POST'])
def insert_adv():
    mongo.db.user.insert_one({"userName":request.form.get('userName'), "userEmail": request.form.get('userEmail'), "userContact": request.form.get('userContact')} )
    my_db=mongo.db.pet.find({"petName":request.form.get('userEmail')})

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/mylogin', methods=['POST'])
def mylogin():
    mykeyword = request.form.get('login')
    mydata = {"userName":  mykeyword}
    myuser=mongo.db.user.find(mydata)
    return render_template("mylogin.html", user=myuser)
    
@app.route('/update_adv/', methods=['POST'])
def update_adv():
    query = {'_id':ObjectId(request.form.get('userid'))}
    mongo.db.user.update(query, {"advID":request.form.get('myid'), "userName": request.form.get('myName'), "userEmail": request.form.get('myEmail'), "userContact": request.form.get('myContact')} )
    return redirect(url_for('mysearch'))

@app.route('/delete_adv/<user_id>')
def delete_adv(user_id):
    return render_template("deleteAdv.html",user_id=user_id) 
    
@app.route('/delete_adv2/', methods=['POST'])
def delete_adv2():
    adv_id=request.form.get('myid')
    mongo.db.user.remove({'_id': ObjectId(adv_id)})
    return redirect(url_for('mysearch'))
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)