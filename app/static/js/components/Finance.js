var React = require("react");
var FinanceTable = require("./FinanceTable");

var Finance = React.createClass({
    getInitialState:function(){
        return{
            accounts: []
        }
    },
    listFinance:function () {
        $.ajax({
            type:'get',
            url: '/list_account'
        }).done(function (resp) {
            if(resp.status == "success"){
                this.setState({accounts:resp.accounts});
            }
        }.bind(this))
    },
    componentDidMount: function () {
        this.listFinance();
    },
    render:function () {
        return(
            <form >
                <FinanceTable finances = {this.state.accounts} />
                <div className="form-group col-lg-3 pull-right">
                    <input className="form-control btn-primary" type="submit"/>
                </div>
            </form>
        )
    }
});
module.exports = Finance;
