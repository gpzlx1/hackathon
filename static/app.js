var that = this;
function resizeIframe(obj) {
    obj.style.height = obj.contentWindow.document.body.scrollHeight + 'px';
}



window.onload = function (){
    var padding = parseInt($('iframe').contents().find('.clearfix').css('marginLeft')) + parseInt($('iframe').contents().find('.col-md-9').css('paddingLeft')) + "px";
    console.log(padding);
    $('.row-align').css("paddingLeft", padding);
};