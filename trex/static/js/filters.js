angular.module('trexFilters', []).filter('checkmark', function() {
    return function(input) {
        return input ? '\u2713' : '\u2718';
    };
});

angular.module('trexFilters', []).filter('duration', function() {
    return function(input) {
        var minutes = input / 60;
        var hours = Math.floor(minutes / 60);
        var minutes = minutes % 60;

        if (minutes.toString().length < 2) {
            return "" + hours + ":0" + minutes;
        }
        return "" + hours + ":" + minutes;
    };
});
