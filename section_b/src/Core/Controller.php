<?php

namespace App\Core;

abstract class Controller
{
    protected function render(string $view, array $data = []): void
    {
        // Extract data to make variables available in view
        extract($data);

        // Define the path to the view file
        $viewFile = __DIR__ . "/../views/{$view}.php";
        
        if (!file_exists($viewFile)) {
            throw new \Exception("View file not found: {$viewFile}");
        }

        // Start output buffering
        ob_start();

        // Include the layout start
        include __DIR__ . "/../views/layouts/header.php";

        // Include the view file
        include $viewFile;

        // Include the layout end
        include __DIR__ . "/../views/layouts/footer.php";

        // Get the contents and clean the buffer
        $content = ob_get_clean();

        // Output the content
        echo $content;
    }
} 