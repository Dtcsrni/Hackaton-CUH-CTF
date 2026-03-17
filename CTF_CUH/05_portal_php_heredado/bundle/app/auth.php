<?php
function loginLegacy($pdo, $usuario, $clave) {
    $sql = "SELECT * FROM usuarios WHERE usuario = '$usuario'";
    $user = $pdo->query($sql)->fetch();
    if (!$user) {
        return false;
    }
    return md5($clave) === $user['clave_hash'];
}
?>
