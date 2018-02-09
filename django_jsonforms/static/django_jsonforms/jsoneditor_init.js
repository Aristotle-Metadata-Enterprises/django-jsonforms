$('document').ready(function() {
  var element = document.getElementById('editor_holder');
  // load options from a view in here?
  console.log(element);
  var schema = JSON.parse(document.getElementById('editor_holder').getAttribute('schema'));
  var options = JSON.parse(document.getElementById('editor_holder').getAttribute('options'));
  options.schema = schema
  var editor = new JSONEditor(element, options);

  $('#submit_editor').click(function() {
      console.log(editor.getValue());
  })

})
