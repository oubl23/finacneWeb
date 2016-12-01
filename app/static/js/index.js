// import { Router, Route, Link, hashHistory, IndexRoute } from 'react-router';
// import React from 'react';
// import ReactDOM from 'react-dom';
// import Finance from './components/Finance';
// import Journal from './components/Journal';
let ReactDOM = require('react-dom');
let React = require('react');
let Finance = require("./components/Finance");
let Journal = require("./components/Journal");
let Balance = require("./components/Balance");
let Router = require('react-router').Router;
let Route = require('react-router').Route;
let Link = require('react-router').Link;
let hashHistory = require('react-router').hashHistory;
// ReactDOM.render(<Finance/>,document.getElementById("container"))
ReactDOM.render((
    <Router history={hashHistory}>
        <Route path="/" component={Finance}/>
        <Route path="/balance" component={Balance}/>
        <Route path="/journal" component={Journal} />
    </Router>
    ), document.getElementById("container"));

