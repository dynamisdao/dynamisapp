import React from 'react';
import {connectRedux} from '../utils';
import actions from '../actions/actions';
import LinkedStateMixin from 'react-addons-linked-state-mixin';
import NotificationPanel from './notification-panel';

export default connectRedux(React.createClass({
  mixins: [LinkedStateMixin],
  getInitialState: function() {
    return {};
  },
  render() {
    return (
      <div>
        <NotificationPanel sectionId="keybase_lookup" />
        <div className="row">
          <div className="input-field">
            <input type="text" id="keybase_username" valueLink={this.linkState('keybaseUsername')} onKeyUp={this.onInputKeyPress} autoFocus={true} />
            <label htmlFor="keybase_username">Keybase username</label>
          </div>
        </div>
        <div className="row">
          <button className="btn" onClick={this.lookupFromKeybase} type="button">Get data</button>
        </div>
      </div>
    );
  },
  lookupFromKeybase() {
    this.props.dispatch(actions.triggerKeybaseLookup(this.state.keybaseUsername));
  },
  onInputKeyPress(event) {
    setTimeout(Materialize.updateTextFields, 0);
    if(event.key === 'Enter') {
      this.lookupFromKeybase();
    }
  },
  renderLoader() {
    if(this.props.store.keybase.loading) {
      return (
        <div className="preloader-wrapper big active">
          <div className="spinner-layer spinner-blue-only">
            <div className="circle-clipper left">
              <div className="circle"></div>
            </div><div className="gap-patch">
              <div className="circle"></div>
            </div><div className="circle-clipper right">
              <div className="circle"></div>
            </div>
          </div>
        </div>
      );
    }
  },
}));
