import React from 'react';
import {connectRedux} from '../utils';
import {AnimateFade} from './animator';
import _ from 'lodash';

export default connectRedux(React.createClass({
    render() {
        return (
            <div>
                <h1>Identity</h1>
                <AnimateFade>
                    {this.renderInner()}
                </AnimateFade>
            </div>
        );
    },
    renderInner() {
        if (this.props.store.keybase.username) {
            return <div className="card light-green lighten-3">
                <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore
                    et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut
                    aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse
                    cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
                    culpa qui officia deserunt mollit anim id est laborum.</p>
                <KeybaseData data={props.keybase}/>
            </div>
        }
    },
}));
