import logging

from cache import cache
from config import Config
from tasks import celery
from api.client import ImageClient

log = logging.getLogger('tasks_images')


@celery.task(queue="images")
def cache_images(page_num):
    # TODO: add lock
    cli = ImageClient(Config.AGILEENGINE_API_KEY)
    msg = "Starting images caching.." if page_num == 1 else "Continuing images caching.."
    log.info(msg)

    images_data = cli.get_images(page_num)
    image_ids = [img["id"] for img in images_data.get("pictures") if img.get("id")]
    for image_id in image_ids:
        if image := cli.get_image_details(image_id):
            cache.store_data(image)

    if images_data.get("hasMore"):
        log.debug("Fetching data from the next page")
        next_page_num = images_data.get("page", 0) + 1
        if page_num < next_page_num:
            cache_images.delay(page_num=next_page_num)
        else:
            log.error("Error getting data: incorrect page order %s < %s", page_num, next_page_num)

    log.debug("Finished caching files data")
