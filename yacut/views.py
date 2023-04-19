from http import HTTPStatus

from flask import abort, flash, redirect, render_template, url_for

from . import app
from .error_handlers import CreatingError
from .forms import URLForm
from .models import URLMap


SHORT_ID_INVALID = "Ссылка должна состоять только из цифр и латинских букв!"
FLASH_SHORT_ID_EXISTS = 'Имя {custom_id} уже занято!'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    original, custom_id = form.original_link.data, form.custom_id.data
    if URLMap.check_unique_short_id(custom_id):
        flash(
            FLASH_SHORT_ID_EXISTS.format(custom_id=custom_id), 'name_exists'
        )
        return render_template('index.html', form=form)
    if (
        custom_id != '' and
        custom_id is not None and
        not URLMap.validate_short_id(custom_id)
    ):
        flash(SHORT_ID_INVALID.format(custom_id=custom_id), 'name_invalid')
        return render_template('index.html', form=form)
    try:
        print(original, custom_id)
        url_object = URLMap.create_new_url_object(original, custom_id)
    except CreatingError:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR)
    print(url_object)
    return render_template(
        'index.html',
        form=form,
        link=url_for('index_view', _external=True) + url_object.short
    )


@app.route('/<string:short_url>', methods=['GET'])
def redirect_to_original(short_url):
    url_object = URLMap.check_unique_short_id(short_url)
    if not url_object:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(url_object.original)
