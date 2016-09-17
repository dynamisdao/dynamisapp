import {Provider} from 'react-redux';
import React from 'react';
import * as Redux from 'redux';
import ReduxThunk from 'redux-thunk';
import rootReducer from '../reducers';
import {getQueryParams} from '../utils';
import actions from '../actions/actions';
import App from './app';
import Wallet from './wallet';
import PolicyForm from './policy-form';
import PolicyFormAdmin from './policy-form-admin';
import PeerReview from './peer-review';
import VerifyKeybase from './verify-keybase';

function initStore(store) {
  var username = getQueryParams()['keybaseUsername'];
  var policyId = window.DjangoInfo.policyId;
  if(policyId) {
    store.dispatch(actions.loadPolicy(policyId));
  } else if(username) {
    store.dispatch(actions.triggerKeybaseLookup(username));
  }
}

function createReduxStore() {
  var store = Redux.compose(
    Redux.applyMiddleware(ReduxThunk)
  )(Redux.createStore)(rootReducer);

  initStore(store);
  return store;
}

export var Root = React.createClass({
  render() {
    return (
      <Provider store={createReduxStore()}>
        <App />
      </Provider>
    );
  },
});

export var PolicyFormRoot = React.createClass({
  render() {
    return (
      <Provider store={createReduxStore()}>
        <PolicyForm />
      </Provider>
    );
  },
});

export var PolicyFormAdminRoot = React.createClass({
  render() {
    return (
      <Provider store={createReduxStore()}>
        <PolicyFormAdmin />
      </Provider>
    );
  },
});

export var WalletRoot = React.createClass({
  render() {
    var store = createReduxStore();
    store.dispatch(actions.initializeWallet());
    return (
      <Provider store={store}>
        <Wallet />
      </Provider>
    );
  },
});

export var PeerReviewRoot = React.createClass({
  render() {
    return (
      <Provider store={createReduxStore()}>
        <PeerReview />
      </Provider>
    );
  }
});

export function VerifyKeybaseRoot(props) {
  return (
    <Provider store={createReduxStore()}>
      <VerifyKeybase token={props.token} />
    </Provider>
  );
}
