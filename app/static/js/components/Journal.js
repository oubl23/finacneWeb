var React = require("react");
var JournalTable = require("./JournalTable");

var Journal = React.createClass({
    getInitialState:function(){
        return{
            journals: []
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