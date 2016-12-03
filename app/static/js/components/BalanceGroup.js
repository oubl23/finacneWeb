let React = require("react");
let BalanceItem = require('./BalanceItem');

let BalanceGroup = React.createClass({
    render:function () {
        let balance = this.props.balance;
        let balance_item = balance.DATA.map(function (item) {
            return <BalanceItem  key = {item.ID} balance_item={item} />
        }.bind(this));
        return(
            <div className="panel panel-default">
                <div className="panel-heading">
                     <h4 className="panel-title">
                        <a  className="list-group-item" data-toggle="collapse" href={"#balance"+ balance.ID } data-parent="#accordion">{balance.DATETIME}
                            <span className="pull-right"><span className="label label-info">{balance.COUNT}</span></span>
                            <span className="pull-right">{"￥"+balance.SUMMARY+"  "}<span className="label label-warning">{balance.UNCHECKED}</span></span>
                        </a>
                     </h4>
                </div>
                <div id={"balance" + balance.ID} className="panel-collapse collapse" >
                    <table className="table table-striped">
                        <thead>
                            <tr>
                                <th>账户名</th>
                                <th>对账状态</th>
                                <td>余额</td>
                            </tr>
                        </thead>
                        <tbody>
                        { balance_item }
                        </tbody>
                    </table>
                </div>
            </div>
        )
    }
});
module.exports = BalanceGroup;
