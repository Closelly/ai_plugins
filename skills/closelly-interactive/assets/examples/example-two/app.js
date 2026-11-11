(function () {
  var stage = document.querySelector('.stage');
  var stageWidth = 900;
  var stageHeight = 1600;

  function fitStage() {
    var width = window.innerWidth;
    var height = window.innerHeight;
    if (width < 1 || height < 1) return;
    var scale = Math.min(width / stageWidth, height / stageHeight);
    stage.style.transform = 'scale(' + scale + ')';
    stage.style.left = ((width - stageWidth * scale) / 2) + 'px';
    stage.style.top = ((height - stageHeight * scale) / 2) + 'px';
  }

  fitStage();
  window.addEventListener('load', fitStage);
  window.addEventListener('resize', fitStage);
  window.addEventListener('pageshow', fitStage);
  document.addEventListener('visibilitychange', function () {
    if (!document.hidden) fitStage();
  });
  if (typeof ResizeObserver === 'function') {
    var viewportObserver = new ResizeObserver(fitStage);
    viewportObserver.observe(document.documentElement);
  }

  // The same example can be reviewed locally without a fake Closelly runtime.
  function notify(method, step) {
    var runtime = window.ClosellyInteractive;
    if (!runtime || typeof runtime[method] !== 'function') return;
    try {
      var result = step ? runtime[method](step) : runtime[method]();
      if (result && typeof result.catch === 'function') result.catch(function () {});
    } catch (error) { /* A tracking failure must not block the content. */ }
  }

  var greeting = document.getElementById('greeting');
  var runtime = window.ClosellyInteractive;
  var name = runtime && runtime.context ? runtime.context.preferred_name : '';
  greeting.textContent = name ? 'Hola, ' + name + '.' : 'Hola.';

  document.addEventListener('click', function (event) {
    var button = event.target.closest('button');
    if (!button) {
      return;
    }
    var action = button.getAttribute('data-action');
    if (action === 'begin') {
      notify('start');
      button.disabled = true;
      document.getElementById('choice').classList.remove('hidden');
    }
    if (action === 'wrong') {
      notify('progress', 'intento');
      document.getElementById('feedback').textContent = 'Revisa la otra opción y vuelve a intentarlo.';
    }
    if (action === 'right') {
      notify('progress', 'respuesta');
      document.getElementById('feedback').textContent = '';
      document.querySelectorAll('#choice button').forEach(function (choice) { choice.disabled = true; });
      notify('complete');
      button.disabled = true;
      document.getElementById('result').classList.remove('hidden');
    }
  });
})();

