var React = require("react");

var FinanceFile = React.createClass({
    render:function () {
        return(
            <fieldset>
                <label htmlFor="file">财务表</label>
                <input name="file" type="file"/>
            </fieldset>
        )
    }
});
module.exports = FinanceFile;
