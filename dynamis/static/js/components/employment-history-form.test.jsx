import React from 'react';
import ReactTestUtils from 'react-addons-test-utils';
import {Provider} from 'react-redux';
import EmploymentHistoryForm from './employment-history-form';

describe('EmploymentHistoryForm', function() {
  beforeEach(function() {
    this.store = TestUtils.mockStore({
      employmentHistory: {
        jobs: []
      }
    });
  });

  it('renders', function() {
    ReactTestUtils.renderIntoDocument(<Provider store={this.store}><EmploymentHistoryForm /></Provider>);
  });
});
