var React = require('react');

var JournalItem = React.createClass({
    render:function () {
        var journal = this.props.journal;
        var date = new Date(journal.DATE);
        var year = date.getFullYear();
        var month = (1 + date.getMonth()).toString();
        month = month.length > 1 ? month : '0' + month;
        var day = date.getDate().toString();
        day = day.length > 1 ? day : '0' + day;
        var journaldate =  year + '/' + month + '/' + day;

        return(
            <tr>
                <td>{ journal.ID  }</td>
                <td>{ journaldate }</td>
                <td>{ journal.MONEY }</td>
                <td>{ journal.REMARK }</td>
                <td>{ journal.RESON }</td>
            </tr>
        )
    }
});

module.exports = JournalItem;