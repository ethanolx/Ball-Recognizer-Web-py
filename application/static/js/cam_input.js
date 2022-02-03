const webcamElement = document.getElementById('webcam');
const canvasElement = document.getElementById('cam-canvas');
const canvasContext = canvasElement.getContext('2d');
const hiddenCanvas = document.getElementById('hidden-canvas');
const webcam = new Webcam(webcamElement, 'user', hiddenCanvas);
const webcamElement2 = document.getElementById('webcamhidden');
const webcamhidden = new Webcam(webcamElement2, 'user');
const hiddenImage = document.getElementById('hidden_img');

let CAM_PREDICTED = false;

function predict_cam() {
    if (!CAM_PREDICTED) {
        let picture = webcam.snap();
        webcam.stop();
        webcamElement.style.display = 'none';

        hiddenImage.src = picture;

        hiddenImage.onload = ev => {
            const SOURCE_DIMS = Math.max(webcamElement2.width, webcamElement2.height);
            const SOURCE_WIDTH = webcamElement2.height / SOURCE_DIMS * 220;
            const SOURCE_HEIGHT = webcamElement2.width / SOURCE_DIMS * 220;

            const CROP_LEFT = (220 - SOURCE_WIDTH) / 2;
            const CROP_RIGHT = (220 - SOURCE_HEIGHT) / 2;

            canvasContext.drawImage(hiddenImage, CROP_LEFT, CROP_RIGHT, SOURCE_WIDTH, SOURCE_HEIGHT, 0, 0, 220, 220);
            canvasElement.hidden = false;
            document.getElementById('result').innerText = 'Fetching prediction from server...';
            fetch(canvasElement.toDataURL('image/png'))
                .then(res => res.blob())
                .then(imgData => {
                    let img_form = new FormData();
                    img_form.append(name = 'image', value = imgData);
                    fetch('/predict', {
                        method: 'POST',
                        body: img_form
                    })
                        .then(res => res.json())
                        .then(result => {
                            document.getElementById('result').innerText = `I think it\'s a ${ result['prediction'] } (${ (result['probability'] * 100.0).toFixed(2) }%)`;
                        });
                });
        };
    }
    CAM_PREDICTED = true;
}

async function clear_cam() {
    webcamElement.style.display = 'block';
    canvasElement.hidden = true;
    webcam.start();
    CAM_PREDICTED = false;
}

