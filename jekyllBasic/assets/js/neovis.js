var viz = null;
var showArrows = true;
var debug = false;

var neo4jHost = debug ? 'localhost' : 'legalhack.tech';
var neo4jPassword = debug ? 'neo4j' : 'aDeRTYlenTor';

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
    // $('#viz').loading('stop');
}

function initNeoVis(config) {
    viz = new NeoVis.default(config);
    viz.registerOnEvent('completed', renderCompleted);
    viz.render();
}
