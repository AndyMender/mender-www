import uuid

from flask import Flask, abort, flash, redirect, render_template, request, session, url_for
from sqlalchemy.engine import Engine

from controllers.queries import get_comments, get_page_views, get_posts
from controllers.store import store_comment, update_page_views


def build_endpoints(app: Flask, engine: Engine) -> Flask:
    """Create application endpoints and routes

    :param app: Flask server/app
    :param engine: SQLAlchemy engine for communicating with the backend
    :return: Fully bootstrapped Flask app
    """

    @app.route('/', methods=['GET'])
    def index():
        """Blog front page"""

        # set up session
        session['identity'] = str(uuid.uuid4())

        # update page_views count
        update_page_views(engine)

        # get total page views
        page_views = get_page_views(engine, mode='all')

        # get 'published' posts from database
        posts = [post for post in get_posts(engine) if post['published']]

        # create Web context
        context = {'posts': posts,
                   'page_views': page_views}

        # generate endpoint
        return render_template('index.html', **context)


    @app.route('/posts/<post_id>', methods=['GET'])
    def posts(post_id):
        """Individual blog post endpoints"""

        # update page_views count
        update_page_views(engine)

        # get total page views
        page_views = get_page_views(engine, mode='all')

        # get 'published' posts from database
        posts = [post for post in get_posts(engine) if post['published']]

        # get all comments for selected post from database
        comments = [comment for comment in get_comments(engine, post_id)
                    if comment['approved']]

        # create Web page context
        context = {'posts': posts,
                   'comments': comments,
                   'page_views': page_views,
                   'post_id': post_id}

        # extract information on selected post
        for post in posts:
            if int(post_id) == post['id']:

                # include 'post' attributes in Web page 'context'
                context.update(post)

                return render_template(post['filename'], **context)

        abort(404)


    @app.route('/posts/<post_id>/submit_comment', methods=['POST'])
    def submit_comment(post_id):
        """Get POSTed comment from form, store in database and refresh page"""

        # update page_views count
        update_page_views(engine)

        # try to store comment and get response from backend
        response = store_comment(post_id, request, engine)

        # validate response and flash corresponding message
        if response == '':
            flash('Error in backend function. Contact administrator.', category='fail')
        elif response == 'success':
            flash('', category='success')
        else:
            flash(response, category='fail')

        return redirect(url_for('posts', post_id=post_id))

    @app.errorhandler(404)
    def not_found(error):
        """Page not found handler"""

        # get total page views
        page_views = get_page_views(engine, mode='all')

        # get 'published' posts from database
        posts = [post for post in get_posts(engine) if post['published']]

        # create Web page context
        context = {'posts': posts,
                   'page_views': page_views}

        return render_template('not_found.html', **context), 404
    
    return app
