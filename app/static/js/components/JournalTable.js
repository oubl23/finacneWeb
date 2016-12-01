var React = require("react");
var JournalItem = require("./JournalItem");

var JournalTable = React.createClass({
    render:function () {
        var journals = this.props.journals.map(function (item) {
            return <JournalItem  key = {item.ID} journal={item} />
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
                {journals}
                </tbody>
            </table>
        )
    }
});
module.exports = JournalTable;
