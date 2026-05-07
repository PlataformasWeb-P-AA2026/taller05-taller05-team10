/**
 * config.js
 * Configuración centralizada para el frontend
 */

export const CONFIG = {
  // URL base de CouchDB
  COUCHDB_HOST: 'localhost',
  COUCHDB_PORT: 5984,
  
  // Base de datos
  DB_NAME: 'jugadores',
  
  // Design Document
  DESIGN_DOC: 'losjugadores',
  
  // Credenciales (dejar vacío si la BD no tiene permisos)
  USUARIO: '',
  PASSWORD: '',
  
  // Vistas disponibles
  VISTAS: {
    POR_CLUB: 'por_club',
    POR_GOLES: 'por_goles',
    POR_PARTIDOS: 'por_partidos'
  }
};

// URL completa generada automáticamente
CONFIG.COUCHDB_URL = `http://${CONFIG.COUCHDB_HOST}:${CONFIG.COUCHDB_PORT}`;
CONFIG.BASE_URL = `${CONFIG.COUCHDB_URL}/${CONFIG.DB_NAME}/_design/${CONFIG.DESIGN_DOC}/_view/`;

// Auth header (solo si hay credenciales)
CONFIG.AUTH_HEADER = CONFIG.USUARIO && CONFIG.PASSWORD
  ? 'Basic ' + btoa(`${CONFIG.USUARIO}:${CONFIG.PASSWORD}`)
  : null;