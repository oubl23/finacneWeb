let React = require("react");

let BalanceGroup = React.createClass({
    render:function () {
        return(
            <div>
                <a href="#" ref="refs" className="list-group-item" data-toggle="collapse" data-target="#sm" data-parent="#menu">MESSAGES <span className="label label-info">5</span> <span className="glyphicon glyphicon-envelope pull-right"> </span></a>
                <div id="" className="sublinks collapse">
                    <a className="list-group-item small"><span className="glyphicon glyphicon-chevron-right"> </span> inbox</a>
                    <a className="list-group-item small"><span className="glyphicon glyphicon-chevron-right"> </span> sent</a>
                </div>
            </div>
        )
    }
});
module.exports = BalanceGroup;

//  <div>
//  <a href="#/balance" className="list-group-item" data-toggle="collapse" data-target="#sm" data-parent="#menu">MESSAGES <span className="label label-info">5</span> <span className="glyphicon glyphicon-envelope pull-right"> </span></a>
//  <div id="sm" className="sublinks collapse">
//   <a className="list-group-item small"><span className="glyphicon glyphicon-chevron-right"> </span> inbox</a>
//   <a className="list-group-item small"><span className="glyphicon glyphicon-chevron-right"> </span> sent</a>
//  </div>
//  </div>
// <div>
//  <a href="#" className="list-group-item" data-toggle="collapse" data-target="#sl" data-parent="#menu">TASKS <span className="glyphicon glyphicon-tag pull-right"> </span></a>
//  <div id="sl" className="sublinks collapse">
//   <a className="list-group-item small"><span className="glyphicon glyphicon-chevron-right"> </span> saved tasks</a>
//   <a className="list-group-item small"><span className="glyphicon glyphicon-chevron-right"> </span> add new task</a>
//  </div>
//     </div>
//     <div>
//  <a href="#" className="list-group-item">ANOTHER LINK ...<span className="glyphicon glyphicon-stats pull-right"> </span></a>
//     </div>
