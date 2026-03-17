async function cargarEstado() {
  const respuesta = await fetch("https://api.cuh.lab/status");
  const data = await respuesta.json();
  document.getElementById("estado").textContent = data.estado;
}

cargarEstado();
