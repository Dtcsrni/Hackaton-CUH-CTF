<?php
function searchReports($pdo, $termino) {
    $sql = "SELECT titulo, area FROM reportes WHERE titulo LIKE :termino";
    $stmt = $pdo->prepare($sql);
    $stmt->bindValue(':termino', '%' . $termino . '%');
    $stmt->execute();
    return $stmt;
}
?>
