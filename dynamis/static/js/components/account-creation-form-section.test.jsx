import React from 'react';
import ReactTestUtils from 'react-addons-test-utils';
import {Provider} from 'react-redux';
import AccountCreationFormSection from './account-creation-form-section';

describe('AccountCreationFormSection', function() {
  beforeEach(function() {
    this.store = TestUtils.mockStore({});
  });

  it('renders', function() {
    ReactTestUtils.renderIntoDocument(<Provider store={this.store}><AccountCreationFormSection /></Provider>);
  });
});
