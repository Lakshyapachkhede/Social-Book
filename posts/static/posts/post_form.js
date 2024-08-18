document.getElementById('id_images').addEventListener('change', function(event) {
    var files = event.target.files;
    var swiperWrapper = document.getElementById('swiper-wrapper');
    swiperWrapper.innerHTML = '';

    for (var i = 0; i < files.length; i++) {
        var file = files[i];

        if (file.type.startsWith('image/')) {
            var reader = new FileReader();
            reader.onload = function(e) {
                var slide = document.createElement('div');
                slide.className = 'swiper-slide';

                var img = document.createElement('img');
                img.src = e.target.result;
                img.className = 'post-img';
                img.style.maxWidth = '100%';

                slide.appendChild(img);
                swiperWrapper.appendChild(slide);
            }
            reader.readAsDataURL(file);
        }
    }
});
