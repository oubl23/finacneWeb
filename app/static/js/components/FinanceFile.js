// var React = require("react");
//
// var FinanceFile = React.createClass({
//     render:function () {
//         return(
//             <fieldset>
//                 <label htmlFor="file">财务表</label>
//                 <input name="file" type="file"/>
//             </fieldset>
//         )
//     }
// });
// module.exports = FinanceFile;

import React from 'react';

export default class FinanceFile extends React.Component{
    render () {
        return(
            <fieldset>
                <label htmlFor="file">财务表</label>
                <input name="file" type="file"/>
            </fieldset>
        )
    }
}