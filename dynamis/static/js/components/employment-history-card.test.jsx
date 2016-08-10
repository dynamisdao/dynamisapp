import React from 'react';
import ReactTestUtils from 'react-addons-test-utils';
import {Provider} from 'react-redux';
import EmploymentHistoryCard from './employment-history-card';

describe('EmploymentHistoryCard', function() {
  beforeEach(function() {
    this.store = TestUtils.mockStore({});
  });

  it('renders', function() {
    ReactTestUtils.renderIntoDocument(<Provider store={this.store}><EmploymentHistoryCard /></Provider>);
  });
});
