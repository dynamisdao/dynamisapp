import React from 'react';
import {connectRedux} from '../utils';
import actions from '../actions/actions';
import {AnimateFade} from './animator';
import CompletedIdentity from './completed-identity';
import _ from 'lodash';
import KeybaseLookup from './keybase-lookup';
import LinkedStateMixin from 'react-addons-linked-state-mixin';
import urls from '../urls';
import NotificationPanel from './notification-panel';
import {dispatchDjangoErrorMessages} from '../utils';

export default connectRedux(React.createClass({
  mixins: [LinkedStateMixin],
  getInitialState() {
    return { done: false };
  },
  render() {
    return (
      <div className="container">
        <AnimateFade>
          {this.renderForm()}
        </AnimateFade>
      </div>
    );
  },
  renderForm() {
    if(this.state.done) {
      return <span key="done"><h2>Keybase verified!</h2><a href={urls['user-profile']}>Click here</a> to go back</span>;
    }
    return (
      <div key="form">
        <NotificationPanel sectionId="verify_keybase_errors" />
        <h1>Verify Your Keybase</h1>
        <AnimateFade>
          {this.renderInner()}
        </AnimateFade>
        <AnimateFade>
          {this.renderSigning()}
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
  renderSigning() {
    if(this.props.store.keybase.username) {
      return (
        <div>
          please sign this: <code className="grey lighten-2" style={{padding: '2px'}}>{this.props.token}</code>
          <textarea className="materialize-textarea" valueLink={this.linkState('signature')} id="keybase_verify_textarea"></textarea>
          <label htmlFor="keybase_verify_textarea">Signature</label>
          <button className="btn" onClick={this.submitSignature}>Submit</button>
        </div>
      );
    }
  },
  submitSignature() {
    var dispatch = this.props.dispatch;
    var _this = this;
    $.ajax({
      method: 'PUT',
      url: urls['verify-keybase'],
      data: JSON.stringify({
        keybase_username: this.props.store.keybase.username,
        signed_message: this.state.signature,
      }),
      contentType: 'application/json'
    }).done(function(data) {
      dispatch({
        type: 'CLEAR_NOTIFICATIONS',
        target: 'verify_keybase_errors',
      });
      _this.setState({done: true});
    }).fail(function(response) {
      dispatchDjangoErrorMessages(dispatch, 'verify_keybase_errors', response.responseJSON);
    });
  },
}));
