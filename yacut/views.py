from http import HTTPStatus

from flask import abort, redirect, render_template, flash, url_for

from . import app
from .error_handlers import ExistenceError, ValidationError
from .forms import URLForm
from .models import URLMap
from settings import REDIRECT_FUNCTION


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    original, custom_id = form.original_link.data, form.custom_id.data
    try:
        urlmap_object = URLMap.create_urlmap(
            original, custom_id
        )
        return render_template(
            'index.html',
            form=form,
            link=url_for(
                REDIRECT_FUNCTION,
                short_url=urlmap_object.short,
                _external=True
            )
        )
    except ExistenceError as error:
        flash(error.message)
    except ValidationError as error:
        flash(error.message)
    return render_template('index.html', form=form)


@app.route('/<string:short_url>', methods=['GET'])
def redirect_to_original(short_url):
    urlmap_object = URLMap.get_urlmap_item(short_url)
    if not urlmap_object:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(urlmap_object.original)
