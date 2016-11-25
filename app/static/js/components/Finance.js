var React = require("react");
var FinanceTable = require("./FinanceTable");
var FinanceFile = require("./FinanceFile");
var FinanceMessage = require("./FinanceMessage");

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

    handleSubmit:function (e) {
        e.preventDefault();
        var form_data = new FormData($('form#account')[0]);

        $.ajax({
            type: 'post',
            url: '/add_balance',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: false,
        }).done(function (resp) {
            if(resp.status == "success"){
                homeLoader.hide();
                $("form#account")[0].reset();
                $("#message").html("success");
                $("#message").addClass("alert alert-success");
                this.listFinance();
            }
        }.bind(this))
    },
    componentDidMount: function () {
        this.listFinance();
    },
    render:function () {
        return(
            <form encType="multipart/form-data" method="post" onSubmit = {this.handleSubmit} id="account">
                <FinanceMessage />
                <FinanceFile/>
                <FinanceTable finances = {this.state.accounts} />
                <div className="form-group col-lg-3 pull-right">
                    <input className="form-control btn-primary" id="submit-form-btn" type="submit" placeholder="提交"/>
                </div>
            </form>
        )
    }
});
module.exports = Finance;
