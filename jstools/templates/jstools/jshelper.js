var {{ NS }} = {{ NS }} || {};
{{ NS }}.settings = {
    DEBUG: {{ settings.DEBUG|yesno:"true,false" }}, {# Override this in the template #}
    MEDIA_URL: "{{ settings.MEDIA_URL }}"
};
{{ NS }}.raise = function(e) {
    if ({{ NS }}.settings.DEBUG) {
        if (e) {
            throw Error(typeof e == "string" ? e : "Error");
        }
    } else {
        {# do some logging here #}
    }
};
{{ NS }}.get_url = function() {
    function printf(format, args) {
        if (args.length != format.split('%s').length - 1) {
            {{ NS }}.raise('Not all parameters formatted in `' + format + '`.');
        }
        var j = 0;
        return format.replace(/%s/g, function(){ return args[j++] });
    };
    var urls = {{ urls }};
    var name = Array.prototype.shift.call(arguments);
    if (typeof urls[name] == 'undefined') {
        {{ NS }}.raise('URL `' + name + '` is not defined.');
    }
    return printf(urls[name], arguments);
};
