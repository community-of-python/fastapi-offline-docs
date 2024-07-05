import os
import pathlib
import typing

from fastapi import FastAPI, Request
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.routing import Route


def enable_offline_docs(
    app: FastAPI,
    static_files_handler: str = "/static",
    static_dir_path: os.PathLike[str] = pathlib.Path(__file__).parent / "static",
    include_docs_in_schema: bool = False,
) -> None:
    """Enable offline documentation that available on paths app.docs_url and app.redoc_url.

    :param static_files_handler: static files serving on /static_files_handler handler
    :param static_dir_path: path to static files being placed
    :param include_docs_in_schema: flag specified whether
    it needs to include doc's routes docs in schema.
    """
    if not (app_openapi_url := app.openapi_url):
        raise RuntimeError("No app.openapi_url specified")

    docs_url: str = app.docs_url or "/docs"
    redoc_url: str = app.redoc_url or "/redoc"
    swagger_ui_oauth2_redirect_url: str = app.swagger_ui_oauth2_redirect_url or "/docs/oauth2-redirect"

    app.router.routes = [
        route
        for route in app.router.routes
        if typing.cast(Route, route).path not in (docs_url, redoc_url, swagger_ui_oauth2_redirect_url)
    ]

    app.mount(static_files_handler, StaticFiles(directory=static_dir_path), name=static_files_handler)

    @app.get(docs_url, include_in_schema=include_docs_in_schema)
    async def custom_swagger_ui_html(request: Request) -> HTMLResponse:
        root_path = typing.cast(str, request.scope.get("root_path", "").rstrip("/"))
        swagger_js_url = f"{root_path}{static_files_handler}/swagger-ui-bundle.js"
        swagger_css_url = f"{root_path}{static_files_handler}/swagger-ui.css"
        return get_swagger_ui_html(
            openapi_url=root_path + app_openapi_url,
            title=f"{app.title} - Swagger UI",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url=swagger_js_url,
            swagger_css_url=swagger_css_url,
        )

    @app.get(swagger_ui_oauth2_redirect_url, include_in_schema=include_docs_in_schema)
    async def swagger_ui_redirect() -> HTMLResponse:
        return get_swagger_ui_oauth2_redirect_html()

    @app.get(redoc_url, include_in_schema=include_docs_in_schema)
    async def redoc_html() -> HTMLResponse:
        return get_redoc_html(
            openapi_url=app_openapi_url,
            title=f"{app.title} - ReDoc",
            redoc_js_url=f"{static_files_handler}/redoc.standalone.js",
        )
