var page = require('webpage').create(),
    system = require('system'),
    address;

if (system.args.length === 1) {
    console.log('Usage: netlog.js <some URL>');
    phantom.exit(1);
} else {
    address = system.args[1];

    page.onResourceRequested = function (req) {
        console.log('requested: ' + req.url);// JSON.stringify(req, undefined, 99));
    };

    //page.onResourceReceived = function (res) {
    //console.log('received: ' + JSON.stringify(res, undefined, 99));
    //};

    page.open(address, function (status) {
        if (status == "success") {
            window.setTimeout(function () {
                phantom.exit();
            }, 2500)
        };
        if (status !== 'success') {
            console.log('FAIL to load the address');
            phantom.exit();
        }
    });
}