import types from '../actions/types';
import _ from 'lodash';

var initialState = {};

if(_.get(window, 'DjangoInfo.user.email')) {
  initialState.email = window.DjangoInfo.user.email;
  initialState.authenticated = true;
}
export default function(state = initialState, action = {}) {
  if(action.type === types.SET_LOGGED_IN) {
    return {
      ...state,
      authenticated: true,
      email: action.email
    };
  }
  return state;
}
