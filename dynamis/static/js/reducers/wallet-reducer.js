import types from '../actions/types';
import Reducer from './reducer';

var reducer = new Reducer('wallet', {
  web3url: localStorage.web3url || 'http://52.16.72.86:8545',
  network: '',
  connected: true,
});

reducer.subscribe(types.INITIALIZE_WALLET, function(state, action) {
  return {
    ...state,
    keystore: action.keystore,
    address: action.address,
  };
});

reducer.subscribe(types.CREATE_WALLET, function(state, action) {
  return {
    ...state,
    keystore: action.keystore,
    address: action.address,
  };
});

reducer.addSetter('value');
reducer.addSetter('web3url');
reducer.addSetter('network');
reducer.addSetter('connected');

export default reducer.build();
