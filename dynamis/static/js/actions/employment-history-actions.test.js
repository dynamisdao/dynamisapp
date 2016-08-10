import * as actions from './employment-history-actions';
import expect from 'expect';
import _ from 'lodash';
import types from './types';

describe('employment-history-actions', function() {
  it('validates a job - no info ', function(done) {
    var store = TestUtils.mockStore({
      employmentHistory: {
        jobs: [
          {current: {}}
        ]
      }
    });

    store.dispatch(actions.validateEmploymentHistoryJob(0)).then(function() {
      var dispatched = _.map(store.getActions(), 'type');
      expect(dispatched).toInclude(types.CLEAR_NOTIFICATIONS);
      expect(dispatched.length).toEqual(1);
    }).then(done).catch(done);
  });

  it('validates a job - bad info ', function(done) {
    var store = TestUtils.mockStore({
      employmentHistory: {
        jobs: [{
          current: {
            startYear: 2016,
            startMonth: 1,
            endYear: 2015,
            endMonth: 3,
          }
        }]
      }
    });

    store.dispatch(actions.validateEmploymentHistoryJob(0)).then(function() {
      var dispatched = _.map(store.getActions(), 'type');
      expect(dispatched).toInclude(types.CLEAR_NOTIFICATIONS);
      expect(dispatched).toInclude(types.ADD_NOTIFICATION);
      expect(dispatched.length).toEqual(2);
    }).then(done).catch(done);
  });

  it('validates a job - good info ', function(done) {
    var store = TestUtils.mockStore({
      employmentHistory: {
        jobs: [{
          current: {
            startYear: 2016,
            startMonth: 1,
            endYear: 2016,
            endMonth: 3,
          }
        }]
      }
    });

    store.dispatch(actions.validateEmploymentHistoryJob(0)).then(function() {
      var dispatched = _.map(store.getActions(), 'type');
      expect(dispatched).toInclude(types.CLEAR_NOTIFICATIONS);
      expect(dispatched.length).toEqual(1);
    }).then(done).catch(done);
  });
});
