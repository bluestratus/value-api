<?php
/**
 * Helper to call the internal Python service.
 * Returns decoded JSON as an array, or null on failure.
 */
function callPython(string $path, array $params = []): ?array {
    $base = getenv('PYTHON_SERVICE_URL') ?: 'http://python:8000';
    $url  = rtrim($base, '/') . '/' . ltrim($path, '/');

    if ($params) {
        $url .= '?' . http_build_query($params);
    }

    $ch = curl_init($url);
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_TIMEOUT        => 15,
        CURLOPT_FAILONERROR    => false,
    ]);

    $body = curl_exec($ch);
    $status = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    if ($body === false || $status < 200 || $status >= 300) {
        return null;
    }

    return json_decode($body, true);
}
