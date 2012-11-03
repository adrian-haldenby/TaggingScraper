

var readable = [];

var casper = require('casper').create();


var upTo = casper.cli.get(0);
var links = casper.cli.get(1);
//parse the commant line arguement (for windows)
links = links.replace(new RegExp("~", "g"), "','");
links = links.replace(new RegExp("\\)", "g"), "');");
links = links.replace(new RegExp("\\(", "g"), "('");
links = links.split("@");


casper.start(upTo)

casper.each(links, function (casper, link) {
    casper.then(function () {
        doesexists = this.exists('a[href="' + link + '"]');
    });

    casper.then(function () {
        if (doesexists === true) {
            this.click('a[href="' + link + '"]');
        }
    });
    casper.then(function () {
        if (doesexists === true) {
            var newline = this.getCurrentUrl();
            readable = readable.concat(newline);
        }
    });
    casper.then(function () {
        if (doesexists === true) {
            this.back();
        }
    })
});




casper.run(function () {
    // echo results in some pretty fashion
    //this.echo(readable.length + ' links found:');
    this.echo(readable.join(',')).exit();
});
//casper.run();