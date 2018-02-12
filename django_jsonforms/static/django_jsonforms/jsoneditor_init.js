$('document').ready(function() {

    $('.editor_holder').each(function() {
        // Get the DOM Element
        var element = $(this).get(0);

        var schema_url = $(this).attr('schema_url')
        var options_url = $(this).attr('options_url')

        var schema
        var options
        var schema_request = 0
        var options_request = 0

        if (schema_url !== undefined) {
            schema_request = $.getJSON(schema_url, function(data) {
                schema = data;
            })
        } else {
            schema = JSON.parse($(this).attr('schema'));
        }

        if (options_url !== undefined) {
            options_request = $.getJSON(options_url, function(data) {
                options = data;
            })
        } else {
            options = JSON.parse($(this).attr('options'));
        }

        var name = $(this).attr('name');
        var hidden_identifier = 'input[name=' + name + ']';
        var initial = $(hidden_identifier).val();

        // Check if editor is within form
        var form = $(this).closest('form')

        //Wait for any ajax requests to complete
        $.when(schema_request, options_request).done(function() {
            options.form_name_root = name;

            // Pass initial value though to editor
            if (initial) {
                options.startval = JSON.parse(initial);
            }

            options.schema = schema;
            var editor = new JSONEditor(element, options);

            if (form) {
                $(form).submit(function() {
                    // Set the hidden field value to the editors value
                    $(hidden_identifier).val(JSON.stringify(editor.getValue()));
                    // Disable the editor so it's values wont be submitted
                    editor.disable();
                })
            }
        })

    });
})
