import random
import string

from flask import flash, redirect, render_template, url_for

from .forms import URLForm
from .models import URLMap
from . import app

NAME_NOT_FREE = 'Имя "{}" уже занято!'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if form.validate_on_submit():
        short_url = form.custom_id.data
        if not short_url:
            short_url = URLMap.get_unique_short_id()
        URLMap.add_u(dict(url=form.original_link.data,
                          custom_id=short_url))
        return render_template('index.html', **{'form': form, 'short_url': short_url})
    return render_template('index.html', form=form)


@app.route('/<string:short_url>')
def redirect_view(short_url):
    return redirect(URLMap.get_url_map_or_404(short_url).original)