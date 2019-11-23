$(document).ready(function () {
  var $flowchart = $('#example_9');
  var $container = $flowchart.parent();

  var cx = $flowchart.width() / 2;
  var cy = $flowchart.height() / 2;


  // Panzoom initialization...
  $flowchart.panzoom();

  // Centering panzoom
  $flowchart.panzoom('pan', -cx + $container.width() / 2, -cy + $container.height() / 2);

  // Panzoom zoom handling...
  var possibleZooms = [0.5, 0.75, 1, 2, 3];
  var currentZoom = 2;
  $container.on('mousewheel.focal', function (e) {
    e.preventDefault();
    var delta = (e.delta || e.originalEvent.wheelDelta) || e.originalEvent.detail;
    var zoomOut = delta ? delta < 0 : e.originalEvent.deltaY > 0;
    currentZoom = Math.max(0, Math.min(possibleZooms.length - 1, (currentZoom + (zoomOut * 2 - 1))));
    $flowchart.flowchart('setPositionRatio', possibleZooms[currentZoom]);
    $flowchart.panzoom('zoom', possibleZooms[currentZoom], {
      animate: false,
      focal: e
    });
  });
  var data = {
    operators: {},
    links: {}
  };

  var $start_info = $('#start_info');
  var $start_dim = $('#start_dim');

  var $end_info = $('#end_info');
  var $end_dim = $('#end_dim');

  var $conv_info = $('#conv_info');
  var $conv_sizeX = $('#conv_sizeX');
  var $conv_sizeY = $('#conv_sizeY');
  var $conv_strideX = $('#conv_strideX');
  var $conv_strideY = $('#conv_strideY');
  var $conv_channel = $('#conv_channel');

  var $pool_info = $('#pool_info');
  var $pool_sizeX = $('#pool_sizeX');
  var $pool_sizeY = $('#pool_sizeY');
  var $pool_strideX = $('#pool_strideX');
  var $pool_strideY = $('#pool_strideY');

  var $act_info = $('#act_info');
  var $act_func = $('#act_func');

  var $dense_info = $('#dense_info');
  var $dense_num = $('#dense_num');

  var $dropout_info = $('#dropout_info');
  var $dropout_rate = $('#dropout_rate');


  // Apply the plugin on a standard, empty div...
  $flowchart.flowchart({
    data: data,
    linkWidth: 6,
    multipleLinksOnInput: true,
    multipleLinksOnOutput: true,
    onOperatorSelect: function (operatorId) {
      var Title = $flowchart.flowchart('getOperatorTitle', operatorId);
      var opData = $flowchart.flowchart('getOperatorInfo', operatorId);
      if (Title.substring(0, 10) == 'Start Node') {
        $start_info.show();
        $start_dim.val(opData.InputDim);
        $end_info.hide();
        $act_info.hide();
        $conv_info.hide();
        $pool_info.hide();
        $dense_info.hide();
        $dropout_info.hide();
      }
      else if (Title.substring(0, 8) == 'End Node') {
        $end_info.show();
        $end_dim.val(opData.OutputDim);
        $start_info.hide();
        $act_info.hide();
        $conv_info.hide();
        $pool_info.hide();
        $dense_info.hide();
        $dropout_info.hide();
      }
      else if (Title.substring(0, 10) == 'Activation') {
        $act_info.show();
        $act_func.val(opData.ActivationFunc);
        $start_info.hide();
        $end_info.hide();
        $conv_info.hide();
        $pool_info.hide();
        $dense_info.hide();
        $dropout_info.hide();
      }
      else if (Title.substring(0, 15) == 'Fully-connected') {
        $dense_info.show();
        $dense_num.val(opData.num);
        $start_info.hide();
        $end_info.hide();
        $act_info.hide();
        $conv_info.hide();
        $pool_info.hide();
        $dropout_info.hide();
      }
      else if (Title.substring(0, 7) == 'Dropout') {
        $dropout_info.show();
        $dropout_rate.val(opData.rate);
        $start_info.hide();
        $end_info.hide();
        $act_info.hide();
        $conv_info.hide();
        $pool_info.hide();
        $dense_info.hide();
      }
      else if (Title.substring(0, 7) == 'Pooling') {
        $pool_info.show();
        $pool_sizeX.val(opData.sizeX);
        $pool_sizeY.val(opData.sizeY);
        $pool_strideX.val(opData.strideX);
        $pool_strideY.val(opData.strideY);
        $start_info.hide();
        $end_info.hide();
        $act_info.hide();
        $conv_info.hide();
        $dense_info.hide();
        $dropout_info.hide();
      }
      else if (Title.substring(0, 11) == 'Convolution') {
        $conv_info.show();
        $conv_sizeX.val(opData.sizeX);
        $conv_sizeY.val(opData.sizeY);
        $conv_strideX.val(opData.strideX);
        $conv_strideY.val(opData.strideY);
        $conv_channel.val(opData.channel);
        $start_info.hide();
        $end_info.hide();
        $act_info.hide();
        $pool_info.hide();
        $dense_info.hide();
        $dropout_info.hide();
      }
      return true;
    },
    onOperatorUnselect: function () {
      $start_info.hide();
      $end_info.hide();
      $act_info.hide();
      $conv_info.hide();
      $pool_info.hide();
      $dense_info.hide();
      $dropout_info.hide();
      return true;
    },
  });

  $start_dim.keyup(function () {
    var selectedOperatorId = $flowchart.flowchart('getSelectedOperatorId');
    if (selectedOperatorId != null) {
      var NewInfo = {
        InputDim: $start_dim.val()
      };
      $flowchart.flowchart('setOperatorInfo', selectedOperatorId, NewInfo);
    }
  });

  $end_dim.keyup(function () {
    var selectedOperatorId = $flowchart.flowchart('getSelectedOperatorId');
    if (selectedOperatorId != null) {
      var NewInfo = {
        OutputDim: $end_dim.val()
      };
      $flowchart.flowchart('setOperatorInfo', selectedOperatorId, NewInfo);
    }
  });

  $conv_sizeX.keyup(function () {
    var selectedOperatorId = $flowchart.flowchart('getSelectedOperatorId');
    if (selectedOperatorId != null) {
      var NewInfo = {
        sizeX: $conv_sizeX.val(),
        sizeY: $conv_sizeY.val(),
        strideX: $conv_strideX.val(),
        strideY: $conv_strideY.val(),
        channel: $conv_channel.val()
      };
      $flowchart.flowchart('setOperatorInfo', selectedOperatorId, NewInfo);
    }
  });

  $conv_sizeY.keyup(function () {
    var selectedOperatorId = $flowchart.flowchart('getSelectedOperatorId');
    if (selectedOperatorId != null) {
      var NewInfo = {
        sizeX: $conv_sizeX.val(),
        sizeY: $conv_sizeY.val(),
        strideX: $conv_strideX.val(),
        strideY: $conv_strideY.val(),
        channel: $conv_channel.val()
      };
      $flowchart.flowchart('setOperatorInfo', selectedOperatorId, NewInfo);
    }
  });

  $conv_strideX.keyup(function () {
    var selectedOperatorId = $flowchart.flowchart('getSelectedOperatorId');
    if (selectedOperatorId != null) {
      var NewInfo = {
        sizeX: $conv_sizeX.val(),
        sizeY: $conv_sizeY.val(),
        strideX: $conv_strideX.val(),
        strideY: $conv_strideY.val(),
        channel: $conv_channel.val()
      };
      $flowchart.flowchart('setOperatorInfo', selectedOperatorId, NewInfo);
    }
  });

  $conv_strideY.keyup(function () {
    var selectedOperatorId = $flowchart.flowchart('getSelectedOperatorId');
    if (selectedOperatorId != null) {
      var NewInfo = {
        sizeX: $conv_sizeX.val(),
        sizeY: $conv_sizeY.val(),
        strideX: $conv_strideX.val(),
        strideY: $conv_strideY.val(),
        channel: $conv_channel.val()
      };
      $flowchart.flowchart('setOperatorInfo', selectedOperatorId, NewInfo);
    }
  });

  $conv_channel.keyup(function () {
    var selectedOperatorId = $flowchart.flowchart('getSelectedOperatorId');
    if (selectedOperatorId != null) {
      var NewInfo = {
        sizeX: $conv_sizeX.val(),
        sizeY: $conv_sizeY.val(),
        strideX: $conv_strideX.val(),
        strideY: $conv_strideY.val(),
        channel: $conv_channel.val()
      };
      $flowchart.flowchart('setOperatorInfo', selectedOperatorId, NewInfo);
    }
  });

  $pool_sizeX.keyup(function () {
    var selectedOperatorId = $flowchart.flowchart('getSelectedOperatorId');
    if (selectedOperatorId != null) {
      var NewInfo = {
        sizeX: $pool_sizeX.val(),
        sizeY: $pool_sizeY.val(),
        strideX: $pool_strideX.val(),
        strideY: $pool_strideY.val()
      };
      $flowchart.flowchart('setOperatorInfo', selectedOperatorId, NewInfo);
    }
  });

  $pool_sizeY.keyup(function () {
    var selectedOperatorId = $flowchart.flowchart('getSelectedOperatorId');
    if (selectedOperatorId != null) {
      var NewInfo = {
        sizeX: $pool_sizeX.val(),
        sizeY: $pool_sizeY.val(),
        strideX: $pool_strideX.val(),
        strideY: $pool_strideY.val()
      };
      $flowchart.flowchart('setOperatorInfo', selectedOperatorId, NewInfo);
    }
  });

  $pool_strideX.keyup(function () {
    var selectedOperatorId = $flowchart.flowchart('getSelectedOperatorId');
    if (selectedOperatorId != null) {
      var NewInfo = {
        sizeX: $pool_sizeX.val(),
        sizeY: $pool_sizeY.val(),
        strideX: $pool_strideX.val(),
        strideY: $pool_strideY.val()
      };
      $flowchart.flowchart('setOperatorInfo', selectedOperatorId, NewInfo);
    }
  });

  $pool_strideY.keyup(function () {
    var selectedOperatorId = $flowchart.flowchart('getSelectedOperatorId');
    if (selectedOperatorId != null) {
      var NewInfo = {
        sizeX: $pool_sizeX.val(),
        sizeY: $pool_sizeY.val(),
        strideX: $pool_strideX.val(),
        strideY: $pool_strideY.val()
      };
      $flowchart.flowchart('setOperatorInfo', selectedOperatorId, NewInfo);
    }
  });

  $dropout_rate.keyup(function () {
    var selectedOperatorId = $flowchart.flowchart('getSelectedOperatorId');
    if (selectedOperatorId != null) {
      var NewInfo = {
        rate: $dropout_rate.val()
      };
      $flowchart.flowchart('setOperatorInfo', selectedOperatorId, NewInfo);
    }
  });

  $dense_num.keyup(function () {
    var selectedOperatorId = $flowchart.flowchart('getSelectedOperatorId');
    if (selectedOperatorId != null) {
      var NewInfo = {
        num: $dense_num.val()
      };
      $flowchart.flowchart('setOperatorInfo', selectedOperatorId, NewInfo);
    }
  });

  $act_func.keyup(function () {
    var selectedOperatorId = $flowchart.flowchart('getSelectedOperatorId');
    if (selectedOperatorId != null) {
      var NewInfo = {
        ActivationFunc: $act_func.val()
      };
      $flowchart.flowchart('setOperatorInfo', selectedOperatorId, NewInfo);
    }
  });


  $flowchart.parent().siblings('.delete_selected_button').click(function () {
    $flowchart.flowchart('deleteSelected');
  });

  $('.get_data').click(function () {
    var url_upload_json = '127.0.0.1:5000/train';
    var data = $flowchart.flowchart('getData');
    // window.parent.send_json(data);
    console.log(data);
    // $('#flowchart_data').val(JSON.stringify(data, null, 2));
    jq3(function ($) {
      // console.log($.prototype.jquery);
      $.post(
        url_upload_json,
        data,
        function (response_data) {
          // $('.toast').toast('show');
          console.log(response_data);
        },
        'json'
      );
    });
  });


  var $draggableOperators = $('.draggable_operator');
  var Idx_Pooling = 0;
  var Idx_Convolution = 0;
  var Idx_Activation = 0;
  var Idx_Fully_Connected = 0;
  var Idx_Start = 0;
  var Idx_End = 0;
  var Idx_Dropout = 0;
  function getOperatorData($element) {
    var nbInputs = parseInt($element.data('nb-inputs'));
    var nbOutputs = parseInt($element.data('nb-outputs'));
    var Title = $element.text();
    var DefaultInfo;
    if (Title == "Start Node") {
      Title = Title + parseInt(Idx_Start / 2);
      Idx_Start++;
      DefaultInfo = {
        InputDim: 784,
      };
    }
    else if (Title == "End Node") {
      Title = Title + parseInt(Idx_End / 2);
      Idx_End++;
      DefaultInfo = {
        OutputDim: 10,
      };
    }
    else if (Title == "Activation") {
      Title = Title + parseInt(Idx_Activation / 2);
      Idx_Activation++;
      DefaultInfo = {
        ActivationFunc: 'Relu',
      };
    }
    else if (Title == "Fully-connected") {
      Title = Title + parseInt(Idx_Fully_Connected / 2);
      Idx_Fully_Connected++;
      DefaultInfo = {
        num: 64
      };
    }
    else if (Title == "Dropout") {
      Title = Title + parseInt(Idx_Dropout / 2);
      Idx_Dropout++;
      DefaultInfo = {
        rate: 0.3,
      };
    }
    else if (Title == "Pooling") {
      Title = Title + parseInt(Idx_Pooling / 2);
      Idx_Pooling++;
      DefaultInfo = {
        sizeX: 3,
        sizeY: 3,
        strideX: 3,
        strideY: 3
      };
    }
    else if (Title == "Convolution") {
      Title = Title + parseInt(Idx_Convolution / 2);
      Idx_Convolution++;
      DefaultInfo = {
        sizeX: 3,
        sizeY: 3,
        strideX: 1,
        strideY: 1,
        channel: 32
      };
    }


    var data = {
      properties: {
        title: Title,
        information: DefaultInfo,
        inputs: {},
        outputs: {}
      }
    };

    var i = 0;

    for (i = 0; i < nbInputs; i++) {
      data.properties.inputs['input_' + i] = {
        label: 'Input ' + (i + 1)
      };
    }
    for (i = 0; i < nbOutputs; i++) {
      data.properties.outputs['output_' + i] = {
        label: 'Output ' + (i + 1)
      };
    }

    return data;
  }



  $draggableOperators.draggable({
    cursor: "move",
    opacity: 0.7,

    helper: 'clone',
    appendTo: 'body',
    zIndex: 1000,

    helper: function (e) {
      var $this = $(this);
      var data = getOperatorData($this);
      return $flowchart.flowchart('getOperatorElement', data);
    },
    stop: function (e, ui) {
      var $this = $(this);
      var elOffset = ui.offset;
      var containerOffset = $container.offset();
      if (elOffset.left > containerOffset.left &&
        elOffset.top > containerOffset.top &&
        elOffset.left < containerOffset.left + $container.width() &&
        elOffset.top < containerOffset.top + $container.height()) {

        var flowchartOffset = $flowchart.offset();

        var relativeLeft = elOffset.left - flowchartOffset.left;
        var relativeTop = elOffset.top - flowchartOffset.top;

        var positionRatio = $flowchart.flowchart('getPositionRatio');
        relativeLeft /= positionRatio;
        relativeTop /= positionRatio;

        var data = getOperatorData($this);
        data.left = relativeLeft;
        data.top = relativeTop;

        $flowchart.flowchart('addOperator', data);
      }
    }
  });


});