var bars = $('.progress-bar'); //概率条
var spinners = $('.spinner-border'); //加载圈圈
var question_marks = $('.question-mark');
var icon_number = $('.icon-number');

function predict(data) {
    spinners.hide();
    var percent;
    var icon_number_path = 'assets/icon/';
    var results = get_results(data);
    //set possibility bars & show number
    for (var i = 0; i < bars.length; i++) {
        percent = parseFloat(results[i].possibility) * 100;
        percent = percent + '%';
        bars[i].style.width = percent;
        bars[i].style.color = '555555';
        bars[i].innerHTML = results[i].possibility;
        icon_number[i].src = icon_number_path + results[i].number + '.svg';
    }
    icon_number.show();
}

function get_results(data) {
    // data = { '0': "0.018187048", '1': "0.26717097", '2': "0.09005827", '3': "0.15439759", '4': "0.030748086", '5': "0.22214343", '6': "0.011058615", '7': "0.15827371", '8': '0.001', '9': '0.0001' };
    console.log(data);
    var results = [];
    var possibility = [];
    var reverse = {};
    for (var i = 0; i <= 9; i++) {
        possibility[i] = data[i.toString()];
        reverse[data[i.toString()]] = i;
    }
    possibility.sort();
    possibility.reverse();


    for (i = 0; i <= 5; i++) {
        results[i] = { 'number': reverse[possibility[i].toString()], 'possibility': possibility[i] };
    }
    // var results = [
    //     { 'number': 1, 'possibility': 0.3 },
    //     { 'number': 2, 'possibility': 0.25 },
    //     { 'number': 8, 'possibility': 0.2 },
    //     { 'number': 5, 'possibility': 0.1 },
    //     { 'number': 7, 'possibility': 0.1 },
    //     { 'number': 0, 'possibility': 0.01 }
    // ];
    return results;
}