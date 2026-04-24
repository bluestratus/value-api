<?php
// PHP CanPrice Service - PHP 5.4 Compatible
// Replaces the Python canprice_service.py

function getDatabaseConnection() {
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
        return $pdo;
    } catch (PDOException $e) {
        error_log("Database connection failed: " . $e->getMessage());
        return null;
    }
}

function getMakes($pdo) {
    $stmt = $pdo->prepare("SELECT DISTINCT make FROM datasource ORDER BY make ASC");
    $stmt->execute();
    return $stmt->fetchAll(PDO::FETCH_COLUMN);
}

function makeExists($pdo, $make) {
    $stmt = $pdo->prepare("SELECT 1 FROM datasource WHERE make = ? LIMIT 1");
    $stmt->execute(array($make));
    return $stmt->fetch() !== false;
}

function getYears($pdo, $make) {
    $stmt = $pdo->prepare(
        "SELECT DISTINCT year FROM datasource WHERE make = ? ORDER BY year DESC"
    );
    $stmt->execute(array($make));
    return $stmt->fetchAll(PDO::FETCH_COLUMN);
}

function getModels($pdo, $make, $year) {
    $stmt = $pdo->prepare(
        "SELECT DISTINCT model FROM datasource WHERE make = ? AND year = ? ORDER BY model ASC"
    );
    $stmt->execute(array($make, $year));
    return $stmt->fetchAll(PDO::FETCH_COLUMN);
}

function runQuery($pdo, $make, $year, $modelPrefix, $debug = false) {
    $sql = "
        SELECT *
        FROM datasource
        WHERE make = ?
          AND year = ?
          AND model LIKE ?
        LIMIT 1
    ";
    $params = array($make, $year, $modelPrefix . '%');

    if ($debug) {
        error_log("SQL: " . $sql);
        error_log("PARAMS: " . json_encode($params));
    }

    try {
        $stmt = $pdo->prepare($sql);
        $stmt->execute($params);
        return $stmt->fetch();
    } catch (PDOException $e) {
        error_log("Query execution failed: " . $e->getMessage());
        return null;
    }
}

function pricenew($make, $model, $year, $debug = false) {
    $pdo = getDatabaseConnection();
    if (!$pdo) {
        return array("status" => "error", "make" => $make, "model" => $model, "year" => $year, "price_new" => 0);
    }

    try {
        $lastYear = $year - 1;
        $nextYear = $year + 1;
        $parts = explode(' ', trim($model));

        // 1. Exact year, full model prefix
        $row = runQuery($pdo, $make, $year, $model, $debug);
        if ($row) {
            return array("status" => "success", "make" => $make, "model" => $model, "year" => $year, "price_new" => intval($row["price_new"]));
        }

        // 2. First 4 parts, same year / last year / next year
        if (count($parts) > 3) {
            $prefix4 = implode(' ', array_slice($parts, 0, 4));

            $row = runQuery($pdo, $make, $year, $prefix4, $debug);
            if ($row) {
                return array("status" => "success", "make" => $make, "model" => $model, "year" => $year, "price_new" => intval($row["price_new"]));
            }

            $row = runQuery($pdo, $make, $lastYear, $prefix4, $debug);
            if ($row) {
                return array("status" => "success", "make" => $make, "model" => $model, "year" => $year, "price_new" => intval($row["price_new"]));
            }

            $row = runQuery($pdo, $make, $nextYear, $prefix4, $debug);
            if ($row) {
                return array("status" => "success", "make" => $make, "model" => $model, "year" => $year, "price_new" => intval($row["price_new"]));
            }
        }

        // 3. First 3 parts, same year / last year / next year
        if (count($parts) > 2) {
            $prefix3 = implode(' ', array_slice($parts, 0, 3));

            $row = runQuery($pdo, $make, $year, $prefix3, $debug);
            if ($row) {
                return array("status" => "success", "make" => $make, "model" => $model, "year" => $year, "price_new" => intval($row["price_new"]));
            }

            $row = runQuery($pdo, $make, $lastYear, $prefix3, $debug);
            if ($row) {
                return array("status" => "success", "make" => $make, "model" => $model, "year" => $year, "price_new" => intval($row["price_new"]));
            }

            $row = runQuery($pdo, $make, $nextYear, $prefix3, $debug);
            if ($row) {
                return array("status" => "success", "make" => $make, "model" => $model, "year" => $year, "price_new" => intval($row["price_new"]));
            }

            // 4. First 2 parts, only if first part length > 2, same year only
            if (strlen($parts[0]) > 2) {
                $prefix2 = implode(' ', array_slice($parts, 0, 2));

                $row = runQuery($pdo, $make, $year, $prefix2, $debug);
                if ($row) {
                    return array("status" => "success", "make" => $make, "model" => $model, "year" => $year, "price_new" => intval($row["price_new"]));
                }
            }
        }

        return array("status" => "failed", "make" => $make, "model" => $model, "year" => $year, "price_new" => 0);

    } catch (Exception $e) {
        error_log("CanPrice service error: " . $e->getMessage());
        return array("status" => "error", "make" => $make, "model" => $model, "year" => $year, "price_new" => 0);
    } finally {
        $pdo = null;
    }
}

// API Endpoint handler
header('Content-Type: application/json');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(array("error" => "Method not allowed. Use POST."));
    exit;
}

$input = json_decode(file_get_contents('php://input'), true) ?: array();
$pdo   = getDatabaseConnection();

if (!$pdo) {
    http_response_code(503);
    echo json_encode(array("status" => "error", "message" => "Database unavailable, please try again shortly."));
    exit;
}

// Step 1: need make
if (!isset($input['make']) || trim($input['make']) === '') {
    echo json_encode(array(
        "status"  => "incomplete",
        "parameter"   => "make",
        "message" => "What is the make of the vehicle? (e.g. Ford, BMW, Toyota)"
    ));
    exit;
}

$make = trim($input['make']);

if (!makeExists($pdo, $make)) {
    echo json_encode(array(
        "status"    => "invalid",
        "parameter" => "make",
        "message"   => "\"$make\" was not found in our database. Please choose from the list.",
        "options"   => getMakes($pdo)
    ));
    exit;
}

// Step 2: need year
if (!isset($input['year']) || trim($input['year']) === '') {
    echo json_encode(array(
        "status"   => "incomplete",
        "parameter"    => "year",
        "message"  => "Got it — $make. What year was the vehicle registered?",
        "options"  => getYears($pdo, $make)
    ));
    exit;
}

$year   = intval($input['year']);
$models = getModels($pdo, $make, $year);

if (empty($models)) {
    echo json_encode(array(
        "status"    => "invalid",
        "parameter" => "year",
        "message"   => "No vehicles found for $make in $year. Please choose from the list.",
        "options"   => getYears($pdo, $make)
    ));
    exit;
}

// Step 3: need model
if (!isset($input['model']) || trim($input['model']) === '') {
    echo json_encode(array(
        "status"  => "incomplete",
        "parameter"   => "model",
        "message" => "Which model? Please choose from the list.",
        "options" => $models
    ));
    exit;
}

$model = trim($input['model']);

if (!in_array($model, $models)) {
    echo json_encode(array(
        "status"  => "invalid",
        "parameter"   => "model",
        "message" => "\"$model\" was not found. Please choose from the list.",
        "options" => $models
    ));
    exit;
}

$debug  = isset($input['debug']) ? $input['debug'] : false;
$result = pricenew($make, $model, $year, $debug);
echo json_encode($result);
?>