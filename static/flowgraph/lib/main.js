$(document).ready(function() {
  $('.flowchart-example').each(function() {
    var $this = $(this);
    var $script = $this.find('script');
    var source = $script.text();
    var $source = $('<pre></pre>');
    $source.text(source);
    $this.append($source);

    var $start_info = $('#start_info');
    var $end_info = $('#end_info');
    var $conv_info = $('#conv_info');
    var $pool_info = $('#pool_info');
    var $act_info = $('#act_info');
    var $dense_info = $('#dense_info');
    var $dropout_info = $('#dropout_info');
    $start_info.hide();
    $end_info.hide();
    $act_info.hide();
    $conv_info.hide();
    $pool_info.hide();
    $dense_info.hide();
    $dropout_info.hide();
  });
});