from flask import redirect, render_template, flash, url_for

from .forms import URLMapForm
from .models import URLMap
from . import app, db


@app.route('/', methods=("GET", "POST"))
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        short_url = form.custom_id.data
        if not short_url:
            short_url = URLMap.get_unique_short_id()
        if URLMap.query.filter_by(short=short_url).first() is not None:
            flash(f'Имя {short_url} уже занято!')
            return render_template('redirect_url.html', form=form)
        url_map = URLMap(
            original=form.original_link.data,
            short=short_url,
        )
        db.session.add(url_map)
        db.session.commit()
        new_url = url_for('index_view', _external=True) + short_url
        return render_template('redirect_url.html', form=form, short=new_url)
    return render_template('redirect_url.html', form=form)


@app.route('/<short_url>')
def redirect_url(short_url):
    original_url = URLMap.query.filter_by(short=short_url).first_or_404().original
    return redirect(original_url)