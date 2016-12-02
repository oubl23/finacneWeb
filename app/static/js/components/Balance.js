let React = require("react");
let BalanceGroup = require('./BalanceGroup');

let Balance = React.createClass({
    getInitialState:function(){
        return{
            balances: []
        }
    },
    listBalance:function () {
        $.ajax({
            type:'get',
            url: '/list_balance'
        }).done(function (resp) {
            if(resp.status == "success"){
                this.setState({balances:resp.balances});
            }
        }.bind(this))
    },
    componentDidMount: function () {
        this.listBalance();
    },
    render:function () {
        //console.log(this.state.balances);
        let balances = this.state.balances.map(function (item) {
            return <BalanceGroup  key = {item.ID} balance={item} />
        }.bind(this));
        return(
            <div className="panel list-group">
                {balances}
            </div>
        )
    }
});
module.exports = Balance;

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