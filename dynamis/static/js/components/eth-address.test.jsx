import React from 'react';
import ReactTestUtils from 'react-addons-test-utils';
import EthAddress from './eth-address';

describe('EthAddress', function() {
  it('renders', function() {
    ReactTestUtils.renderIntoDocument(<EthAddress address="0x1234" />);
  });

});
