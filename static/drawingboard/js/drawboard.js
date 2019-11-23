let canvas = document.getElementById("drawing-board");
let ctx = canvas.getContext("2d");
let eraser = document.getElementById("eraser");
let brush = document.getElementById("brush");
let reSetCanvas = document.getElementById("clear");
let aColorBtn = document.getElementsByClassName("color-item");
let save = document.getElementById("save");
let undo = document.getElementById("undo");
let range = document.getElementById("range");
let run = document.getElementById("run");
let clear = false;
let activeColor = 'black';
let lWidth = 4;
let X = canvas.getBoundingClientRect().left;
let Y = canvas.getBoundingClientRect().top;
// let Y = canvas.clientTop;

autoSetSize(canvas);

setCanvasBg('white');

listenToUser(canvas);

getColor();



function autoSetSize(canvas) {
    canvasSetSize();

    function canvasSetSize() {
        //let pageWidth = canvas.parentNode.clientWidth;
        let pageHeight = 280;

        canvas.width = canvas.parentNode.clientWidth;
        // console.log(canvas.width);
        canvas.height = pageHeight;
    }

    window.onresize = function () {
        canvasSetSize();
    }
}

function setCanvasBg(color) {
    ctx.fillStyle = color;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = "black";
}

function listenToUser(canvas) {
    let painting = false;
    let lastPoint = { x: undefined, y: undefined };
    canvas.onmousedown = function (e) {
        this.firstDot = ctx.getImageData(0, 0, canvas.width, canvas.height);//在这里储存绘图表面
        saveData(this.firstDot);
        painting = true;
        // console.log(e.clientY);
        // console.log(Y);
        // let x = e.clientX - X;
        // let y = e.clientY - Y;

        var rect = canvas.getBoundingClientRect();
        var x = event.clientX - rect.left * (canvas.width / rect.width);
        var y = event.clientY - rect.top * (canvas.height / rect.height);

        lastPoint = { "x": x, "y": y };
        ctx.save();
        drawCircle(x, y, 0);
    };
    canvas.onmousemove = function (e) {
        if (painting) {
            var rect = canvas.getBoundingClientRect();
            var x = event.clientX - rect.left * (canvas.width / rect.width);
            var y = event.clientY - rect.top * (canvas.height / rect.height);
            let newPoint = { "x": x, "y": y };
            // console.log(1,lastPoint.x);
            // console.log(2,lastPoint.y);
            // console.log(3,newPoint.x);
            // console.log(4,newPoint.y);

            drawLine(lastPoint.x, lastPoint.y, newPoint.x, newPoint.y, clear);
            lastPoint = newPoint;
        }
    };

    canvas.onmouseup = function () {
        painting = false;
    };

    canvas.mouseleave = function () {
        painting = false;
    };

}

function drawCircle(x, y, radius) {
    ctx.save();
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, Math.PI * 2);
    ctx.fill();
    if (clear) {
        ctx.clip();
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.restore();
    }
}

function drawLine(x1, y1, x2, y2) {
    ctx.lineWidth = lWidth;
    ctx.lineCap = "round";
    ctx.lineJoin = "round";
    if (clear) {
        ctx.save();
        ctx.globalCompositeOperation = "destination-out";
        ctx.moveTo(x1, y1);
        ctx.lineTo(x2, y2);
        ctx.stroke();
        ctx.closePath();
        ctx.clip();
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.restore();
    } else {
        ctx.moveTo(x1, y1);
        ctx.lineTo(x2, y2);
        ctx.stroke();
        ctx.closePath();
    }
}

range.onchange = function () {
    lWidth = this.value;
};

eraser.onclick = function () {
    clear = true;
    this.classList.add("active");
    brush.classList.remove("active");
};

brush.onclick = function () {
    clear = false;
    this.classList.add("active");
    eraser.classList.remove("active");
};

reSetCanvas.onclick = function () {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    setCanvasBg('white');
};

save.onclick = function () {
    let imgUrl = canvas.toDataURL("image/png");
    let saveA = document.createElement("a");
    document.body.appendChild(saveA);
    saveA.href = imgUrl;
    saveA.download = "zspic" + (new Date).getTime();
    saveA.target = "_blank";
    saveA.click();
};

function getColor() {
    for (let i = 0; i < aColorBtn.length; i++) {
        aColorBtn[i].onclick = function () {
            for (let i = 0; i < aColorBtn.length; i++) {
                aColorBtn[i].classList.remove("active");
                this.classList.add("active");
                activeColor = this.style.backgroundColor;
                ctx.fillStyle = activeColor;
                ctx.strokeStyle = activeColor;
            }
        }
    }
}

let historyDeta = [];

function saveData(data) {
    (historyDeta.length === 10) && (historyDeta.shift());// 上限为储存10步，太多了怕挂掉
    historyDeta.push(data);
}

undo.onclick = function () {
    if (historyDeta.length < 1) return false;
    ctx.putImageData(historyDeta[historyDeta.length - 1], 0, 0);
    historyDeta.pop();
};


run.onclick = function () {
    var url_upload_img = 'http://127.0.0.1:5000/predict';
    var img_data = canvas.toDataURL('image/png', 1);  //1表示质量(无损压缩)
    console.log(img_data);

    var bars = $('.progress-bar'); //概率条
    var spinners = $('.spinner-border'); //加载圈圈
    var question_marks = $('.question-mark');
    var icon_number = $('.icon-number');
    question_marks.hide();
    icon_number.hide();
    spinners.show();
    for (var i = 0; i < bars.length; i++) {
        percent = 0 + '%';
        bars[i].style.width = percent;
        bars[i].innerHTML = '';
    }

    $.post(
        url_upload_img,
        { img_base64: img_data },
        function (data) {
            $('.toast').toast('show');
            predict(data);
            //$('.spinner-border').show();
        },
        'json'
    );
};

