import os
import uuid
import re
from flask import Blueprint
from .logger import Logger
from .exceptions.http_exception import HTTPException
from .helps._error import render
from .http.request import Request
from .http.response import Response

class Router(Blueprint):
    """
    Flask Blueprint extension that adds custom handling for prefixes,
    route paths, and dynamic loading of controllers.
    """
    def __init__(self, path: str = "/", prefix: str = "/", **kwargs):
        """
        Router constructor.
        
        :param path: Base path for the routes. Example: "/" or "/my-route".
                     This path is used to locate the controller directory.
        :param prefix: Optional prefix for routes. Example: "/api".
                       This prefix will be used to construct route URLs.
        :param kwargs: Additional parameters for the Blueprint (e.g., static_folder, template_folder, etc.).
        """
        # Generate a unique name to avoid conflicts between blueprints
        blueprint_name = f"{self.__class__.__name__}_{uuid.uuid4().hex[:8]}"
        
        # Validate and normalize prefix and path values
        self._prefix = self.__validate_prefix(prefix)
        self._path = self.__validate_path(path)

        # Initialize the Blueprint without defining url_prefix, as the prefix will be included in routes
        super().__init__(blueprint_name, __name__, url_prefix=self._prefix, **kwargs)

    def get(self, route: str, controller_action: str):
        return self.__add_route(route, controller_action, methods=["GET"])

    def post(self, route: str, controller_action: str):
        return self.__add_route(route, controller_action, methods=["POST"])

    def put(self, route: str, controller_action: str):
        return self.__add_route(route, controller_action, methods=["PUT"])

    def delete(self, route: str, controller_action: str):
        return self.__add_route(route, controller_action, methods=["DELETE"])

    def patch(self, route: str, controller_action: str):
        return self.__add_route(route, controller_action, methods=["PATCH"])

    def options(self, route: str, controller_action: str):
        return self.__add_route(route, controller_action, methods=["OPTIONS"])

    def head(self, route: str, controller_action: str):
        return self.__add_route(route, controller_action, methods=["HEAD"])

    def trace(self, route: str, controller_action: str):
        return self.__add_route(route, controller_action, methods=["TRACE"])

    def __add_route(self, route: str, controller_action: str, methods: list):
        """
        Adds a route to the blueprint, associating it with a specific controller and action.
        """
        def handler(**kwargs):
            try:
                controller_name, action_name = controller_action.split("@")
            except ValueError:
                return Response.html(
                    content=render(
                        code=500,
                        title="Invalid Format",
                        description="🚨 The route format is invalid. Please use 'Controller@action'."
                    ),
                    status=500
                )
            
            controller = self._load_controller(controller_name)

            if not controller:
                return Response.html(
                    content=render(
                        code=404,
                        title="Not Found",
                        description=f"🚨 Controller {controller_name} not found."
                    ),
                    status=404
                )

            try:
                action = getattr(controller, action_name, None)
                if not action:
                    return Response.html(
                        content=render(
                            code=501,
                            title="Not Implemented",
                            description=f"⚠️ Method '{action_name}' is not implemented in controller '{controller_name}'."
                        ),
                        status=501
                    )

                request = Request()
                response = Response()
                return action(request, response)
            except Exception as e:
                Logger.error(f"Error executing {controller_name}@{action_name}: {e}")
                return Response.error(f"❌ Error executing method {action_name}", 500)

        Logger.info(f"Registering '{controller_action}' on route '{route}'")
        self.add_url_rule(route, endpoint=controller_action, view_func=handler, methods=methods)
        return handler

    def _load_controller(self, controller_name: str):
        """
        Dynamically loads the controller from the given name.
        """
        controller_file = f"{self.__camel_to_snake(controller_name)}_controller"
        try:
            module_path = "app.http.controllers"
            if self._path.strip("/"):
                module_path += f".{self._path.strip('/').replace('/', '.')}"

            module_path += f".{controller_file}"

            module = __import__(module_path, fromlist=[controller_name])
            controller_class = getattr(module, controller_name)
            Logger.info(f"Controller '{controller_name}' successfully loaded.")
            return controller_class()

        except ModuleNotFoundError:
            Logger.error(f"The specified module '{module_path.replace('.', '/')}.py' could not be found.")
            raise HTTPException(
                code=404, 
                title="Resource Not Found", 
                description="🚨 The requested module does not exist on the server. Please verify the module path."
            )

        except AttributeError:
            Logger.error(f"The controller '{controller_name}' was not found in the module '{module_path.replace('.', '/')}'.")
            raise HTTPException(
                code=404, 
                title="Controller Not Found", 
                description=f"🚨 The specified controller '{controller_name}' could not be located within the module '{module_path}'."
            )

        except FileNotFoundError as e:
            Logger.error(f"The requested file could not be located: {str(e)}.")
            raise HTTPException(
                code=404, 
                title="File Not Found", 
                description="📂 The requested file is missing or unavailable. Please check the file path."
            )

        except ImportError as e:
            Logger.error(f"Failed to import module '{module_path}': {str(e)}.")
            raise HTTPException(
                code=500, 
                title="Module Import Error", 
                description="⚠️ An error occurred while importing the module. Please ensure it is correctly installed and accessible."
            )

        except Exception as e:
            Logger.error(f"An unexpected server error occurred: {str(e)}")
            raise HTTPException(
                code=500, 
                title="Internal Server Error", 
                description="🚨 An unexpected error occurred on the server. Please try again later or contact support."
            )

    def __camel_to_snake(self, name: str) -> str:
        """
        Converts a CamelCase name to snake_case.
        
        :param name: Name in CamelCase.
        :return: Converted name in snake_case.
        """
        without_prefix = re.sub(r'(?i)_(controller|Controller)$', '', name)
        without_prefix = re.sub(r'(?i)controller$', '', without_prefix)
        return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', without_prefix).lower()

    def __validate_path(self, path: str) -> str:
        """
        Validates and normalizes the Blueprint path.
        
        :param path: Provided path.
        :return: Normalized path.
        :raises ValueError: If validation fails.
        """
        if not path:
            self.__raise_validation_error("The 'path' of the Blueprint cannot be empty.")
        if not isinstance(path, str):
            self.__raise_validation_error("The 'path' of the Blueprint must be a string.")
        if not path.startswith("/"):
            self.__raise_validation_error("The 'path' of the Blueprint must start with '/'.")
        
        normalized_path = path.strip("/").lower()
        controllers_dir = os.path.join("app", "http", "controllers")
        expected_dir = os.path.join(controllers_dir, normalized_path)
        
        if not os.path.exists(expected_dir):
            self.__raise_validation_error(f"The folder 'app/http/controllers/{normalized_path}' does not exist.")
        
        return f"/{normalized_path}" if normalized_path else "/"

    def __validate_prefix(self, prefix: str) -> str:
        if not isinstance(prefix, str):
            self.__raise_validation_error("The 'prefix' of the Blueprint must be a string.")
        if prefix and not prefix.startswith("/"):
            self.__raise_validation_error("The 'prefix' of the Blueprint must start with '/'.")
        return prefix if prefix else "/"

    def __raise_validation_error(self, message: str):
        Logger.error(f"{message}")
        raise ValueError(f"❌ {message}")
