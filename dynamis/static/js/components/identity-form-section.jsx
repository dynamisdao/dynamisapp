import React from 'react';
import {connectRedux} from '../utils';
import actions from '../actions/actions';
import {AnimateFade} from './animator';
import CompletedIdentity from './completed-identity';
import _ from 'lodash';
import KeybaseLookup from './keybase-lookup';

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
    if(this.props.store.keybase.username) {
      return <CompletedIdentity key="complete" changeAccount={this.changeAccount} keybase={this.props.store.keybase}/>;
    }
    return <KeybaseLookup key="form" />;
  },
  changeAccount() {
    if(_.isEqual(this.props.store.keybase, {})) {
      return;
    }
    this.props.dispatch(actions.resetIdentity());
  },
}));
