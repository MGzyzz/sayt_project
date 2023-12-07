$(document).ready(function () {
    $('.open-chat-btn').on('click', function () {
        var receiverId = $(this).data('receiver-id');
        var userName = $(this).data('username');
        var currentUserId = $('#currentUserId').val();

        console.log(receiverId, userName);
        $('#chatWithUsername').text(userName);
        $('#receiverId').val(receiverId);
        $('#chatMessages').empty();
        loadChatMessages(currentUserId, receiverId)
        $('#chatModal').modal('show');

    });


     $('#messageText').keypress(function (e) {
        if(e.which == 13 && !e.shiftKey) {
            e.preventDefault();
            $('#sendMessageButton').click();
        }
    });

    $('#sendMessageButton').on('click', function () {
        var messageText = $('#messageText').val();
        var receiverId = $('#receiverId').val();
        if (messageText.trim() !== '') {
            sendChatMessage(receiverId, messageText, currentUserName);
            $('#messageText').val('');
        }
    });

});


function sendChatMessage(receiverId, messageText) {
    var csrfToken = getCookie('csrftoken')
    console.log(receiverId)
    console.log(csrfToken)
    $.ajax({
        url: '/api/send_message/',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            receiver: receiverId,
            text: messageText
        }),
        headers: {
            'X-CSRFToken': csrfToken
        },
        success: function (response) {

            console.log("Message sent:", response);
            $('#chatMessages').append(`<div class="chat-message"> <strong>${response.sender_name}</strong>: ${messageText}</div> <hr>`);


            var chatMessages = $('#chatMessages');
            chatMessages.scrollTop(chatMessages.prop("scrollHeight"));
        },
        error: function (xhr, status, error) {

            console.error("Error sending message:", error);
        }
    });
}


function loadChatMessages(userId, otherUserId) {
    $.ajax({
        url: `/api/messages/?user_id=${userId}&other_user_id=${otherUserId}`,
        type: 'GET',
        success: function (response) {
            if (Array.isArray(response)) {
                response.forEach(function (message) {
                    console.log(`work: ${message.sender_name}`)

                    var messageSenderName = message.sender_name || 'Аноним';
                    $('#chatMessages').append(
                        `<div class="chat-message">
                        <strong>${messageSenderName}</strong>: ${message.text}
                       </div><hr>`
                    );
                });
                var chatMessages = $('#chatMessages');
                chatMessages.scrollTop(chatMessages.prop("scrollHeight"));
            } else {
                console.log("No messages or incorrect format", response);
            }
        },
        error: function (xhr, status, error) {
            console.error("Error loading messages:", error);
        }
    });
}


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


