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
    try:
        take_url_map = URLMap.create(
            form.original_link.data,
            form.custom_id.data
        )
        return render_template(
            'index.html',
            form=form,
            url_map=url_for('redirect_view',
                            short_id=take_url_map.short,
                            _external=True)
        )
    except ShortIdGenerationError as error:
        flash(str(error))


@ app.route('/<string:short_id>')
def redirect_view(short_id):
    return redirect(URLMap.get_url_map_or_404(short_id).original)
