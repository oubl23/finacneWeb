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
                    { "data": "ACCOUNT_ID", "title":"ID","defaultContent":""},
                    { "data": "DATE", "title":"TYPE","defaultContent":""},
                    { "data": "ID", "title":"DESCRIPTION","defaultContent":""},
                    { "data": "JOB_ID", "title":"MANUFACTURER","defaultContent":""},
                    { "data": "MONEY", "title":"MODEL","defaultContent":""},
                    { "data": "REASON", "title":"VALUE","defaultContent":""},
                    { "data": "REMARK", "title":"LIBRARY_REF","defaultContent":""},
            ],
        });
    },
    componentWillUnmount:function(){
        datatable.destroy();
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