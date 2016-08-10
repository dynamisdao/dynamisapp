import React from 'react';
import ReactTestUtils from 'react-addons-test-utils';
import {Provider} from 'react-redux';
import EmploymentHistoryFormSection from './employment-history-form-section';

describe('EmploymentHistoryFormSection', function() {
  beforeEach(function() {
    this.store = TestUtils.mockStore({
      employmentHistory: {
        jobs: []
      }
    });
  });

  it('renders', function() {
    ReactTestUtils.renderIntoDocument(<Provider store={this.store}><EmploymentHistoryFormSection /></Provider>);
  });
});
