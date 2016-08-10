import React from 'react';
import {connectRedux} from '../utils';
import {AnimateFade} from './animator';
import NewPolicySignUp from './new-policy-sign-up';
import CompletedAccount from './completed-account';

export default connectRedux(React.createClass({
  render() {
    return (
      <div>
        <h1>Account</h1>
        <AnimateFade>
          {this.renderInner()}
        </AnimateFade>
      </div>
    );
  },
  renderInner() {
    if(this.props.store.account.authenticated) {
      return <CompletedAccount key="complete" email={this.props.store.account.email} />;
    }
    return <NewPolicySignUp key="form" />;
  },
}));
