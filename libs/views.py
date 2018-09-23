import uuid

from flask import Flask, flash, redirect, render_template, request, session, url_for
from sqlalchemy.engine import Engine

from libs.controllers import get_comments, get_posts, store_comment


def build_endpoints(app: Flask, engine: Engine) -> None:
    """Create application endpoints and routes

    :param app: Flask server/app
    :param engine: SQLAlchemy engine for communicating with the backend
    """

    @app.route('/', methods=['GET'])
    def index():
        """Blog front page"""

        # set up session
        session['identity'] = str(uuid.uuid4())

        # get 'published' posts from database
        posts = [post for post in get_posts(engine) if post['published']]

        # create website context
        context = {'posts': posts}

        # generate endpoint
        return render_template('index.html', **context)


    @app.route('/<post_id>', methods=['GET'])
    def posts(post_id):
        """Individual blog post endpoints"""

        # get all posts from database
        posts = [post for post in get_posts(engine) if post['published']]

        # get all comments for selected post from database
        comments = [comment for comment in get_comments(engine, post_id)
                    if comment['approved']]

        # build Web page context
        context = {'posts': posts,
                   'comments': comments,
                   'post_id': post_id}

        # extract information on selected post
        for post in posts:
            if int(post_id) == post['id']:

                # include 'post' attributes in Web page 'context'
                context.update(post)

                return render_template(post['filename'], **context)

        return render_template('not_found.html', **context)


    @app.route('/<post_id>/submit_comment', methods=['POST'])
    def submit_comment(post_id):
        """Get POSTed comment from form, store in database and refresh page"""

        # try to store comment and get response from backend
        response = store_comment(request, engine)

        # validate response and flash corresponding message
        if response == '':
            flash('Error in backend function. Contact administrator.', category='fail')
        elif response == 'success':
            flash('', category='success')
        else:
            flash(response, category='fail')

        return redirect(url_for('posts', post_id=post_id))
