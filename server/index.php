<?php

require '/app/vendor/autoload.php';

Flight::route('GET /', function (): void {
    renderFrontend();
});

function renderFrontend(): void
{
    header('Content-Type: text/html; charset=UTF-8');
    echo '<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="/style.css">
<script type="module" src="/bundle.js"></script>
</head>
<body></body>
</html>';
}

Flight::start();
