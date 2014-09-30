var http = require("http")
var st = require("st")

var mount = st({
  path: 'resources/static/', // resolved against the process cwd
  url: 'static/', // defaults to '/'
  })
  
http.createServer(function (req, res) {
  if (mount(req, res)) return // serving a static file
}).listen(8888)