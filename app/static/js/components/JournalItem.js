var React = require('react');

var JournalItem = React.createClass({

    render:function () {
        var journal = this.props.journal;
        var updateAccount;
        if(account.LIMIT == 0){
            updateAccount = <input type="text" className="form-control input-sm"  name={"balance[" + account.ID  + "][ACCESSARY]"}   />
        }else {
            updateAccount = <input type="text" className="form-control input-sm" value= { account.LIMIT } name={"balance[" + account.ID  + "][ACCESSARY]"}  readOnly="readOnly"/>
        }

        return(

            <tr>
                 <td>{ journal.NAME  }</td>
                    <td>{ journal.SHORT_NAME }</td>
                  <td>{ journal.DATETIME }</td>
            </tr>
        )
    }
});

module.exports = JournalItem;