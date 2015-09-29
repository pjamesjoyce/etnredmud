function d3_main(treeData){

  var margin = {top:20, right:120, bottom:20, left:120},
      width = 960 - margin.right - margin.left,
      height = 500 - margin.top - margin.bottom;

  var i = 0,
  duration = 750,
  root;

  var  tree = d3.layout.tree()
        .size([height, width]);

  var diagonal = d3.svg.diagonal()
        .projection(function(d){return [d.y, d.x];});

  var svg = d3.select('.tree').append('svg')
        .attr('width', width + margin.right + margin.left)
        .attr('height',height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

  root = treeData;
  root.x0 = height/2;
  root.y0=0;

  update(root);

  d3.select(self.frameElement).style('height','500px');

  //this is the update function

  function update(source){

    //compute the tree layout

    var nodes = tree.nodes(root).reverse(),
        links = tree.links(nodes);

    //normalise for fixed depth

    nodes.forEach(function(d){d.y = d.depth * 180;})

    console.log(nodes)
    console.log(links)

    // Update the nodes…
  var node = svg.selectAll("g.node")
	  .data(nodes, function(d) { return d.id || (d.id = ++i); });

  // Enter any new nodes at the parent's previous position.
  var nodeEnter = node.enter().append("g")
	  .attr("class", "node")
	  .attr("transform", function(d) { return "translate(" + source.y0 + "," + source.x0 + ")"; })
	  .on("click", click);

  nodeEnter.append("circle")
	  .attr("r", 1e-6)
	  .style("fill", function(d) { return d._children ? "lightsteelblue" : "#fff"; });

  nodeEnter.append("text")
	  .attr("x", function(d) { return d.children || d._children ? -13 : 13; })
	  .attr("dy", ".35em")
	  .attr("text-anchor", function(d) { return d.children || d._children ? "end" : "start"; })
	  .text(function(d) { return d.name; })
	  .style("fill-opacity", 1e-6);

  // Transition nodes to their new position.
  var nodeUpdate = node.transition()
	  .duration(duration)
	  .attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; });

  nodeUpdate.select("circle")
	  .attr("r", 10)
	  .style("fill", function(d) { return d._children ? "lightsteelblue" : "#fff"; });

  nodeUpdate.select("text")
	  .style("fill-opacity", 1);

  // Transition exiting nodes to the parent's new position.
  var nodeExit = node.exit().transition()
	  .duration(duration)
	  .attr("transform", function(d) { return "translate(" + source.y + "," + source.x + ")"; })
	  .remove();

  nodeExit.select("circle")
	  .attr("r", 1e-6);

  nodeExit.select("text")
	  .style("fill-opacity", 1e-6);

  // Update the links…
  var link = svg.selectAll("path.link")
	  .data(links, function(d) { return d.target.id; });

  // Enter any new links at the parent's previous position.
  link.enter().insert("path", "g")
	  .attr("class", "link")
	  .attr("d", function(d) {
		var o = {x: source.x0, y: source.y0};
		return diagonal({source: o, target: o});
	  });

  // Transition links to their new position.
  link.transition()
	  .duration(duration)
	  .attr("d", diagonal);

  // Transition exiting nodes to the parent's new position.
  link.exit().transition()
	  .duration(duration)
	  .attr("d", function(d) {
		var o = {x: source.x, y: source.y};
		return diagonal({source: o, target: o});
	  })
	  .remove();

  // Stash the old positions for transition.
  nodes.forEach(function(d) {
	d.x0 = d.x;
	d.y0 = d.y;
  });
}

// Toggle children on click.
function click(d) {
  if (d.children) {
	d._children = d.children;
	d.children = null;
  } else {
	d.children = d._children;
	d._children = null;
  }
  update(d);
}




/*
  //define the size

  var width = 640,
      height = 480;

// this is the tutorial data - we'll get rid  of this

  var nodes = [
    {x: 50, y:50},
    {x: 50, y:100},
    {x: 100, y:50},
    {x: 100, y:100}
  ]

  var links = [
    { source: 0, target:1 },
    { source: 1, target:2 },
    { source: 2, target:3 },
    { source: 3, target:1 },
    { source: 2, target:0 },
    { source: 1, target:3 }
  ]

  // create an svg container

  var svg = d3.select('.tree').append('svg')
        .attr('width',width)
        .attr('height', height);

  // create the force layout and define it's properties

  var force = d3.layout.force()
        .size([width,height])
        .nodes(nodes)
        .links(links);

  force.linkDistance(width/2);

  // add the nodes and links to the svg

  var link = svg.selectAll('.link')
        .data(links)
        .enter().append('line')
        .attr('class','link');

  var node = svg.selectAll('.node')
        .data(nodes)
        .enter().append('circle')
        .attr('class','node');

  // define the function that will run when the force calculations stop

  force.on('end', function(){
    // reposition the nodes
    node.attr('r', width/25)
        .attr('cx', function(d){return d.x})
        .attr('cy', function(d){return d.y});

    // now the links (via source and target)

    link.attr('x1', function(d){return d.source.x})
    link.attr('y1', function(d){return d.source.y})
    link.attr('x2', function(d){return d.target.x})
    link.attr('y2', function(d){return d.target.y});
  });

  //start the force calculations

  force.start();
*/

}


function d3_radial(treeData){



  var diameter = 960;

  var tree = d3.layout.tree()
      .size([360, diameter / 2 - 120])
      .separation(function(a, b) { return (a.parent == b.parent ? 1 : 2) / a.depth; });

  var diagonal = d3.svg.diagonal.radial()
      .projection(function(d) { return [d.y, d.x / 180 * Math.PI]; });

  var svg = d3.select(".tree").append("svg")
      .attr("width", diameter)
      .attr("height", diameter - 150)
    .append("g")
      .attr("transform", "translate(" + diameter / 2 + "," + diameter / 2 + ")");

  root = treeData

    var nodes = tree.nodes(root),
        links = tree.links(nodes);

    var link = svg.selectAll(".link")
        .data(links)
      .enter().append("path")
        .attr("class", "link")
        .attr("d", diagonal);

    var node = svg.selectAll(".node")
        .data(nodes)
      .enter().append("g")
        .attr("class", "node")
        .attr("transform", function(d) { return "rotate(" + (d.x - 90) + ")translate(" + d.y + ")"; })

    node.append("circle")
        .attr("r", 4.5);

    node.append("text")
        .attr("dy", ".31em")
        .attr("text-anchor", function(d) { return d.x < 180 ? "start" : "end"; })
        .attr("transform", function(d) { return d.x < 180 ? "translate(8)" : "rotate(180)translate(-8)"; })
        .text(function(d) { return d.name; });


  d3.select(self.frameElement).style("height", diameter - 150 + "px");

}


function d3_force(treeData, max_footprint){

  var width = 500,
    height = 500;

  var force = d3.layout.force()
      .gravity(.01)
      .charge(-2000)
      .linkDistance(height/20)
      .size([width, height]);

  var svg = d3.select(".tree").append("svg:svg")
      //.attr("width", width)
      //.attr("height", height)
      .attr("viewBox","0 0 500 500")
      .attr("preserveAspectRatio","none");

  var root = treeData;//getData();
  var nodes = flatten(root),
      links = d3.layout.tree().links(nodes);

  var scale = d3.scale.linear()
              .domain([0,max_footprint])
              .range([0,height/16]);

  var colours = d3.scale.category10();

  nodes.forEach(function(d, i) {
      d.x = width/2 + i;
      d.y = height/2 + 100 * d.depth;
  });

  root.fixed = true;
  root.x = width / 2;
  root.y = height / 2;

  force.nodes(nodes)
      .links(links)
      .start();



  var link = svg.selectAll("line")
      .data(links)
     .enter()
      .insert("svg:line")
      .attr("class", "link");

  var gnodes = svg.selectAll('g.gnode')
     .data(nodes)
     .enter()
     .append('g')
     .classed('gnode', true);

  var node = gnodes.append("circle")
      .attr("r", function(d){return scale(d.footprint)})
      .style("fill", function(d){return colours(d.level);})
      .attr("class", "node")
      .call(force.drag);

  var labels = gnodes.append("text")
        .text(function(d){ return d.name})

  force.on("tick", function(e) {

      link.attr("x1", function(d) { return d.source.x; })
          .attr("y1", function(d) { return d.source.y; })
          .attr("x2", function(d) { return d.target.x; })
          .attr("y2", function(d) { return d.target.y; });

      //node.attr("cx", function(d) { return d.x; })
          //.attr("cy", function(d) { return d.y; });

      gnodes.attr("transform", function(d){ return 'translate(' + [d.x, d.y] + ')';})

  });

  function flatten(root) {
      var nodes = [];
      function recurse(node, depth) {
          if (node.children) {
              node.children.forEach(function(child) {
                  recurse(child, depth + 1);
              });
          }
          node.depth = depth;
          nodes.push(node);
      }
      recurse(root, 1);
      return nodes;
  }

}
