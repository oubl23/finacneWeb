// var React  = require("react");
//
// var FinanceMessage = React.createClass({
//     render:function () {
//         return (
//             <center>
//                 <div id = "message">
//                 </div>
//             </center>
//         )
//     }
// });
//
// module.exports = FinanceMessage;

import React from 'react';

export default class FinanceMessage extends React.Component {
    constructor(props){
        super(props);
        this.state = {};
    }
    render() {
        return(
            <center>
                <div id = "message">
                </div>
            </center>
            )
    }
};