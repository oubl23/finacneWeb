var React = require('react');

var FinanceItem = React.createClass({

    render:function () {
        var account = this.props.finance;
        var updateAccount;
        if(account.LIMIT == 0){
            updateAccount = <input type="text" className="form-control input-sm"  name={"balance[" + account.ID  + "][ACCESSARY]"}   />
        }else {
            updateAccount = <input type="text" className="form-control input-sm" value= { account.LIMIT } name={"balance[" + account.ID  + "][ACCESSARY]"}  readOnly="readOnly"/>
        }

        return(

            <tr>
                 <td>{ account.NAME  }</td>
                    <td>{ account.SHORT_NAME }</td>
                    <td>{ account.DATETIME }</td>
                    <td className="col-sm-2">
                        <input type="text" className="form-control input-sm" name={"balance[" + account.ID  + "][MONEY]"}/>
                    </td>
                    <td className="col-sm-2">
                        {updateAccount}
                    </td>
                    <td>
                        <input type="checkbox" className="form-control input-sm" name={"balance[" + account.ID  + "][LACKd]"}/>
                    </td>
            </tr>
        )
    }
});

module.exports = FinanceItem;