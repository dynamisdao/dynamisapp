import types from '../actions/types';
import Reducer from './reducer';

var reducer = new Reducer('policy', {
  id: null,
  signature: null,
  applicationHash: null,
  done: false,
  premium: 250,
});

reducer.addSetter('id');
reducer.addSetter('signature');
reducer.addSetter('premium');

reducer.subscribe(types.SET_POLICY_DATA, function(state, action) {
  return {
    ...state,
    id: action.policyId,
    premium: action.premium || state.premium,
  };
});

reducer.subscribe(types.MARK_POLICY_DONE, function(state, action) {
  if(action.applicationHash === undefined || action.applicationHash === state.applicationHash) {
    return { ...state, done: action.done };
  } else {
    return {
      ...state,
      done: action.done,
      applicationHash: action.applicationHash,
      signature: null,
    };
  }
});

export default reducer.build();
