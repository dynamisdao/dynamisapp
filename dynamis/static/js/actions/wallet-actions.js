import types from './types';
import lightwallet from 'eth-lightwallet';
import {
  getBalance,
  getTransactionCount,
  sendRawTransaction,
  // getTransactionReceipt,
  getFirstBlockHash,
} from '../services/web3-service';
import {setOn} from './gourmet-redux';

function getGasPrice() {
  return 20000000000;
}

function getGasLimit() {
  return 30000;
}

function saveKeystore(keystore) {
  localStorage.keystore = keystore.serialize();
}

function readKeystoreFromLocalstorage() {
  if(localStorage.keystore) {
    return lightwallet.keystore.deserialize(localStorage.keystore);
  }
}

export function initializeWallet() {
  return function(dispatch, getState) {
    var keystore = readKeystoreFromLocalstorage();
    if(keystore) {
      var address = keystore.getAddresses()[0];
      dispatch({
        keystore: keystore,
        type: types.INITIALIZE_WALLET,
        address: address,
      });
      dispatch(readFromWeb3());
    }
  };
}

export function readFromWeb3() {
  return function(dispatch, getState) {
    var store = getState();
    $.post(store.wallet.web3url)
      .error(function() {
        dispatch(setOn('wallet', 'connected', false));
      })
      .then(function() {
        dispatch(setOn('wallet', 'connected', true));
        dispatch(_readFromWeb3());
      });
  };
}

function _readFromWeb3() {
  return function(dispatch, getState) {
    var store = getState();

    var address = store.wallet.address;
    if(address) {
      getBalance(store.wallet.web3url, address, function(err, value) {
        if(err) { return; }
        dispatch(setOn('wallet', 'value', value ? value.toString() : null));
      });
    }
    getFirstBlockHash(store.wallet.web3url, function(err, block) {
      if(err) { return; }
      var net = {
        '0x0cd786a2425d16f152c658316c423e6ce1181e15c3295826d7c9904cba9ce303': 'Ethereum Testnet',
        '0xd4e56740f876aef8c010b86a40d5f56745a118d0906a34e69aec8c0db1cb8fa3': 'Ethereum Main Network',
      }[block.hash] || 'Unknown Network';
      dispatch(setOn('wallet', 'network', net));
    });
  };
}

export function createWallet(password) {
  return function(dispatch, getState) {
    var secretSeed = lightwallet.keystore.generateRandomSeed();
    lightwallet.keystore.deriveKeyFromPassword(password, function(err, pwDerivedKey) {

      var keystore = new lightwallet.keystore(secretSeed, pwDerivedKey);
      keystore.generateNewAddress(pwDerivedKey);

      saveKeystore(keystore);
      var address = keystore.getAddresses()[0];
      dispatch({
        keystore: keystore,
        type: types.CREATE_WALLET,
        address: address,
      });
      dispatch(readFromWeb3());
    });

  };
}

export function setWeb3Url(url) {
  return function(dispatch, getState) {
    dispatch(setOn('wallet', 'web3url', url));
    dispatch(readFromWeb3());
  };
}

export function makeTransaction(toAddress, value, password) {
  return function(dispatch, getState) {
    lightwallet.keystore.deriveKeyFromPassword(password, function(err, pwDerivedKey) {
      var store = getState();
      var address = store.wallet.keystore.getAddresses()[0];
      getTransactionCount(store.wallet.web3url, address, function(err, nonce) {
        var tx = lightwallet.txutils.valueTx({
          to: toAddress,
          gasPrice: getGasPrice(),
          gasLimit: getGasLimit(),
          value: value,
          nonce: nonce
        });
        var signed = lightwallet.signing.signTx(
          store.wallet.keystore,
          pwDerivedKey,
          tx,
          address,
          store.wallet.keystore.defaultHdPathString
        );
        sendRawTransaction(store.wallet.web3url, signed, function(err, hash) {
          if(err) {
            // eslint-disable-next-line no-console
            console.log('err:',err);
          } else {
            // eslint-disable-next-line no-console
            console.log(hash);
          }
        });
      });
    });
  };
}

export function readWallet(json) {
  return function(dispatch, getState) {
    var keystore = lightwallet.keystore.deserialize(json);
    var address = keystore.getAddresses()[0];
    saveKeystore(keystore);
    dispatch({
      keystore: keystore,
      type: types.CREATE_WALLET,
      address: address,
    });
    dispatch(readFromWeb3());
  };
}
