$('document').ready(function() {

    $('.editor_holder').each(function() {
        // Get the DOM Element
        var element = $(this).get(0);

        var schema = JSON.parse($(this).attr('schema'));
        var options = JSON.parse($(this).attr('options'));
        var name = $(this).attr('name')
        options.schema = schema;
        options.form_name_root = $(this).attr('name');

        // Pass initial value though to editor
        var hidden_identifier = 'input[name=' + name + ']';
        options.startval = JSON.parse($(hidden_identifier).val());

        var editor = new JSONEditor(element, options);

        // Check if editor is within form
        var form = $(this).closest('form')
        if (form) {
            $(form).submit(function() {
                // Set the hidden field value to the editors value
                $(hidden_identifier).val(JSON.stringify(editor.getValue()));
                // Disable the editor so it's values wont be submitted
                editor.disable();
            })
        }
    });
})
