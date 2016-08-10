import React from 'react';
import ReactTestUtils from 'react-addons-test-utils';
import {Provider} from 'react-redux';
import EmploymentHistoryProgress from './employment-history-progress';

describe('EmploymentHistoryProgress', function() {
  beforeEach(function() {
    this.store = TestUtils.mockStore({});
  });

  it('renders', function() {
    ReactTestUtils.renderIntoDocument(<Provider store={this.store}><EmploymentHistoryProgress /></Provider>);
  });
});
