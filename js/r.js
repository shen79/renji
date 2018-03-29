var nodes, edges, network;
// http://visjs.org/docs/network/


// convenience method to stringify a JSON object
function toJSON(obj) {
	return JSON.stringify(obj, null, 4);
}

function dbg(x) {
	console.log(toJSON(x));
}
var phy = true

function addNodeManual() {
	dbg('Function addNodeManual');
	nt = document.getElementById('node-type').value;
	nv = document.getElementById('node-value').value;
	//dbg({nt,nv});
	nodeLabel = nt + "\n" + nv;
	// http://visjs.org/docs/network/nodes.html
	nodes.add({
		id: getID([nt,nv]),
		label: nodeLabel,
		shape: 'box',
		physics: phy,
		color: '#DDF',
		data: {
			type: nt,
			value: nv
		}
	});
	$( "#dialog-add" ).dialog('close');
}

function addNodes(r) {
	dbg({'Function addNodes': r});
	for (idx in r) {
//		dbg(r.response[idx]);
		addNode({
			'request': r[idx].request,
			'response': r[idx].response
		});
	}
}

//var xid = 0;
function getID(t) {
	dbg(t.join('--') + ' --> x' + md5(t.join('--')));
	return 'x' + md5(t.join('--'));
//	xid++;
//	return 'x' + xid;
}
//function addNode(nodeType, nodeValue) {
function addNode(rData) {
	dbg({'Function addNode': rData});
	srcID = getID([rData.request.type,rData.request.value])
	dstID = getID([rData.response.type,rData.response.value])
	dstLabel = rData.response.type + "\n" + rData.response.value
	dbg(['--------',nodes._data[dstID]]);
	if(nodes._data[dstID] == null) {
		nodes.add({
			id: dstID,
			label: dstLabel,
			color: '#FDD',
			physics: phy,
			shape: 'box',
			data: {
				type: rData.response.type,
				value: rData.response.value
			}
		});
	}
	addEdge(srcID, dstID, rData.response.method);

}


function addEdge(eFrom, eTo, eLabel) {
	dbg({'Function addEdge': [eFrom, eTo, eLabel]});
	edges.add({
		id: getID([eFrom,eTo]),
		label: eLabel,
		smooth: true,
//		length: 400,
		from: eFrom,
		to: eTo
	});
}
/*
function updateNode() {
	nodes.update({
		id: document.getElementById('node-id').value,
		label: document.getElementById('node-label').value
	});
}

function removeNode() {
	nodes.remove({id: document.getElementById('node-id').value});
}

function updateEdge() {
	edges.update({
		id: document.getElementById('edge-id').value,
		from: document.getElementById('edge-from').value,
		to: document.getElementById('edge-to').value
	});
}

function removeEdge() {
	edges.remove({id: document.getElementById('edge-id').value});
}
*/
function draw() {
	   // create an array with nodes
	nodes = new vis.DataSet();
	edges = new vis.DataSet();

	nodes.on('*', function () {
		document.getElementById('nodes').value = JSON.stringify(nodes.get(), null, 4);
	});
	edges.on('*', function () {
		document.getElementById('edges').value = JSON.stringify(edges.get(), null, 4);
	});
/*
	edges.add([
		{id: '4', from: '2', to: '5'}
	]);
*/
	var container = document.getElementById('network');
	var data = {
		nodes: nodes,
		edges: edges
	};
	var options = {
		physics: {
			solver: 'repulsion'
		},
		layout: {
			improvedLayout: true,
//			hierarchical: {
//				direction: 'UD',
//				levelSeparation: 200,
//				nodeSpacing: 100,
//				sortMethod: 'directed'
//			}
		}
	};
	network = new vis.Network(container, data, options);

	network.on( 'click', function(properties) {
		var ids = properties.nodes;
		var clickedNodes = nodes.get(ids);
		dbg({'clicked node': clickedNodes});
		if (clickedNodes.length > 0) {
			var nodeID = clickedNodes[0].id;
			var nodeType = clickedNodes[0].data.type;
			nodeData = clickedNodes[0].data;
			contextItem = nodeType;
		} else {
			contextItem = 'nul';
		}
	});
	var contextItems = {
		nul: {
			"add-node": {name: "add node"},
		},
		ip: {
			"dns": {name: "Get DNS PTR record (DNS)"},
			"whois": {name: "Get Whois record"}
		},
		asn: {
		},
		domain: {
			"dns": {name: "DNS"},
 			"whois": {name: "Get Whois record"}
		},
		cidr: {
			"ipcalc": {name: "IPcalc"},
			"ping": {name: "Ping all hosts in range"}
		},
		service: {
		},
		
	};
	
	
	var contextItem = 'nul';
	var nodeData;
	
	$.contextMenu({
		selector: '#network',
		build: function($trigger, e) {
            return {
				callback: function(key, options) {
//					console.log("CI: ", contextitem);
					console.log("clicked: " + key);
					if (key == 'add-node') {
						console.log("ADD");
						$( function() { $( "#dialog-add" ).dialog().show(); });
					}
					else {
						console.log("rCall " + key);
						rCall(key, nodeData);
					}
				},
				items: contextItems[contextItem]
			}
		}
	});
	
	$('.contextmenu').on('click', function(e){
		console.log('clicked', this);
	});
}

function rCall(rCallProc, nData) {
	console.log(rCallProc);
	console.table({nData});
	
	$.ajax({
		url: '/api/' + rCallProc + '/' + nData.type + '/' + nData.value.replace('/','%252f'),
		type: 'GET',
//		data: nData,
		success: function(rData){
			console.log(rData);
			addNodes(rData);
			//addNode(rData);
		},
		error: function(rData) {
			alert('woops!'); //or whatever
		}
	});
	
/*
	var jqxhr = $.getJSON(rCallProc, function(rData) {
		console.log( "success", rData );
		addNode(rCallProc, nData, rData);
	})
	.done(function() {
		console.log( "second success" );
	})
	.fail(function(e) {
		console.log( "error", e );
	})
	.always(function() {
		console.log( "complete" );
	});
/**/
}

