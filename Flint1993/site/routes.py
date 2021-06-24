# from forms import TForm
from Flint1993.models import Closet, User, db
from flask import Blueprint, render_template,request,redirect,url_for #1
from flask_login import login_required, current_user
site = Blueprint('site', __name__, template_folder='site_templates') #1 create site BP
from Flint1993.forms import ClosetForm


"""
IN the above code, some arguments are specified when creating the Blueprint object
This first argument 'site', is the Blueprint's name,
this will be used by flasks routing mechanism.
The second parameter __name__, is the BP's import name,
which flask uses to locate resources
"""
#1 home route
@site.route('/', methods = ['GET', 'POST']) 
def home():
    closet = Closet.query.all()
    return render_template('index.html', closet = closet)

#1 route to show feed 
@site.route('/explore')
@login_required
def explore():
    users=User.query.all()
    return render_template('explore.html', users=users)

# route to view personal info and closet
@site.route('/account' , methods = ['GET'])
@login_required
def account():
    closet=Closet.query.filter_by(user_id= current_user.id).all()
    form=ClosetForm()
    return render_template('account.html', closet=closet,form=form)

# route to view personal info and closet
@site.route('/usercloset/<id>' , methods = ['GET'])
@login_required
def user_closet(id):
    user = User.query.get(id)
    if current_user == user:
        return redirect (url_for('site.account'))
    else:
        user_closet=Closet.query.filter_by(user_id=id).all()
        return render_template('user_closet.html', user_closet=user_closet, user=user)
    

# delete items route
@site.route('/delete/<id>')
@login_required
def delete_item(id):
        item=Closet.query.get(id)
        try:
            db.session.delete(item)
            db.session.commit()
            return redirect (url_for('site.account'))
        except:
            return "There was an error"

# update items route
@site.route('/update/<id>', methods = ['GET', 'POST'])
@login_required
def update_item(id):
        item=Closet.query.get(id)
        form=ClosetForm()
        if request.method == 'POST' and form.validate_on_submit():
            try:
                item.article_category = form.article_category.data
                item.designer = request.form['designer']
                item.name = request.form['name']
                item.price = request.form['price']
                item.image = request.form['image']
                db.session.commit()
                return redirect (url_for('site.account'))
            except:
                return "Error updating"




@site.route('/createcloset', methods=['GET', 'POST'])
@login_required
def createcloset():
    form = ClosetForm() #9 parentheses 
    if request.method == 'POST' and form.validate():
        article = form.article_category.data
        desginer = form.designer.data
        name = form.name.data
        price = form.price.data
        image = form.image.data
        user_id = current_user.id #10 change to username
        closet = Closet(article,desginer,name,price,image, user_id)
        db.session.add(closet) #1 post typo
        db.session.commit()
        return redirect(url_for('site.createcloset'))
    return render_template("createcloset.html", form = form)


