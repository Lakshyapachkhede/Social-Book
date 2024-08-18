const modal = document.getElementById("simpleModal");
const closeBtn = document.querySelector('.closeBtn');
const cropBtn = document.querySelector('#btn-crop');

let cropper;

// closeBtn.addEventListener('click', closeModal);

function openModal() {
    modal.style.display = 'block';
}

function closeModal() {
    modal.style.display = 'none';
    if(cropper){
        cropper.destroy()
        cropper = null
    }
}

function handleCropping(inputElement, OutputImageElement, aspectRatio) {
    inputElement.addEventListener('change', function(event){
        if (event.target.files && event.target.files[0]){
            const url = URL.createObjectURL(event.target.files[0]);
            const image = document.getElementById('modal-image');
            image.src = url;
            openModal();

            if (cropper){
                cropper.destroy();
            }

            cropper = new Cropper(image, {
                aspectRatio: aspectRatio,
            });

            cropBtn.addEventListener('click', function(event){
                event.preventDefault();
                if (cropper){
                    let croppedImage = cropper.getCroppedCanvas().toDataURL('image/png');
                    const blob = dataURLToBlob(croppedImage);
                    const file = new File([blob], 'cropped_image.png', {type:'image/png'});

                    const dataTransfer = new DataTransfer();
                    dataTransfer.items.add(file);
                    inputElement.files = dataTransfer.files;
                    OutputImageElement.src = croppedImage;
                    closeModal();
                    
                }
            }, {once: true});
        }
    });
}

function dataURLToBlob(dataURL){
    const binary = atob(dataURL.split(',')[1]);
    const array = [];
    for (let i = 0; i < binary.length; i++) {
        array.push(binary.charCodeAt(i));
        
    }
    return new Blob([new Uint8Array(array)], {type: 'image/png' });
}


const user_image_input = document.getElementById("profile-image");
const user_image = document.getElementById("user-image");
handleCropping(user_image_input, user_image, 1);


const banner_image_input = document.getElementById("cover-image");
const banner_image = document.getElementById("banner-image");
handleCropping(banner_image_input, banner_image, 3.16);



















// const modal = document.getElementById('simpleModal');

// const closeBtn = document.querySelector('.closeBtn');

// closeBtn.addEventListener('click', closeModal);

// let cropper;

// function openModal() {
//     modal.style.display = 'block';
// }

// function closeModal() {
//     modal.style.display = 'none';
// }


// image_input = document.getElementById("cover-image");
// banner_image = document.getElementById("banner-image");

// image_input.addEventListener('change', function(event) {

//     if (event.target.files && event.target.files[0]) {
//         banner_image.src = URL.createObjectURL(event.target.files[0]);
//         let url = URL.createObjectURL(event.target.files[0]);
//         const image = document.getElementById("modal-image");
//         banner_image.src = url;
//         image.src = url;
//         openModal();

//         if (cropper){
//             cropper.destroy()
//         }

//         cropper = new Cropper(image, {
//             aspectRatio: 3.16,
//         });

//         document.querySelector("#btn-crop").addEventListener('click', function(event){
//             event.preventDefault();

//             var cropped_image = cropper.getCroppedCanvas().toDataURL('image/png');
//             const blob = dataURLToBlob(cropped_image);
//             const file = new File([blob], "cropped_image_cover.png", {type: 'image/png'});
            
//             const dataTransfer = new DataTransfer();
//             dataTransfer.items.add(file)
//             image_input.files = dataTransfer.files
//             banner_image.src = cropped_image;



//         })






//     }


// })


// user_image_input = document.getElementById("profile-image");
// user_image = document.getElementById("user-image");

// user_image_input.addEventListener('change', function(event) {

//     if (event.target.files && event.target.files[0]) {
//         url = URL.createObjectURL(event.target.files[0]);
//         const image = document.getElementById('modal-image');

//         user_image.src = url
//         image.src = url;
//         openModal();

//         if (cropper){
//             cropper.destroy();
//         }
//         cropper = new Cropper(image, {
//         aspectRatio: 1,
//         });
//         document.querySelector('#btn-crop').addEventListener('click', function(event) {
//             event.preventDefault();
//             var croppedImage = cropper.getCroppedCanvas().toDataURL("image/png");
        
//             const blob = dataURLToBlob(croppedImage);

//             const file = new File([blob], "cropped_image.png", {type: 'image/png'});

//             const dataTransfer = new DataTransfer();
//             dataTransfer.items.add(file);
//             user_image_input.files = dataTransfer.files;


//             user_image.src = croppedImage

//         });
//     }

// })



