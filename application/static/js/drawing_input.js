let DRAWING_PREDICTED = false;

// Sensible Default Values
const DEFAULT_BRUSH_WIDTH = 20;
const DEFAULT_BRUSH_COLOUR = '#000000';

// Initialise Canvas and Canvas Context variables
let CANVAS = document.getElementById('canvas');
let CANVAS_CONTEXT = CANVAS.getContext('2d');

// Initialise Settings
let BRUSH_WIDTH_SELECTOR = document.getElementById('brush-width');
let BRUSH_CURRENT_WIDTH = document.getElementById('current-width');
let BRUSH_COLOUR_SELECTOR = document.getElementById('brush-colour');
let BRUSH_PREVIEW = document.getElementById('brush-preview');
CANVAS_CONTEXT.lineCap = CANVAS_CONTEXT.lineJoin = 'round';

// Initialise Canvas Drawing Utilities
let ORIGIN_COORDS = { x: 0, y: 0 };
let DESTINATION_COORDS = { x: 0, y: 0 };


function load_defaults() {
    BRUSH_WIDTH_SELECTOR.value = DEFAULT_BRUSH_WIDTH;
    BRUSH_COLOUR_SELECTOR.value = DEFAULT_BRUSH_COLOUR;
}

function load_canvas() {
    CANVAS_CONTEXT.fillStyle = 'white';
    CANVAS_CONTEXT.fillRect(0, 0, CANVAS.width, CANVAS.height);
}

function load_page() {
    load_defaults();
    load_canvas();
    updatePreview();
    load_event_listeners();
}

function update_brush_parameters() {
    CANVAS_CONTEXT.lineWidth = parseInt(BRUSH_WIDTH_SELECTOR.value);
    CANVAS_CONTEXT.strokeStyle = BRUSH_COLOUR_SELECTOR.value;
}

function begin_paint(ev) {
    CANVAS_CONTEXT.moveTo(ORIGIN_COORDS.x, ORIGIN_COORDS.y);
    CANVAS_CONTEXT.beginPath();
    PAINT_ON = true;
    DRAWING_PREDICTED = false;
}

let PAINT_ON = false;

function paint(ev) {
    const RECT = CANVAS.getBoundingClientRect();
    DESTINATION_COORDS.x = ev.clientX - RECT.left;
    DESTINATION_COORDS.y = ev.clientY - RECT.top;

    ORIGIN_COORDS.x = DESTINATION_COORDS.x;
    ORIGIN_COORDS.y = DESTINATION_COORDS.y;
    if (PAINT_ON) {
        CANVAS_CONTEXT.lineTo(DESTINATION_COORDS.x, DESTINATION_COORDS.y);
        CANVAS_CONTEXT.stroke();
    }
}

function paint_mobile(ev) {
    const RECT = CANVAS.getBoundingClientRect();

    let evt = (typeof ev.originalEvent === 'undefined') ? ev : ev.originalEvent;
    let touch = evt.touches[0] || evt.changedTouches[0];
    DESTINATION_COORDS.x = touch.pageX - RECT.left;
    DESTINATION_COORDS.y = touch.pageY - RECT.top;

    ORIGIN_COORDS.x = DESTINATION_COORDS.x;
    ORIGIN_COORDS.y = DESTINATION_COORDS.y;
    if (PAINT_ON) {
        CANVAS_CONTEXT.lineTo(DESTINATION_COORDS.x, DESTINATION_COORDS.y);
        CANVAS_CONTEXT.stroke();
    }
}

function end_paint(ev) {
    PAINT_ON = false;
}

function updatePreview() {
    let BRUSH_PREVIEW_CONTEXT = BRUSH_PREVIEW.getContext('2d');
    BRUSH_PREVIEW.width = parseInt(BRUSH_WIDTH_SELECTOR.value);
    BRUSH_PREVIEW.height = parseInt(BRUSH_WIDTH_SELECTOR.value);
    BRUSH_PREVIEW_CONTEXT.fillStyle = BRUSH_COLOUR_SELECTOR.value;
    BRUSH_PREVIEW_CONTEXT.fillRect(0, 0, BRUSH_PREVIEW.width, BRUSH_PREVIEW.height);
    BRUSH_CURRENT_WIDTH.innerText = BRUSH_WIDTH_SELECTOR.value;

    update_brush_parameters();
}

function load_event_listeners() {
    CANVAS.addEventListener("mousedown", begin_paint, false);
    CANVAS.addEventListener("mousemove", paint, false);
    CANVAS.addEventListener("mouseup", end_paint, false);
    CANVAS.addEventListener("touchstart", (ev) => {
        ev.preventDefault();
        ev.stopPropagation();
        begin_paint(ev);
    });
    CANVAS.addEventListener("touchmove", (ev) => {
        ev.preventDefault();
        ev.stopPropagation();
        paint_mobile(ev);
    });
    CANVAS.addEventListener("touchend", (ev) => {
        ev.preventDefault();
        ev.stopPropagation();
        end_paint(ev);
    });
};


function clear_canvas() {
    CANVAS_CONTEXT.clearRect(0, 0, 220, 220);
    CANVAS_CONTEXT.fillStyle = "white";
    CANVAS_CONTEXT.fillRect(0, 0, CANVAS.width, CANVAS.height);
    DRAWING_PREDICTED = false;
}

function predict_drawing() {
    if (!DRAWING_PREDICTED) {
        document.getElementById('result').innerText = 'Fetching prediction from server...';
        CANVAS.toBlob(blob => {
            let img_form = new FormData();
            img_form.append(name = 'image', value = blob);

            fetch('/predict', {
                method: 'POST',
                body: img_form
            })
                .then(res => res.json())
                .then(result => {
                    document.getElementById('result').innerText = `I think it\'s a ${ result['prediction'] } (${ (result['probability'] * 100.0).toFixed(2) }%)`;
                });
        }, 'image/png');
    }
    DRAWING_PREDICTED = true;
}

load_page();
