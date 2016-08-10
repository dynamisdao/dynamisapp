import types from './types';
import urls from '../urls';
import _ from 'lodash';
import * as PolicyActions from './policy-actions';
import * as KeybaseActions from './keybase-actions';
import * as EmploymentHistoryActions from './employment-history-actions';
import {dispatchDjangoErrorMessages} from '../utils';
import * as WalletActions from './wallet-actions';
import * as QueueActions from './queue-actions';
import {setOn} from './gourmet-redux';

var actions = {
  ...PolicyActions,
  ...KeybaseActions,
  ...EmploymentHistoryActions,
  ...WalletActions,
  ...QueueActions,
  setOn: setOn,
  signup(email, password1, password2) {
    if (password1 !== password2) {
      return {
        type: types.ADD_NOTIFICATION,
        message: 'Passwords do not match',
        target: 'account_creation',
        uuid: 'password-mismatch'
      };
    }
    return function(dispatch, getState) {
      dispatch({
        type: types.CLEAR_NOTIFICATIONS,
        target: 'account_creation',
      });
      $.ajax({
        url: urls['account-create'],
        data: JSON.stringify({
          email: email,
          password1: password1,
          password2: password2
        }),
        contentType: 'application/json',
        method: 'POST'
      }).done(function(data) {
        dispatch({
          type: types.SET_LOGGED_IN,
          email: email
        });
        dispatch(actions.savePolicy());
      }).fail(function(response) {
        if(response.status === 400) {
          dispatchDjangoErrorMessages(dispatch, 'account_creation', response.responseJSON);
        } else {
          dispatch({
            type: types.ADD_NOTIFICATION,
            message: 'An error occurred while creating your account.',
            target: 'account_creation',
          });
        }
      });
    };
  },
  submitPolicyApplication() {
    return function(dispatch, getState) {
      var store = getState();
      $.ajax({
        url: urls['policy-create'] + store.policy.id + '/',
        data: JSON.stringify({
          data: {
            identity: {
              verification_method: 'keybase',
              verification_data: {
                username: store.keybase.username,
              },
            },
            employmentHistory: _.map(store.employmentHistory.jobs, 'current'),
          },
        }),
        contentType: 'application/json',
        method: 'PUT'
      }).done(function(data) {
        // TODO: fill this in
        // debugger;
      }).fail(function(response) {
        if(response.status === 400) {
          // TODO: fill this in
          // debugger;
        } else {
          // eslint-disable-next-line no-console
          console.error('Actual server error happened: ', response.responseText);
        }
      });
    };
  },
  dismissNotification(notificationId, sectionId) {
    return {
      type: types.DISMISS_NOTIFICATION,
      notificationId: notificationId,
      sectionId: sectionId,
    };
  },
};

export default actions;
