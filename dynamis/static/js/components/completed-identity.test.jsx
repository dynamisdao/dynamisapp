import React from 'react';
import ReactTestUtils from 'react-addons-test-utils';

import CompletedIdentity from './completed-identity';

describe('CompletedIdentity', function() {
  beforeEach(function() {
    this.store = TestUtils.mockStore({});
  });

  it('renders', function() {
    ReactTestUtils.renderIntoDocument(<CompletedIdentity keybase={{}} />);
  });
});
