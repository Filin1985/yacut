from http import HTTPStatus

from flask import abort, redirect, render_template, flash, url_for

from . import app
from .error_handlers import ExistenceError, ValidationError
from .forms import URLForm
from .models import URLMap
from settings import REDIRECT_FUNCTION


FLASH_SHORT_ID_EXISTS = 'Имя {custom_id} уже занято!'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    original, custom_id = form.original_link.data, form.custom_id.data
    try:
        url_object = URLMap.create_urlmap(
            original, custom_id, FLASH_SHORT_ID_EXISTS
        )
    except ExistenceError as error:
        flash(error.message)
        return render_template('index.html', form=form)
    except ValidationError as error:
        flash(error.message)
        return render_template('index.html', form=form)
    return render_template(
        'index.html',
        form=form,
        link=url_for(
            REDIRECT_FUNCTION,
            short_url=url_object.short,
            _external=True
        )
    )


@app.route('/<string:short_url>', methods=['GET'])
def redirect_to_original(short_url):
    url_object = URLMap.get_unique_custom_id(short_url)
    if not url_object:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(url_object.original)
