from fastapi import FastAPI
from logging import Logger
from typing import Sequence
from .base import add_base_middleware
from .cors import add_cors_middleware

class MiddlewareManager:
    _default_limit:int = 10
    _default_window:int = 1
    _default_cleanup_interval:int = 60
    _default_ip_timeout:int = 300
    _default_allow_origins:Sequence[str] = ()
    _default_allow_methods:Sequence[str] = ("GET",)
    _default_allow_headers:Sequence[str] = ()
    _default_allow_credentials:bool = False
    _default_expose_headers:Sequence[str] = ()

    def __init__(self, app:FastAPI):
        self.app = app

    def add_all_middlewares(
        self,
        logger:Logger,
        limit:int = _default_limit,
        window:int = _default_window,
        cleanup_interval:int = _default_cleanup_interval,
        ip_timeout:int = _default_ip_timeout,
        allow_origins:Sequence[str] = _default_allow_origins,
        allow_methods:Sequence[str] = _default_allow_methods,
        allow_headers:Sequence[str] = _default_allow_headers,
        allow_credentials:bool = _default_allow_credentials,
        expose_headers:Sequence[str] = _default_expose_headers
    ):
        self.add_cors_middleware(
            allow_origins=allow_origins,
            allow_methods=allow_methods,
            allow_headers=allow_headers,
            allow_credentials=allow_credentials,
            expose_headers=expose_headers
        )
        self.add_base_middleware(
            logger=logger,
            limit=limit,
            window=window,
            cleanup_interval=cleanup_interval,
            ip_timeout=ip_timeout
        )

    def add_cors_middleware(
        self,
        allow_origins:Sequence[str] = _default_allow_origins,
        allow_methods:Sequence[str] = _default_allow_methods,
        allow_headers:Sequence[str] = _default_allow_headers,
        allow_credentials:bool = _default_allow_credentials,
        expose_headers:Sequence[str] = _default_expose_headers
    ):
        add_cors_middleware(
            app=self.app,
            allow_origins=allow_origins,
            allow_methods=allow_methods,
            allow_headers=allow_headers,
            allow_credentials=allow_credentials,
            expose_headers=expose_headers
        )

    def add_base_middleware(
        self,
        logger:Logger,
        limit:int = _default_limit,
        window:int = _default_window,
        cleanup_interval:int = _default_cleanup_interval,
        ip_timeout:int = _default_ip_timeout
    ):
        add_base_middleware(
            app=self.app,
            logger=logger,
            limit=limit,
            window=window,
            cleanup_interval=cleanup_interval,
            ip_timeout=ip_timeout
        )