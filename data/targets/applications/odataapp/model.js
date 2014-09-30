$data.Class.define("myservice.Product", $data.Entity, null, {
    Id: { type: "id", key: true, computed: true, nullable: false },
    Name: { type: "string" },
    Price: { type: "integer" }
}, null);
$data.Class.defineEx("myservice.Context", [$data.EntityContext,$data.ServiceBase], null, {
    Products: { type: $data.EntitySet, elementType: myservice.Product }
});
exports = myservice.Context;
