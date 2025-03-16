<?php

namespace App\Core;

class Router
{
    private array $routes = [];

    public function addRoute(string $path, string $controller, string $method): void
    {
        $this->routes[$path] = [
            'controller' => $controller,
            'method' => $method
        ];
    }

    public function dispatch(): void
    {
        $path = $_SERVER['REQUEST_URI'] ?? '/';
        $path = parse_url($path, PHP_URL_PATH);
        
        if (!isset($this->routes[$path])) {
            http_response_code(404);
            echo "404 Not Found";
            return;
        }

        $route = $this->routes[$path];
        $controllerClass = $route['controller'];
        $method = $route['method'];

        try {
            $controller = new $controllerClass();
            $controller->$method();
        } catch (\Exception $e) {
            http_response_code(500);
            echo "Internal Server Error: " . $e->getMessage();
        }
    }
} 