import logging
from collections import defaultdict

log = logging.getLogger('client')


class Cache:

    def __init__(self):
        self.images = {}
        self.name_to_image_map = defaultdict(list)
        self.author_to_image_map = defaultdict(list)
        self.camera_to_image_map = defaultdict(list)
        self.tag_to_image_map = defaultdict(list)

    def store_data(self, image_data):
        if image_id := image_data.get("id"):
            if cropped_picture_url := image_data.get("cropped_picture"):
                self.images[image_id] = {
                    "cropped_picture_url": cropped_picture_url,
                }
                cropped_picture_filename = cropped_picture_url.split("/")[-1]
                self.name_to_image_map.update({cropped_picture_filename: image_id})

            if full_picture_url := image_data.get("full_picture"):
                self.images[image_id].update({
                    "full_picture": full_picture_url,
                })
                full_picture_filename = full_picture_url.split("/")[-1]

                self.name_to_image_map.update({full_picture_filename: image_id})

            if author := image_data.get("author", "").strip():
                self.author_to_image_map[author].append(image_id)

            if camera := image_data.get("camera"):
                self.camera_to_image_map[camera.strip()].append(image_id)

            if tags := image_data.get("tags").split("#"):
                for tag in tags:
                    if tag:
                        self.tag_to_image_map[tag.strip()].append(image_id)
        else:
            log.info("Image data is corrupted: %s", image_data)

    def do_search(self, term):
        image_ids = []
        image_ids.extend(self.author_to_image_map.get(term, []))
        image_ids.extend(self.name_to_image_map.get(term, []))
        image_ids.extend(self.camera_to_image_map.get(term, []))
        image_ids.extend(self.tag_to_image_map.get(term, []))
        return [self.images[image_id] for image_id in image_ids]


cache = Cache()
