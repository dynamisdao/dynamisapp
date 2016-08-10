import types from './types';
import KeyBaseService from '../services/keybase-service';

export function triggerKeybaseLookup(username) {
  return function(dispatch, getState) {
    dispatch(setKeybaseLoading());
    var promise = KeyBaseService.lookupUser(username);
    return promise.then(function(data) {
      dispatch(triggerKeybaseSetUser(data));
      dispatch({
        type: types.CLEAR_NOTIFICATIONS,
        target: 'keybase_lookup',
      });
    }, function(status) {
      dispatch({
        type: types.ADD_NOTIFICATION,
        message: status.desc,
        target: 'keybase_lookup',
        uuid: 'keybase_lookup_error'
      });
    });
  };
}

export function triggerKeybaseSetUser(userData) {
  return {
    type: types.KEYBASE_SET_USER,
    keybaseData: userData,
  };
}

export function setKeybaseLoading() {
  return {
    type: types.SET_KEYBASE_LOADING
  };
}

export function resetIdentity() {
  return {
    type: types.RESET_IDENTITY
  };
}
