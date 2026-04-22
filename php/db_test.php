<?php
// Database connection configuration - PHP 5.4 Compatible
$host = getenv('DB_HOST') ?: 'db';
$port = getenv('DB_PORT') ?: 3306;
$dbname = getenv('DB_NAME') ?: 'value';
$user = getenv('DB_USER') ?: 'user';
$password = getenv('DB_PASSWORD') ?: 'password';

try {
    $dsn = "mysql:host=" . $host . ";port=" . $port . ";dbname=" . $dbname . ";charset=utf8";
    $pdo = new PDO($dsn, $user, $password, array(
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        PDO::ATTR_EMULATE_PREPARES => false,
    ));

    echo "Database connection successful!<br>";

    // Example query
    $stmt = $pdo->query("SHOW TABLES");
    $tables = $stmt->fetchAll();

    echo "Tables in database:<br>";
    echo "<ul>";
    foreach ($tables as $table) {
        echo "<li>" . htmlspecialchars($table['Tables_in_' . $dbname]) . "</li>";
    }
    echo "</ul>";

} catch (PDOException $e) {
    echo "Database connection failed: " . $e->getMessage();
}
?>