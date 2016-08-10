import React from 'react';
import ReactTestUtils from 'react-addons-test-utils';
import {Provider} from 'react-redux';
import EmploymentHistoryCompleted from './employment-history-completed';

describe('EmploymentHistoryCompleted', function() {
  beforeEach(function() {
    this.store = TestUtils.mockStore({});
  });

  it('renders', function() {
    ReactTestUtils.renderIntoDocument(<Provider store={this.store}><EmploymentHistoryCompleted jobData={{files: []}}/></Provider>);
  });
});
