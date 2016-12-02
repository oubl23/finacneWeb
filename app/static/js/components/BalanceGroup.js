let React = require("react");
let BalanceItem = require('./BalanceItem');

let BalanceGroup = React.createClass({
    render:function () {
        let balance = this.props.balance;
        let balance_item = balance.DATA.map(function (item) {
            return <BalanceItem  key = {item.ID} balance_item={item} />
        }.bind(this));
        return(
            <div>
                <a href="#/balance" className="list-group-item" data-toggle="collapse" data-target={"#balance"+ balance.ID } >{balance.DATETIME}
                    <span className="pull-right"><span className="label label-info">{balance.COUNT}</span></span>
                    <span className="pull-right"><span className="label label-warning">{balance.UNCHECKED}</span></span>
                </a>
                <div id={"balance" + balance.ID} className="sublinks collapse" >
                    <table className="table table-striped">
                        <thead>
                            <tr>
                                <th>账户名</th>
                                <th>对账状态</th>
                            </tr>
                        </thead>
                        <tbody>
                        { balance_item }
                        </tbody>
                    </table>
                    {/*<a className="list-group-item small"><span className="glyphicon glyphicon-chevron-right"> </span> inbox</a>*/}
                    {/*<a className="list-group-item small"><span className="glyphicon glyphicon-chevron-right"> </span> sent</a>*/}
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
