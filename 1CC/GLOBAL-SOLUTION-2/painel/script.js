
// Rolagem da página sobre o mapa.
(() => {
  const quadro = document.querySelector('.mapa-integrado');
  if (!quadro) return;

  window.addEventListener('message', evento => {
    if (evento.source !== quadro.contentWindow) return;

    const dados = evento.data;
    if (!dados || dados.tipo !== 'vila-scroll-pagina') return;

    if (typeof dados.dy !== 'number' ||
        !Number.isFinite(dados.dy)) return;

    const dx = typeof dados.dx === 'number' &&
               Number.isFinite(dados.dx) ? dados.dx : 0;

    window.scrollBy(dx, dados.dy);
  });
})();
