import './init-ajax';
import * as roots from './components/root';
import EthAddress from './components/eth-address';
import EthAddressIcon from './components/eth-address-icon';
import EthAddressHex from './components/eth-address-hex';

window.Dynamis = {
  ...roots,
  components: {
    EthAddress: EthAddress,
    EthAddressIcon: EthAddressIcon,
    EthAddressHex: EthAddressHex,
  }
};
