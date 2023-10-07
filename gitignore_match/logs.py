import logging

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# add handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
log.addHandler(handler)
