from flask import abort, flash, redirect, render_template, url_for
from http import HTTPStatus

from . import app, db
from .constants import FLASH_SHORT_ID_EXISTS, SHORT_ID_INVALID
from .forms import URLForm
from .models import URLMap
from .utils import check_validity_shirt_id

@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        url_object = URLMap()
        if not custom_id or custom_id == '':
            custom_id = url_object.get_unique_short_id()
        if URLMap.query.filter_by(short=custom_id).first():
            flash(FLASH_SHORT_ID_EXISTS.format(custom_id=custom_id), 'name_exists')
            return render_template('index.html', form=form)
        if not check_validity_shirt_id(custom_id):
            flash(SHORT_ID_INVALID.format(custom_id=custom_id), 'name_invalid')
            return render_template('index.html', form=form)
        short_url = URLMap(
            original=form.original_link.data,
            short=custom_id
        )
        db.session.add(short_url)
        db.session.commit()
        flash(
            url_for(
                'redirect_to_original', short_url=custom_id, _external=True), 'full_link'
        )
    return render_template('index.html', form=form)

@app.route('/<string:short_url>', methods=['GET'])
def redirect_to_original(short_url):
    return redirect(
        URLMap.query.filter_by(short=short_url).first_or_404().original)
