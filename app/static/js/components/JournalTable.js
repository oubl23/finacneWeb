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
                        <th>备注</th>
                        <th>原因</th>
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
