import logging

from flask import jsonify

from cache import cache
from . import bp

log = logging.getLogger('images')


@bp.route(
    '/search/<string:search_term>',
    methods=['POST'],
)
def search_images(search_term):
    """
        Perform search with specified query
        ---
        responses:
          200:
            description: Returns a list of images
          400:
            description: Bad request
        """

    result = cache.do_search(search_term)

    return jsonify(result)
