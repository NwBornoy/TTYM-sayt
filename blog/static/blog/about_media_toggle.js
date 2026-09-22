django.jQuery(function($) {
    function toggleFields() {
        var type = $('#id_media_type').val();
        if (type === 'photo') {
            $('.field-image').show();
            $('.field-video_url').hide();
        } else if (type === 'video') {
            $('.field-image').hide();
            $('.field-video_url').show();
        }
    }
    $('#id_media_type').change(toggleFields);
    toggleFields();
});