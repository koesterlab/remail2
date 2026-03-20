from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass

import flet as ft

class View(ft.Container, ABC):
    @abstractmethod
    def create_view(self) -> ft.Control:
        ...

    @abstractmethod
    def on_subroute_change(self, subview: "View|None") -> None:
        ...

    def __init__(self, route:str) -> None:
        self.route: str = route
        self.sub_route: str|None = None
        self.router: ViewRouter|None = None

class ViewRouter:
    def __init__(self, page: ft.Page) -> None:
        self.views: dict[str, "View"] = {}
        self.route = "/"
        self.current_view: ft.Control|None = None
        self.callback: Callable[[ft.Control], None] = lambda c: None
        self.page = page
        page.on_route_change = lambda: self._set_route(page.route)
    
    def get_overflowing_route(self) -> str:
        return self.overflowing_route
    
    def _set_route(self, route:str) -> None:
        self.route = route
        found_routes = []
        for r, _ in self.views:
            if len(route) < len(r): #to short, cannot be the right page
                continue
            if route[:len(r)] == r:
                found_routes.append(r)

        found_routes.sort(reverse=True) #order so the most specific link comes first
        view:View|None = None
        for r in found_routes: #iterating every match and pass sub-view to view
            v = self.views[r]
            if not v.rendered_view:
                v.rendered_view = v.create_view()
                v.router = self

            sub_route = route[len(r):]
            if v.sub_route != sub_route:
                v.sub_route = sub_route
                v.on_subroute_change(view)

        self.page.clean()
        self.page.add(view if view else ft.Text("URI: " + route + " not found"))
        self.callback(self.current_view)

    def register_view(self, view:View) -> None:
        self.views[view.route] = view
        
    def set_on_change(self, callback: Callable[[ft.Control], None]) -> None:
        self.callback = callback
