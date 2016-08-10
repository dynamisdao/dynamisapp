import React from 'react';
import ReactTestUtils from 'react-addons-test-utils';
import KeybaseData from './keybase-data';

describe('KeybaseData', function() {

  it('renders', function() {
    ReactTestUtils.renderIntoDocument(<KeybaseData data={{}}/>);
  });
});
