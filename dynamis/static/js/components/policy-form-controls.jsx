import React from 'react';
import {connectRedux} from '../utils';
import {AnimateFade} from './animator';
import actions from '../actions/actions';
import LinkedStateMixin from 'react-addons-linked-state-mixin';
import NotificationPanel from './notification-panel';

export default connectRedux(React.createClass({
  mixins: [LinkedStateMixin],
  getInitialState() {
    return {};
  },
  render() {
    return (
      <div>
        <AnimateFade>
          {this.renderControls()}
        </AnimateFade>
      </div>
    );
  },
  renderControls() {
    if(!this.props.store.policy.done) {
      return (
        <div>
          <h1>Finalize Application</h1>
          <button className="btn" onClick={this.markDone}>Done Editing Application</button>
        </div>
      );
    } else {
      if(!this.props.store.policy.signature) {
        return (
          <div>
            <h1>Sign Application</h1>
            <NotificationPanel sectionId="policy_signature" />
            To complete your application, you must sign all your information here with keybase: <a href="https://keybase.io/sign" target="_blank">https://keybase.io/sign</a>.
            This will verify that all your information is accurate and we didn't change it.
            <br /><code>{JSON.stringify(actions.encodePolicy(this.props.store).data)}</code>
            <div className="input-field col s6">
              <textarea valueLink={this.linkState('signature')} className="materialize-textarea" name="verification" type="text" id="signature" />
            </div>
            <button className="btn" onClick={this.signApplication}>Submit Signature</button>
            <button className="btn" onClick={this.markNotDone}>Cancel</button>
          </div>
        );
      } else {
        return (
          <div>
            <h1>Application Finalized</h1>
            <NotificationPanel sectionId="policy_submission" />
            <pre><code>{this.props.store.policy.signature}</code></pre>
            <button className="btn" onClick={this.clearSignature}>Re-Sign Application</button>
            <button className="btn" onClick={this.submitSignedApplication}>Submit Application</button>
            <button className="btn" onClick={this.markNotDone}>Edit Application</button>
          </div>
        );
      }
    }
  },
  submitSignedApplication() {
    this.props.dispatch(actions.submitSignedApplication());
  },
  markDone() {
    this.props.dispatch(actions.markPolicyDone());
  },
  markNotDone() {
    this.props.dispatch(actions.markPolicyNotDone());
  },
  clearSignature() {
    this.props.dispatch(actions.setOn('policy', 'signature', null));
  },
  signApplication() {
    var signature = this.state.signature;
    this.props.dispatch(actions.signPolicy(signature));
  }
}));
