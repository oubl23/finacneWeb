var ReactDOM = require('react-dom');
var React = require('react');
var Finance = require("./components/Finance");
var Journal = require("./components/Journal");

ReactDOM.render(<Finance/>, document.getElementById("finance-container"));
ReactDOM.render(<Journal/>, document.getElementById("journal-container"));
