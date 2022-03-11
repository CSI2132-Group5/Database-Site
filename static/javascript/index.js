$(document).ready(function() {
    console.log("hello friend.");

    $('#cv-page-button').on({
        mouseenter: function(e) {
            $(this).html("[ CV ]");
        },
        mouseleave: function(e) {
            $(this).html("[CV]");
        },
        click: function(e) {
            $(this).removeClass("text-black").addClass("text-purple-500");
            $("#commit-page-button").removeClass("text-purple-500").addClass("text-black");

            $("#cv-page").removeClass("hidden");
            $("#project-page").addClass("hidden");

            $("#research-interests").removeClass("hidden");
            $("#main-projects").addClass("hidden");
        }
    });

    $('#commit-page-button').on({
        mouseenter: function (e) {
            $(this).html("[ Recent Commits ]");
            console.log("idk if this works");
        },
        mouseleave: function (e) {
            $(this).html("[Recent Commits]");
        },
        click: function(e) {
            $(this).removeClass("text-black").addClass("text-purple-500");
            $("#cv-page-button").removeClass("text-purple-500").addClass("text-black");

            $("#project-page").removeClass("hidden");
            $("#cv-page").addClass("hidden");

            $("#main-projects").removeClass("hidden");
            $("#research-interests").addClass("hidden");
        }
    }); 

    $("#api-button").on({
        click: function(e) {
            $("#api-dropdown").removeClass("hidden");
            UrlExists('http://api.gabriel.cordovado.me', function(status) {
                if (status == 200) {
                    $("#api-status-icon").prop("color", "#00e64d");
                    $("#api-status-text").text("Online");
                } else {
                    $("#api-status-icon").prop("color", "#c30808");
                    $("#api-status-text").text("Offline");
                }
            });
        }
    });

    $("#close-api-dropdown").on({
        click: function(e) {
            $("#api-dropdown").addClass("hidden");
        }
    });
});

function UrlExists(url, cb) {
    jQuery.ajax({
        url: url,
        dataType: 'text',
        type: 'GET',
        complete: function (xhr) {
            if (typeof cb === 'function')
                cb.apply(this, [xhr.status]);
        }
    })
}