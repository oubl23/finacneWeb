let React = require("react");
let BalanceGroup = require('./BalanceGroup');

let Balance = React.createClass({
    getInitialState: function () {
        return {
            balances: []
        }
    },
    listBalance: function () {
        $.ajax({
            type: 'get',
            url: '/list_balance'
        }).done(function (resp) {
            if (resp.status == "success") {
                this.setState({balances: resp.balances});
            }
        }.bind(this))
    },
    componentDidMount: function () {
        this.listBalance();
    },
    render: function () {
        //console.log(this.state.balances);
        let i = 0;
        let balances = this.state.balances.map(function (item) {
            return (
                <BalanceGroup key={item.ID} balance={item}  />
            )
        }.bind(this));
        return (
            <div className="fancy-collapse-panel">
                <div className="panel-group" id="accordion">
                    {balances}
                </div>
            </div>
        )
    }
});
module.exports = Balance;
