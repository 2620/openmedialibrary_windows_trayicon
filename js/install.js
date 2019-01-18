'use strict';

(function() {

    loadImages(function(images) {
        loadScreen(images);
        initUpdate();
    });

    function initUpdate(browserSupported) {
        window.update = {};
        update.status = document.createElement('div');
        update.status.className = 'OxElement';
        update.status.style.position = 'absolute';
        update.status.style.left = '16px';
        update.status.style.top = '336px';
        update.status.style.right = 0;
        update.status.style.bottom = 0;
        update.status.style.width = '512px';
        update.status.style.height = '16px';
        update.status.style.margin = 'auto';
        update.status.style.textAlign = 'center';
        update.status.style.color = 'rgb(16, 16, 16)';
        update.status.style.fontFamily = 'Lucida Grande, Segoe UI, DejaVu Sans, Lucida Sans Unicode, Helvetica, Arial, sans-serif';
        update.status.style.fontSize = '11px';
        document.querySelector('#loadingScreen').appendChild(update.status);
        update.status.innerHTML = '';
        updateStatus();
    }

    function load() {
        var base = '//127.0.0.1:9842',
            ws = new WebSocket('ws:' + base + '/ws');
        ws.onopen = function(event) {
            document.location.href = 'http:' + base;
        };
        ws.onerror = function(event) {
            ws.close();
            setTimeout(load, 500);
        };
        ws.onclose = function(event) {
            setTimeout(load, 500);
        };
    }

    function loadImages(callback) {
        var images = {};
        images.logo = document.createElement('img');
        images.logo.onload = function() {
            images.logo.style.position = 'absolute';
            images.logo.style.left = 0;
            images.logo.style.top = 0;
            images.logo.style.right = 0;
            images.logo.style.bottom = '96px';
            images.logo.style.width = '256px';
            images.logo.style.height = '256px';
            images.logo.style.margin = 'auto';
            images.logo.style.MozUserSelect = 'none';
            images.logo.style.MSUserSelect = 'none';
            images.logo.style.OUserSelect = 'none';
            images.logo.style.WebkitUserSelect = 'none';
            images.loadingIcon = document.createElement('img');
            images.loadingIcon.setAttribute('id', 'loadingIcon');
            images.loadingIcon.style.position = 'absolute';
            images.loadingIcon.style.left = '16px';
            images.loadingIcon.style.top = '256px'
            images.loadingIcon.style.right = 0;
            images.loadingIcon.style.bottom = 0;
            images.loadingIcon.style.width = '32px';
            images.loadingIcon.style.height = '32px';
            images.loadingIcon.style.margin = 'auto';
            images.loadingIcon.style.MozUserSelect = 'none';
            images.loadingIcon.style.MSUserSelect = 'none';
            images.loadingIcon.style.OUserSelect = 'none';
            images.loadingIcon.style.WebkitUserSelect = 'none';
            images.loadingIcon.src = '/svg/symbolLoading.svg';
            callback(images);
        };
        images.logo.src = '/png/oml.png';
    }

    function loadScreen(images) {
        var loadingScreen = document.createElement('div');
        loadingScreen.setAttribute('id', 'loadingScreen');
        loadingScreen.className = 'OxScreen';
        loadingScreen.style.position = 'absolute';
        loadingScreen.style.width = '100%';
        loadingScreen.style.height = '100%';
        loadingScreen.style.backgroundColor = 'rgb(224, 224, 224)';
        loadingScreen.style.zIndex = '1002';
        loadingScreen.appendChild(images.logo);
        loadingScreen.appendChild(images.loadingIcon);
        // FF3.6 document.body can be undefined here
        window.onload = function() {
            document.body.style.margin = 0;
            document.body.appendChild(loadingScreen);
            startAnimation();
        };
        // IE8 does not call onload if already loaded before set
        document.body && window.onload();
    }


    function startAnimation() {
        var css, deg = 0, loadingIcon = document.getElementById('loadingIcon'),
            previousTime = +new Date();
        var animationInterval = setInterval(function() {
            var currentTime = +new Date(),
                delta = (currentTime - previousTime) / 1000;
            previousTime = currentTime;
            deg = Math.round((deg + delta * 360) % 360 / 30) * 30;
            css = 'rotate(' + deg + 'deg)';
            loadingIcon.style.MozTransform = css;
            loadingIcon.style.MSTransform = css;
            loadingIcon.style.OTransform = css;
            loadingIcon.style.WebkitTransform = css;
            loadingIcon.style.transform = css;
        }, 83);
    }

    function updateStatus() {
        var xhr = new XMLHttpRequest();
        xhr.onload = function() {
            var response = JSON.parse(this.responseText);
            if (response.step) {
                var status = response.step;
                if (response.progress) {
                    status = parseInt(response.progress * 100) + '% ' + status;
                }
                update.status.innerHTML = status;
                setTimeout(updateStatus, 1000);
            } else {
                update.status.innerHTML = 'Relaunching...';
                setTimeout(load, 500);
            }
        };
        xhr.onerror = function() {
            var status = update.status.innerHTML;
            if (['Relaunching...', ''].indexOf(status) == -1) {
                update.status.innerHTML = 'Installation failed';
            }
            load();
        }
        xhr.open('get', '/status');
        xhr.send();
    }

}());
