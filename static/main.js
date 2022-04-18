$(document).ready(function () {
    let swappable = new Swappable.default(document.querySelectorAll('table'), {
        draggable: 'td'
    });
    function isNumeric(value) {
        return /^-?\d+$/.test(value);
    }

    function updateSelf(event) {
        // get event target element
        event.preventDefault()
        event.stopPropagation()
        let target = event.target;
        // update innerHTml
        const input = window.prompt('Enter new value');
        if (isNumeric(input)) {
            target.innerHTML = input;
        } else {
            target.innerHTML = '-1';
        }
    }

    $('#edit').click(function (event) {
        event.preventDefault();
        swappable.destroy();
        // add eventlistener to all items
        $('.item').click(updateSelf);
    })
    $('#swap').click(function (event) {
        event.preventDefault()
        swappable = new Swappable.default(document.querySelectorAll('table'), {
            draggable: 'td'
        });
    })

    $('#createTable').click(function (event) {
        event.preventDefault();
        // first remove old table
        $('table').remove();
        // read id cols and id rows
        const rows = $('#rows').val();
        const cols = $('#cols').val();
        // create html table with rows and cols
        const table = $('<table><tbody>');
        table.addClass('grabbable');
        for (let r = 0; r < rows; r++) {
            const tr = $('<tr>');
            for (let c = 0; c < cols; c++) {
                const td = $(`<td>${r * cols + c + 1}</td>`);
                td.addClass('item');
                td.appendTo(tr);
            }
            tr.appendTo(table);
        }
        $('#mergeBtn').before(table);
        swappable = new Swappable.default(document.querySelectorAll('table'), {
            draggable: 'td'
        });
    });

    $('#formFiles').submit(function (e) {
        e.preventDefault();
        // change button to loading and disable it
        $('#mergeBtn').prop('disabled', true);
        $('#spinner').show();
        // sleep for 0.5 seconds

        const formdata = new FormData(this);
        // get table in 2d array
        const table = [];
        $('.grabbable tr').each(function () {
            const row = [];
            $(this).find('td').each(function () {
                row.push(parseInt($(this).text()));
            });
            table.push(row);
        });
        // add table to formdata
        formdata.append('positions', JSON.stringify(table));
        $.ajax({
            url: '/process_form',
            type: 'POST',
            data: formdata,
            processData: false,
            contentType: false,
            success: function (data) {
                //JSON parse error, this is not json (or JSON isn't in your browser)
                const blob = new Blob([data]);
                const link = document.createElement('a');
                link.href = window.URL.createObjectURL(blob);
                link.download = "merged.xml";
                link.click();
            },
            error: function (err) {
				try {
                    const errJson = JSON.parse(err.responseText);
                    if ('error_msg' in errJson) {
                        alert(errJson.error_msg)
                    }
                }
				catch (e){
                    console.log(e)
					alert("Something went wrong, please check that server is running and try again")
				}
            },
            complete: function () {
                // change button to success
                $('#mergeBtn').prop('disabled', false);
                $('#spinner').hide();
            }
        });
    });
});
