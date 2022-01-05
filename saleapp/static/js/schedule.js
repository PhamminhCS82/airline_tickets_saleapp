$(function () {
    $('#datetimepicker4').datetimepicker({
        pickDate: false,
        minuteStepping:30,
        format: 'hh:mm',
        pickTime: true,
        defaultDate: new Date(1979, 0, 1, 8, 0, 0, 0),
        language:'en',
        use24hours: true
    });
    $('#flight-datetime').datetimepicker({
         format: 'MM/DD/YYYY HH:mm'
 });
});


$('.time-picker').timepicker({
            showMeridian: false
        });

$('#fecha').datetimepicker({
   format : 'DD/MM/YYYY HH:mm'
});
