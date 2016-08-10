import React from 'react';
import _ from 'lodash';

export default React.createClass({
  getDefaultProps() {
    return {
      address: '0x0000000000000000000000000000000000000000',
      truncate: false,
      extraClasses: [],
    };
  },

  getAddressDisplay() {
    var displayAddress = this.props.address;

    // Ensure it has a 0x prefir
    if (!_.startsWith(displayAddress, '0x')) {
      displayAddress = '0x' + displayAddress;
    }

    // TODO: return a checksummed address via `web3.toChecksumAddress`
    // address = web3.toChecksumAddress(address);

    if (this.props.truncate) {
      return displayAddress = _.truncate(displayAddress, {
        length: this.props.truncate,
        omission: '…',
      });
    }

    return displayAddress;
  },

  render() {
    var classes = _.flatten(['eth-address-hex'], this.props.extraClasses);
    return <code className={_.join(classes, ' ')}>{this.getAddressDisplay()}</code>;
  }
});
