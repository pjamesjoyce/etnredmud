$(document).ready(function(){


  //$('.node').click(function () { console.log(this)});

  $.contextMenu({
      selector: '.process',
      trigger: 'left',
      callback: function(key, options) {
          var m = "clicked: " + key;
          var command = key + "|" + options.$trigger[0].id;
          console.log(command);
          window.location = command;
      },
      items: {
          "Edit_process": {name: "Edit process", icon:"edit"},
          "sep1": "---------",
          "Add_input": {name: "Add input", icon: "right" },
          "Add_output": {name: "Add output to the environment", icon: "left"},
          "sep1": "---------",
          "Add_Tech_Output": {name: "Add intermediate output (an input to another process)", icon: "left"},
          "sep2": "---------",
          "Delete": {name: "Delete", icon: "delete"},
      }
  });

  $.contextMenu({
      selector: '.input',
      trigger: 'left',
      callback: function(key, options) {
        var command = key + "|" + options.$trigger[0].id;
        console.log(command);
        window.location = command;
      },
      items : {
        "Edit_amount": {name: "Edit amount", icon:"edit"},
        "sep1": "---------",
        "Delete": {name: "Remove", icon: "delete" },
      }
  });

  $.contextMenu({
      selector: '.output',
      trigger: 'left',
      callback: function(key, options) {
        var command = key + "|" + options.$trigger[0].id;
        console.log(command);
        window.location = command;
      },
      items : {
        "Edit_amount": {name: "Edit amount", icon:"edit"},
        "sep1": "---------",
        "Delete": {name: "Remove", icon: "delete" },
      }
  });

  $.contextMenu({
      selector: '.intermediate',
      trigger: 'left',
      callback: function(key, options) {
        var command = key + "|" + options.$trigger[0].id;
        console.log(command);
        window.location = command;
      },
      items : {
        "linkProcess": {name: "Link to process", icon:"edit"},
        "sep1": "---------",
        "Delete": {name: "Remove", icon: "delete" },
      }
  });

  $.contextMenu({
      selector: '.graph_svg',
      trigger: 'right',
      callback: function(key, options) {
        var command = key + "|" + options.$trigger[0].id;
        console.log(command);
        window.location = command;
      },
      items : {
        "addProcess": {name: "Add process", icon:"edit"},
      }
  });

});
