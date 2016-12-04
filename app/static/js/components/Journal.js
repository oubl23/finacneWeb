var React = require("react");
var JournalTable = require("./JournalTable");
var FinanceMessage = require("./FinanceMessage");

var Journal = React.createClass({
    getInitialState:function(){
        return{
            journals: [],

        }
    },
    listJournal:function () {
        $.ajax({
            type:'get',
            url: '/list_journal'
        }).done(function (resp) {
            if(resp.status == "success"){
                this.setState({journals:resp.journals});
            }
        }.bind(this))
    },
    componentDidMount: function () {
        this.listJournal();
        let datatable = $('#table-journal').DataTable({
            "ajax": {
               "url": "/list_journal",
               "type": "get",
               "error":function(){alert("服务器未正常响应，请重试!!!");}
            },
            "columns": [
                    { "data": "ID", "title":"ID","defaultContent":""},
                    { "data": "ACCOUNT_ID", "title":"账户","defaultContent":""},
                    { "data": "DATE", "title":"日期","defaultContent":""},
                    { "data": "MONEY", "title":"金额","defaultContent":""},
                    { "data": "REMARK", "title":"备注","defaultContent":""},
                    { "data": "REASON", "title":"原因","defaultContent":""},

            ],
        });
        datatable.MakeCellsEditable({
            "onUpdate":function (updatedCell,updatedRow) {
                waitingDialog.show('Custom message', {dialogSize: 'sm', progressType: 'warning'});
                console.log(updatedCell.data());
                console.log(updatedRow.data().ID);
                let update_reason = updatedCell.data();
                let update_id = updatedRow.data().ID;

                $.ajax({
                    type:'post',
                    url: '/update_journal',
                    data : {update_reason:update_reason ,update_id:update_id}
                }).done(function (resp) {
                    if(resp.status == "success"){
                        $("#message").html(resp.message);
                        $("#message").addClass("alert alert-success");
                    }
                    waitingDialog.hide();
                }.bind(this));

            },
            "inputCss":'my-input-class',
            "columns": [5],
            "confirmationButton": { // could also be true
                "confirmCss": 'my-confirm-class',
                "cancelCss": 'my-cancel-class'
            },
            "inputTypes": [
                {
                    "column": 5,
                    "type": "text",
                    "options": null
                }]
        });
    },
    componentWillUnmount:function(){
        $('#table-journal').DataTable().destroy();
    },
    render:function () {
        return(
            <div>
                 <FinanceMessage />
                <JournalTable journals={this.state.journals}/>
            </div>
        )
    }
});
module.exports = Journal;

//
// import React from 'react';
//
// export default class Journal extends React.Component {
//     constructor(props){
//         super(props);
//         this.state = {};
//     }
//     render() {
//         return(
//                 <div>
//                 world
//                 </div>
//             )
//     }
// };