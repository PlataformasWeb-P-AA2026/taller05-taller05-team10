import './style.css';
import DataTable from 'datatables.net-dt';
import 'datatables.net-dt/css/dataTables.dataTables.css';
import { CONFIG } from './config.js';

let tabla = null;

function parsearValor(valor) {
  if (valor === "") return null;
  const numero = Number(valor);
  if (!isNaN(numero)) return numero;
  return valor;
}

async function cargarDatos(vista = CONFIG.VISTAS.POR_CLUB, filtro = "") {
  try {
    let url = `${CONFIG.BASE_URL}${vista}`;
    const v = parsearValor(filtro);

    if (filtro !== "") {
      url += `?key=${encodeURIComponent(JSON.stringify(v))}`;
    }

    const options = {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    };

    // Solo agregar autenticación si existe
    if (CONFIG.AUTH_HEADER) {
      options.headers['Authorization'] = CONFIG.AUTH_HEADER;
    }

    const respuesta = await fetch(url, options);

    if (!respuesta.ok) {
      throw new Error(`Error ${respuesta.status}: ${respuesta.statusText}`);
    }

    const json = await respuesta.json();

    if (!json.rows || json.rows.length === 0) {
      alert("⚠️ La vista no devolvió datos.");
      return;
    }

    const datos = json.rows.map(row => ({
      criterio: row.key ?? "",
      nombre: row.value?.nombre ?? "",
      seleccion: row.value?.seleccion ?? "",
      posicion: row.value?.posicion ?? "",
      edad: row.value?.edad ?? ""
    }));

    if (tabla) {
      tabla.destroy();
      document.querySelector("#tabla-posts").innerHTML = "";
    }

    tabla = new DataTable("#tabla-posts", {
      data: datos,
      columns: [
        { data: "criterio", title: "Criterio" },
        { data: "nombre", title: "Nombre" },
        { data: "seleccion", title: "Selección" },
        { data: "posicion", title: "Posición" },
        { data: "edad", title: "Edad" }
      ],
      pageLength: 10,
      language: {
        search: "Buscar:",
        lengthMenu: "Mostrar _MENU_ registros",
        info: "Mostrando _START_ a _END_ de _TOTAL_ registros",
        infoEmpty: "No hay registros",
        zeroRecords: "Sin resultados",
        paginate: { previous: "Anterior", next: "Siguiente" }
      }
    });

  } catch (error) {
    console.error("❌ Error:", error);
    alert(error.message);
  }
}

document.getElementById("vista").addEventListener("change", function () {
  document.getElementById("filtro").value = "";
  cargarDatos(this.value);
});

document.getElementById("filtro").addEventListener("keyup", function () {
  const vista = document.getElementById("vista").value;
  cargarDatos(vista, this.value.trim());
});

cargarDatos();