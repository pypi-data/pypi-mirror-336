"""LogicLayer class module.

Contains the main definitions for the LogicLayer class.
"""

from __future__ import annotations

import asyncio
import logging
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse, Response
from starlette.status import HTTP_204_NO_CONTENT
from starlette.types import Receive, Scope, Send

from .common import P, R_co, _await_for_it

if TYPE_CHECKING:
    from .module import CallableMayReturnCoroutine, LogicLayerModule

logger = logging.getLogger("logiclayer")


class LogicLayer:
    """Main LogicLayer app handler.

    Instances of this class act like ASGI callables.
    """

    app: FastAPI
    debug: bool
    healthchecks: list[CallableMayReturnCoroutine[[], bool]]

    def __init__(self, *, debug: bool = False, healthchecks: bool = True, **kwargs) -> None:
        self.app = FastAPI(**kwargs)
        self.debug = debug
        self.healthchecks = []

        if healthchecks:
            self.app.add_api_route(
                "/_health",
                endpoint=self.call_healthchecks,
                name="LogicLayer healthcheck",
                status_code=HTTP_204_NO_CONTENT,
            )

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """Enable the :class:`LogicLayer` instance into an ASGI-compatible callable."""
        await self.app(scope, receive, send)

    def add_check(self, func: CallableMayReturnCoroutine[[], bool]) -> None:
        """Store a function to be constantly run as a healthcheck for the app.

        Arguments:
            func :Callable[..., Coroutine[Any, Any, Response]]:

        """
        logger.debug("Check added: %s", func.__name__)
        self.healthchecks.append(func)

    def add_module(self, prefix: str, module: LogicLayerModule, **kwargs) -> None:
        """Configure a module instance in the current LogicLayer instance.

        Arguments:
            prefix :str:
                The prefix path to all routes in the module.
                Must start, and not end, with `/`.
            module :logiclayer.LogicLayerModule:
                An instance of a subclass of :class:`logiclayer.LogicLayerModule`.

        Keyword Arguments:
            {any from :func:`FastAPI.include_router` function}

        """
        logger.debug("Module added on path %s: %s", prefix, module.name)
        module.include_into(self, prefix=prefix, **kwargs)

    def add_redirect(self, path: str, url: str, **kwargs) -> None:
        """Configure a route with the sole purpose of redirecting the user to another location."""
        logger.debug("Redirect added on path %s", path)
        self.app.add_api_route(path, lambda: url, response_class=RedirectResponse, **kwargs)

    def add_route(self, path: str, endpoint: CallableMayReturnCoroutine[[], Any], **kwargs) -> None:
        """Configure a path function to be used directly in the root app.

        Arguments:
            path :str:
                The full path to the route this function will serve.
            func :Callable[..., Response] | Callable[..., Coroutine[Any, Any, Response]]:
                The function which will serve the content for the route.

        """
        logger.debug("Route added on path %s: %s", path, endpoint.__name__)
        self.app.add_api_route(path, endpoint, **kwargs)

    def add_static(self, path: str, target: str | Path, *, html: bool = False) -> None:
        """Configure a static folder to serve the files inside it.

        Arguments:
            path :str:
                The full path to the route where the folder will be available.
            target :str: | :pathlib.Path:
                The path to the directory containing the static files to serve.

        Keyword Arguments:
            html :bool:
                HTML mode. Looks for an index.html file when the requested path
                is a directory, and serves it automatically.

        """
        target = (Path(target) if isinstance(target, str) else target).resolve()
        logger.debug("Static folder added on path %s")
        self.app.mount(path, StaticFiles(directory=target, html=html))

    async def call_startup(self) -> None:
        """Force a call to all handlers registered for the 'startup' event."""
        await self.app.router.startup()

    async def call_shutdown(self) -> None:
        """Force a call to all handlers registered for the 'shutdown' event."""
        await self.app.router.shutdown()

    async def call_healthchecks(self) -> Response:
        """Force a call to all healthchecks registered."""
        try:
            gen = (_await_for_it(item) for item in self.healthchecks)
            await asyncio.gather(*gen)
        except Exception as exc:
            logger.exception("Healthcheck failure", exc_info=exc)
            raise HTTPException(500, "One of the healthchecks failed.") from exc
        else:
            return Response(status_code=HTTP_204_NO_CONTENT)

    def healthcheck(
        self,
        fn: CallableMayReturnCoroutine[[], bool],
    ) -> CallableMayReturnCoroutine[[], bool]:
        """Decorate a method as a healthcheck for the module."""
        self.add_check(fn)
        return fn

    def route(self, path: str, **kwargs) -> Callable[[Callable[P, R_co]], Callable[P, R_co]]:
        """Decorate a method as a route for the module."""

        def route_decorator(fn: Callable[P, R_co]) -> Callable[P, R_co]:
            self.add_route(path, fn, **kwargs)
            return fn

        return route_decorator
