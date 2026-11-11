(function () {
  var stage = document.querySelector('.stage');
  var stageWidth = 1600;
  var stageHeight = 900;

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

  var screens = Array.prototype.slice.call(document.querySelectorAll('.screen'));
  var greeting = document.getElementById('greeting');
  var runtime = window.ClosellyInteractive;
  var name = runtime && runtime.context ? runtime.context.preferred_name : '';
  greeting.textContent = name ? 'Hola, ' + name + '.' : 'Hola.';

  function show(name) {
    screens.forEach(function (screen) {
      screen.classList.toggle('hidden', screen.getAttribute('data-screen') !== name);
    });
  }

  document.addEventListener('click', function (event) {
    var button = event.target.closest('button');
    if (!button) {
      return;
    }
    var action = button.getAttribute('data-action');
    if (action === 'begin') {
      notify('start');
      show('compare');
    }
    if (action === 'compare') {
      notify('progress', 'comparacion');
      show('close');
    }
    if (action === 'audio') {
      document.getElementById('clip').play().catch(function () {
        button.textContent = 'Reintentar audio';
      });
    }
    if (action === 'finish') {
      notify('complete');
      button.disabled = true;
    }
  });
})();

