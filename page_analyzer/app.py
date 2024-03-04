from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    get_flashed_messages
)
from page_analyzer import page_db
from dotenv import load_dotenv
from page_analyzer.valid import validate_url, normalize_url
import os


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def get_main():
    return render_template('index.html')


@app.get('/urls')
def get_urls_page():
    data = page_db.get_all_urls()
    return render_template(
        'urls.html',
        urls=data
    )


@app.post('/urls')
def add_url():
    data = request.form.to_dict()
    url = normalize_url(data.get('url'))
    erorrs = validate_url(data)
    if erorrs:
        return render_template(
            'index.html',
            data=data.get('url'),
            messages=erorrs
        ), 422
    url_id = page_db.get_id_by_url(url)
    if url_id:
        flash('Страница уже существует', 'info')
        return redirect(url_for('get_url', id=url_id))
    url_id = page_db.add_url(url)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('get_url', id=url_id))


@app.get('/urls/<id>')
def get_url(id):
    data = page_db.get_data_by_id(id)
    messag = get_flashed_messages(with_categories=True)
    checks = page_db.get_checks(id)
    return render_template(
        'new.html',
        id=id,
        name=data[1],
        created_at=data[2],
        messages=messag,
        checks=checks
    )


@app.post('/urls/<id>/checks')
def check_url(id):
    try:
        page_db.url_check(id)
        flash('Страница успешно проверена', 'success')
        return redirect(url_for('get_url', id=id))
    except Exception:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('get_url',
                                id=id))
