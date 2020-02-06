
#Import all the required libraries
import os
from flask import Flask, render_template, redirect, request, url_for, flash
from werkzeug.utils import secure_filename
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


# Connection to MongoDB
app = Flask(__name__)
app.secret_key = 'This_is_secret_key'
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
    
    # Display the list of pets or No result found.
    mypet1=mongo.db.pet.find_one(mydata)
    if not mypet1: 
        flash('The pets is not available. Please search for other pets')
        return render_template("searchResult.html", pet=mypet,user=list(myuser))  
    else:
        return render_template("searchResult.html", pet=mypet,user=list(myuser))  



# Form for user to sign up user account
@app.route('/add_user')
def add_user():
    return render_template("add_user.html", pet=mongo.db.user.find())



# Insert user information to MongoDB database. Check if the username already exist.
@app.route('/insert_user/', methods=['POST'])
def insert_user():
    if request.method == 'POST':
        users = mongo.db.user
        existing_user = users.find_one({'userName' : request.form['userName']})
        
        if existing_user is None:
            mongo.db.user.insert_one({"userName":request.form.get('userName'), "userEmail": request.form.get('userEmail'), "userContact": request.form.get('userContact')} )
            myuser=mongo.db.user.find({"userName": request.form['userName']})
            return render_template("mylogin.html", user=myuser)
            
        flash('USER NAME ALREADY EXIST! PLEASE REGISTER WITH A DIFFERENT USER NAME.')
        return redirect(url_for('add_user'))
        # return 'User Name already exist! Please click back and register with a different User Name.'
    
    return render_template("add_user.html", pet=mongo.db.user.find())



# Form for user to add advertisment
@app.route('/add_adv/<user_id>')
def add_adv(user_id):
    return render_template("add_adv.html",user_id=user_id) 



# Insert pet information to MongoDB database
@app.route('/insert_adv/', methods=['POST'])
def insert_adv():
    mongo.db.pet.insert_one({"user_id": ObjectId(request.form.get('userID')), "petName": request.form.get('petName'), "petCat": request.form.get('petCat'), "gender": request.form.get('gender'), "color": request.form.get('color'), "age": request.form.get('age'), "description": request.form.get('description')} )
    mypet1=mongo.db.pet.find({"user_id": ObjectId(request.form.get("userID"))})
    return render_template("my_adv.html", pet=mypet1) 



# Go to the login page for user to log in their account
@app.route('/login')
def login():
    return render_template("login.html")



# Retrieve the details of the user from MongoDB. Check if the user name is valid.
@app.route('/mylogin', methods=['POST'])
def mylogin():
    myuser=mongo.db.user.find_one({"userName": request.form['login']})
    
    if myuser:
        myuser=mongo.db.user.find({"userName": request.form['login']})
        return render_template("mylogin.html", user=myuser)
    
    flash('INVALID USER NAME! PLEASE SIGN IN WITH A VALID USER NAME.')
    return redirect(url_for('login'))
   
   
   
# Update the user details to MongoDB
@app.route('/update_user/', methods=['POST'])
def update_user():
    query = {'_id':ObjectId(request.form.get('user_id'))}
    mongo.db.user.update(query, {"userName": request.form.get('myName'), "userEmail": request.form.get('myEmail'), "userContact": request.form.get('myContact')} )
    flash('Details Update Successfully.')
    myuser=mongo.db.user.find({"userName": request.form['myName']})
    return render_template("mylogin.html", user=myuser)



# Search and display the advertisment posted by the user
@app.route('/my_adv/<user_id>')
def my_adv(user_id):
    mypet=mongo.db.pet.find({"user_id":  ObjectId(user_id)})
    
    mypet1=mongo.db.pet.find_one({"user_id":  ObjectId(user_id)})
    if not mypet1:
        flash('You do not have any existing Advertisment. Please go back to add new Advertisment.')
        return render_template("my_adv.html", pet=mypet) 
    else:
        return render_template("my_adv.html", pet=mypet)  



# Insert pet information to MongoDB database
@app.route('/update_adv/', methods=['POST'])
def update_adv():
    query = {'_id':ObjectId(request.form.get('adv_id'))}
    mongo.db.pet.update(query, {"user_id": ObjectId(request.form.get('user_id')), "petName": request.form.get('petName'), "petCat": request.form.get('petCat'), "gender": request.form.get('gender'), "color": request.form.get('color'), "age": request.form.get('age'), "description": request.form.get('description')} )
    mypet1=mongo.db.pet.find({"user_id": ObjectId(request.form.get("user_id"))})
    flash('Advertisment Update Successfully.')
    return render_template("my_adv.html", pet=mypet1) 
      
      
      
# Delete the Advertisment
@app.route('/delete_adv/<adv_id>')
def delete_adv(adv_id):
    return render_template("deleteAdv.html",adv_id=adv_id) 
    
    
    
@app.route('/delete_adv2/', methods=['POST'])
def delete_adv2(): 
    adv_id=request.form.get('adv_id')
    mongo.db.pet.remove({'_id': ObjectId(adv_id)})
    return redirect(url_for('login'))
    
    
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)