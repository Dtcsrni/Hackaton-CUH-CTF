<?php
function searchReports($pdo, $termino) {
    $sql = "SELECT titulo, area FROM reportes WHERE titulo LIKE '%$termino%'";
    return $pdo->query($sql);
}
?>
