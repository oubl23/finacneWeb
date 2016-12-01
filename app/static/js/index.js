// import { Router, Route, Link, hashHistory, IndexRoute } from 'react-router';
// import React from 'react';
// import ReactDOM from 'react-dom';
// import Finance from './components/Finance';
// import Journal from './components/Journal';
var ReactDOM = require('react-dom');
var React = require('react');
var Finance = require("./components/Finance");
var Journal = require("./components/Journal");
var Router = require('react-router').Router;
var Route = require('react-router').Route;
var Link = require('react-router').Link;
var hashHistory = require('react-router').hashHistory;
// ReactDOM.render(<Finance/>,document.getElementById("container"))
ReactDOM.render((
    <Router history={hashHistory}>
        <Route path="/" component={Finance}/>
        <Route path="/journal" component={Journal} />
    </Router>
    ), document.getElementById("container"));

