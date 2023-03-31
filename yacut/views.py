from flask import flash, redirect, render_template, url_for

from .forms import URLForm
from .models import URLMap, ShortIdGenerationError
from . import app

NAME_NOT_FREE = 'Имя "{}" уже занято!'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    if not form.custom_id.data:
        short_id = form.custom_id.data
        try:
            URLMap.create(form.original_link.data, short_id)
        except ShortIdGenerationError as error:
            flash(str(error))
        return render_template('index.html', form=form)
    URLMap.create(form.original_link.data, form.custom_id.data)
    return render_template(
        'index.html',
        form=form,
        url_map=url_for('redirect_view',
                        short_id=form.custom_id.data,
                        _external=True)
    )


@app.route('/<string:short_id>')
def redirect_view(short_id):
    return redirect(URLMap.get_url_map_or_404(short_id).original)
