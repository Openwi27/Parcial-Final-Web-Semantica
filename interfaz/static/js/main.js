function toggleSecciones() {
    const tipo = document.getElementById('tipo');
    if (!tipo) return;

    const valor = tipo.value;
    ['usuario', 'alimento', 'condicion'].forEach(function (seccion) {
        const el = document.getElementById('sec-' + seccion);
        if (el) el.style.display = 'none';
    });

    if (valor) {
        const activo = document.getElementById('sec-' + valor);
        if (activo) activo.style.display = 'block';
    }
}
