let React = require("react");

let BalanceItem = React.createClass({
    render:function () {
        let balance_item = this.props.balance_item;
        return(
                <tr>
                    <td>{ balance_item.ACCOUNT_ID}</td>
                    <td>{balance_item.CHECKED}</td>
                    <td>{balance_item.MONEY}</td>
                </tr>
        )
    }
});
module.exports = BalanceItem;
