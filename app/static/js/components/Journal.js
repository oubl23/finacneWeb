var React = require("react");
var JournalTable = require("./JournalTable");

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
                    { "data": "ACCOUNT_ID", "title":"账户","defaultContent":""},
                    { "data": "DATE", "title":"日期","defaultContent":""},
                    // { "data": "ID", "title":"ID","defaultContent":""},
                    // { "data": "JOB_ID", "title":"MANUFACTURER","defaultContent":""},
                    { "data": "MONEY", "title":"金额","defaultContent":""},
                    { "data": "REMARK", "title":"备注","defaultContent":""},
                    { "data": "REASON", "title":"原因","defaultContent":""},

            ],
        });
        datatable.MakeCellsEditable({
        "onUpdate": myCallbackFunction,
        "inputCss":'my-input-class',
        "columns": [4],
        "confirmationButton": { // could also be true
            "confirmCss": 'my-confirm-class',
            "cancelCss": 'my-cancel-class'
        },
        "inputTypes": [
            {
                "column": 4,
                "type": "text",
                "options": null
            }
        ]
    });
    },
    componentWillUnmount:function(){
        $('#table-journal').DataTable().destroy();
    },
    render:function () {
        return(
            <JournalTable journals={this.state.journals}/>
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