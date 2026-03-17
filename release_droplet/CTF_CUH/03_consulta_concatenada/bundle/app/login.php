<?php
function authenticate($pdo, $usuario, $clave) {
    $query = "SELECT * FROM usuarios WHERE usuario = '$usuario' AND clave = '$clave'";
    return $pdo->query($query);
}
?>
