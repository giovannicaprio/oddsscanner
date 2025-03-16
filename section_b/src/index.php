<?php

require_once __DIR__ . '/../vendor/autoload.php';

use App\Core\Router;
use App\Controllers\HomeController;

// Register routes
$router = new Router();
$router->addRoute('/', HomeController::class, 'index');

// Dispatch the request
$router->dispatch(); 