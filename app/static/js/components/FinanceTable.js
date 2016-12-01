// var React = require("react");
// var FinanceItem = require("./FinanceItem");
//
// var FinanceTable = React.createClass({
//     render:function () {
//         var finances = this.props.finances.map(function (item) {
//             return <FinanceItem  key = {item.ID} finance={item} />
//         }.bind(this));
//         return (
//
//             <table className="table table-striped">
//                 <thead>
//                     <tr>
//                         <th>账户名</th>
//                         <th>账户别名</th>
//                         <th>无交易记录</th>
//                         <th>余额/剩余额度</th>
//                         <th>额度/附属理财</th>
//                         <th>上次对账时间</th>
//                     </tr>
//                 </thead>
//                 <tbody>
//                 {finances}
//                 </tbody>
//             </table>
//         )
//     }
// });
//
// module.exports = FinanceTable;

import React from 'react';
import FinanceItem from './FinanceItem';

export default class FinanceTable extends React.Component {
    // constructor(props){
    //     super(props);
    //     this.state = {};
    // }
    render () {
        var finances = this.props.finances.map(function (item) {
            return <FinanceItem  key = {item.ID} finance={item} />
        }.bind(this));
        return (

            <table className="table table-striped">
                <thead>
                    <tr>
                        <th>账户名</th>
                        <th>账户别名</th>
                        <th>无交易记录</th>
                        <th>余额/剩余额度</th>
                        <th>额度/附属理财</th>
                        <th>上次对账时间</th>
                    </tr>
                </thead>
                <tbody>
                {finances}
                </tbody>
            </table>
        )
    }
};