import types from '../actions/types';

export default function(state = {}, action = {}) {
  if(action.type === types.KEYBASE_SET_USER) {
    return action.keybaseData;
  } else if(action.type === types.RESET_IDENTITY) {
    return {};
  } else if(action.type === types.SET_KEYBASE_LOADING)  {
    return { ...state, loading: true };
  }
  return state;
}
