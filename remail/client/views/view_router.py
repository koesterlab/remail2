from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass

import flet as ft

class View(ABC):
    @abstractmethod
    def create_view(self) -> ft.Control:
        ...

    @abstractmethod
    def on_subroute_change(self, subview: "View|None") -> None:
        ...

    def get_view(self) -> ft.Control:
        return self.create_view()

    def __init__(self, route:str) -> None:
        self.route: str = route
        self.sub_route: str|None = None
        self.router: ViewRouter|None = None
        self._view: ft.Control|None = None
        self.page: ft.Page|None = None

class ViewRouter:
    def __init__(self, page: ft.Page) -> None:
        self.views: dict[str, "View"] = {}
        self.route = "/"
        self.current_view: ft.Control|None = None
        self.callback: Callable[[ft.Control], None] = lambda c: None
        self.page = page
        page.on_route_change = lambda: self._set_route(page.route)
    
    def _set_route(self, route:str) -> None:
        print(route)
        self.route = route
        found_routes = []
        for r, _ in self.views.items():
            if len(route) < len(r): #to short, cannot be the right page
                continue
            if route[:len(r)] == r:
                found_routes.append(r)

        found_routes.sort(reverse=True) #order so the most specific link comes first
        view:View|None = None
        for r in found_routes: #iterating every match and pass sub-view to view
            subview = view
            view = self.views[r]
            if not view:
                continue
            sub_route = route[len(r):]
            if view.sub_route != sub_route and subview:
                view.sub_route = sub_route
                view.on_subroute_change(subview)

        self.page.clean()
        self.page.add(view.get_view() if view else ft.Text("URI: " + route + " not found"))
        self.callback(self.current_view)

    def register_view(self, view:View) -> None:
        self.views[view.route] = view
        view.router = self
        view.page = self.page

        
    def set_on_change(self, callback: Callable[[ft.Control], None]) -> None:
        self.callback = callback
