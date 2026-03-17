<?php
function loginLegacy($pdo, $usuario, $clave) {
    $stmt = $pdo->prepare("SELECT * FROM usuarios WHERE usuario = :usuario");
    $stmt->execute([':usuario' => $usuario]);
    $user = $stmt->fetch();
    if (!$user) {
        return false;
    }
    return password_verify($clave, $user['clave_hash']);
}
?>
