import React from 'react';
import ReactTestUtils from 'react-addons-test-utils';
import {Provider} from 'react-redux';
import NotificationPanel from './notification-panel';

describe('NotificationPanel', function() {
  beforeEach(function() {
    this.store = TestUtils.mockStore({});
  });

  it('renders', function() {
    ReactTestUtils.renderIntoDocument(<Provider store={this.store}><NotificationPanel /></Provider>);
  });
});
