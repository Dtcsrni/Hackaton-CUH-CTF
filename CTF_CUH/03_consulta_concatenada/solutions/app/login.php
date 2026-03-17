<?php
function authenticate($pdo, $usuario, $clave) {
    $stmt = $pdo->prepare("SELECT * FROM usuarios WHERE usuario = :usuario AND clave = :clave");
    $stmt->execute([':usuario' => $usuario, ':clave' => $clave]);
    return $stmt;
}
?>
