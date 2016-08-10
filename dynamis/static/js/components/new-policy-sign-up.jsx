import React from 'react';
import {connectRedux} from '../utils';
import actions from '../actions/actions';
import LinkedStateMixin from 'react-addons-linked-state-mixin';
import NotificationPanel from './notification-panel';

export default connectRedux(React.createClass({
  mixins: [LinkedStateMixin],
  getInitialState() {
    return {
      email: '',
      password1: '',
      password2: ''
    };
  },
  render() {
    return (
      <div>
        <NotificationPanel sectionId="account_creation" />
        <div className="input-field">
          <input type="text" id="email" valueLink={this.linkState('email')} />
          <label htmlFor="email">Email</label>
        </div>
        <div className="input-field">
          <input type="password" id="password1" valueLink={this.linkState('password1')} />
          <label htmlFor="password1">Password</label>
        </div>
        <div className="input-field">
          <input type="password" id="password2" valueLink={this.linkState('password2')} />
          <label htmlFor="password2">Password Confirmation</label>
        </div>
        <button className="btn" onClick={this.signup}>signup</button>
      </div>
    );
  },
  signup() {
    this.props.dispatch(actions.signup(
      this.state.email,
      this.state.password1,
      this.state.password2
    ));
  },
}));
