from pickle import GET
from flask import render_template, flash, redirect, url_for
from app.auth.forms import RegistrationForm, LoginForm, ScrapyForm
from app.auth import authentication
from app.auth.models import User
from flask_login import login_user, logout_user,login_required, current_user
from bs4 import BeautifulSoup
from lxml import etree
import requests


@authentication.route("/register", methods=["GET","POST"])
def register_user():
    if current_user.is_authenticated:
        flash("you are already logged in the system")
        return redirect(url_for("authentication.homepage"))
    
    form = RegistrationForm()

    if form.validate_on_submit():
        User.create_user(
            user = form.name.data,
            email = form.email.data,
            password = form.password.data
        )
        flash("Registration Done...")
        return redirect(url_for("authentication.log_in_user"))
    
    return render_template("registration.html", form=form)



@authentication.route("/")
def index():
    return render_template("index.html")

@authentication.route("/login",methods=["GET","POST"])
def log_in_user():
    if current_user.is_authenticated:
        flash("you are already logged in the system")
        return redirect (url_for("authentication.homepage"))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(user_email=form.email.data).first()
        if not user or not user.check_password(form.password.data):
            flash("Invalid credentials...")
            return redirect(url_for("authentication.log_in_user"))
        
        login_user(user, form.stay_loggedin.data)
        return redirect(url_for("authentication.homepage"))

    return render_template("login.html", form=form)

@authentication.route('/homepage')
@login_required
def homepage():
    return render_template("homepage.html")

@authentication.route('/logout', methods=["GET"])
@login_required
def log_out_user():
    logout_user()
    return redirect(url_for("authentication.log_in_user"))


@authentication.route("/scrapy_data", methods=["GET", "POST"])
@login_required
def scrapy_data():
    form = ScrapyForm()
    if form.validate_on_submit():
        search = form.search_article.data
        url = f"https://listado.mercadolibre.cl/{search}#D[A:{search}]"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        dom = etree.HTML(str(soup))
        # 🔹 Extraer enlaces y texto usando XPath
        data_articles = dom.xpath("//ol[@class='ui-search-layout ui-search-layout--stack shops__layout']"
                                "//li[@class='ui-search-layout__item shops__layout-item']"
                                "//div[@class='ui-search-result__wrapper']")

        # 🔹 Extraer títulos con enlaces y las imágenes
        results = []
        for article in data_articles:
            title_element = article.xpath(".//h3[@class='poly-component__title-wrapper']//a")
            image_element = article.xpath(".//div[@class='poly-card__portada']//img/@src")

            if title_element and image_element:
                title = title_element[0].text.strip() if title_element[0].text else "Sin título"
                link = title_element[0].get("href", "Sin enlace")
                image = image_element[0] if image_element else "Sin imagen"

                results.append((title, link, image))

        data = {"links": results}
        return render_template("scrapy_data.html", **data)
    return render_template("scrapy_data.html", form = form)
    



@authentication.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html'),404


