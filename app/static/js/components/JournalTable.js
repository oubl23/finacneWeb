var React = require("react");
var FinanceTable = require("./FinanceTable");
var FinanceFile = require("./FinanceFile");
var FinanceMessage = require("./FinanceMessage");

var Journal = React.createClass({
    render:function () {
        var finances = this.props.finances.map(function (item) {
            return <FinanceItem  key = {item.ID} finance={item} />
        }.bind(this));
        return(
                <table className="table table-striped">
                <thead>
                    <tr>
                        <th>账户名</th>
                        <th>消费时间</th>
                        <th>金额</th>
                        <th>余额/剩余额度</th>
                        <th>额度/附属理财</th>
                        <th>上次对账时间</th>
                    </tr>
                </thead>
                <tbody>
                {finances}
                </tbody>
            </table>
        )
    }
});
module.exports = Journal;
