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
                this.setState({balances:resp.balances_list});
            }
        }.bind(this))
    },
    componentDidMount: function () {
        this.listBalance();
    },
    render:function () {
        let balances = this.props.balances.map(function (item) {
            return <BalanceGroup  key = {item.ID} Balance={item} />
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