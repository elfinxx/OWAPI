"""
Main OWAPI App.
"""

import logging

from asphalt.core import ContainerComponent

from asphalt.redis.component import RedisComponent
from kyoukai import Kyoukai
from kyoukai.asphalt import KyoukaiComponent
from kyoukai.context import HTTPRequestContext
from kyoukai.response import Response

from owapi import util, routes

# Fuck your logging config.

logging.basicConfig(filename='/dev/null', level=logging.INFO)

formatter = logging.Formatter('%(asctime)s - [%(levelname)s] %(name)s -> %(message)s')
root = logging.getLogger()

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(formatter)
root.addHandler(consoleHandler)

logger = logging.getLogger("OWAPI")


class APIComponent(ContainerComponent):
    """
    Container for other components. I think.
    """

    async def start(self, ctx):
        self.add_component('kyoukai', KyoukaiComponent, ip="127.0.0.1", port=4444,
                           app="app:app", template_renderer=None)
        self.add_component('redis', RedisComponent)
        await super().start(ctx)

        logger.info("Started OWAPI server.")


app = Kyoukai("owapi")


@app.route("/")
async def root(ctx: HTTPRequestContext):
    return Response.redirect("https://github.com/SunDwarf/OWAPI/blob/master/api.md")


@app.errorhandler(404)
async def e404(ctx: HTTPRequestContext):
    return {"error": 404}, 404


app.register_blueprint(routes.bp)
