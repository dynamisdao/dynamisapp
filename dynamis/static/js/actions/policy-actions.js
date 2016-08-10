import urls from '../urls';
import types from './types';
import _ from 'lodash';
import {triggerKeybaseLookup} from './keybase-actions';
import sortify from 'json-stable-stringify';
import murmurhash from 'murmurhash';
import {dispatchDjangoErrorMessages} from '../utils';
import {setOn} from './gourmet-redux';

function setPolicyData(data) {
  return {
    type: types.SET_POLICY_DATA,
    policyId: data.policyId,
    jobs: data.jobs,
    premium: data.premium,
  };
}

export function decodePolicy(data) {
  return {
    keybaseUsername: _.get(data, 'data.identity.verification_data.username'),
    policyId: data.id,
    jobs: _.get(data, 'data.employmentHistory.jobs', []),
    premium: _.get(data, 'data.requestedPremiumAmount'),
  };
}

export function encodePolicy(store) {
  var jobs = _.compact(_.map(_.cloneDeep(store.employmentHistory.jobs), 'saved'));
  return {
    data: {
      identity: {
        verification_method: 'keybase',
        verification_data: {
          username: store.keybase.username,
          proofs: store.keybase.proofs,
        },
      },
      employmentHistory: {
        jobs: jobs
      },
      requestedPremiumAmount: store.policy.premium
    }
  };
}

export function loadPolicy(policyId) {
  return function(dispatch, getState) {
    $.ajax({
      url: urls['policy-create'] + policyId + '/',
      method: 'get'
    }).done(function(data) {
      var parsed = decodePolicy(data);
      if(parsed.keybaseUsername) {
        dispatch(triggerKeybaseLookup(parsed.keybaseUsername));
      }
      dispatch(setPolicyData(parsed));
    });
  };
}

export function savePolicy() {
  return function(dispatch, getState) {
    var store = getState();
    var policyId = store.policy.id;
    var url = urls['policy-create'];
    var method = 'POST';
    if(policyId) {
      url += policyId + '/';
      method = 'PUT';
    }
    $.ajax({
      url: url,
      data: JSON.stringify(encodePolicy(store)),
      contentType: 'application/json',
      method: method
    }).done(function(data) {
      dispatch(setOn('policy', 'id', data.id));
    }).fail(function(response) {
      // TODO: need formal error handling system to dedup this code.
      if(response.status === 400) {
        // eslint-disable-next-line no-console
        console.error('Something went wrong', response.responseJSON);
      } else {
        // eslint-disable-next-line no-console
        console.error('Actual server error happened: ', response.responseText);
      }
    });
  };
}

export function submitSignedApplication() {
  return function(dispatch, getState) {
    dispatch({
      type: types.CLEAR_NOTIFICATIONS,
      target: 'policy_submission',
    });
    var store = getState();
    var policyId = store.policy.id;

    if(!policyId) {
      // eslint-disable-next-line no-console
      console.error('Something is wrong.  Policy should have an ID');
      dispatch({
        type: types.ADD_NOTIFICATION,
        target: 'policy_submission',
        message: 'No policy Id.',
        uuid: 'no_policy_id',
      });
      return;
    }
    var data = {
      keybase_username: store.keybase.username,
      signed_message: store.policy.signature,
    };
    $.ajax({
      url: urls['policy-create'] + policyId + '/submit/',
      data: JSON.stringify(data),
      contentType: 'application/json',
      method: 'post',
    }).done(function(data) {
      // Redirect the user to the user profile.
      window.location = urls['user-profile'];
    }).fail(function(response) {
      if(response.status === 400) {
        dispatchDjangoErrorMessages(dispatch, 'policy_submission', response.responseJSON);
      } else {
        // eslint-disable-next-line no-console
        console.error('Actual server error happened: ', response.responseText);
        dispatch({
          type: types.ADD_NOTIFICATION,
          target: 'policy_submission',
          message: 'Server Error. Please try again.',
          uuid: 'server_error',
        });
      }
    });
  };
}

export function markPolicyDone() {
  return function(dispatch, getState) {
    var store = getState();
    var hash = murmurhash.v3(sortify(encodePolicy(store)));
    dispatch({
      type: types.MARK_POLICY_DONE,
      done: true,
      applicationHash: hash,
    });
  };
}

export function markPolicyNotDone() {
  return {
    type: types.MARK_POLICY_DONE,
    done: false,
  };
}

export function validatePolicySignature() {
  // TODO: real validation:
}

export function signPolicy(signature) {
  return function(dispatch, getState) {
    var promise = new Promise(function(resolve, reject) {
      // TODO: validate the policy data
      if(signature) {
        resolve(signature);
      } else {
        reject(signature);
      }
    });
    return promise.then(function(valid_signature) {
      dispatch({
        type: types.CLEAR_NOTIFICATIONS,
        target: 'policy_signature',
      });
      dispatch(setOn('policy', 'signature', signature));
    }, function(invalid_signature) {
      dispatch({
        type: types.ADD_NOTIFICATION,
        target: 'policy_signature',
        message: 'Bad Signature',
        uuid: 'signature_error',
      });
    });
  };
}
