import React from 'react';
import ReactTestUtils from 'react-addons-test-utils';
import EthAddressHex from './eth-address-hex';
import expect from 'expect';

describe('EthAddressHex', function() {
  it('renders', function() {
    ReactTestUtils.renderIntoDocument(<EthAddressHex address='0x1234' />);
  });

  [
    {truncate: false, expected: '0x1234567890'},
    {truncate: 4, expected: '0x1…'},
    {truncate: 6, expected: '0x123…'},
    {truncate: 12, expected: '0x1234567890'},
  ].forEach(function(testCase) {
    it('truncates 0x1234567890 to `' + testCase.expected + '` when truncate=`' + testCase.truncate + '`', function() {
      var component = ReactTestUtils.renderIntoDocument(<EthAddressHex address='0x1234567890' truncate={testCase.truncate} />);
      expect(component.getAddressDisplay()).toEqual(testCase.expected);
    });
  });
});

