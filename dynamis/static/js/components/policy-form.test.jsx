import React from 'react';
import ReactTestUtils from 'react-addons-test-utils';
import {Provider} from 'react-redux';
import PolicyForm from './policy-form';

describe('PolicyForm', function() {
  beforeEach(function() {
    this.store = TestUtils.mockStore({});
  });

  it('renders', function() {
    ReactTestUtils.renderIntoDocument(<Provider store={this.store}><PolicyForm /></Provider>);
  });
});
