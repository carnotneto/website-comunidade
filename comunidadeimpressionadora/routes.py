from flask import render_template, redirect, url_for, flash, request
from comunidadeimpressionadora import app, database, bcrypt
from comunidadeimpressionadora.forms import FormLogin, FormCriarConta
from comunidadeimpressionadora.models import Usuario
from flask_login import login_user, logout_user, current_user

lista_usuarios = ['João', 'Carnot', 'Maurício']


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/contato")
def contato():
    return render_template('contato.html')


@app.route("/usuarios")
def usuarios():
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criar_conta = FormCriarConta()

    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f'Logado como {form_login.email.data}', 'alert-success')
            return redirect(url_for('home'))
        else:
            flash(f'Não foi possivel logar como {form_login.email.data}. Verifique email ou senha e tente novamente.',
                  'alert-danger')
                            
    if form_criar_conta.validate_on_submit() and 'botao_submit_criar_conta' in request.form:
        senha_cript: bytes = bcrypt.generate_password_hash(form_criar_conta.senha.data)
        usuario = Usuario(username=form_criar_conta.username.data, email=form_criar_conta.email.data,
                          senha=senha_cript)
        database.session.add(usuario)
        database.session.commit()
        flash(f'Conta criada para {form_criar_conta.email.data}', 'alert-success')
        return redirect(url_for('home'))
    return render_template('login.html', form_login=form_login, form_criar_conta=form_criar_conta)


@app.route('/logout')
def logout():
    logout_user()
    flash('Logout feito com sucesso!', 'alert-success')
    return redirect(url_for('home'))


@app.route('/perfil')
def perfil():
    return render_template('perfil.html')


@app.route('/post/criar')
def post():
    return render_template('criarpost.html')
