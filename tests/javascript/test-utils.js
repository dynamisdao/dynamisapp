import configureStore from 'redux-mock-store';
import thunk from 'redux-thunk';

export const mockStore = function(store) {
  return configureStore([thunk])({
    keybase: {},
    account: {},
    employmentHistory: {},
    policy: {},
    notifications: {},
    ...store
  });
};
