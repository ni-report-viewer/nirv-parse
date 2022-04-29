import logging


logger = logging.getLogger('NIRV.HTMLfinder')


def get_html(bids_layout, all_filters):
        found_html = bids_layout.get(**all_filters)
        if len(found_html) < 1:
            if "session" in all_filters:
                del all_filters["session"]
                return get_html(bids_layout, all_filters)
            else:
                logger.warning(f"No HTML found with filters: {all_filters}")
                return None
        else:
            if len(found_html) > 1:
                logger.warning((
                    f"More than one HTML found with filters: {all_filters}. "
                    f"The following path was chosen: {found_html[0].path}"))
            return found_html[0].path
