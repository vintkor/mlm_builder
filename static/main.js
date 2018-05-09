$(document).ready(function () {

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    function sameOrigin(url) {
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    //Masked Input ============================================================================================================================

    try {
        $('input.phone').inputmask('+99 (999) 999-99-99', {placeholder: '+__ (___) ___-__-__'});
    } catch (e) {

    }

    $('#clearFocuse').find('.form-line').removeClass('focused');

});

// =================================    Форма редактирования вебинаров  =================================
(function () {
    var pageUpdate = $('#webinarUpdateForm');
    pageUpdate.find('input[type=text], input[type=url]').addClass('form-control');
    setTimeout(function () {
        pageUpdate.find('.form-line').removeClass('focused');
    }, 500);
})();

// =================================    Удаление вебинара  =================================
(function () {
    $('.deleteWebinar').click(function (e) {
        e.preventDefault();

        var self = $(this);

        swal({
            title: "Вы точно хотите удалить вебинар?",
            text: "Так-же будут удалены связаные лендинги!",
            type: "warning",
            showCancelButton: true,
            confirmButtonColor: "#DD6B55",
            confirmButtonText: "Да, удалить!",
            cancelButtonText: "Нет, не надо!",
            closeOnConfirm: false,
            closeOnCancel: false
        }, function (isConfirm) {
            if (isConfirm) {

                $.ajax({
                    method: 'POST',
                    url: self.attr('href'),
                    type: 'json',
                    success: function (data) {
                        if (data.success) {
                            self.parents('.card').hide('slow').remove();
                            swal("успешно!", "Вебинар удалён!.", "success");
                        } else {
                            swal("Ой!", "Что-то пошло не так", "error");
                        }
                    },
                    error: function (e) {
                        swal("Ой!", "Что-то пошло не так", "error");
                    }
                });
            } else {
                swal("Отмена!", "Вебинар удалён не будет", "error");
            }
        });
    });
})();

// =================================    Удаление лендинга  =================================
(function () {
    $('.deleteLending').click(function (e) {
        e.preventDefault();

        var self = $(this);

        swal({
            title: "Вы точно хотите удалить лендинг?",
            type: "warning",
            showCancelButton: true,
            confirmButtonColor: "#DD6B55",
            confirmButtonText: "Да, удалить!",
            cancelButtonText: "Нет, не надо!",
            closeOnConfirm: false,
            closeOnCancel: false
        }).then(function (result) {
            if (result.value) {

                $.ajax({
                    method: 'POST',
                    url: self.attr('href'),
                    type: 'json',
                    success: function (data) {
                        if (data.success) {
                            self.parents('.card').hide('slow').remove();
                            swal("успешно!", "Лендинг удалён!.", "success");
                        } else {
                            swal("Ой!", "Что-то пошло не так", "error");
                        }
                    },
                    error: function (e) {
                        swal("Ой!", "Что-то пошло не так", "error");
                    }
                });
            } else {
                swal("Отмена!", "Лендинг удалён не будет", "error");
            }
        });

    });
})();

try {
    $('.select2').select2();
} catch (e) {
    // console.log(e);
}

// =================================   прикрепление шаблона к вебинару  =================================

(function () {
    var form = $('#choiceTemplateToWebinar'),
        select = form.find('select'),
        button = form.find('button');

    select.change(function () {
        button.show();
    });

})();

// =================================   копирование ссылки в буфер обмена  =================================
(function () {
    $('.js-textareacopybtn').click(function (e) {

        e.preventDefault();

        var linkText = window.location.origin + $(this).attr('href');

        var $temp = $("<input>");
        $("body").append($temp);
        $temp.val(linkText).select();
        document.execCommand("copy");
        $temp.remove();

        swal(
            '',
            'Ссылка ' + linkText + ' скопирована',
            'success'
        );

    });

})();

//  =================================  Edit landing description   =================================
(function () {
    $('.editLendingDescription').click(function (e) {
        e.preventDefault();

        var landingId = $(this).data('lending'),
            modalContainer = $('#editLendingModal'),
            image = document.getElementById('image'),
            crop = {
                one: null,
                two: null
            },
            inputImage = $('#imageEdit'),
            imageData = {},
            saveButton = $('#saveLendingModalForm'),
            landingImage = $('#imageFor-' + landingId),
            form = $('#editLendingModalForm'),
            landingTitle = $('#landingTitle-' + landingId),
            landingDescription = $('#landingDescription-' + landingId);

        $('#titleEdit').val(landingTitle.text());
        $('#descriptionEdit').val(landingDescription.text());

        modalContainer.modal('show');

        inputImage.change(function () {

            var file = this.files[0];
            var reader = new FileReader();
            reader.onload = function (e) {
                image.src = e.target.result;
                cropper = new Cropper(image, {
                    aspectRatio: crop.one / crop.two,
                    viewMode: 1,
                    zoomable: false,
                    crop: function crop(event) {

                        imageData.imageWidth = event.detail.width;
                        imageData.imageHeight = event.detail.height;
                        imageData.image_x = event.detail.x;
                        imageData.image_y = event.detail.y;
                    }
                });
            };
            reader.readAsDataURL(file);
        });

        saveButton.click(function (e) {
            e.preventDefault();
            var formdata = new FormData();

            formdata.append('image', document.getElementById('imageEdit').files[0]);
            formdata.append('imageWidth', imageData.imageWidth);
            formdata.append('imageHeight', imageData.imageHeight);
            formdata.append('image_x', imageData.image_x);
            formdata.append('image_y', imageData.image_y);
            formdata.append('title', $('#titleEdit').val());
            formdata.append('description', $('#descriptionEdit').val());
            formdata.append('lendingId', landingId);

            $.ajax({
                method: 'post',
                url: window.location.href,
                data: formdata,
                processData: false,
                contentType: false,
                success: function success(data) {
                    landingTitle.text(data.title);
                    landingDescription.text(data.description);
                    if (data.image_url) {
                        landingImage.attr('src', data.image_url);
                    }
                    modalContainer.modal('hide');
                    imageTag = '';
                    form[0].reset();
                    cropper.destroy();
                    $(image).attr('src', '');
                },
                error: function error(_error) {
                    console.log(_error);
                }
            });

        });

    });
})();


//  =================================  Действя картинки в модальном окне   =================================
(function () {
//
//     var modalListGroup = $('#modalListGroup'),
//         modal =          $('#MyLendingModal');

    //  =================================  Детальная информация по картинке   =================================
    // $('.showMyLendingModal').click(function (e) {
    //     e.preventDefault();
    //
    //     var imageId =        $(this).data('image'),
    //         modalTitle =     $('#MyLendingModalLabel'),
    //         modalImage =     $('#modalImage'),
    //         imageTitle =     $('#imageTitle-' + imageId),
    //         imageImageSrc =  $('#imageImage-' + imageId).attr('src');
    //
    //     modalTitle.text(imageTitle.text());
    //     modalImage.attr('src', imageImageSrc);
    //
    //     $.ajax({
    //         url: window.location.href,
    //         method: 'get',
    //         data: {get_image_info: imageId},
    //         success: function (data) {
    //             var landings = data.landings;
    //             landings.map(function (el) {
    //
    //                 const template = `
    //                     <li class="list-group-item">
    //                         <h4>${ el.title }</h4>
    //                         <a href="${ el.link }" target="_blank" class="btn btn-sm btn-info pull-right" style="margin: 0 5px;">
    //                             Смотреть лендинг
    //                         </a>
    //                         <button class="btn btn-sm btn-danger pull-right delLanding" data-id="${ el.id }" data-image="${ el.image_id }">
    //                             Отвязать лендинг
    //                         </button>
    //                         <div>
    //                             <h5>${ el.set_title }</h5>
    //                             <p>${ el.set_description }</p>
    //                         </div>
    //                     </li>
    //                 `;
    //
    //                 modalListGroup.append(
    //                     template
    //                 );
    //             });
    //         },
    //         error: function (e) {
    //             console.log('Error');
    //         }
    //     });
    //
    //     modal.modal('show');

    // });

    // modal.on('hidden.bs.modal', function () {
    //     modalListGroup.html('');
    // });

    //  =================================  Отвязать лендинг от картинки   =================================
    $('.delLanding').click(function (e) {
        e.preventDefault();
        var landingId = $(this).data('id'),
            parentEl = $(this).parents('.landing-row'),
            imageId = $(this).data('image');

        swal({
            title: "Вы точно хотите отвязать этот лендинг?",
            type: "warning",
            showCancelButton: true,
            confirmButtonColor: "#DD6B55",
            confirmButtonText: "Да, отвязать!",
            cancelButtonText: "Нет, не надо!"
        }).then(function (result) {
            if (result.value) {
                $.ajax({
                    url: window.location.href,
                    method: 'POST',
                    data: {landing_id: landingId, image_id: imageId},
                    success: function (data) {
                        if (data.success) {
                            parentEl.addClass('animated bounceOut');
                            setTimeout(function () {
                                parentEl.remove();
                            }, 1000);
                            swal({
                                position: 'top-end',
                                type: 'success',
                                title: 'Лендинг отвязан',
                                showConfirmButton: false,
                                timer: 800
                            })
                        }
                    },
                    error: function (e) {
                        console.log('Error');
                    }
                });
            }
        });

    });

})();

//  =================================  Удаление изображения   =================================
(function () {
    $('.deleteMyImage').click(function (e) {
        e.preventDefault();

        var imageCard = $(this).parents('.imageCard'),
            url = $(this).attr('href');

        swal({
            title: "Вы точно хотите удалить изображения?",
            type: "warning",
            showCancelButton: true,
            confirmButtonColor: "#DD6B55",
            confirmButtonText: "Да, удалить!",
            cancelButtonText: "Нет, не надо!"
        }).then(function (result) {
            if (result.value) {
                $.ajax({
                    url: url,
                    method: 'POST',
                    success: function (response) {
                        if (response.status) {
                            imageCard.addClass('animated bounceOut');
                            setTimeout(function () {
                                imageCard.remove();
                            }, 1000);
                            swal({
                                position: 'top-end',
                                type: 'success',
                                title: 'Изображение удалено',
                                showConfirmButton: false,
                                timer: 800
                            })
                        }
                    },
                    error: function (e) {
                        console.log('Error');
                    }
                });
            }
        });
    });
})();


(function () {
    $('.photoboxGallery').photobox('a');
})();

(function () {
    const modal = $('#MyLendingModal');
    const select = modal.find('select');

    $('#image-to-landing').click(function (e) {
        e.preventDefault();

        $.ajax({
            url: window.location.href,
            method: 'POST',
            data: {imageToLanding: true},
            success: function (response) {
                let options = {
                    data: response.data,
                    width: '100%'
                };
                select.select2(options);
                modal.modal('show');
            },
            error: function () {
                console.log('Error');
            }
        });

    });

    modal.on('hide.bs.modal', function () {
        select.select2('destroy');
    });
})();
