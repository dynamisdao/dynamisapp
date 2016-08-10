import * as actions from './policy-actions';
import expect from 'expect';
import _ from 'lodash';
import types from './types';

describe('keybase-actions', function() {
  it('signs the policy - happy path ', function(done) {
    var store = TestUtils.mockStore({});

    store.dispatch(actions.signPolicy('o2nk12jk1d')).then(function() {
      var dispatched = _.map(store.getActions(), 'type');

      expect(dispatched).toInclude(types.CLEAR_NOTIFICATIONS);
      expect(dispatched).toInclude('SET.policy.signature');
      expect(dispatched.length).toEqual(2);
    }).then(done).catch(done);
  });

  it('signs the policy - sad path ', function(done) {
    var store = TestUtils.mockStore({});

    store.dispatch(actions.signPolicy('')).then(function() {
      var dispatched = _.map(store.getActions(), 'type');

      expect(dispatched).toInclude(types.ADD_NOTIFICATION);
      expect(dispatched.length).toEqual(1);
    }).then(done).catch(done);
  });
});
