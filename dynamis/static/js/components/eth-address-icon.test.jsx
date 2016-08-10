import React from 'react';
import ReactTestUtils from 'react-addons-test-utils';
import EthAddressIcon from './eth-address-icon';

describe('EthAddressIcon', function() {
  it('renders', function() {
    ReactTestUtils.renderIntoDocument(<EthAddressIcon address="0x1234" />);
  });
});
