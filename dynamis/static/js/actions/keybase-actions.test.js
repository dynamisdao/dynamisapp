import * as actions from './keybase-actions';
import expect, {spyOn} from 'expect';
import KeyBaseService from '../services/keybase-service';
import _ from 'lodash';
import types from './types';

describe('keybase-actions', function() {
  it('looks up from keybase - happy path ', function(done) {
    var store = TestUtils.mockStore({});
    var spy = spyOn(KeyBaseService, 'lookupUser').andCall(TestMocks.MockKeyBaseService.lookupUser);

    store.dispatch(actions.triggerKeybaseLookup('pipermerriam')).then(function() {
      expect(spy).toHaveBeenCalledWith('pipermerriam');
      var dispatched = _.map(store.getActions(), 'type');

      expect(dispatched).toInclude(types.SET_KEYBASE_LOADING);
      expect(dispatched).toInclude(types.CLEAR_NOTIFICATIONS);
      expect(dispatched).toInclude(types.KEYBASE_SET_USER);
      expect(dispatched.length).toEqual(3);
    }).then(done).catch(done);
  });

  it('looks up from keybase - sad path ', function(done) {
    var store = TestUtils.mockStore({});
    var spy = spyOn(KeyBaseService, 'lookupUser').andCall(TestMocks.MockKeyBaseService.lookupUser);

    store.dispatch(actions.triggerKeybaseLookup('some_random_username')).then(function() {
      expect(spy).toHaveBeenCalledWith('some_random_username');
      var dispatched = _.map(store.getActions(), 'type');

      expect(dispatched).toInclude(types.SET_KEYBASE_LOADING);
      expect(dispatched).toInclude(types.ADD_NOTIFICATION);
      expect(dispatched.length).toEqual(2);
    }).then(done).catch(done);
  });
});
