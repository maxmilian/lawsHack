var viz;
var showArrows = true;
var neo4jHost = 'localhost';
var neo4jPassword = 'neo4j';
// var neo4jHost = '13.113.158.197';
// var neo4jPassword = 'aDeRTYlenTor';

var neovisConfig = {
    container_id: "viz",
    server_url: "bolt://" + neo4jHost + ":7687",
    server_user: "neo4j",
    server_password: neo4jPassword,
    labels: {
        "CASE": {
            "caption": "yearcaseno",
            "size": "pagerank",
            "community": "community",
            //"sizeCypher": "MATCH (n) WHERE id(n) = {id} MATCH (n)-[r]-() RETURN sum(r.weight) AS c"
        }
    },
    relationships: {
        "REFER": {
            "thickness": "weight",
            "caption": false
        }
    },
    initial_cypher: "MATCH (n)-[r:REFER]->(m) WHERE m.pagerank > 0.21 RETURN * ORDER BY m.pagerank LIMIT 1000",
    arrows: showArrows,
    console_debug: false
};

function renderCompleted(stats) {
    new Noty({
        type: "success",
        text: stats.record_count + " 個節點抓取成功",
        timeout: 3000,
        theme: "relax"
    }).show();
    $('#viz').loading('stop');
}

function draw() {
    viz = new NeoVis.default(neovisConfig);
    viz.registerOnEvent('completed', renderCompleted);
    viz.render();
}
