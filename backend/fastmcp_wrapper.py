"""
Wrapper simple para FastMCP que utiliza decoradores estándar de Python
"""
from typing import Callable, Any, Dict, Optional
import uvicorn
from fastapi import FastAPI, HTTPException, Request
import json
import logging

log = logging.getLogger(__name__)

class SimpleFastMCP:
    def __init__(self, name: str, stateless_http: bool = False):
        self.name = name
        self.stateless_http = stateless_http
        self.tools = {}
        self.app = FastAPI(title=f"{name} API")
        
        # Registramos rutas para cada herramienta
        self._setup_routes()
    
    def _setup_routes(self):
        @self.app.get("/")
        async def root():
            return {"message": f"Bienvenido a {self.name}", "tools": list(self.tools.keys())}
            
        @self.app.get("/tools")
        async def list_tools():
            tools_info = {}
            for name, tool in self.tools.items():
                tools_info[name] = {"description": tool["description"]}
            return tools_info
    
    def tool(self, name: str, description: str):
        """Decorador para registrar una herramienta"""
        def decorator(func: Callable):
            self.tools[name] = {
                "function": func,
                "description": description
            }
            
            # Crear endpoint para esta herramienta
            async def tool_endpoint(request: Request):
                try:
                    if request.method == "GET":
                        # Para peticiones GET, usamos query params
                        params = dict(request.query_params)
                    else:
                        # Para POST, usamos el body JSON
                        try:
                            params = await request.json()
                        except Exception:
                            params = {}
                            
                    # Llamamos a la función
                    result = await func(**params)
                    return result
                except Exception as e:
                    log.exception(f"Error al ejecutar la herramienta {name}")
                    raise HTTPException(status_code=500, detail=str(e))
                    
            # Registrar rutas en FastAPI para esta herramienta
            self.app.add_api_route(f"/tools/{name}", tool_endpoint, methods=["POST", "GET"])
            
            return func
        return decorator
    
    async def process_tool_call(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """Procesar una llamada a herramienta"""
        if tool_name not in self.tools:
            return {"success": False, "error": f"Herramienta '{tool_name}' no encontrada"}
        
        tool = self.tools[tool_name]
        result = await tool["function"](**kwargs)
        return result
        
    def run(self, transport="sse", host="localhost", port=8000, path="/sse", log_level="info"):
        """Ejecutar el servidor FastAPI"""
        print(f"Iniciando servidor FastAPI en {host}:{port}")
        log.info(f"Herramientas disponibles: {list(self.tools.keys())}")
        
        # Si se solicita usar server-sent events, podríamos implementarlo aquí
        if transport == "sse":
            print("Modo SSE activado en la ruta", path)
        
        # Iniciamos el servidor
        uvicorn.run(self.app, host=host, port=port, log_level=log_level) 