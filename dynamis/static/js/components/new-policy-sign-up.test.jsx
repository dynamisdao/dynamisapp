import React from 'react';
import ReactTestUtils from 'react-addons-test-utils';
import {Provider} from 'react-redux';
import NewPolicySignUp from './new-policy-sign-up';

describe('NewPolicySignUp', function() {
  beforeEach(function() {
    this.store = TestUtils.mockStore({});
  });

  it('renders', function() {
    ReactTestUtils.renderIntoDocument(<Provider store={this.store}><NewPolicySignUp /></Provider>);
  });
});
