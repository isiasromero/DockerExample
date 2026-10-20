// Errores del dominio: no dependen de Express ni de MySQL.

class ErrorDeValidacion extends Error {
  constructor(errores) {
    super(errores.join(' '));
    this.name = 'ErrorDeValidacion';
    this.errores = errores;
  }
}

class CategoriaDuplicada extends Error {
  constructor() {
    super('Ya existe una categoría con ese código.');
    this.name = 'CategoriaDuplicada';
  }
}

class CategoriaInexistente extends Error {
  constructor() {
    super('La categoría seleccionada no existe.');
    this.name = 'CategoriaInexistente';
  }
}

module.exports = { ErrorDeValidacion, CategoriaDuplicada, CategoriaInexistente };
