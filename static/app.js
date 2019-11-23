var that = this;
function resizeIframe(obj) {
    obj.style.height = obj.contentWindow.document.body.scrollHeight + 'px';
}

// function send_json(data) {
//     that.send(data);
// }

// function send(data) {
//     var url_upload_json = '192.168.43.217:5000/train';
//     console.log(data);
//     $.post(
//         url_upload_json,
//         data,
//         function (response_data) {
//             // $('.toast').toast('show');
//             console.log(response_data);
//         },
//         'json'
//     );
// }