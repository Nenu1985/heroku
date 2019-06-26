$(document).ready(function () {
    // catch the submit event of the form.#}
    $('#collage_form').submit(function () {
        $("#photo")[0].src = ""
        $('#progress_div').text(0 + '%');
        let pb = $('.progress-bar');
        pb.attr('aria-valuenow', 0);
        pb.width(0 + '%');
        // create an AJAX call…
        $.ajax({
            // get the form data
            data: $('#collage_form').serialize() + "&query_type=" + "collage_launch",
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
            query_type: 'collage_launch',
            // GET or POST
            type: $('#collage_form').attr('method'),
            // the file to call
            url: $('#collage_form').attr('action'),
            // on success..
            success: function (response) {
                // Displays the success message.
                response = JSON.parse(response);

                let view_url = $('#collage_form').attr('action');
                let long_task_id = response["task_id"];

                // Clear PB state view
                $('#progress_div').text(0);
                let pb = $('.progress-bar');
                pb.attr('aria-valuenow', 0);
                pb.width(0 + '%');

                setTimeout(myPeriodicMethod, 500, view_url, long_task_id);
            },
            error: function (response) {
                // Displays the error message.
                alert(JSON.parse(response)["message"]);
            },
        });
        return false;
    });
});

// var url_to_get_polls = ''
function myPeriodicMethod(view_url, long_task_id) {
    $.ajax({

        type: "POST",
        url: view_url,
        data: {
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
            query_type: 'poll',
            task_id: long_task_id,
        },
        success: function (data) {
            data = JSON.parse(data);
            progress = data["progress"];
            proc_name = data["proc_name"];

            $('#progress_div').text(proc_name + ': ' + progress + '%');
            let pb = $('.progress-bar');
            pb.attr('aria-valuenow', progress);
            pb.width(progress + '%');
            if (progress < 100 || proc_name != "Collage has generated!")
                setTimeout(myPeriodicMethod, 1000, this.url, long_task_id); // this.url = /pb_ajax/
            else {
                getFinalImage(view_url, long_task_id)
            }
        },

    });
}

function getFinalImage(view_url, progress_recorder_id) {
    $.ajax({

        type: "POST",
        url: view_url,
        data: {
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
            query_type: 'get_collage',
            task_id: progress_recorder_id,
        },
        success: function (data) {
            $("#photo")[0].src = data;
        },

    });
}