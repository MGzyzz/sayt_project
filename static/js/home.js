$(document).ready(function () {
    loadUsers();

    function loadUsers() {
        $.ajax({
            url: '/api/users_list/', // URL вашего API-эндпоинта
            type: 'GET',
            success: function (data) {
                if (data.length > 0) {
                    updateUserInfo(data[0]);
                    $('#no-users-message').hide(); // Скрыть сообщение "Пользователей нет"
                    $('.block-one, .block-two').show(); // Показать блоки с информацией о пользователе
                    console.log(data)
                } else {
                    console.log('Нет доступных пользователей.');
                    $('#no-users-message').show(); // Показать сообщение "Пользователей нет"
                    $('.block-one, .block-two').hide(); // Скрыть блоки с информацией о пользователе
                }
            },
            error: function (error) {
                console.error("Ошибка при загрузке пользователей:", error);
            }
        });
    }

    function updateUserInfo(user) {
        $('#userName').text('Имя: ' + user.first_name + ' ' + user.last_name);
        $('#userHeight').text('Рост: ' + 180); // Допустим, у нас есть поле рост в объекте user
        $('#userStatus').text('Статус: ' + (user.status ? 'Активен' : 'Неактивен'));
        $('#userDescription').text(user.description);
        $('.image').css('background-image', 'url(' + user.image + ')');
        $('.like-icon, .dislike-icon').data('user-id', user.id);
        console.log(user.id)// Обновляем data-user-id для иконок
    }

    function updateUserLikeDislike(userId, action) {
        $.ajax({
            url: '/api/users/' + userId + '/' + action + '/',
            type: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            success: function (response) {
                if (response.status === 'success') {
                    console.log('User ' + userId + ' was ' + (action === 'like' ? 'liked' : 'disliked'));
                    loadUsers(); // Загрузка следующего пользователя
                }
            },
            error: function (xhr, status, error) {
                console.error("Ошибка при выполнении действия " + action + " для пользователя с ID " + userId + ": ", error);
            }
        }).done(function () {
            // После выполнения запроса принудительно обновляем список пользователей
            loadUsers();
        });
    }


    $('.like-icon, .dislike-icon').click(function (e) {
        e.preventDefault();
        var userId = $(this).data('user-id');
        console.log(userId)
        var action = $(this).hasClass('like-icon') ? 'like' : 'dislike';
        updateUserLikeDislike(userId, action);
    });

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
});
