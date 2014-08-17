var http = require('http');
var yaml = require('js-yaml');
var url = require('url')
var fs = require('fs')
var qs = require('querystring');

var server = http.createServer(function (req,res){
	var url_parts = url.parse(req.url, true);

	var body = '';
    if(req.method === 'POST'){
        req.on('data', function (data) {
            body += data;
            console.log('got data:'+data);
        });
        req.on('end', function () {
 
            var POST = qs.parse(body);
 
            //a: !!js/function function f() {console.log(1);}();
            //a: !!js/function function f() {process.abort();}();
            yaml.load(POST.name)
            res.end("Sent data are name:"+POST.name+" age:"+POST.age);
 
        });
	} else {
		req.on('data',function(data){ res.end(' data event: '+data);});
		if(url_parts.pathname == '/')		
			fs.readFile('./form.html',function(error,data){ 
				res.end(data);
				});
 
		else if(url_parts.pathname == '/getData'){
			getData(res,url_parts);
		}
	}	
});

server.listen(8888);

function  getData(res,url_parts){
    res.end("Data submitted by the user name:"+url_parts.query.name+" and age:"+url_parts.query.age);
}
