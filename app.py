from flask import Flask , request , render_template, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models.model import User, BlogContant,db
from decorator.login_required import login_required
from datetime import datetime


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///blog.db'
app.config['SECRET_KEY'] = "my_blog"


db.init_app(app) # for connect flask to db


with app.app_context(): #for create all db tables
     db.create_all()




@app.route('/')
def Home():
    all_blog = BlogContant.query.all()
    return render_template('index.html', all_blog=all_blog)




@app.route('/register', methods=['GET','POST'])
def register():
     
    if request.method == 'POST':
       uname = request.form.get('uname')  
       upass = request.form.get('upass')  
       user = User.query.filter_by(uname=uname).first()
       new_pass = generate_password_hash(upass)

       if not user:
            new_user = User( uname = uname, upass = new_pass)
            db.session.add(new_user)
            db.session.commit()
            return redirect('/login') 
       else:
            return redirect('/login') 
     
    return render_template('register.html')


@app.route('/login', methods=['GET','POST'])
def login():

     if request.method == 'POST':
          uname = request.form.get('uname')
          upass = request.form.get('upass')

          user = User.query.filter_by(uname = uname).first()

          if user and check_password_hash(user.upass , upass):
               session['user'] = uname
               flash("Login successfully", "success")
               return redirect('/')
          else:
               return redirect('/register')
             
     

     return render_template('login.html')



@app.route('/logout')
def logout():

     session.pop('user', None)
     flash("Logged out successfully", "unsuccess")

     return redirect('/')




@app.route('/delete', methods=['GET', 'POST'])
def delete():
     uname = request.form.get('uname')
     upass = request.form.get('upass')
     user = User.query.filter_by(uname = uname).first()

     if user and check_password_hash(user.upass, upass):
          db.session.delete(user)
          db.session.commit()
          print('delete user successfully')
          return redirect('/')
     
     return render_template('delete.html')

#----------------------------------------------------------------------------------Blog Methords start

@app.route('/blog/<int:id>', methods=['GET', 'POST'])
def bogconte(id):  
                                                                 #{{ blog.clreated_at.strftime("%Y-%m-%d")}}
     blog = BlogContant.query.filter_by(blogId=id).first()

     return render_template('blog.html', blog = blog)



@app.route('/blog/MyBlog')
@login_required
def MyBlog():

     my_blog = BlogContant.query.filter_by(auther =session['user'])

     return render_template('MyBloge.html', my_blog=my_blog)



@app.route('/blog/create', methods=['GET', 'POST'])
@login_required
def BlogCreat():

     if request.method == 'POST':
          headline = request.form.get('headline')
          contant = request.form.get('contant')
          author = session['user']


          if headline and contant and author:
               new_blog = BlogContant(title = headline, contant = contant, auther=author)
               db.session.add(new_blog)
               db.session.commit()
               return redirect('/blog/MyBlog')
          else:
               print('if not working', headline)
               print('if not working', contant)
               print('if not working', author)
     
     return render_template('CreateBlog.html')


@app.route('/blog/update/<int:id>', methods=['GET', 'POST'])
@login_required
def BlogUpdate(id):
   

   blog = BlogContant.query.filter_by( blogId = id).first()
   if not blog.auther == session['user']:
             return redirect('/')
   
   if request.method == 'POST':
        
        title = request.form.get('headline')
        contant = request.form.get('contant')
        
        if title != '' :
             blog.title = title
          
        if contant != '':
             blog.contant = contant
               

        db.session.add(blog)
        db.session.commit()

        return redirect('/blog/MyBlog')    
     
   return render_template('update.html')



@app.route('/blog/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def BlogDelet(id):

     blogDel = BlogContant.query.filter_by(blogId=id).first()
     if not blogDel.auther == session['user']:
          return redirect('/')
     db.session.delete(blogDel)
     db.session.commit()

     return redirect('/blog/MyBlog')







if __name__ == "__main__":

     app.run(debug=True)