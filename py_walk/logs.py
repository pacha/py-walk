import logging

log = logging.getLogger("py_walk")
log.setLevel(logging.INFO)

# add handler
formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
handler = logging.StreamHandler()
handler.setFormatter(formatter)
log.addHandler(handler)
