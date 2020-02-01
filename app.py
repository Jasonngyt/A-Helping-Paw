
#Import all the required libraries
import os
from flask import Flask, render_template, redirect, request, url_for
from werkzeug.utils import secure_filename
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 

# Connection to MongoDB
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/home/ubuntu/enivroment/uploads'
app.config["MONGO_DBNAME"] = 'pet_adopt'
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')

mongo = PyMongo(app)

@app.route('/')

# Search for the advertisment
@app.route('/mysearch')
def mysearch():
    return render_template("index.html", pet=mongo.db.pet.find(), user=list(mongo.db.user.find()))

# Display the search Result
@app.route('/showsearch', methods=['POST'])
def showsearch():
    mykeyword = request.form.get('searchPetCat')
    mydata = {"petCat":  mykeyword}
    mypet=mongo.db.pet.find(mydata)
    myuser=mongo.db.user.find()
    return render_template("searchResult.html", pet=mypet,user=list(myuser))  

# Form for user to sign up user account
@app.route('/add_user')
def add_user():
    return render_template("add_user.html", pet=mongo.db.user.find())

# Insert user information to MongoDB database
@app.route('/insert_user/', methods=['POST'])
def insert_user():
    mongo.db.user.insert_one({"userName":request.form.get('userName'), "userEmail": request.form.get('userEmail'), "userContact": request.form.get('userContact')} )
    return redirect(url_for('mysearch'))

# Form for user to add advertisment
@app.route('/add_adv/<user_id>')
def add_adv(user_id):
    return render_template("add_adv.html",user_id=user_id) 

# Insert pet information to MongoDB database
@app.route('/insert_adv/', methods=['POST'])
def insert_adv():
    mongo.db.pet.insert_one({"user_id": ObjectId(request.form.get('userID')), "petName": request.form.get('petName'), "petCat": request.form.get('petCat'), "gender": request.form.get('gender'), "color": request.form.get('color'), "age": request.form.get('age'), "description": request.form.get('description')} )
    return redirect(url_for('mysearch'))

# Go to the login page for user to log in their account
@app.route('/login')
def login():
    return render_template("login.html")

# Retrieve the details of the user from MongoDB 
@app.route('/mylogin', methods=['POST'])
def mylogin():
    mykeyword = request.form.get('login')
    mydata = {"userName":  mykeyword}
    myuser=mongo.db.user.find(mydata)
    return render_template("mylogin.html", user=myuser)

# Update the user details to MongoDB
@app.route('/update_user/', methods=['POST'])
def update_user():
    query = {'_id':ObjectId(request.form.get('user_id'))}
    mongo.db.user.update(query, {"userName": request.form.get('myName'), "userEmail": request.form.get('myEmail'), "userContact": request.form.get('myContact')} )
    return redirect(url_for('mysearch'))

# Search and display the advertisment posted by the user
@app.route('/my_adv/<user_id>')
def my_adv(user_id):
    mypet=mongo.db.pet.find({"user_id":  ObjectId(user_id)})
    return render_template("my_adv.html", pet=mypet)  

# Insert pet information to MongoDB database
@app.route('/update_adv/', methods=['POST'])
def update_adv():
    query = {'_id':ObjectId(request.form.get('adv_id'))}
    mongo.db.pet.update(query, {"user_id": ObjectId(request.form.get('user_id')), "petName": request.form.get('petName'), "petCat": request.form.get('petCat'), "gender": request.form.get('gender'), "color": request.form.get('color'), "age": request.form.get('age'), "description": request.form.get('description')} )
    return redirect(url_for('mysearch'))
      
# Delete the Advertisment
@app.route('/delete_adv/<adv_id>')
def delete_adv(adv_id):
    return render_template("deleteAdv.html",adv_id=adv_id) 
    
@app.route('/delete_adv2/', methods=['POST'])
def delete_adv2(): 
    adv_id=request.form.get('adv_id')
    mongo.db.pet.remove({'_id': ObjectId(adv_id)})
    return redirect(url_for('mysearch'))
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)