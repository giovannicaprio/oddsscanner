<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Currency Rates - Odds Scanner</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f0f2f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            border-radius: 12px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            padding: 30px;
        }
        h1 {
            color: #1a73e8;
            margin: 0 0 20px 0;
            font-size: 24px;
            text-align: center;
        }
        h2 {
            color: #1a73e8;
            font-size: 20px;
            margin: 0 0 15px 0;
        }
        .last-update {
            color: #666;
            font-size: 14px;
            text-align: center;
            margin-bottom: 30px;
        }
        .content-wrapper {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
        }
        .rates-section, .files-section {
            background: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }
        .rates-table, .files-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }
        .rates-table th,
        .rates-table td,
        .files-table th,
        .files-table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e0e0e0;
        }
        .rates-table th,
        .files-table th {
            background-color: #f8f9fa;
            font-weight: 600;
            color: #1a73e8;
        }
        .rates-table tr:hover,
        .files-table tr:hover {
            background-color: #f5f5f5;
        }
        .rates-table td:last-child {
            text-align: right;
            font-family: 'Courier New', monospace;
        }
        .no-files {
            color: #666;
            text-align: center;
            padding: 20px;
            font-style: italic;
        }
        .view-file-btn {
            display: inline-block;
            padding: 6px 12px;
            background-color: #1a73e8;
            color: white;
            text-decoration: none;
            border-radius: 4px;
            font-size: 14px;
            transition: background-color 0.2s;
        }
        .view-file-btn:hover {
            background-color: #1557b0;
        }
        .selected {
            background-color: #e8f0fe !important;
        }
        .view-current {
            margin-top: 20px;
            text-align: center;
        }
        .btn-current {
            display: inline-block;
            padding: 8px 16px;
            background-color: #34a853;
            color: white;
            text-decoration: none;
            border-radius: 4px;
            font-size: 14px;
            transition: background-color 0.2s;
        }
        .btn-current:hover {
            background-color: #2d8a46;
        }
        @media (max-width: 768px) {
            .content-wrapper {
                grid-template-columns: 1fr;
            }
            body {
                padding: 10px;
            }
            .container {
                padding: 15px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <?php echo $content; ?>
    </div>
</body>
</html> 