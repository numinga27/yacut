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
        create_dates = URLMap.create(form.original_link.data, form.custom_id.data)
    except ShortIdGenerationError as error:
        flash(str(error))
    return render_template(
        'index.html',
        form=form,
        url_map=url_for('redirect_view',
                        short_id=create_dates.short,
                        _external=True)
    )


@ app.route('/<string:short_id>')
def redirect_view(short_id):
    return redirect(URLMap.get_url_map_or_404(short_id).original)
