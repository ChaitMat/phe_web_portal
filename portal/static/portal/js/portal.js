$(document).ready(function(){

    $('#post-form').on('submit', function(event){
        event.preventDefault();
        var serializedData = $(this).serialize();
        $.ajax({
            type : 'POST',
            url : $('#js-booking-submit').attr("data-url"),
            data : serializedData,
            dataType: 'json',
            success : function(data){
                $('#post-form')[0].reset();
                $('#total-participants').text(data.total_participants);
                $('#booking-list').html(data.html_bookings_list);       
            },
        })
    });


    $('.js-delete-booking').click(function(){
        console.log("Modal open")
        $('.modal').modal();
        $('#modal-delete-booking').modal("open")
        var bookedBy = $(this).data('name')
        var bookedUrl = $(this).data('url')
        $('#modal-book-by').text(bookedBy)
        $('#modal-yes-button').attr("href", bookedUrl)      
    });
    

    $('#post-delete-booking').on('submit', function(event){
        event.preventDefault();
        var serializedData = $(this).serialize();
        $.ajax({
            type : 'POST',
            url : $('#modal-yes-button').attr("href"),
            data : serializedData,
            dataType: 'json',
            success : function(data){
                $('#total-participants').text(data.total_participants);
                $('#booking-list').html(data.html_bookings_list);    
                $('#modal-delete-booking').modal("close")   
                $('.modal').modal();
            },
        })
    });

});