<?php
require_once 'python_api.php';

$uri = trim(parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH), '/');

switch ($uri) {
    case '':
        // Home page
        echo "<h1>Value API</h1>";
        echo "<ul>";
        echo "<li><a href='/canprice'>CanPrice</a></li>";
        echo "</ul>";
        break;

    case 'pricenew':
        require 'pricenew.php';
        break;

    default:
        http_response_code(404);
        echo "<h1>404 Not Found</h1>";
        break;
}
