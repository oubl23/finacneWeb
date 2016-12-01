// import React from 'react';
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
        waitingDialog.show('Custom message', {dialogSize: 'sm', progressType: 'warning'});
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
                $("form#account")[0].reset();
                $("#message").html(resp.message);
                $("#message").addClass("alert alert-success");
                this.listFinance();
            }else{
                $("#message").html(resp.message);
                $("#message").addClass("alert alert-danger");
            }
            waitingDialog.hide();
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

// import React from 'react';
// import FinanceTable from './FinanceTable';
// import FinanceFile from './FinanceFile';
// import FinanceMessage from './FinanceMessage';
//
// export default class Finance extends React.Component {
//     constructor(props){
//         super(props);
//         this.listFinance();
//         this.state = {
//             accounts: [],
//         };
//     }
//     // getInitialState(){
//     //     return{
//     //         accounts: []
//     //     }
//     // }
//     listFinance() {
//         $.ajax({
//             type:'get',
//             url: '/list_account'
//         }).done(function (resp) {
//             if(resp.status == "success"){
//                 this.setState({accounts:resp.accounts});
//             }
//         }.bind(this));
//     }
//
//     handleSubmit(e) {
//         //let _this = this;
//         e.preventDefault();
//         waitingDialog.show('Custom message', {dialogSize: 'sm', progressType: 'warning'});
//         let form_data = new FormData($('form#account')[0]);
//         $.ajax({
//             type: 'post',
//             url: '/add_balance',
//             data: form_data,
//             contentType: false,
//             cache: false,
//             processData: false,
//             async: false,
//             success:function(data){
//                 this.listFinance();
//             }
//         });
//         //     .done(function (resp) {
//         //     if(resp.status == "success"){
//         //         $("form#account")[0].reset();
//         //         $("#message").html(resp.message);
//         //         $("#message").addClass("alert alert-success");
//         //         this.listFinance();
//         //     }else{
//         //         $("#message").html(resp.message);
//         //         $("#message").addClass("alert alert-danger");
//         //     }
//         //     waitingDialog.hide();
//         // }.bind(this));
//     }
//     componentDidMount() {
//         this.listFinance();
//     }
//     render() {
//         return(
//             <form encType="multipart/form-data" method="post" onSubmit = {this.handleSubmit} id="account">
//                 <FinanceMessage />
//                 <FinanceFile/>
//                 <FinanceTable finances = {this.state.accounts} />
//                 <div className="form-group col-lg-3 pull-right">
//                     <input className="form-control btn-primary" id="submit-form-btn" type="submit" placeholder="提交"/>
//                 </div>
//             </form>
//         )
//     }
// };